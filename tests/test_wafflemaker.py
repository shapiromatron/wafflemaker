#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wafflemaker` package."""

import numpy as np
import pytest
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

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
        3, 3,
        values=[4, 3, 2],
        title='data: list'
    ).figure


@pytest.mark.mpl_image_compare
def test_data_nparray(df):
    return waffle(
        3, 3,
        values=np.array([4, 3, 2]),
        title='data: np.ndarray'
    ).figure


@pytest.mark.mpl_image_compare
def test_data_dataframe(df):
    return waffle(
        3, 3,
        values='values',
        data=df,
        title='data: pd.DataFrame'
    ).figure


# EMBEDDING
@pytest.mark.mpl_image_compare
def test_subplot(df):
    np.random.seed(123)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for i, ax in enumerate(axes):
        data = np.random.normal(100, 50, 4)
        data.sort()
        waffle(7, 5,
               values=list(reversed(data)),
               title='subplot #%d' % (i + 1),
               ax=ax)
    return fig


# LAYOUT
@pytest.mark.mpl_image_compare
def test_order_row(df):
    return waffle(
        3, 3,
        values='values', hue='hues', data=df,
        fill_direction=CellFillDirection.ByRow,
        title='layout: row'
    ).figure


@pytest.mark.mpl_image_compare
def test_order_column(df):
    return waffle(
        3, 3,
        values='values', hue='hues', data=df,
        fill_direction=CellFillDirection.ByColumn,
        title='layout: column'
    ).figure


# LEGEND
@pytest.mark.mpl_image_compare
def test_legend_dataframe(df):
    return waffle(
        3, 3,
        values='values', labels='categories', data=df,
        title='legend: pd.DataFrame'
    ).figure


@pytest.mark.mpl_image_compare
def test_legend_list(df):
    return waffle(
        3, 3,
        values='values',
        labels=['a', 'b', 'c'], data=df,
        title='legend: list'
    ).figure


@pytest.mark.mpl_image_compare
def test_legend_long(df):
    return waffle(
        3, 3,
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
        3, 3,
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
        3, 3,
        values='values', labels='categories', data=df,
        icon='\u26AB',
        background_color='#efefef',
        icon_options=dict(fontsize=100),
        grid_options=dict(color='#eaeaea', linewidth=10),
        title='icon: custom icon'
    ).figure


# COLOR
@pytest.mark.mpl_image_compare
def test_color_base(df):
    return waffle(
        3, 3,
        values='values', data=df,
        title='color: default'
    ).figure


@pytest.mark.mpl_image_compare
def test_color_dataframe(df):
    return waffle(
        3, 3,
        values='values', hue='hues', data=df,
        title='color: pd.DataFrame'
    ).figure


@pytest.mark.mpl_image_compare
def test_color_colormap(df):
    return waffle(
       3, 3,
       values='values', data=df, colormap=mpl.cm.Purples_r,
       title='color: colormap'
    ).figure


@pytest.mark.mpl_image_compare
def test_color_list(df):
    return waffle(
        3, 3,
        values='values', hue=['#c1d3a2', '#1d4dff', '#cecece'], data=df,
        title='color: list'
    ).figure


# BACKGROUND COLOR
@pytest.mark.mpl_image_compare
def test_background_color(df):
    return waffle(
        3, 3,
        values='values', data=df,
        background_color='black',
        title='background color: black'
    ).figure


# GRID STYLES
@pytest.mark.mpl_image_compare
def test_grid_color_base(df):
    return waffle(
        3, 3,
        values='values', data=df,
        title='grid: base'
    ).figure


@pytest.mark.mpl_image_compare
def test_grid_color_altered(df):
    return waffle(
        3, 3,
        values='values', data=df,
        grid_options=dict(color='black', linewidth=25),
        title='grid: custom'
    ).figure
