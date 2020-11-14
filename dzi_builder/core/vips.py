import os
import subprocess

from dzi_builder.core.toolkit import (
    get_layer_list
)

from dzi_builder.core.constants import (
    ARRAYJOIN,
    COMPOSITE,
    DZSAVE
)


def combine_transparent_layer(layer_path, col, vips_path, verbose=False):
    """
    Uses libvips to combine individual tiles into a complete layer, to convert to a Deep Zoom Image.

    Blank tiles and tiles with no transparency are by default produced as 24 bit, while transparent layers have an
    alpha channel (are 32 bit). libvips fails when trying to combine 24 and 32 bit images; as such, the libvips
    function 'composite' is called as a loop on each tile to force-add an alpha channel to the image.

    Once all tiles are 32 bit, a list of all tiles is generated, and fed to the libvips function 'arrayjoin', joining
    all tiles into a single image, with the number of images across corresponding to the col variable of this function.

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

    :param layer_path:      str, required       folder path, e.g. 'C:\\path\\to\\file\\'
    :param col:             int, required       count of artboard columns in Illustrator file (starting at 1)
    :param vips_path:       str. required       path to vips.exe, e.g. 'C:\\Program Files\\vips\\bin\\'
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                none
    """

    try:

        layer_list = []
        vips_fmt_layer_path = layer_path.replace('\\', '\\\\')                  # libvips arrays need double \\ in paths
        lx = 0

        tile_list = [f for f in os.listdir(layer_path) if os.path.isfile(os.path.join(layer_path, f))]
        layer_name_list = get_layer_list(layer_path)

        for l in layer_name_list:

            for layer_name in layer_name_list:
                layer_list.append([t for t in tile_list if t.startswith(layer_name)])

            tile_list = layer_list[lx]
            lx += 1

            for t in tile_list:
                temp_t = 'temp_' + t
                os.rename(layer_path + t, layer_path + temp_t)
                composite = COMPOSITE.format(vips_fmt_layer_path + temp_t, vips_fmt_layer_path + t)
                print(composite) if verbose else None
                subprocess.run(composite, cwd=vips_path, shell=True, capture_output=True, text=True)
                os.remove(layer_path + 'temp_' + t)

            tile_list = [vips_fmt_layer_path + t for t in tile_list]

            tile_array = '"' + ' '.join(tile_list) + '"'
            arrayjoin = ARRAYJOIN.format(tile_array, vips_fmt_layer_path + l + '.png', col)
            print(arrayjoin) if verbose else None
            subprocess.run(arrayjoin, cwd=vips_path, shell=True, capture_output=True, text=True)

    except IndexError as e:
        print('tile_{}; clear non-tile files from layer_path'.format(e))


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
    :param vips_path:       str. required       path to vips.exe, e.g. 'C:\\Program Files\\vips\\bin\\'
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                none
    """
    for layer in layer_list:
        dz_save = DZSAVE.format(
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
    elif (n + mod >= 10) and (n + mod < 100):
        s = '0' + str(n + mod)
    else:
        s = str(n + mod)

    return s
