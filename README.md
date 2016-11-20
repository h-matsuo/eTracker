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
Usage: python eTracker.py <command> [<args>]

eTracker は，Adafruit INA219 チップと I2C 接続された Raspberry Pi 上で，
目標デバイスの電力消費状況の監視，およびその分析を行うことができる
ユーティリティツールです．
Python 2.x 系での動作を確認しています．

次のコマンドが使用できます：

help
    このテキストを表示します．

track <delay_time> [<output_path>]
    目標デバイスの電力消費状況を監視します．
    Adafruit INA219 チップからデータを取得し，整形して標準出力に出力します．
    <delay_time>
            データを取得する間隔を秒単位で指定します．
    <output_path>
            データの出力ファイルを指定できます．

analyze <input_path> <begin_date> <end_date>
    track コマンドで得られたデータを分析し，累計の電力消費量を計算します．
    <input_path>
            分析対象となる入力ファイルを指定します．
    <begin_date>
            分析対象のデータの開始時刻を指定します．
            時刻は '2016/09/22-09:59:30.005' のように指定してください．
            '-' を指定すると，入力ファイルの最初から分析します．
    <end_date>
            分析対象のデータの終了時刻を指定します．
            時刻は '2016/09/22-10:01:15.090' のように指定してください．
            '-' を指定すると，入力ファイルの最後まで分析します．
```
