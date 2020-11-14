import os

from dzi_builder.core.illustrator import (
    generate_tiles
)

from dzi_builder.core.toolkit import (
    create_folder_structure,
    get_file_list,
    get_layer_list
)

from dzi_builder.core.vips import (
    combine_transparent_layer,
    make_image_pyramid
)

from dzi_builder.core.image_magick import (
    convert_tiles,
    combine_tiles
)

from dzi_builder.core.tile_filler import (
    build_matrix,
    create_matrix,
    get_filler_tiles,
    restructure_layer_matrix
)

from dzi_builder.html.openseadragon_html import (
    make_site
)


def create_tiles(ai_path, offset_right, transparency=True):
    """
    Given an Illustrator file, creates a 'layers' folder in place and generates tiles from all Illustrator layers.

    :param ai_path:         str, required       path to Illustrator file, e.g. 'C:\\path\\to\\file.ai'
    :param offset_right:    int, required       width of artboard tile
    :param transparency:    bool, optional      if True, runs subsequent functions through libvips, not ImageMagick
    :return:                list                list of layer names
    """
    offset_right_f = float(offset_right / 10)
    create_folder_structure(ai_path)
    layer_names = generate_tiles(ai_path, offset_right_f, transparency)

    return layer_names


def fill_incomplete(layer_path, col, row, verbose=False):
    """
    Given a folder of individual tiles, fills the grid in with "filler" tiles, as specified by user input.

    :param layer_path:      str, required       folder path, e.g. 'C:\\path\\to\\file\\'
    :param col:             int, required       count of artboard columns in Illustrator file (starting at 1)
    :param row:             int, required       count of artboard rows in Illustrator file (starting at 1)
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                none
    """
    layer_names = get_layer_list(layer_path, verbose=verbose)
    tile_list = get_file_list(layer_path)

    create_matrix(col, row)
    filler_tile_ct, duplicates = get_filler_tiles()
    layers_list, filler_list = build_matrix(tile_list, filler_tile_ct, duplicates, col, row)
    restructure_layer_matrix(layer_path, layers_list, layer_names, filler_list)


def create_layers(layer_path, vips_path, col, offset_right, offset_down=0, transparency=True, verbose=False):
    """
    Given a folder path containing tiles, combines tiles into single layer png files, named for each layer.
    Assumes layer_path contains tiles named [layer]-[iter]; for instance:

        base-000.png    grid-000.png
        base-001.png    grid-001.png
        base-002.png    grid-002.png
        base-003.png    grid-003.png
        etc.

    Combined-layer output would then be:

        base.png        grid.png

    Also assumes tile structure is complete, either NxN or NxM, with no gaps in tiles; e.g., a 3x3 grid has 9 tiles.

    :param layer_path:      str, required       folder path, e.g. 'C:\\path\\to\\file\\'
    :param vips_path:       str. required       path to vips.exe, e.g. 'C:\\Program Files\\vips\\bin\\'
    :param col:             int, required       count of artboard columns in Illustrator file (starting at 1)
    :param offset_right:    int, required       width of artboard tile
    :param offset_down:     int, optional       height of artboard tile
    :param transparency:    bool, optional      if True, runs subsequent functions through libvips, not ImageMagick
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                none
    """
    offset_down_rect = offset_right if offset_down == 0 else offset_down
    layer_names = get_layer_list(layer_path, verbose=verbose)

    if transparency:
        combine_transparent_layer(layer_path, col, vips_path, verbose)
    else:
        convert_tiles(layer_path, offset_right, verbose=verbose)
        [os.remove(layer_path + f) for f in os.listdir(layer_path) if f.endswith('.svg')]
        combine_tiles(layer_path, layer_names, offset_down_rect, col, verbose=verbose)


def create_dzi_and_site(layer_path, vips_path, verbose=False):
    """
    Given a folder path containing layer tiles, creates dzi structures and relevant html/css/js for basic site.

    :param layer_path:      str, required       folder path, e.g. 'C:\\path\\to\\file\\'
    :param vips_path:       str. required       path to vips.exe, e.g. 'C:\\Program Files\\vips\\bin\\'
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                none
    """
    layer_names = get_layer_list(layer_path, verbose=verbose)
    make_image_pyramid(layer_path, layer_names, vips_path, verbose=verbose)
    make_site(layer_path, layer_names)


