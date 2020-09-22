import subprocess


def convert_tiles(path, width, height=0, verbose=False):
    """
    Covert all svg files in a given folder path to png. Only width of png output must be given; if no height
    is given, height defaults to width.

    See more on ImageMagick's mogrify command here:

        https://www.imagemagick.org/Usage/basics/#mogrify
        https://www.imagemagick.org/script/mogrify.php

    :param path:            str, required       folder path, e.g. 'C:\path\to\file\'
    :param width:           int, required       width of output tile
    :param height:          int, optional       height of output tile; if 0, height is equal to length
    :param verbose:         bool, optional      if True, prints out any mogrify errors
    :return:                none
    """
    h = width if height == 0 else height

    mogrify = 'mogrify -format png -size {}x{} {}*.svg -verbose'.format(width, h, path)
    sp_out = subprocess.run(mogrify, capture_output=verbose, text=verbose)
    print(sp_out.stdout) if verbose else None

    # if cp.returncode == 0:
    #     print(cp.stdout) if verbose else None
    # else:
    #     raise RuntimeError('mogrify failed; check that all text was converted to outlines in Illustrator.')


def combine_tiles(path, layers, width, columns, height=0, verbose=False):
    """

    :param path:            str, required       folder path, e.g. 'C:\path\to\file\'
    :param layers:          list, required      list of layer names generated by generate_tiles()
    :param width:           int, required       width of output tile
    :param columns:         int, required       number of columns in tile grid to montage
    :param height:          int, optional       height of output tile; if 0, height is equal to length
    :param verbose:         bool, optional      if True, prints out any montage errors
    :return:                none
    """
    h = width if height == 0 else height

    for layer in layers:
        print('Begin combining {}.'.format(layer)) if verbose else None

        montage = 'montage -density 300 -tile {0}x0 -size {1}x{2} -geometry +0+0 -border 0 {3}{4}*.png {3}{4}.png'\
            .format(columns, width, h, path, layer)
        sp_out = subprocess.run(montage, capture_output=verbose, text=verbose)
        print(sp_out.stdout) if verbose else None

        print('Complete combining {}.'.format(layer)) if verbose else None
