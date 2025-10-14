# MQTT Simulator

A lightweight, easy-to-configure MQTT simulator written in [Python 3](https://www.python.org/) for publishing JSON objects to a broker, simulating sensors and devices.

[Features](#features) •
[Getting Started](#getting-started) •
[Configuration](#configuration) •
[Main contributors](#main-contributors)

![Simulator Running](docs/images/simulator-running.gif)

## Features

* Lightweight and easy-to-configure simulator for publishing data to an MQTT broker
* Simple setup with a single JSON configuration file
* Publish data on predefined fixed topics
* Publish data on multiple topics that have a variable id or items at the end
* Simulated random variation of data based on configurable parameters
* Real-time event logging during simulation

## Getting Started

### Running using Python

Run the simulator with the default settings file (`config/settings.json`):

```shell
python3 mqtt-simulator/main.py 
```

Or specify a custom settings file:

```shell
python3 mqtt-simulator/main.py -f <path/settings.json>
```

To install all dependencies with a virtual environment before using:

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Running using uv

Run the simulator with [uv](https://github.com/astral-sh/uv), a fast Python package and project manager - no need to manually setup a virtual environment:

```shell
uv run mqtt-simulator/main.py -f <path/settings.json>
```

### Running using Docker

Additionally, you can run the simulator via [Docker](https://docs.docker.com/get-docker/) using the provided `Dockerfile`.

Build the image:

```shell
docker build -t mqtt-simulator .
```

Run the container:

```shell
docker run mqtt-simulator -f <path/settings.json>
```

## Configuration

See the [configuration documentation](./docs/configuration.md) for detailed usage instructions.

You can also check a full settings file example at: [settings.json](../config/settings.json).

Below is a minimal configuration file that connects to the `broker.hivemq.com` broker and publishes data to the `/place/roof` and `/place/basement` topics. The simulator generates `temperature` variations based on the provided parameters:

```json
{
  "BROKER_URL": "broker.hivemq.com",
  "TOPICS": [
    {
      "TYPE": "list",
      "PREFIX": "place",
      "LIST": ["roof", "basement"],
      "TIME_INTERVAL": 8,
      "DATA": [
        {
          "NAME": "temperature",
          "TYPE": "float",
          "MIN_VALUE": 20,
          "MAX_VALUE": 55,
          "MAX_STEP": 3,
          "RETAIN_PROBABILITY": 0.5,
          "INCREASE_PROBABILITY": 0.6
        }
      ]
    }
  ]
}
```

## Main contributors

[![DamascenoRafael](https://github.com/DamascenoRafael.png?size=70)](https://github.com/DamascenoRafael)
[![Maasouza](https://github.com/Maasouza.png?size=70)](https://github.com/Maasouza)
[![AJ Danelz](https://github.com/vordimous.png?size=70)](https://github.com/vordimous)
