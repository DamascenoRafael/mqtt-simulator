# MQTT Simulator

Easy-to-configure MQTT simulator written in [Python 3](https://www.python.org/) to simulate the sending of JSON objects from sensors or devices to a broker.

[Features](#features) •
[Getting Started](#getting-started) •
[Configuration](#configuration) •
[Authors](#authors)

![Simulator Running](images/simulator-running.gif)

## Features

* Small and easy-to-configure simulator for publishing data to a broker  
* Configuration from a single JSON file  
* Connection on pre-defined fixed topics  
* Connection on multiple topics that have a variable id or items at the end  
* Random variation of data generated according to configuration parameters  

## Getting Started

#### Prerequisites

* [Python 3](https://www.python.org/) (with pip)

#### Installing Dependencies

To install all dependencies with a virtual environment:

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### Running

The default simulator settings can be changed in the `config/settings.json` file.

```shell
python3 mqtt-simulator/main.py
```

Runs the simulator according to the settings file.  
The terminal will show the simulator event log.

Optionally, you can pass a flag with the path to settings file:

```shell
python3 mqtt-simulator/main.py -f <path/settings.json>
```

## Configuration

* The `config/settings.json` file has three main configuration parameters:

    ```json
    {
        "BROKER_URL": "mqtt.eclipse.org",
        "BROKER_PORT": 1883,
        "TOPICS": [
            ...
        ]
    }
    ```

    | Key | Type | Description | Required |
    | --- | --- | --- | --- |
    | `BROKER_URL` | string | The broker URL where the data will be published | yes |
    | `BROKER_PORT` | number | The port used by the broker | yes |
    | `TOPICS` | array\<Objects> | Specification of topics and how they will be published | yes |

* The key **TOPICS** has a array of objects where each one has the format:

    ```json
    {
        "TYPE": "multiple",
        "PREFIX": "temperature",
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
    | `TIME_INTERVAL` | number | Time interval in seconds between submissions towards the topic | yes |
    | `DATA` | array\<Objects> | Specification of the data that will form the JSON to be sent in the topic | yes |

* The key **DATA** inside TOPICS has a array of objects where each one has the format:

    ```json
    {
        "NAME": "temperature",
        "TYPE": "float",
        "INITIAL_VALUE": 35,
        "MIN_VALUE": 30,
        "MAX_VALUE": 40,
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
    | `TYPE` | string | It can be `"int"`, `"float"`, `"bool"` or `"math_expression"` | yes |
    | `INITIAL_VALUE` | number or bool (same as defined in `TYPE`) | Initial value that the property will assume when the simulation starts (random otherwise) | optional. Only valid if `TYPE` is different from `"math_expression"` |
    | `MIN_VALUE` | number | Minimum value that the property can assume | if `TYPE` is `"int"` or `"float"` |
    | `MAX_VALUE` | number | Maximum value that the property can assume | if `TYPE` is `"int"` or `"float"`  |
    | `MAX_STEP` | number | Maximum change that can be applied to the property from a published data to the next | if `TYPE` is `"int"` or `"float"` |
    | `RETAIN_PROBABILITY` | number | Number between 0 and 1 for the probability of the value being retained and sent again | yes |
    | `RESET_PROBABILITY` | number | Number between 0 and 1 for the probability of the value being reset to `INITIAL_VALUE` | optional, default is 0. Only valid if `TYPE` is different from `"math_expression"` |
    | `INCREASE_PROBABILITY` | number | Number between 0 and 1 for the probability of the next value being greater than the previous one | optional, default is 0.5 (same probability to increase or decrease). Only valid if `TYPE` is `"int"` or `"float"` |
    | `RESTART_ON_BOUNDARIES` | bool | When true and the value reaches `MAX_VALUE` or `MIN_VALUE` the next value will be the `INITIAL_VALUE` | optional, default is false. Only valid if `TYPE` is `"int"` or `"float"` |
    | `MATH_EXPRESSION` | string | Math expression writen in a *Pythonic* way<br/> Also accept fuctions from [Math modules](https://docs.python.org/3/library/math.html)  | if `TYPE` is `"math_expression"` | 
    | `INTERVAL_START` | number | Minimum value that the `MATH_EXPRESSION`'s variable `x` can assume | if `TYPE` is `"math_expression"` |
    | `INTERVAL_END` | number | Maximum value that the `MATH_EXPRESSION`'s variable `x` can assume | if `TYPE` is `"math_expression"` |
    | `MIN_DELTA` | number | Minimum value that can be added to the  `MATH_EXPRESSION`'s variable `x` from a published data to the next | if `TYPE` is `"math_expression"` |
    | `MAX_DELTA` | number | Maximum value that can be added to the  `MATH_EXPRESSION`'s variable `x` from a published data to the next | if `TYPE` is `"math_expression"` |
    

    > **_NOTE:_** Access [math_expression.md](./math_expression.md) file for more explanations and a example of `TYPE: "math_expression"`.

    

## Authors

[![DamascenoRafael](https://github.com/DamascenoRafael.png?size=70)](https://github.com/DamascenoRafael)
 [![Maasouza](https://github.com/Maasouza.png?size=70)](https://github.com/Maasouza)
