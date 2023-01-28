#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test cover_df.py
@Author  : Gan Yuyang
@Time    : 2023/1/17 20:31
"""
import pandas as pd
from href_collector import Href_Collecter
from driver_init import Driver
from Parser import ArticleParser, LivecoverageParser, parser_choser
from lib import *
from wsj_selenium_crawler import lib
from namer import Namer
from bs4 import BeautifulSoup
from threading import Thread

df = pd.DataFrame({
    "write_time": [],
    "title": [],
    "brief": [],
    "content": [],
    "href": []
})

df.iloc[3] = '1', '2', '3', '4', '5'
print(df)