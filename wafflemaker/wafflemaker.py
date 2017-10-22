# -*- coding: utf-8 -*-

def waffle(plt, series, rows, cols, max_tiles, from_left):
    totals = series.colors + series.grays
    whites = max_tiles - series.colors - series.grays

    class_portion = [
        series.colors / max_tiles,
        series.grays / max_tiles,
        whites / max_tiles
    ]
    tiles_per_class = [
        round(p * max_tiles)
        for p in class_portion
    ]

    if from_left:
        plot_matrix = np.zeros((cols, rows))
        class_index = 0
        tile_index = 0
        for col in range(rows):
            for row in range(cols):
                tile_index += 1
                if tile_index > sum(tiles_per_class[0:class_index]):
                    class_index += 1
                plot_matrix[row, col] = class_index
    else:
        plot_matrix = np.zeros((cols, rows))
        class_index = 0
        tile_index = 0
        for row in reversed(range(cols)):
            for col in range(rows):
                tile_index += 1
                if tile_index > sum(tiles_per_class[0:class_index]):
                    class_index += 1
                plot_matrix[row, col] = class_index

    colormap = mpl.colors.ListedColormap([
        series.colors_color,
        series.grays_color,
        'white'
    ])
    plt.matshow(plot_matrix, cmap=colormap, fignum=False)
    ax = plt.gca()

    ax.set_xticks(np.arange(-.5, (rows), 1), minor=True);
    ax.set_yticks(np.arange(-.5, (cols), 1), minor=True);
    ax.grid(which='minor', color='w', linestyle='-', linewidth=5)

    plt.tick_params(
        axis='both',
        which='both',
        bottom='off',
        left='off',
        top='off',
        labeltop='off',
        labelleft='off'
    )

    for child in ax.get_children():
        if isinstance(child, mpl.spines.Spine):
            child.set_color('w')

    plt.text(
        1.01, 0.8,
        series.text,
        fontsize=16,
        transform=ax.transAxes
    )

def make_waffles(df, rows=None, cols=None, figsize=None, from_left=True):

    max_tiles = -1
    for i, (idx, series) in enumerate(df.iterrows()):
        totals = series.colors + series.grays
        tiles = int(math.ceil(totals / 10.) * 10)
        if tiles > max_tiles:
            max_tiles = tiles

    if rows is not None and cols is not None:
        pass
    elif rows is None and cols is None:
        raise ValueError('Specify rows or cols or both')
    elif rows is None:
        rows = int(max_tiles / cols)
    elif cols is None:
        cols = int(max_tiles / rows)

    if figsize is None:
        figsize = (4, 4)

    plt.figure(figsize=(figsize[0], figsize[1] * 4))
    for i, (idx, series) in enumerate(df.iterrows()):
        plt.subplot(int(f'{df.shape[0]}1{i+1}'))
        waffle(plt, series, rows, cols, max_tiles, from_left)

