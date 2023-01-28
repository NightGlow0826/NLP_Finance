#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : csv_combine.py
@Author  : Gan Yuyang
@Time    : 2023/1/20 19:34
"""

import pandas as pd
import os
from collections import Counter
import re
import pyecharts
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

pd.options.mode.chained_assignment = None  # default='warn'

pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)
pd.set_option('max_colwidth', 500)


def folderpath2df(folder_path: str):
    # 给出储存csv语料的文件夹, 返回合并后的 dataframe
    file_list = os.listdir(folder_path)
    all_data_frame: pd.DataFrame

    for single_csv in file_list:
        single_data_frame = pd.read_csv(os.path.join(folder_path, single_csv), index_col=0)
        if single_csv == file_list[0]:
            all_data_frame = single_data_frame
        else:
            all_data_frame = pd.concat([all_data_frame, single_data_frame], ignore_index=True)
    return all_data_frame


def word_count(series):
    lst = [i for i in series]
    str_seq = ''.join(lst)
    # print(str_seq)
    lst_seq = str_seq.split()
    print(type(Counter(lst_seq)))
    # print(Counter(lst_seq))
    c = Counter(lst_seq)
    return c


def data_clean(df: pd.DataFrame):
    df = df.dropna(subset=['content', ])
    df['content'] = df['content'].map(lambda x: re.sub(r'- WSJ', '', x))
    df['content'] = df['content'].map(lambda x: x.lower())
    df['content'] = df['content'].map(lambda x: re.sub(r'\\xa0', '', x))
    df['content'] = df['content'].map(lambda x: re.sub(r'u\.s', 'US', x))
    df['content'] = df['content'].map(lambda x: re.sub(r'\.', ' ', x))
    df['content'] = df['content'].map(lambda x: re.sub(r',', ' ', x))
    df['content'] = df['content'].map(lambda x: re.sub(r'-', ' ', x))
    df['content'] = df['content'].map(lambda x: re.sub(r'"', '', x))
    df['content'] = df['content'].map(lambda x: re.sub(r' ', ' ', x))
    df['content'] = df['content'].map(lambda x: re.sub(r'\d', ' ', x))
    df['content'] = df['content'].map(lambda x: re.sub(r'\$', ' ', x))
    df['content'] = df['content'].map(lambda x: re.sub(r'%', ' ', x))
    df['content'] = df['content'].map(lambda x: re.sub(r'\(.*?\)', '', x))
    my_stop_words = [
        'the', 'to', 'of', 'and', 'in', 'a', 'for', 'that', 'said',
        'on', 'is', 'as', 'with', 'Mr', 'at', 'from', 'its', 'has',
        'mr', 'year',
    ]
    import nltk
    from nltk.corpus import stopwords
    nltk.download('stopwords')

    my_stop_words.extend(stopwords.words('english'))
    my_stop_words = [r'\b' + i + r'\b' for i in my_stop_words]

    clean_pattern = "|".join(my_stop_words)
    df['content'] = df['content'].map(lambda x: re.sub(clean_pattern, '', x))
    df['text_len'] = df['content'].map(lambda x: len(x))
    df['write_time'].fillna(method='ffill', inplace=True)
    return df


def freq_visualize(df: pd.DataFrame, type: str, max=200):
    path = os.path.join('freq_visual', type + '.html')

    a = word_count(df['content'])
    a = sorted(a.items(), key=lambda x: x[1], reverse=True)
    vocab = []
    freq = []
    print(len(a))
    for i in a[0:200]:
        vocab.append(i[0])
        freq.append(i[1])
    # print(vocab)
    # print(cover_df['text_len'])
    # print(cover_df['write_time'])

    c = (
        Bar(init_opts=opts.InitOpts(
            theme=ThemeType.MACARONS,
            width='1500px',
            height='800px'
        )
        )

            .add_xaxis(
            vocab,
        )
            .add_yaxis(
            "freq", freq
        )
            .reversal_axis()
            # 全局配置项
            .set_global_opts(
            # 设置x轴  （轴标签旋转-15度（顺时针））
            # xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-75)),
            # 标题配置项
            yaxis_opts=opts.AxisOpts(is_inverse=True),
            title_opts=opts.TitleOpts(title="WSJ 词频统计", subtitle='By YoimiyaInUSTC'),

            visualmap_opts=opts.VisualMapOpts(type_='color'
                                              , max_=300, min_=0,
                                              range_text=['高', '低'],
                                              dimension=0
                                              ),
            # title_opts=opts.TitleOpts(title="Bar-DataZoom（slider+inside）"),
            # 设置操作图表缩放功能，orient="vertical" 为Y轴 滑动
            datazoom_opts=[
                opts.DataZoomOpts(
                    type_='slider',
                    orient='vertical',
                    range_start=0,
                    range_end=10
                ),
                opts.DataZoomOpts(
                    type_='inside',
                    orient='vertical',
                    is_zoom_lock=True
                ),
                opts.DataZoomOpts(
                    range_end=100
                )
            ]
        )
            .set_series_opts(label_opts=opts.LabelOpts(position='right'))
            .render(path)
    )


source_path = r'D:\Python Projects\Crawler\wsj_selenium_crawler\source'

cover_folder_path = os.path.join(source_path, 'cover', 'csv')
market_folder_path = os.path.join(source_path, 'market', 'csv')

cover_df = data_clean(folderpath2df(cover_folder_path).drop_duplicates())
market_df = data_clean(folderpath2df(market_folder_path).drop_duplicates())

cover_df.to_csv(os.path.join('source', 'cover.csv'), sep=',', header=True, index=True)
market_df.to_csv(os.path.join('source', 'market.csv'), sep=',', header=True, index=True)

freq_visualize(cover_df, type='cover')
freq_visualize(market_df, type='market')
