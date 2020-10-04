import os
import re
import shutil

from dzi_builder.core.toolkit import (
    get_file_list
)

from dzi_builder.core.vips import (
    tile_number
)


def build_matrix(tile_list, filler, duplicate_spaces, col, row):
    """

    :param tile_list:
    :param filler:
    :param duplicate_spaces:
    :param col:
    :param row:
    :return:
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
        squared_matrix, filler_tile = build_layer_matrix(layer_tiles, filler, duplicate_spaces, col, row)

        filler_list.append(filler_tile)
        layers_lists.append(squared_matrix)

    return layers_lists, filler_list


def build_layer_matrix(tile_list, filler, duplicate_spots, col, row):
    """

    :param tile_list:
    :param filler:
    :param duplicate_spots:
    :param col:
    :param row:
    :return:
    """
    tile = col * row

    filler_tile = ''
    squared_matrix = []

    t_iter = t_iter_list = 0

    while t_iter < tile:
        if t_iter in duplicate_spots:
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

    :param col:
    :param row:
    :param tile_list:
    :return:
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

    :return:
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

    :param tiles_ct:
    :return:
    """
    ct = len(str(tiles_ct))

    if ct == 1:
        spacing = '    '
    elif ct == 2:
        spacing = '   '
    else:
        spacing = '  '

    return spacing


def reset_tile_names(tile_path):
    """

    :param tile_path:
    :return:
    """
    tile_list = get_file_list(tile_path)
    for tile in tile_list:
        layer_name = re.match(r'^\D+', tile).group(0)
        layer_number = tile.replace(layer_name, '')
        reformatted_layer_name = layer_name + '-' + layer_number
        os.rename(tile_path + tile, tile_path + reformatted_layer_name)


def restructure_layer_matrix(tile_path, layers_list, layer_names, filler_list):
    """

    :param tile_path:
    :param layers_list:
    :param layer_names:
    :param filler_list:
    :return:
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
                shutil.copy(tile_path + tile, tile_path + layer_name + t + '.png')
            else:
                os.rename(tile_path + tile, tile_path + layer_name + t + '.png')
            tile_ct += 1
        layer_ct += 1
        os.remove(tile_path + file_to_remove)

    reset_tile_names(tile_path)
