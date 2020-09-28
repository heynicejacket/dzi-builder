import os

from dzi_builder.core.illustrator import (
    generate_tiles
)

from dzi_builder.core.toolkit import (
    create_folder_structure
)

from dzi_builder.core.vips import (
    combine_transparent_layer,
    make_image_pyramid
)

from dzi_builder.core.image_magick import (
    convert_tiles,
    combine_tiles
)

from dzi_builder.html.openseadragon_html import (
    make_site
)


def dzi_builder(ai_file, vips_path, offset_right, offset_down=0, transparency=True, verbose=False):
    """
    Given an illustrator file, creates a Deep Zoom Image for each top-level layer of the Illustrator file,
    and generates an html and css file to resolve a basic example, when adding the requisite openseadragon
    and jquery files to /layers/html/openseadragon/:

        https://openseadragon.github.io/#download
        https://jquery.com/download/

    Steps to generate the dzi and html are as follows:

    create_folder_structure()


    generate_tiles()


    combine_transparent_layer()


    make_image_pyramid()


    make_site()


    By default, make_site() sets any layer named 'base' to the 0th position, and is otherwise ignored for
    opacity toggling; if you need to set a specific order for your layers, do it between make_image_pyramid()
    and make_site() on layers_list, before it is passed to make_site(). if you want all layers to be toggle-able,
    don't have any layers named 'base', or rename the constant BASE_LAYER to some other value.

    See an example output here: https://embers.nicejacket.cc/viewer.html

    :param ai_file:         str, required
    :param vips_path:       str, required
    :param offset_right:    int, required
    :param offset_down:     int, optional
    :param transparency:    bool, optional
    :param verbose:         bool, optional      if True, prints out details of task
    :return:
    """
    offset_right_f = float(offset_right / 10)
    offset_down_rect = offset_right if offset_down == 0 else offset_down

    layer_path, html_path, dzi_path, osd_path = create_folder_structure(ai_file)

    layer_list = generate_tiles(ai_file, offset_right_f, transparency)
    if transparency:
        combine_transparent_layer(layer_path, 3, 3, offset_right, offset_down_rect, vips_path, verbose)
    else:
        convert_tiles(layer_path, offset_right, verbose=verbose)
        [os.remove(layer_path + f) for f in os.listdir(layer_path) if f.endswith('.svg')]
        combine_tiles(layer_path, layer_list, offset_down_rect, 3, verbose=verbose)

    make_image_pyramid(layer_path, layer_list, vips_path, verbose=verbose)
    make_site(layer_path, layer_list)


dzi_builder(
    ai_file='C:\\localtemp\\demo.ai',
    vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
    offset_right=3000,
    verbose=False
)
