import os
import re
import shutil

from dzi_builder.core.toolkit import (
    get_file_list
)

from dzi_builder.core.vips import (
    tile_number
)


def build_matrix(tile_list, filler, duplicate_list, col, row):
    """
    Constructs lists of layers with filler tile placeholders, as well as filler tile names per layer. Passes to
    restructure_layer_matrix() for copying and renaming of tiles:

        layers_lists returns a list of lists, one list for each tile, with added "filler" tiles at the end, e.g.:

            [['base-000.png', 'base-001.png', ...],
             ['grid-000.png', 'grid-001.png', ...]]

        filler_list returns a list of "filler" tiles for each layer, e.g.:

            ['base-003.png', 'grid-003.png']

    :param tile_list:       list, required      list of all tiles in folder, e.g. ['base-000.png', 'base-001.png'...]
    :param filler:          int, required       "filler" tile position to duplicate into duplicate_list positions
    :param duplicate_list:  list, required      int tile positions to duplicate "filler" tile into, e.g. [7, 11, 12]
    :param col:             int, required       count of artboard columns in Illustrator file (starting at 1)
    :param row:             int, required       count of artboard rows in Illustrator file (starting at 1)
    :return:                list                layers_lists:   list of layer tile lists, e.g. [[...], [...]]
                            list                filler_list:    list of filler tiles for each layer
    """
    filler_list = []
    layer_list = []
    layers_lists = []

    for tile in tile_list:
        tile = re.sub(r'(?=-).*', '', tile)
        layer_list.append(tile)
    layer_list = list(set(layer_list))

    for layer in layer_list:
        layer_tiles = [tile for tile in tile_list if tile.startswith(layer)]
        squared_matrix, filler_tile = build_layer_matrix(layer_tiles, filler, duplicate_list, col, row)

        filler_list.append(filler_tile)
        layers_lists.append(squared_matrix)

    return layers_lists, filler_list


def build_layer_matrix(tile_list, filler, duplicate_pos, col, row):
    """
    For a given layer, for each int in duplicate_pos, append "filler" tile name once, creating a number of items in list
    equal to col x row.

    In a 3x3 matrix where filler tile was in position 2 and missing tiles in positions [5, 7, 8], squared_matrix list
    would return:

        ['t-000.png', 't-001.png', 't-002.png',
         't-003.png', 't-004.png', 't-006.png',
         't-002.png', 't-002.png', 't-002.png']

    This is then passed to restructure_layer_matrix() for renaming of tiles, including "filler" positions.

    :param tile_list:       list, required      list of tiles in a layer, e.g. ['base-001.png', 'base-002.png', ...]
    :param filler:          int, required       "filler" tile position to duplicate into duplicate_list positions
    :param duplicate_pos:   list, required      int tile positions to duplicate "filler" tile into, e.g. [7, 11, 12]
    :param col:             int, required       count of artboard columns in Illustrator file (starting at 1)
    :param row:             int, required       count of artboard rows in Illustrator file (starting at 1)

    :return:                list                squared_matrix: list of tile names to make a complete matrix
                            str                 filler_tile:    name of "filler" tile
    """
    tile = col * row

    filler_tile = ''
    squared_matrix = []

    t_iter = t_iter_list = 0

    while t_iter < tile:
        if t_iter in duplicate_pos:
            squared_matrix.append(filler_tile)
        else:
            if t_iter_list == filler:
                filler_tile = tile_list[filler]
            squared_matrix.append(tile_list[t_iter_list])
            t_iter_list += 1
        t_iter += 1

    return squared_matrix, filler_tile


