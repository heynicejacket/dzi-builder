import os
import subprocess
import re

from dzi_builder.core.toolkit import (
    get_layer_list
)

from dzi_builder.core.constants import (
    TILE_NAME,
    ROW_NAME
)


def combine_transparent_layer(layer_path, col, row, offset_right, offset_down, vips_path, verbose=False):
    """
    Uses libvips to combine individual tiles into a complete layer, to convert to a Deep Zoom Image.

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
    :param col:             int, required       count of artboard columns in Illustrator file (starting at 1)
    :param row:             int, required       count of artboard rows in Illustrator file (starting at 1)
    :param offset_right:    int, required       width of artboard tile
    :param offset_down:     int, optional       height of artboard tile
    :param vips_path:       str. required       path to vips.exe, e.g. 'C:\\Program Files\\vips\\bin\\vips.exe'
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


def make_rows(tile_path, col, row, layer, offset, vips_path, verbose=False):
    """
    https://libvips.github.io/libvips/
    :param tile_path:
    :param col:             int, required       count of artboard columns in Illustrator file (starting at 1)
    :param row:             int, required       count of artboard rows in Illustrator file (starting at 1)
    :param layer:
    :param offset:
    :param vips_path:       str. required       path to vips.exe, e.g. 'C:\\Program Files\\vips\\bin\\vips.exe'
    :param verbose:         bool, optional      if True, prints out details of task
    :return:
    """
    final_rows = []
    row_ct = tile_iter = 0

    while row_ct < row:
        col_ct = 0
        temp_offset = offset
        while col_ct < col - 1:
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
    :param vips_path:       str. required       path to vips.exe, e.g. 'C:\\Program Files\\vips\\bin\\vips.exe'
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
    Use libvips to generate a Deep Zoom Image from png in directory, for every layer name provided.
    In the .../layers/html/dzi/ folder, a dzi file and a series of tile pyramid folders will be created:

        dzi/
            layer.dzi

        dzi/layer_files/
                0/
                1/
                2/
                ...

    For more, see: https://libvips.github.io/libvips/API/current/Making-image-pyramids.md.html

    :param layer_path:      str, required       folder path, e.g. 'C:\\path\\to\\file\\'
    :param layer_list:      list, required      list of layer names, e.g. ['river', 'base', 'grid']
    :param vips_path:       str. required       path to vips.exe, e.g. 'C:\\Program Files\\vips\\bin\\vips.exe'
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                none
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


def tile_number(n, mod=0):
    """
    Given an int, returns a three-digit string, prefixed with zeroes. For example, if given 9, returns '009' .

    :param n:               int, required       integer to be converted to a three-character string
    :param mod:             int, optional       integer to add to integer to be converted
    :return:                str                 string constructed from n + mod
    """
    if n + mod < 10:
        s = '00' + str(n + mod)
    elif n + mod >= 10 & n + mod < 100:
        s = '0' + str(n + mod)
    else:
        s = str(n + mod)

    return s
