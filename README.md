# eTracker

Utility Tool for [Raspberry Pi](https://www.raspberrypi.org/) by [Hiroyuki Matsuo](http://sdl.ist.osaka-u.ac.jp/~h-matsuo/)

Track energy consumption of your device with Adafruit INA219 chip.

## Installation

1. Clone this repository.

    ```bash
    $ git clone https://github.com/h-matsuo/eTracker.git
    ```

1. Update submodule.

    ```bash
    $ cd eTracker
    $ git submodule update --init
    ```

## Usage

Just run `eTracker.py`.

```bash
$ sudo ./eTracker.py 1 result.json
```