def create_matrix(col, row, tile_list=None):
    """
    Generates a tile matrix diagram to be printed to user based on column and row count, e.g.:

        First call:     None
        Second:         [0]
        Third:          [0]    [1]
        Fourth:         [0]    [1]    [2]
        etc.

    Until a complete matrix is constructed:

        [0]    [1]    [2]    [3]
        [4]    [5]    [6]    [7]
        [8]    [9]    [10]   [11]
        [12]   [13]   [14]   [15]

    :param col:             int, required       count of artboard columns in Illustrator file (starting at 1)
    :param row:             int, required       count of artboard rows in Illustrator file (starting at 1)
    :param tile_list:       str, optional       formatted matrix of tile numbers
    :return:                str                 printable tile number matrix
    """
    tile_matrix_str = ''
    tiles_ct = 0

    while tiles_ct < col * row:
        spacing = make_spacing(tiles_ct) if not tile_list else '  '
        try:
            tile = tile_list[tiles_ct] if tile_list else str(tiles_ct)
        except IndexError:
            tile = ' '

        if tiles_ct % col == 0:
            tile_matrix_str += '\n'

        tile_matrix_str += '[' + tile + ']' + spacing
        tiles_ct += 1

    print(tile_matrix_str)


def get_filler_tiles():
    """
    Requests from user location of "filler" tile, and "empty" locations in the tile matrix in which to place "filler".

    :return:                int     f_tile          "filler" tile number
                            list    duplicates_sep  matrix locations to place "filler" tile
    """
    dialog_get_filler_tile_space = 'Enter number of tile to duplicate into empty spaces (e.g. 3): '
    dialog_get_filler_tiles_list = \
        'List tiles, separated by commas, where \'filler tile\' should be placed (e.g. 4,5,6): '

    f_tile = int(input(dialog_get_filler_tile_space))
    duplicate_spaces = input(dialog_get_filler_tiles_list)
    duplicates_sep = [int(i) for i in duplicate_spaces.replace(' ', '').split(',')]

    return f_tile, duplicates_sep


def make_spacing(tiles_ct):
    """
    Given a tile number (0-n), determines the number of spaces between it and the next, to generate a row of tiles in
    create_matrix() for the tile matrix diagram printed to user, e.g.:

        [0]    [1]    [2]    [3]

    :param tiles_ct:        int, required       tile number
    :return:                str                 str of empty spaces between two tile numbers
    """
    ct = len(str(tiles_ct))

    if ct == 1:
        spacing = '    '
    elif ct == 2:
        spacing = '   '
    else:
        spacing = '  '

    return spacing


def reset_tile_names(layer_path):
    """

    :param layer_path:       str, required       folder path, e.g. 'C:\\path\\to\\file\\'
    :return:
    """
    tile_list = get_file_list(layer_path)
    for tile in tile_list:
        layer_name = re.match(r'^\D+', tile).group(0)
        layer_number = tile.replace(layer_name, '')
        reformatted_layer_name = layer_name + '-' + layer_number
        os.rename(layer_path + tile, layer_path + reformatted_layer_name)


def restructure_layer_matrix(layer_path, layers_list, layer_names, filler_list):
    """
    Iterates through each tile list in layers_list, renaming numbers (000, 001, etc.) of existing and "filler" tiles,
    creating "filler" tiles where necessary.

    :param layer_path:      str, required       folder path, e.g. 'C:\\path\\to\\file\\'
    :param layers_list:     list, required      list of tiles list, e.g. [['base-000.png', ...], ['grid-000.png', ...]]
    :param layer_names:     list, required      list of layer names, e.g. ['base', 'grid']
    :param filler_list:     list, required      list of "filler" tiles by layer, e.g. ['base-003.png', 'grid-003.png']
    :return:                none
    """
    layer_ct = 0
    file_to_remove = ''

    for layer in layers_list:
        tile_ct = 0
        layer_name = layer_names[layer_ct]
        for tile in layer:
            t = tile_number(tile_ct)
            if tile == filler_list[layer_ct]:
                file_to_remove = tile
                shutil.copy(layer_path + tile, layer_path + layer_name + t + '.png')
            else:
                os.rename(layer_path + tile, layer_path + layer_name + t + '.png')
            tile_ct += 1
        layer_ct += 1
        os.remove(layer_path + file_to_remove)

    reset_tile_names(layer_path)
