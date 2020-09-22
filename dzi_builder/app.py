from dzi_builder.core.illustrator import (
    generate_tiles
)

# these functions are for a basic, non-transparent layer implementation;
# see: https://embers.nicejacket.cc/blog/2018/06/14/making-large-maps-with-openseadragon/
from dzi_builder.core.image_magick import (
    convert_tiles,
    combine_tiles
)


src_file = 'C:\\localtemp\\demo.ai'
layer_path = 'C:\\localtemp\\layers\\'

layer_list = generate_tiles(src_file)

# these functions are for a basic, non-transparent layer implementation;
# see: https://embers.nicejacket.cc/blog/2018/06/14/making-large-maps-with-openseadragon/
# convert_tiles(layer_path, 3000, verbose=True)
# combine_tiles(layer_path, layer_list, 3000, 3, verbose=True)
