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

```txt
usage: eTracker.py track [-h] [-i <interval>] [-o <filename>]

track energy consumption of target device

optional arguments:
  -h, --help     show this help message and exit
  -i <interval>  set the tracking interval in [sec]; default = 0.02
  -o <filename>  write output to <filename>
```

```txt
usage: eTracker.py analyze [-h] [-b <begin_date>] [-e <end_date>] <filename>

analyze the json file created by track sub-command

positional arguments:
  <filename>            specify the file to analyze

optional arguments:
  -h, --help            show this help message and exit
  -b <begin_date>, --begin <begin_date>
                        specify the beginning of the section of time to
                        analyze; if '-' is given, analyze from the beginning
                        of the file; default = '-'
  -e <end_date>, --end <end_date>
                        specify the end of the section of time to analyze; if
                        '-' is given, analyze to the end of the file; default
                        = '-'
```


## License

MIT License.
