#!/usr/bin/python3
# wphelper.py
# Copyright 2025 Hayden Schiff
#
# Uses code from wireplumber_audio_switcher.py from https://gist.github.com/fsantand/846fbdd9ed2db5c89838b138a2e48ceb
# Copyright 2025 fsantand
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import subprocess
import sys
import pprint
import argparse
import re

GROUP_DELIMITER = " ├─"
ITEM_DELIMITER  = " │  "

# strips formatting characters from a line of wpctl output
def clean_line(line: str):
    line = line.replace(GROUP_DELIMITER, "").replace(ITEM_DELIMITER, "")
    return line.strip()

# nicely formats the name of a subgroup from wpctl output
def clean_subgroup(line: str):
    return clean_line(line).replace(":", "").lower()

# converts a line of wpctl output to a dict representing an object
def parse_line(line: str):
    line = clean_line(line)

    # split bracketted info (e.g. volume) out of the line
    split_brackets = line.split("[")
    line = split_brackets.pop(0)
    bracketted = '['.join(split_brackets)

    # find the closing bracket and cut the string short there
    end_bracket_index = bracketted.find("]")
    if end_bracket_index > 0:
        bracketted = bracketted[:end_bracket_index]

    # check if the device is default (then remove the asterisk)
    is_active = ("*" in line)
    line = line.replace("*", "")

    splitted = line.split(".")
    data = {
        "id": splitted.pop(0).strip(),
        "name": ".".join(splitted).strip(),
        "active": is_active,
    }

    if bracketted != '':
        vol_match = re.search(r"^vol: ([01]\.\d+)( MUTED)?$", bracketted)
        if vol_match:
            data['vol'] = vol_match.group(1)
            data['muted'] = (vol_match.group(2) == " MUTED")
        else:
            data['extra'] = bracketted

    return data

# gets the current state of WirePlumber as a list of dicts
def parse_wpctl_status():
    found_audio_tab = False
    current_subgroup = None
    processed_data = {}
    output = subprocess.run(
        "wpctl status -k",
        shell=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    for line in output.stdout.split("\n"):
        if not found_audio_tab and line == "Audio":
            found_audio_tab = True

        elif found_audio_tab:
            if line == "":
                found_audio_tab = False
                break
            elif line == ITEM_DELIMITER:
                current_subgroup = None
                continue
            elif line.startswith(GROUP_DELIMITER):
                current_subgroup = clean_subgroup(line)
                processed_data[current_subgroup] = []
                continue
            elif current_subgroup and line.startswith(ITEM_DELIMITER):
                processed_data[current_subgroup].append(parse_line(line))
                continue
    return processed_data

# returns a human-friendly label for an object (sink, source, etc)
def get_obj_label(obj):
    return "{id}. {name}".format(
        id = obj['id'],
        name = obj['name'],
    )

# searches for an object by id/name, and sets it as the default
def set_default(query, objs):
    query = query.strip().lower()
    for obj in objs:
        if query in obj['name'].lower() or obj['id'] == query:
            subprocess.run(
                "wpctl set-default {id}".format(
                    id = obj['id']
                ),
                shell=True
            )
            return obj

    return False

# initializes argparse
def parse_args(args=None):
    parser = argparse.ArgumentParser(
        prog='wphelper',
        description='Utility script for controlling WirePlumber',
    )
    subparsers = parser.add_subparsers(
        title='command',
        dest='command',
        required=True,
    )

    parser_list = subparsers.add_parser(
        'list',
        help='list objects'
    )
    parser_list.add_argument(
        'type',
        nargs='?',
        choices=['devices','filters','sinks','sources','all'],
        default='all',
        help='type of objects to list'
    )

    parser_get = subparsers.add_parser(
        'get',
        help='show which objects are active'
    )
    parser_get.add_argument(
        'type',
        choices=['device','filter','sink','source'],
        help='type of object to check'
    )

    parser_set_output = subparsers.add_parser(
        'set-output',
        help='set default sink'
    )
    parser_set_output.add_argument(
        'object',
        help='name or ID of object'
    )

    parser_set_input = subparsers.add_parser(
        'set-input',
        help='set default source'
    )
    parser_set_input.add_argument(
        'object',
        help='name or ID of object'
    )

    return parser.parse_args(args)



def main():
    args = parse_args()
    status = parse_wpctl_status()

    if args.command == 'list':
        if args.type == 'all':
            pprint.pprint(status)
        else:
            pprint.pprint(status[args.type])

    elif args.command == 'get':
        objs = status[args.type+'s']
        for obj in objs:
            if obj['active']:
                print(get_obj_label(obj))

    elif args.command == 'set-output':
        query = args.object.strip().lower()
        obj = set_default(args.object, status['sinks'])
        if obj:
            print("Default sink is now '{obj}'".format(
                obj=get_obj_label(obj)
            ))
        else:
            print("Could not find a sink matching '{query}'".format(
               query=query
            ))

    elif args.command == 'set-input':
        query = args.object.strip().lower()
        obj = set_default(args.object, status['sources'])
        if obj:
            print("Default source is now '{obj}'".format(
                obj=get_obj_label(obj)
            ))
        else:
            print("Could not find a source matching '{query}'".format(
               query=query
            ))

main()
