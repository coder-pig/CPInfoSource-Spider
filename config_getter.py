# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File: config_getter.py
  Desc: 获取配置信息
  Author: CoderPig
  .Date: 2019/3/22 0022 14:48
-------------------------------------------------
"""

import configparser
import os
import os.path


def get_config(section, key):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'config.ini'), encoding='utf8')
    return config.get(section, key)


if __name__ == '__main__':
    c = get_config('DB', 'type')
    print(c)
