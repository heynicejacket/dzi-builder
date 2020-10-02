col = c = 4
row = r = 4
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


def make_spacing(tiles_ct):
    ct = len(str(tiles_ct))
    if ct == 1:
        spacing = '    '
    elif ct == 2:
        spacing = '   '
    else:
        spacing = '  '
    return spacing


def create_matrix(tile_list=None):
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


def build_matrix(tile_list, filler, duplicate_spots):
    # TODO: THIS IS ALL TEST STUFF
    for t in duplicate_spots:
        print('Space {} is tile #{}.'.format(filler, t))

    i = len(tile_list)
    for tile in tile_list:

        print(tile)
        # if t in duplicate_spots:


def get_filler_tiles():
    dialog_get_filler_tile_space = 'Enter number of tile to duplicate into empty spaces: '
    dialog_get_filler_tiles_list = \
        'List tile numbers, separated by commas, where \'filler tile\' should be placed: '

    filler_tile = input(dialog_get_filler_tile_space)
    duplicates = input(dialog_get_filler_tiles_list)
    duplicates_sep = [int(i) for i in duplicates.replace(' ', '').split(',')]

    return filler_tile, duplicates_sep


tile_matrix = create_matrix()
print(tile_matrix)
f_tile, duplicates = get_filler_tiles()
build_matrix(t_list, f_tile, duplicates)
