import os
import subprocess

from dzi_builder.core.toolkit import (
    get_layer_list
)


TILE_NAME = '{}-{}.png'
ROW_NAME = '{}-row{}tile{}.png'


def combine_transparent_layer(layer_path, col, row, offset_right, offset_down, vips_path, verbose=False):
    """
    # TODO: replace vips with pyvips, and/or make helper function to find vips.exe for vips_path
    :param layer_path:
    :param col:
    :param row:
    :param offset_right:
    :param offset_down:
    :param vips_path:
    :param verbose:
    :return:
    """
    layer_list = get_layer_list(layer_path)
    for l in layer_list:
        rows_list = make_rows(layer_path, col, row, l, offset_right, vips_path, verbose=verbose)
        layer_png = make_columns(layer_path, rows_list, l, offset_down, vips_path, verbose=verbose)

    return layer_png


def make_rows(tile_path, columns, rows, layer, offset, vips_path, verbose=False):
    """
    https://libvips.github.io/libvips/
    :param tile_path:
    :param columns:
    :param rows:
    :param layer:
    :param offset:
    :param vips_path:
    :param verbose:
    :return:
    """
    final_rows = []
    row_ct = tile_iter = 0
    while row_ct < rows:
        col_ct = 0
        temp_offset = offset
        while col_ct < columns - 1:
            tile_to_add = TILE_NAME.format(layer, tile_number(col_ct, 1 + tile_iter - col_ct))
            current_row_output = ROW_NAME.format(layer, 0 + row_ct, col_ct + 1)
            if col_ct == 0:
                prior_row_output = TILE_NAME.format(layer, tile_number(col_ct, tile_iter))
                remove_temp_row = False
            else:
                prior_row_output = ROW_NAME.format(layer, 0 + row_ct, col_ct)
                remove_temp_row = True

            mogrify = 'vips merge {0}{1} {0}{2} {0}{3} horizontal {4} 0'.format(
                tile_path,
                tile_to_add,
                prior_row_output,
                current_row_output,
                temp_offset
            )

            sp_out = subprocess.run(mogrify, cwd=vips_path, shell=True, capture_output=verbose, text=verbose)
            print(sp_out.stdout) if verbose else None

            os.remove(tile_path + prior_row_output) if remove_temp_row else None

            col_ct += 1
            tile_iter += 1
            temp_offset += offset

        row_ct += 1
        tile_iter += 1
        final_rows.append(current_row_output)

    return final_rows


def make_columns(tile_path, row_list, layer, offset, vips_path, verbose=False):
    """
    # TODO: DELETE TEMP/BUILDING-UP COLUMN IMAGES
    https://libvips.github.io/libvips/
    :param tile_path:
    :param row_list:
    :param layer:
    :param offset:
    :param vips_path:
    :param verbose:
    :return:
    """
    row_ct = 0
    row_iter = len(row_list) - 1
    temp_offset = offset

    while row_ct < row_iter:
        if row_ct == 0:
            row_to_add = ROW_NAME.format(layer, row_ct + 1, row_iter)
            prior_output = ROW_NAME.format(layer, row_ct, row_iter)
        else:
            prior_output = TILE_NAME.format(layer, row_ct - 1)
            row_to_add = ROW_NAME.format(layer, row_ct + 1, row_iter)
        current_output = TILE_NAME.format(layer, row_ct)

        mogrify = 'vips merge {0}{1} {0}{2} {0}{3} vertical 0 {4}'.format(
            tile_path,
            row_to_add,
            prior_output,
            current_output,
            temp_offset
        )

        sp_out = subprocess.run(mogrify, cwd=vips_path, shell=True, capture_output=verbose, text=verbose)
        print(sp_out.stdout) if verbose else None

        row_ct += 1
        temp_offset += offset

    return current_output


def tile_number(a, mod=0):
    """
    Given an int, returns a three-digit string, prefixed with zeroes. For example, if given 9, returns '009' .
    :param a:
    :param mod:
    :return:
    """
    if a + mod < 10:
        i = '00' + str(a + mod)
    elif a + mod >= 10 & a + mod < 100:
        i = '0' + str(a + mod)
    else:
        i = str(a + mod)

    return i
