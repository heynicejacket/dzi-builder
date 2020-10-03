# todo: this is a work in progress

import re

# from dzi_builder.core.vips import (
#     tile_number
# )


def build_matrix(tile_list, filler, duplicate_spots, col, row):
    tile = col * row

    tile_filler = ''
    full_matrix = []

    t_iter = t_iter_list = 0

    while t_iter < tile:
        if t_iter in duplicate_spots:
            full_matrix.append(tile_filler)
        else:
            if t_iter_list == filler:
                tile_filler = tile_list[filler]
            full_matrix.append(tile_list[t_iter_list])
            t_iter_list += 1
        t_iter += 1

    # t = 0
    # retitled_matrix = []
    # for tile in full_matrix:
    #     t_str = tile_number(t)
    #     new_tile = re.sub(r'\d{3}', t_str, tile)
    #     retitled_matrix.append(new_tile)
    #     t += 1
    # print(retitled_matrix)

    return full_matrix


def create_matrix(col, row, tile_list=None):
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

    return tile_matrix_str


def get_filler_tiles():
    dialog_get_filler_tile_space = 'Enter number of tile to duplicate into empty spaces: '
    dialog_get_filler_tiles_list = \
        'List tile numbers, separated by commas, where \'filler tile\' should be placed: '

    f_tile = int(input(dialog_get_filler_tile_space))
    duplicate_spaces = input(dialog_get_filler_tiles_list)
    duplicates_sep = [int(i) for i in duplicate_spaces.replace(' ', '').split(',')]

    return f_tile, duplicates_sep


def make_spacing(tiles_ct):
    ct = len(str(tiles_ct))

    if ct == 1:
        spacing = '    '
    elif ct == 2:
        spacing = '   '
    else:
        spacing = '  '

    return spacing


r = 4
c = 4
t_list = [
    'base-000.png', 'base-001.png', 'base-002.png', 'base-003.png',
    'base-004.png', 'base-005.png', 'base-006.png',
    'base-007.png', 'base-008.png', 'base-009.png',
                    'base-010.png',
]
#     'paths-000.png', 'paths-001.png', 'paths-002.png', 'paths-003.png',
#     'paths-004.png', 'paths-005.png', 'paths-006.png',
#     'paths-007.png', 'paths-008.png', 'paths-009.png',
#                      'paths-010.png'
# ]

print(create_matrix(c, r))
filler_tile, duplicates = get_filler_tiles()
build_matrix(t_list, filler_tile, duplicates, c, r)
