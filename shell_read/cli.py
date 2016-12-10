#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
from argparse import ArgumentParser

import configparser
import requests
from colorama import (
    # Back,
    colorama_text, Fore, Style
)

DEFAULT_URL = "http://shell-read.leonornot.org/api/post/"
DEFAULT_NICKNAME = "anonymous"

COLUMN_STYLE = Fore.BLUE + Style.BRIGHT
RESET_COLUMN_STYLE = Fore.RESET + Style.RESET_ALL


def read(category=None):
    config = _read_config()

    params = dict(nickname=config['nickname'])
    resp = requests.get(config['url'], params=params, timeout=15)
    if not resp.ok:
        with colorama_text():
            print("%serror:%s %d, %s" % (
                Fore.RED,
                Fore.RESET,
                resp.status_code,
                resp.reason))
        return

    data = resp.json()
    if not data.get('success'):
        with colorama_text():
            print("%serror:%s %s" % (Fore.RED, Fore.RESET, data.get('msg')))
        return

    with colorama_text():
        post = data['data']
        if not post:
            print("""
No data. How about to write your first post?
Use:
    %sswrite "your text"%s
""" % (Fore.GREEN, Fore.RESET))
        else:
            print("""%snickname:%s %s,
%sdate:%s %s,
%scontent:%s %s
""".strip() % (COLUMN_STYLE, RESET_COLUMN_STYLE, post['nickname'],
               COLUMN_STYLE, RESET_COLUMN_STYLE, post['created_at'],
               COLUMN_STYLE, RESET_COLUMN_STYLE, post['content']))


def write():
    config = _read_config()

    parser = ArgumentParser()
    parser.add_argument(dest='text', nargs=1,
                        help="what do you want to say?")
    args = parser.parse_args()
    text = args.text[0].decode('utf-8').strip()

    post_data = dict(nickname=config['nickname'], content=text)
    resp = requests.post(config['url'], data=post_data, timeout=15)
    if not resp.ok:
        with colorama_text():
            print("%serror:%s %d, %s" % (
                Fore.RED,
                Fore.RESET,
                resp.status_code,
                resp.reason))
        return

    data = resp.json()
    with colorama_text():
        if not data.get('success'):
            print("%serror:%s %s" % (Fore.RED, Fore.RESET, data.get('msg')))
        else:
            print("%ssuccess%s" % (Fore.GREEN, Fore.RESET))


def _read_config():
    home = os.path.expanduser('~')
    config_file = os.path.join(home, '.shell_read.conf')
    if os.path.exists(config_file):
        c_parser = configparser.ConfigParser()
        c_parser.read(config_file)
        try:
            url = c_parser.get('settings', 'url')
        except configparser.NoOptionError:
            url = DEFAULT_URL
        try:
            nickname = c_parser.get('settings', 'nickname')
        except configparser.NoOptionError:
            nickname = DEFAULT_NICKNAME
    else:
        url = DEFAULT_URL
        nickname = DEFAULT_NICKNAME

        content = """[settings]
url : %s
nickname: %s
""" % (url, nickname)
        with open(config_file, 'wb') as f:
            f.write(content)

    return dict(url=url, nickname=nickname)


if __name__ == "__main__":
    import sys
    usage = "python cli.py read|write"
    if len(sys.argv) < 2:
        print(usage)
        raise SystemExit
    if sys.argv[1] == "read":
        read()
    elif sys.argv[1] == "write":
        del sys.argv[1]
        write()
    else:
        print(usage)
