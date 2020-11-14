# dzi-builder
Generate [Deep Zoom Image](https://docs.microsoft.com/en-us/previous-versions/windows/silverlight/dotnet-windows-silverlight/cc645077(v=vs.95)?redirectedfrom=MSDN) 
(DZI) and accompanying HTML/CSS structures and requisite JavaScript for [OpenSeadragon](https://openseadragon.github.io/) 
from an Illustrator file with multiple layers.

See example simple 
Illustrator input [here](https://github.com/heynicejacket/dzi-builder/blob/master/dzi_builder/demo-basic.ai) and 
`dzi_builder()` output [here](https://embers.nicejacket.cc/dzi-builder/artboard-simple/viewer.html), and complex 
Illustrator input [here](https://github.com/heynicejacket/dzi-builder/blob/master/dzi_builder/demo-missing-tiles.ai) and 
`dzi_builder()` output [here](https://embers.nicejacket.cc/dzi-builder/artboard-incomplete/viewer.html).

*Future updates will include options for Photoshop and GIMP.*

## Why?

<p align="center"><img src="https://embers.nicejacket.cc/dzi-builder/dzi-builder-header.png"></p>

The [first map](https://embers.nicejacket.cc/known-eilarun.html) I converted into a functioning DZI was a pain. My 
map was massive, with a ton of detail; I used 59 artboards to make 58 unique files, and, to fill out a square, a 59th 
generic "ocean" tile to fill in empty ocean areas that was otherwise making the Illustrator file nearly impossible to 
work in.

From Illustrator, I mass-exported these as svg files to more rapidly generate high resolution png files with 
ImageMagick, which I also used to combine all the individual tiles together, renumbering each png to fill in the empty
ocean areas with that 59th tile, 41 times.

I ran 90 individual commands to append each row of images together, and 9 more to combine each row into a single, 
36,000 x 30,000 pixel image.

Finally, I used libvips to convert that into a DZI.

Later, when I wanted to add transparent layers - nation borders, etc. - I had to do it all over again, for those 
layers, this time solely in libvips as ImageMagick doesn't really support transparent png.

I've done that [once since](https://embers.nicejacket.cc/remembered-blacklands.html) for one other map, but staring 
down the completion of my third and fourth (and a recolor of the first), I couldn't stomach it again.

dzi-builder does all of the above for you and outputs a basic version of the HTML/CSS/JS and DZI structure to get a map 
up and running.

### Current caveats

Currently, the following parameters are required of your Illustrator file:

- [x] Artboards are 1000x1000 pixels ([issue #4](https://github.com/heynicejacket/dzi-builder/issues/4))
- [x] Illustrator top-level layers only contain alphanum characters 
([issue #5](https://github.com/heynicejacket/dzi-builder/issues/5))
- [x] Only "always-visible" base layer in Illustrator contains the word "base" ([issue #7](https://github.com/heynicejacket/dzi-builder/issues/7))
- [x] 0th tile in tile matrix must exist ([issue #9](https://github.com/heynicejacket/dzi-builder/issues/9))

## Basic implementation

The demo Illustrator file can be found 
[here](https://github.com/heynicejacket/dzi-builder/blob/master/dzi_builder/demo-basic.ai). 
Basic output of this file via `dzi-builder()` can be seen 
[here](https://embers.nicejacket.cc/dzi-builder/artboard-simple/viewer.html).

Export of the basic, square Illustrator-generated map requires a map where artboards were generated in a sequential 
order; roughly resembling the following format:

<p align="center"><img src="https://embers.nicejacket.cc/dzi-builder/square%20artboard%20structure.png"></p>

### Execution

:rotating_light: *See [issue #4](https://github.com/heynicejacket/dzi-builder/issues/4); my demo maps - and my 
production maps - all were set to 1000x1000 pixel artboards; as such, these are the dimensions dzi-builder currently 
requires for correct scale and position math. For now, make your artboards 1000x1000 pixels.*

:rotating_light: *See [issue #5](https://github.com/heynicejacket/dzi-builder/issues/5); after executing on my 
production maps, I realized that non-alphanumeric characters in top-level Illustrator layers break the JavaScript that 
exports tiles in Illustrator's scripting functions. Similarly, see 
[issue #7](https://github.com/heynicejacket/dzi-builder/issues/7); any top-level Illustrator layer that includes the 
word 'base', but is not the base layer (named simply, 'base') will break normal functionality. This is due to the 
default assignment of opacity - base layer is 1, other layers are 0.*

Generate an HTML/CSS/JS and DZI structure for an Illustrator file with a complete artboard 
matrix as follows:

    dzi_builder(
        ai_path='C:\\file\\to\\path\\demo.ai',                  // map AI file
        vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',    // vips.exe location
        col=3,                                                  // number of tile cols
        row=3,                                                  // number of row cols
        offset_right=3000,                                      // width of each tile
        verbose=True                                            // prints status to user
    )

*(A number of people who use Anaconda or Docker seem to have issues with pyvips; I don't use either, but to make 
implementation as easy as possible, especially for non-technical users, pointing to where vips.exe lives is easy 
enough)*

Each top-level layer in Illustrator will be treated as a single DZI. Sub-layers will be subsumed into the top level 
layer, which will be treated as a toggle-able layer. Any media you wish to not be toggle-able should be collected under 
a top-level layer named "base" - though you can change the name of the "always on" layer with the 
[constant](https://github.com/heynicejacket/dzi-builder/blob/master/dzi_builder/core/constants.py) BASE_LAYER.

`dzi_builder()` generates the following directories and files:

    layers\
        html\
            dzi\
                [dzi structures]
            openseadragon\
                README.txt              // instructions for installing OpenSeadragon
            viewer.html
            viewer.css
        [png tiles]

Individual png tiles are left in \layers\ to aid in debugging the order of your artboards, but are otherwise not 
necessary - just add the OpenSeadragon and jQuery files noted in README.txt, and drop everything inside \html\ into 
your site as-is.

The html/css structure is fairly basic, but the html structure includes the following relevant lines generated by the 
Illustrator layers. The DZI layers:

    // map layers
    var base = 'dzi/base.dzi'
    var grid = 'dzi/grid.dzi'
    ...

...the tileSources:

    // openseadragon viewer
    tileSources: [
        {
            x: 0,
            y: 0,
            opacity: 1,
            tileSource: base
        },
        {
            x: 0,
            y: 0,
            opacity: 0,
            tileSource: grid
        },
        ...
    ]

...and the jQuery toggle for changing the opacity of non-base layers:

    // jquery button functionality 
    var gridOpacity = 0;
    $('.gridToggle').on('click', function() {
        if (gridOpacity === 0) {
            gridOpacity = 1;
        } else {
            gridOpacity = 0;
        }
        gridFade(viewer.world.getItemAt(1), gridOpacity);
    });
    var gridFade = function(image, opacity) {
        image.setOpacity(gridOpacity);
        OpenSeadragon.requestAnimationFrame(frame);
    };
    ...

The layer in Illustrator named "base" is always the 0th layer. Depending on the how you want the layers to appear, you 
may need to rearrange the order of your layers in either Illustrator or the sections noted above.

You may also want to edit the "toggleButtons" div and rearrange the order of the layers under tileSources (first layer 
listed is index position 0, second is 1, etc.), in order to have layers that appear over or between toggle-able layers, 
while preserving their "always on" status. You'll need to also adjust the other layer positions in 
[getItemAt](https://openseadragon.github.io/docs/OpenSeadragon.World.html#getItemAt) here:

    pathsFade(viewer.world.getItemAt(2) 

## Incomplete artboard implementation

The demo Illustrator file can be found 
[here](https://github.com/heynicejacket/dzi-builder/blob/master/dzi_builder/demo-missing-tiles.ai). 
Final output of this file via `dzi_builder()` can be seen 
[here](https://embers.nicejacket.cc/dzi-builder/artboard-incomplete/viewer.html).

Export of an incomplete Illustrator-generated map does not require a map where artboards were generated in a sequential 
order, but subsequent steps will be easier; below is an example of a complex artboard structure:

<p align="center"><img src="https://embers.nicejacket.cc/dzi-builder/incomplete%20artboard%20structure.png"></p>

### Execution

:rotating_light: *See [issue #9](https://github.com/heynicejacket/dzi-builder/issues/9); currently,* 
`restructure_layer_matrix()` *will crash if the 0th artboard is empty. For now, if your artboard would have the 0th tile 
empty, just make your "filler tile" the 0th artboard.*

Generation of an HTML/CSS/JS and DZI structure from an Illustrator file with an incomplete artboard matrix is 
similar to the basic implementation, with the following changes:

    dzi_builder(
        ai_path='C:\\file\\to\\path\\demo.ai',                  // map AI file
        vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',    // vips.exe location
        col=4,                                                  // number of tile cols
        row=4,                                                  // number of row cols
        offset_right=3000,                                      // width of each tile
        incomplete=True,                                        // add this optional var
        verbose=True                                            // prints status to user
    )

Given the following variables:

    col=4,
    row=4,
    incomplete=True

...the user is prompted with a diagram of the tile matrix, based on the input columns and rows:

    [0]    [1]    [2]    [3]
    [4]    [5]    [6]    [7]
    [8]    [9]    [10]   [11]
    [12]   [13]   [14]   [15]
    
The user should enter which tile exists in the above matrix, which should be considered the "filler tile":
    
    Enter number of tile to duplicate into empty spaces (e.g. 3):

...and then identify empty spaces where the "filler tile" should be placed:

    List tiles, separated by commas, where 'filler tile' should be placed (e.g. 4,5,6):

The script continues as the basic implementation, generating the necessary HTML/CSS/JS and DZI structures.

## Incremental Implementations

The recolor and expansion of my [first map](https://embers.nicejacket.cc/known-eilarun.html) weighed in at 36,000 x 
60,000 pixels, composed of five Illustrator files, due to memory limitations (two were nearly 500mb each).

A future version of dzi-builder will take multi-file positioning into account (as this does require some manual tile 
renaming), but for compiling multiple artboards - as well as debugging issues with your map (or this script) - it can be 
helpful to run subsets of the full script.

If you need to add multiple files together before creating your DZI, these incremental functions within 
[app.py](https://github.com/heynicejacket/dzi-builder/blob/master/dzi_builder/app.py) may be helpful.

### Create Tiles

Creates basic folder structure (needed in the complete script), and creates tiles from an Illustrator file for all 
layers.

    create_tiles(
        ai_path='C:\\path\\to\\file\\demo-incomplete.ai',
        offset_right=3000,
        transparency=True
    )

### Fill Incomplete

User is prompted with a diagram of the tile matrix to identify "filler tile" and where to place said tile; tiles are 
renamed to create a complete matrix, for each layer.

    fill_incomplete(
        layer_path='C:\\path\\to\\file\\layers\\',
        col=4,
        row=4,
        verbose=True
    )

### Create Layers

Creates layer png files using complete layer tile matrices in `\layers\` folder.

    create_layers(
        layer_path='C:\\path\\to\\file\\layers\\',
        vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
        col=4,
        offset_right=3000,
        verbose=True
    )

### Create DZI and Site

Generates Deep Zoom Image file structures and necessary HTML/CSS/JS content for publishing to web, given complete layer 
png files (requires download of [OpenSeadragon](https://openseadragon.github.io/#download); see `\html\readme.txt`)

    create_dzi_and_site(
        layer_path='C:\\path\\to\\file\\layers\\',
        vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
        verbose=True
    )
