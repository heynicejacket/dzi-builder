import os

from dzi_builder.core.illustrator import (
    generate_tiles
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
    make_openseadragon_html,
    make_openseadragon_css
)


def dzi_builder(ai_file, layers_path, vips_path, offset_right, offset_down=0, transparency=True, verbose=False):
    """

    :param ai_file:
    :param layers_path:
    :param vips_path:
    :param offset_right:
    :param offset_down:
    :param transparency:
    :param verbose:
    :return:
    """
    offset_right_f = float(offset_right / 10)
    offset_down_rect = offset_right if offset_down == 0 else offset_down

    layer_list = generate_tiles(ai_file, offset_right_f, transparency)
    if transparency:
        png_layer_output = combine_transparent_layer(layers_path, 3, 3, offset_right, offset_down_rect, vips_path, verbose)
    else:
        convert_tiles(layers_path, offset_right, verbose=verbose)
        [os.remove(layers_path + f) for f in os.listdir(layers_path) if f.endswith('.svg')]
        combine_tiles(layers_path, layer_list, offset_down_rect, 3, verbose=verbose)
        png_layer_output = [layer + '.png' for layer in layer_list]

    make_image_pyramid(layers_path, png_layer_output, '', vips_path, verbose=verbose)


dzi_builder(
    ai_file='C:\\localtemp\\demo.ai',
    layers_path='C:\\localtemp\\layers\\',
    vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
    offset_right=3000,
    offset_down=3000,
    transparency=True,
    verbose=False
)
