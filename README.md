# BME280 Temperature, Pressure, & Humidity Sensor

[![Build Status](https://travis-ci.com/pimoroni/bme280-python.svg?branch=master)](https://travis-ci.com/pimoroni/bme280-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/bme280-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/bme280-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/pimoroni-bme280.svg)](https://pypi.python.org/pypi/pimoroni-bme280)
[![Python Versions](https://img.shields.io/pypi/pyversions/pimoroni-bme280.svg)](https://pypi.python.org/pypi/pimoroni-bme280)

Suitable for measuring ambient temperature, barometric pressure, and humidity, the BME280 is a great indoor environmental sensor.

# Pre-requisites

You must enable:

* i2c: `sudo raspi-config nonint do_i2c 0`

You can optionally run `sudo raspi-config` or the graphical Raspberry Pi Configuration UI to enable interfaces.

# Installing

Stable library from PyPi:

* Just run `sudo pip install pimoroni-bme280`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/bme280-python`
* `cd bme280-python`
* `sudo ./install.sh`

