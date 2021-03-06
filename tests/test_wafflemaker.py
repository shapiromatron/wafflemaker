#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wafflemaker` package."""

import tempfile

import numpy as np
import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import pytest
import requests

from wafflemaker import waffle, CellFillDirection


@pytest.fixture
def df():
    return pd.DataFrame(dict(
        values=[4, 3, 2],
        categories=['category #1', 'category #2', 'category #3'],
        hues=['blue', 'orange', 'white']
    ))


# DATA
@pytest.mark.mpl_image_compare
def test_data_list(df):
    return waffle(
        nrows=3, ncols=3,
        values=[4, 3, 2],
        title='data: list'
    ).figure


@pytest.mark.mpl_image_compare
def test_data_nparray(df):
    return waffle(
        nrows=3, ncols=3,
        values=np.array([4, 3, 2]),
        title='data: np.ndarray'
    ).figure


@pytest.mark.mpl_image_compare
def test_data_dataframe(df):
    return waffle(
        nrows=3, ncols=3,
        values='values',
        data=df,
        title='data: pd.DataFrame'
    ).figure


# UNSCALED DATA
def test_unscaled_validation():
    fail_kwargs = [
        dict(values=[10, 20]),
        dict(nrows=3, values=[10, 20]),
        dict(ncols=3, values=[10, 20]),
        dict(scale_to_dims=False, values=[10, 20]),
        dict(nrows=3, ncols=3, scale_to_dims=False, values=[10, 20])
    ]
    for kwargs in fail_kwargs:
        with pytest.raises(ValueError):
            waffle(**kwargs)


@pytest.mark.mpl_image_compare
def test_unscaled_data_column(df):
    return waffle(
        ncols=8,
        scale_to_dims=False,
        values=[25, 15, 10],
        labels=['A', 'B', 'C'],
        title='data: unscaled, column specified',
        fill_direction=CellFillDirection.ByRow,
    ).figure


@pytest.mark.mpl_image_compare
def test_unscaled_data_row(df):
    return waffle(
        nrows=4,
        scale_to_dims=False,
        values=[25, 15, 10],
        labels=['A', 'B', 'C'],
        title='data: unscaled, row specified',
        fill_direction=CellFillDirection.ByColumn,
    ).figure


# EMBEDDING
@pytest.mark.mpl_image_compare
def test_subplot(df):
    np.random.seed(123)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for i, ax in enumerate(axes):
        data = np.random.normal(100, 50, 4)
        data.sort()
        waffle(nrows=7, ncols=5,
               values=list(reversed(data)),
               title='subplot #%d' % (i + 1),
               ax=ax)
    return fig


# LAYOUT
@pytest.mark.mpl_image_compare
def test_order_row(df):
    return waffle(
        nrows=3, ncols=3,
        values='values', hue='hues', data=df,
        fill_direction=CellFillDirection.ByRow,
        title='layout: row'
    ).figure


@pytest.mark.mpl_image_compare
def test_order_column(df):
    return waffle(
        nrows=3, ncols=3,
        values='values', hue='hues', data=df,
        fill_direction=CellFillDirection.ByColumn,
        title='layout: column'
    ).figure


# LEGEND
@pytest.mark.mpl_image_compare
def test_legend_dataframe(df):
    return waffle(
        nrows=3, ncols=3,
        values='values', labels='categories', data=df,
        title='legend: pd.DataFrame'
    ).figure


@pytest.mark.mpl_image_compare
def test_legend_list(df):
    return waffle(
        nrows=3, ncols=3,
        values='values',
        labels=['a', 'b', 'c'], data=df,
        title='legend: list'
    ).figure


@pytest.mark.mpl_image_compare
def test_legend_long(df):
    return waffle(
        nrows=3, ncols=3,
        values='values',
        labels=[
            'Supercalifragilisticexpialidocious',
            'Even though the sound of it\nIs something quite atrocious',
            'If you say it loud enough\nYou\'ll always sound precocious',
        ], data=df,
        title='legend: long label'
    ).figure


# FIGURE_OPTIONS
def test_figure_options(df):
    # custom figsize
    fig = waffle(
        nrows=3, ncols=3,
        values='values', data=df,
        figure_options={'figsize': (10, 10)}
    ).figure
    figsize = fig.get_size_inches()
    assert np.isclose(figsize, (10, 10), atol=0.1).all()


