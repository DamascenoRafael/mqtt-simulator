# Configuration

The MQTT Simulator configuration consists of 3 main sections: **Broker**, **Topics**, and **Data**.

Quick Navigation:  
[Broker settings](#broker-settings) •
[Topics settings](#topics-settings) •
[Data settings](#data-settings)

You can also check a full settings file example at: [settings.json](../config/settings.json).

## Broker settings

The **Broker settings** section is located at the root level of the JSON configuration file and defines the fundamental MQTT connection parameters:

```json
{
    "BROKER_URL": "broker.hivemq.com",
    "BROKER_PORT": 1883,
    "TOPICS": [
        ...
    ]
}
```

| Key | Type |  Default | Description |
| --- | --- | --- | --- |
| `BROKER_URL` | string | localhost | The broker URL where the data will be published |
| `BROKER_PORT` | number | 1883 | The port used by the broker |
| `PROTOCOL_VERSION` | number | 4 | Sets the [paho.mqtt.client] `protocol` param. Version of the MQTT protocol to use for this client. Can be either `3` (MQTTv31), `4` (MQTTv311) or `5` (MQTTv5) |
| `TLS_CA_PATH` | string | None | Sets the [paho.mqtt.client.tls_set] `ca_certs` param. String path to the Certificate Authority certificate file |
| `TLS_CERT_PATH` | string | None | Sets the [paho.mqtt.client.tls_set] `certfile` param. String path to the PEM encoded client certificate file |
| `TLS_KEY_PATH` | string | None | Sets the [paho.mqtt.client.tls_set] `keyfile` param. String path to the PEM encoded client private keys file |
| `AUTH_USERNAME` | string | None | Sets the [paho.mqtt.client.username_pw_set] `username` param. Username to authenticate with |
| `AUTH_PASSWORD` | string | None | Sets the [paho.mqtt.client.username_pw_set] `password` param. Password to authenticate with |
| `CLEAN_SESSION` | bool | True | Sets the [paho.mqtt.client] `clean_session` param. Boolean that determines the client type. This property is ignored if `PROTOCOL_VERSION` is `5`. |
| `RETAIN` | bool | False | Sets the [paho.mqtt.client.publish] `retain` param. If set to true, the message will be set as the “last known good”/retained message for the topic |
| `QOS` | number | 2 | Sets the [paho.mqtt.client.publish] `qos` param. Quality of service level to use |
| `TIME_INTERVAL` | number | 10 | Time interval in seconds between submissions towards the topic |
| `TOPICS` | array\<object> | None | Specification of topics and how they will be published |

[paho.mqtt.client]:https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client
[paho.mqtt.client.publish]:https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.publish
[paho.mqtt.client.tls_set]:https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.tls_set
[paho.mqtt.client.username_pw_set]:https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.username_pw_set

## Topics settings

The **TOPICS** key is a list. Each topic entry is an `object` containing parameters that define how topics will be structured and published:

```json
{
    "TYPE": "multiple",
    "PREFIX": "place",
    "RANGE_START": 1,
    "RANGE_END": 2,
    "TIME_INTERVAL": 25,
    "DATA": [
        ...
    ]
}
```

| Key | Type | Description | Required |
| --- | --- | --- | --- |
| `TYPE` | string | It can be `"single"`, `"multiple"` or `"list"` | yes |
| `PREFIX` | string | Prefix of the topic URL, depending on the `TYPE` it can be concatenated to `/<id>` or `/<item>` | yes |
| `LIST` | array\<any> | When the `TYPE` is `"list"` the topic prefix will be concatenated with `/<item>` for each item in the array | if `TYPE` is `"list"` |
| `RANGE_START` | number | When the `TYPE` is `"multiple"` the topic prefix will be concatenated with `/<id>` where `RANGE_START` will be the first number  | if `TYPE` is `"multiple"`  |
| `RANGE_END` | number | When the `TYPE` is `"multiple"` the topic prefix will be concatenated with `/<id>` where `RANGE_END` will be the last number | if `TYPE` is `"multiple"`  |
| `CLEAN_SESSION` | bool | Overwrites the broker level config value and applies only to this Topic | no |
| `RETAIN` | bool | Overwrites the broker level config value and applies only to this Topic | no |
| `QOS` | number | Overwrites the broker level config value and applies only to this Topic | no |
| `TIME_INTERVAL` | number |  Overwrites the broker level config value and applies only to this Topic | no |
| `PAYLOAD_ROOT` | object | The root set of params to include on all messages | optional |
| `DATA` | array\<object> | Specification of the data that will form the JSON to be sent in the topic | yes |

## Data settings

The key **DATA** inside TOPICS is a list. Each data entry is an `object` containing parameters that define individual data properties and how values are simulated:

```json
{
    "NAME": "temperature",
    "TYPE": "float",
    "INITIAL_VALUE": 35,
    "MIN_VALUE": 20,
    "MAX_VALUE": 55,
    "MAX_STEP": 0.2,
    "RETAIN_PROBABILITY": 0.5,
    "RESET_PROBABILITY": 0.1,
    "INCREASE_PROBABILITY": 0.7,
    "RESTART_ON_BOUNDARIES": true
}
```

| Key | Type | Description | Required |
| --- | --- | --- | --- |
| `NAME` | string | JSON property name to be sent | yes |
| `TYPE` | string | It can be `"int"`, `"float"`, `"bool"`, `"math_expression"` or `"raw_values"` | yes |
| `INITIAL_VALUE` | same that is returned according to `TYPE` | Initial value that the property will assume when the simulation starts. If not specified: random for `"int"`, `"float"` or `"bool"`, and determined by other parameters for `"math_expression"` or `"raw_values"` | optional |
| `RETAIN_PROBABILITY` | number | Number between 0 and 1 for the probability of the value being retained and sent again | optional, default is `0` |
| `RESET_PROBABILITY` | number | Number between 0 and 1 for the probability of the value being reset to `INITIAL_VALUE` | optional, default is `0` |
| `MIN_VALUE` | number | Minimum value that the property can assume | if `TYPE` is `"int"` or `"float"` |
| `MAX_VALUE` | number | Maximum value that the property can assume | if `TYPE` is `"int"` or `"float"`  |
| `MAX_STEP` | number | Maximum change that can be applied to the property from a published data to the next | if `TYPE` is `"int"` or `"float"` |
| `INCREASE_PROBABILITY` | number | Number between 0 and 1 for the probability of the next value being greater than the previous one | optional, default is `0.5` (same probability to increase or decrease). Only valid if `TYPE` is `"int"` or `"float"` |
| `RESTART_ON_BOUNDARIES` | bool | When true and the value reaches `MAX_VALUE` or `MIN_VALUE` the next value will be the `INITIAL_VALUE` | optional, default is false. Only valid if `TYPE` is `"int"` or `"float"` |
| `MATH_EXPRESSION` | string | Math expression written in a *Pythonic* way. Also accept functions from [Math modules](https://docs.python.org/3/library/math.html)  | if `TYPE` is `"math_expression"` |
| `INTERVAL_START` | number | Minimum value that the `MATH_EXPRESSION`'s variable `x` can assume | if `TYPE` is `"math_expression"` |
| `INTERVAL_END` | number | Maximum value that the `MATH_EXPRESSION`'s variable `x` can assume | if `TYPE` is `"math_expression"` |
| `MIN_DELTA` | number | Minimum value that can be added to the  `MATH_EXPRESSION`'s variable `x` from a published data to the next | if `TYPE` is `"math_expression"` |
| `MAX_DELTA` | number | Maximum value that can be added to the  `MATH_EXPRESSION`'s variable `x` from a published data to the next | if `TYPE` is `"math_expression"` |
| `INDEX_START` | number | The index to start publishing from the `VALUES` array | optional, default is `0`. Only valid if `TYPE` is `"raw_values"` |
| `INDEX_END` | number | The index to end publishing from the `VALUES` array | optional, default is `len(values) - 1`. Only valid if `TYPE` is `"raw_values"` |
| `RESTART_ON_END` | bool | When true and the index of the `VALUES` array reaches `INDEX_END`, the next index will be `INDEX_START`. Otherwise, the param will become inactive and won’t be sent after reaching `INDEX_END` | optional, default is false. Only valid if `TYPE` is `"raw_values"` |
| `VALUES` | array\<any> | The values to be published in array order | if `TYPE` is `"raw_values"` |
| `VALUE_DEFAULT` | object | The default value params used or overwritten by params in `VALUES` | optional, default is `{}`. Only valid if `TYPE` is `"raw_values"` and `VALUES` is an array\<object> |

> **_NOTE:_** Access [math_expression.md](./math_expression.md) file for more explanations and a example of `TYPE: "math_expression"`.
