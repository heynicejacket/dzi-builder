import os

from dzi_builder.core.illustrator import (
    generate_tiles
)

from dzi_builder.core.toolkit import (
    create_folder_structure,
    get_file_list
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


def dzi_builder(ai_path, vips_path, col, row, offset_right,
                offset_down=0, transparency=True, incomplete=False, verbose=False):
    """
    Given an illustrator file, creates a Deep Zoom Image for each top-level layer of the Illustrator file,
    and generates an html and css file to resolve a basic example, when adding the requisite openseadragon
    and jquery files to /layers/html/openseadragon/:

        https://openseadragon.github.io/#download
        https://jquery.com/download/

    Steps to generate the dzi and html are as follows:

    create_folder_structure()
    Generates the necessary folder structure in the location of the target Illustrator file.

    generate_tiles()


    combine_transparent_layer()


    make_image_pyramid()


    make_site()


    By default, make_site() sets any layer named 'base' to the 0th position, and is otherwise ignored for
    opacity toggling; if you need to set a specific order for your layers, do it between make_image_pyramid()
    and make_site() on layers_list, before it is passed to make_site(). if you want all layers to be toggle-able,
    don't have any layers named 'base', or rename the constant BASE_LAYER to some other value.

    See an example output here: https://embers.nicejacket.cc/viewer.html

    :param ai_path:         str, required       path to Illustrator file, e.g. 'C:\\path\\to\\file.ai'
    :param vips_path:       str, required       path to vips.exe, e.g. 'C:\\Program Files\\vips\\bin\\vips.exe'
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
        combine_transparent_layer(layer_path, col, row, offset_right, offset_down_rect, vips_path, verbose)
    else:
        convert_tiles(layer_path, offset_right, verbose=verbose)
        [os.remove(layer_path + f) for f in os.listdir(layer_path) if f.endswith('.svg')]
        combine_tiles(layer_path, layer_names, offset_down_rect, 3, verbose=verbose)

    make_image_pyramid(layer_path, layer_names, vips_path, verbose=verbose)
    make_site(layer_path, layer_names)


# basic implementation
dzi_builder(
    ai_path='C:\\file\\to\\path\\demo-simple.ai',
    vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
    col=3,
    row=3,
    offset_right=3000
)

# # incomplete implementation
# dzi_builder(
#     ai_path='C:\\file\\to\\path\\demo-incomplete.ai',
#     vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
#     col=4,
#     row=4,
#     offset_right=3000,
#     incomplete=True
# )
