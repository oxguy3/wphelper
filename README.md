# wphelper
Utility script for controlling WirePlumber

## Usage

This is a tiny command-line tool designed to make it a little bit easier to control PipeWire sinks/sources in Bash scripts. Instead of having to know the ID of the object you want to control, this script allows you to use a partial case-insensitive string match for the name of the object.

For example, to set the default audio sink to a device named "Fosi Audio K5 Pro", you can simply run:
```
wphelper set-output "fosi audio"
```
To set the default audio source to a device named "Blue Snowball", you can run:
```
wphelper set-input snowball
```

There are also `list` and `get` commands; more details about all commands can be found using `wphelper -h`.

## Installation
Assuming you already have PipeWire, WirePlumber, and Python 3 installed, you can just drop `wphelper.py` somewhere in your PATH (you may wish to rename it to just `wphelper`).

## License
Copyright 2025 Hayden Schiff, MIT License (full text below)

The logic for parsing the output from `wpctl` was adapted from [wireplumber_audio_switcher.py](https://gist.github.com/fsantand/846fbdd9ed2db5c89838b138a2e48ceb). Copyright 2025 fsantand, MIT License (full text below)

### MIT License
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.