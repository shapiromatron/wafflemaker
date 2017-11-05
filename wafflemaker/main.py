import matplotlib as mpl
from matplotlib.cm import viridis
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.text import Text
import numpy as np
import pandas as pd

from .constants import CellFillDirection


def _fill_plot_matrix(dims, values: np.ndarray, fill_direction):
    class_portion = values / values.sum()
    tiles = dims[0] * dims[1]
    tiles_per_class = (class_portion * tiles).round()

    class_index = -1
    tile_index = 0
    plot_matrix = np.zeros(dims)
    if fill_direction == CellFillDirection.ByColumn:
        for col in range(dims[1]):
            for row in range(dims[0]):
                tile_index += 1
                if tile_index > sum(tiles_per_class[0:class_index]):
                    class_index += 1
                plot_matrix[row, col] = class_index
    else:
        for row in reversed(range(dims[0])):
            for col in range(dims[1]):
                tile_index += 1
                if tile_index > sum(tiles_per_class[0:class_index]):
                    class_index += 1
                plot_matrix[row, col] = class_index

    return plot_matrix


def _resize_figure(ax, lgd):
    # make sure legend fits on figure [only if legend is to the right]
    ax.figure.canvas.draw()
    inv_figure = ax.figure.transFigure.inverted()

    # get legend coordinates
    lgd_pos = lgd.get_window_extent()
    lgd_coord = inv_figure.transform(lgd_pos)
    lgd_xmax = lgd_coord[1, 0]

    # get axis coordinates
    ax_pos = ax.get_window_extent()
    ax_coord = inv_figure.transform(ax_pos)
    ax_xmax = ax_coord[1, 0]

    # shift to include new coordinates
    shift = 1 - (lgd_xmax - ax_xmax)
    ax.figure.tight_layout(rect=(0, 0, shift, 1))


class TextLegend(object):
    def __init__(self, text, color):
        self.text = text
        self.color = color


class TextLegendHandler(object):
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x = handlebox.xdescent + handlebox.width * 0.5
        annotation = Text(
            x, 3, orig_handle.text,
            horizontalalignment='center',
            verticalalignment='center',
            color=orig_handle.color,
            fontsize=20)
        handlebox.add_artist(annotation)
        return annotation


def waffle(
        nrows, ncols, values=None,
        labels=None, hue=None, data=None,
        rescale=True,
        icon=None,
        icon_options=None,
        fill_direction=CellFillDirection.ByColumn,
        colormap=None, grid_options=None,
        figure_options=None,
        title=None, ax=None,
        show_legend=True,
        background_color='#ffffff'
   ):

    # get data values
    if isinstance(values, np.ndarray):
        pass
    elif isinstance(data, pd.DataFrame) and isinstance(values, str):
        values = data[values].values
    elif isinstance(values, list):
        values = np.array(values)

    # get matrix
    dims = (nrows, ncols)
    plot_matrix = _fill_plot_matrix(dims, values, fill_direction)

    # get colormap
    if colormap is None:
        if hue is None:
            colormap = viridis
        else:
            if isinstance(hue, str) and isinstance(data, pd.DataFrame):
                colormap = mpl.colors.ListedColormap(data[hue].values)
            elif isinstance(hue, list):
                colormap = mpl.colors.ListedColormap(hue)

    # get icon or icon colormap
    if icon is not None:
        icon_colormap = colormap
        colormap = mpl.colors.ListedColormap([background_color])

    if ax is None:
        fig_opts = {}
        if figure_options is None:
            pass
        elif isinstance(figure_options, dict):
            fig_opts.update(figure_options)
        else:
            raise ValueError('Figure options must be dict or None')
        fig = plt.figure(**fig_opts)
        ax = fig.gca()

    ax.matshow(plot_matrix, cmap=colormap)

    # draw icons if exist
    if icon is not None:
        icon_opts = dict(
            va='center',
            ha='center',
            fontsize=30,
        )
        if icon_options is not None:
            icon_opts.update(icon_options)

        x, y = np.meshgrid(
            np.arange(0, nrows, 1),
            np.arange(0, ncols, 1)
        )

        colors = icon_colormap((plot_matrix)/(plot_matrix.max()))
        for i, j in zip(x.flatten(), y.flatten()):
            ax.text(i, j, icon,  color=colors[j, i], **icon_opts)

    ax.set_xticks(np.arange(-0.5, ncols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, nrows, 1), minor=True)
    grid_opts = dict(
        which='minor',
        color=background_color,
        linestyle='-',
        linewidth=5
    )
    if grid_options is None:
        pass
    elif isinstance(grid_options, dict):
        grid_opts.update(grid_options)
    else:
        raise ValueError('Grid options must be dict or None')

    ax.grid(**grid_opts)

    ax.tick_params(
        axis='both',
        which='both',
        bottom='off',
        left='off',
        top='off',
        right='off',
        labeltop='off',
        labelleft='off'
    )

    # remove border
    for child in ax.get_children():
        if isinstance(child, mpl.spines.Spine):
            child.set_color('w')

    # draw legend
    if show_legend and labels is not None:

        if isinstance(labels, list):
            pass
        elif isinstance(labels, str) and isinstance(data, pd.DataFrame):
            labels = [str(d) for d in data[labels].tolist()]
        else:
            raise ValueError('Labels must be a list of strings or the name of a data frame column')

        if icon is None:

            handles = []
            for i, label in enumerate(labels):
                color = colormap(float(i)/(len(labels) - 1))
                handles.append(mpatches.Patch(color=color, label=label))

            legend_args = dict(
                handles=handles,
                loc='center left',
                ncol=1,
                bbox_to_anchor=(1, 0.5)
            )
            lgd = ax.legend(**legend_args)
        else:
            patches = []
            lbls = []

            for i, label in enumerate(labels):
                color = icon_colormap(float(i)/(len(labels) - 1))
                patches.append(TextLegend(icon, color))
                lbls.append(label)

            legend_args = dict(
                loc='center left',
                ncol=1,
                bbox_to_anchor=(1, 0.5),
                handler_map={TextLegend: TextLegendHandler()}
            )
            lgd = ax.legend(patches, lbls, **legend_args)

        _resize_figure(ax, lgd)

    # add title if exists
    if title is not None:
        ax.title.set_text(title)

    return ax