# ICON
@pytest.mark.mpl_image_compare
def test_icon(df):
    # custom figsize
    return waffle(
        nrows=3, ncols=3,
        values='values', labels='categories', data=df,
        icon='\u26AB',
        background_color='#efefef',
        icon_options=dict(fontsize=130),
        icon_legend_options=dict(fontsize=30),
        grid_options=dict(color='#eaeaea', linewidth=10),
        title='icon: custom icon'
    ).figure


@pytest.mark.mpl_image_compare
def test_unscaled_icon(df):
    # custom figsize
    return waffle(
        nrows=5,
        values='values', labels='categories', hue=['r', 'g', 'b'], data=df,
        icon='\u2764',
        scale_to_dims=False,
        background_color='grey',
        icon_options=dict(fontsize=75),
        icon_legend_options=dict(fontsize=30),
        grid_options=dict(color='black', linewidth=10),
        title='icon: custom icon'
    ).figure


# COLOR
@pytest.mark.mpl_image_compare
def test_color_base(df):
    return waffle(
        nrows=3, ncols=3,
        values='values', data=df,
        title='color: default'
    ).figure


@pytest.mark.mpl_image_compare
def test_color_dataframe(df):
    return waffle(
        nrows=3, ncols=3,
        values='values', hue='hues', data=df,
        title='color: pd.DataFrame'
    ).figure


@pytest.mark.mpl_image_compare
def test_color_colormap(df):
    return waffle(
       nrows=3, ncols=3,
       values='values', data=df, colormap=mpl.cm.Purples_r,
       title='color: colormap'
    ).figure


@pytest.mark.mpl_image_compare
def test_color_list(df):
    return waffle(
        nrows=3, ncols=3,
        values='values', hue=['#c1d3a2', '#1d4dff', '#cecece'], data=df,
        title='color: list'
    ).figure


# BACKGROUND COLOR
@pytest.mark.mpl_image_compare
def test_background_color(df):
    return waffle(
        nrows=3, ncols=3,
        values='values', data=df,
        background_color='black',
        title='background color: black'
    ).figure


# GRID STYLES
@pytest.mark.mpl_image_compare
def test_grid_color_base(df):
    return waffle(
        nrows=3, ncols=3,
        values='values', data=df,
        title='grid: base'
    ).figure


@pytest.mark.mpl_image_compare
def test_grid_color_altered(df):
    return waffle(
        nrows=3, ncols=3,
        values='values', data=df,
        grid_options=dict(color='black', linewidth=25),
        title='grid: custom'
    ).figure


# DOCUMENTATION
@pytest.mark.mpl_image_compare
def test_docs_household_debt(df):
    # https://github.com/hrbrmstr/waffle
    # http://www.nytimes.com/2008/07/20/business/20debt.html
    df = pd.DataFrame(dict(
        values=[84911, 14414, 10062, 8565],
        categories=['Mortgage ($85k)', 'Auto and tuition loans ($14k)', 'Home equity loans ($10k)', 'Credit cards ($9k)'],
        hues=["#c7d4b6", "#a3aabd", "#a0d0de", "#97b5cf"]
    ))

    df['scaled_values'] = df['values'] / 500.

    return waffle(
        nrows=7,
        scale_to_dims=False,

        data=df,
        values='scaled_values',
        labels='categories',
        hue='hues',

        title='Average Household Debt',
        grid_options=dict(linewidth=2),
        figure_options=dict(figsize=(14, 5)),

    ).figure


@pytest.mark.mpl_image_compare
def test_docs_icon(df):
    font_awesome_url = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/fonts/fontawesome-webfont.ttf'
    tf = tempfile.NamedTemporaryFile()
    r = requests.get(font_awesome_url)
    with open(tf.name, 'wb') as f:
        f.write(r.content)

    # use font in waffle plot
    prop = fm.FontProperties(fname=tf.name)

    # build plot
    figure = waffle(
            nrows=3, ncols=3,
            values='values', labels='categories', data=df,
            colormap=mpl.cm.cool,
            icon='\uf015',
            background_color='#efefef',
            icon_options=dict(fontproperties=prop, size=85),
            icon_legend_options=dict(size=20),
            grid_options=dict(color='#eaeaea', linewidth=15),
            title='icon: custom icon'
        ).figure

    # delete temporary font
    tf.close()

    return figure