def dzi_builder(ai_path, vips_path, col, row, offset_right,
                offset_down=0, transparency=True, incomplete=False, verbose=False):
    """
    Given an illustrator file, creates a Deep Zoom Image for each top-level layer of the Illustrator file,
    and generates an html and css file to resolve a basic example, when adding the requisite openseadragon
    and jquery files to /layers/html/openseadragon/:

        https://openseadragon.github.io/#download
        https://jquery.com/download/

    Basic steps to generate the dzi and html are as follows:

    create_folder_structure()
    Generates the necessary folder structure in the location of the target Illustrator file.

    generate_tiles()
    Opens an Illustrator file and creates individual png tiles with JavaScript.

    combine_transparent_layer()
    Uses libvips to combine png tiles into single layer png files.

    make_image_pyramid()
    Use libvips to generate a dzi structure from layer png files, for every layer name provided.

    make_site()
    Generates the necessary html/css/js files for OpenJavascript to load a dzi file on the web.

    By default, make_site() sets any layer named 'base' to the 0th position, and is otherwise ignored for
    opacity toggling; if you need to set a specific order for your layers, do it between make_image_pyramid()
    and make_site() on layers_list, before it is passed to make_site(). if you want all layers to be toggle-able,
    don't have any layers named 'base', or rename the constant BASE_LAYER to some other value.

    See issues that are known to cause failures here: https://github.com/heynicejacket/dzi-builder/issues

    See basic implementation here:
        https://embers.nicejacket.cc/dzi-builder/artboard-simple/viewer.html

    See implementation of incomplete example file here:
        https://embers.nicejacket.cc/dzi-builder/artboard-incomplete/viewer.html

    :param ai_path:         str, required       path to Illustrator file, e.g. 'C:\\path\\to\\file.ai'
    :param vips_path:       str. required       path to vips.exe, e.g. 'C:\\Program Files\\vips\\bin\\'
    :param col:             int, required       count of artboard columns in Illustrator file (starting at 1)
    :param row:             int, required       count of artboard rows in Illustrator file (starting at 1)
    :param offset_right:    int, required       width of artboard tile
    :param offset_down:     int, optional       height of artboard tile
    :param transparency:    bool, optional      if True, runs subsequent functions through libvips, not ImageMagick
    :param incomplete:      bool, optional      if True, requests user input to fill in missing tiles
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                None
    """
    offset_right_f = float(offset_right / 10)
    offset_down_rect = offset_right if offset_down == 0 else offset_down

    layer_path, html_path, dzi_path, osd_path = create_folder_structure(ai_path)

    layer_names = generate_tiles(ai_path, offset_right_f, transparency)

    if incomplete:
        tile_list = get_file_list(layer_path)
        create_matrix(col, row)
        filler_tile_ct, duplicates = get_filler_tiles()
        layers_list, filler_list = build_matrix(tile_list, filler_tile_ct, duplicates, col, row)
        restructure_layer_matrix(layer_path, layers_list, layer_names, filler_list)

    if transparency:
        combine_transparent_layer(layer_path, col, vips_path, verbose)
    else:
        convert_tiles(layer_path, offset_right, verbose=verbose)
        [os.remove(layer_path + f) for f in os.listdir(layer_path) if f.endswith('.svg')]
        combine_tiles(layer_path, layer_names, offset_down_rect, col, verbose=verbose)

    make_image_pyramid(layer_path, layer_names, vips_path, verbose=verbose)
    make_site(layer_path, layer_names)


# ===== Basic and incomplete implementations of DZI builders ===========================================================
# # basic implementation
# dzi_builder(
#     ai_path='C:\\path\\to\\file\\demo-simple.ai',
#     vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
#     col=3,
#     row=3,
#     offset_right=3000,
#     verbose=True
# )

# incomplete implementation
dzi_builder(
    # ai_path='C:\\path\\to\\file\\demo-incomplete.ai',
    ai_path='C:\\localtemp\\demo-incomplete.ai',
    vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
    col=4,
    row=4,
    offset_right=3000,
    incomplete=True,
    verbose=True
)

# ===== Implementation of individual scripts ===========================================================================
# # create image tiles from an Illustrator file
# create_tiles(
#     ai_path='C:\\path\\to\\file\\demo-incomplete.ai',
#     offset_right=3000,
#     transparency=True
# )
#
# # copies 'filler' tile into empty tile spaces
# fill_incomplete(
#     layer_path='C:\\path\\to\\file\\layers\\',
#     col=4,
#     row=4,
#     verbose=False
# )
#
# # combine tiles into layer images
# create_layers(
#     layer_path='C:\\path\\to\\file\\layers\\',
#     vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
#     col=4,
#     offset_right=3000,
#     verbose=True
# )
#
# # create dzi from layer images and html/css/js
# create_dzi_and_site(
#     layer_path='C:\\path\\to\\file\\layers\\',
#     vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
#     verbose=True
# )
