import os
import subprocess
import re

from dzi_builder.core.toolkit import (
    get_layer_list
)


TILE_NAME = '{}-{}.png'
ROW_NAME = '{}-row{}tile{}.png'


def combine_transparent_layer(layer_path, col, row, offset_right, offset_down, vips_path, verbose=False):
    """


    Here, I'm pointing to the location of vips.exe and using subprocess, rather than pyvips, as there seems, for
    some users, to be an issue with locating _libvips when attempting to import pyvips; see:

        https://github.com/libvips/pyvips/issues/86
        https://github.com/libvips/pyvips/issues/83
        https://github.com/libvips/pyvips/issues/76
        https://github.com/libvips/pyvips/issues/59
        etc

    I'm not using anaconda or docker, but I had the same issue when I tried to add an option to run vips
    from pyvips rather than from subprocess - which I was initially just using to get a working script going
    and was going to deprecate after I was finished - and I may do so in the future - but for now, it's easy
    enough to point the script to wherever you compiled/unzipped vips-dev-x.x

    :param layer_path:
    :param col:
    :param row:
    :param offset_right:
    :param offset_down:
    :param vips_path:
    :param verbose:         bool, optional      if True, prints out details of task
    :return:
    """
    dzi_layer_list = []
    layer_list = get_layer_list(layer_path)

    for l in layer_list:
        rows_list = make_rows(layer_path, col, row, l, offset_right, vips_path, verbose=verbose)
        layer_png = make_columns(layer_path, rows_list, l, offset_down, vips_path, verbose=verbose)
        dzi_layer_list.append(layer_png)

    return dzi_layer_list


def make_rows(tile_path, columns, rows, layer, offset, vips_path, verbose=False):
    """
    https://libvips.github.io/libvips/
    :param tile_path:
    :param columns:
    :param rows:
    :param layer:
    :param offset:
    :param vips_path:
    :param verbose:         bool, optional      if True, prints out details of task
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

            merge = 'vips merge {0}{1} {0}{2} {0}{3} horizontal {4} 0'.format(
                tile_path,
                tile_to_add,
                prior_row_output,
                current_row_output,
                temp_offset
            )
            print(merge) if verbose else None

            sp_out = subprocess.run(merge, cwd=vips_path, shell=True, capture_output=verbose, text=verbose)
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
    https://libvips.github.io/libvips/
    :param tile_path:
    :param row_list:
    :param layer:
    :param offset:
    :param vips_path:
    :param verbose:         bool, optional      if True, prints out details of task
    :return:
    """
    row_ct = 0
    row_iter = len(row_list) - 1
    temp_offset = offset

    while row_ct < row_iter:
        if row_ct == 0:
            prior_output = ROW_NAME.format(layer, row_ct, row_iter)
        else:
            prior_output = TILE_NAME.format(layer, row_ct - 1)
        row_to_add = ROW_NAME.format(layer, row_ct + 1, row_iter)
        current_output = TILE_NAME.format(layer, row_ct)

        merge = 'vips merge {0}{1} {0}{2} {0}{3} vertical 0 {4}'.format(
            tile_path,
            row_to_add,
            prior_output,
            current_output,
            temp_offset
        )
        print(merge) if verbose else None

        sp_out = subprocess.run(merge, cwd=vips_path, shell=True, capture_output=verbose, text=verbose)
        print(sp_out.stdout) if verbose else None

        os.remove(tile_path + prior_output)
        os.remove(tile_path + row_to_add)

        row_ct += 1
        temp_offset += offset

    layer_output = re.sub(r'-\d{1}', '', current_output)
    os.rename(tile_path + current_output, tile_path + layer_output)

    return layer_output


def make_image_pyramid(layer_path, layer_list, vips_path, verbose=False):
    """

    :param layer_path:      str, required       folder path, e.g. 'C:\\path\\to\\file\\'
    :param layer_list:      list, required      list of layer names, e.g. ['river', 'base', 'grid']
    :param output_prefix:
    :param vips_path:
    :param verbose:         bool, optional      if True, prints out details of task
    :return:
    """

    for layer in layer_list:
        dz_save = 'vips dzsave {0}{1} {2}{3} --suffix .png'.format(
            layer_path,
            layer + '.png',
            layer_path + 'html\\dzi\\',
            layer
        )
        print(dz_save) if verbose else None

        sp_out = subprocess.run(dz_save, cwd=vips_path, shell=True, capture_output=verbose, text=verbose)
        print(sp_out.stdout) if verbose else None


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
