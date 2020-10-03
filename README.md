# dzi-builder
Generate [Deep Zoom Image](https://docs.microsoft.com/en-us/previous-versions/windows/silverlight/dotnet-windows-silverlight/cc645077(v=vs.95)?redirectedfrom=MSDN) 
(dzi) and accompanying html/css structures and requisite javascript for [Openseadragon](https://openseadragon.github.io/) 
from an Illustrator file with multiple layers.

Future updates will include conversion from Photoshop and GIMP.

## Why?
The [first map](https://embers.nicejacket.cc/known-eilarun.html) I converted into a functioning dzi was a pain. My 
map was massive, with a ton of detail, so I used 59 artboards to make 58 unique files, and, to make a square, a 59th 
generic "ocean" tile to fill in empty ocean areas that was making the Illustrator file nearly impossible to load.

From Illustrator, I mass-exported these as svg files to more rapidly generate high resolution png files with 
ImageMagick, which I also used to combine all the individual tiles together, renumbering each png to fill in the empty
ocean areas with that 59th tile, 41 times.

Then, I ran 90 individual commands to append each row of images together, and 9 more to combine each row into a 
single, 30,000 x 30,000 pixel image.

Then, I used libvips to convert that into a dzi.

Later, when I wanted to add transparent layers - nation borders, etc. - I had to do it all over again, for those 
layers, this time with libvips as ImageMagick doesn't (not really, anyway) support transparent png.

I've done that [once since](https://embers.nicejacket.cc/remembered-blacklands.html) for one other map, but staring 
down the completion of my third (and a recolor of the first), I couldn't stomach going through it again.

dzi-builder does all of the above, with minimal user input, and outputs a basic version of the html/css/javascript to 
get a map up and running.

## Basic implementation

The demo Illustrator file can be found 
[here](https://github.com/heynicejacket/dzi-builder/blob/master/dzi_builder/demo-basic.ai). 
Basic output of this file via dzi-viewer can be seen [here](https://embers.nicejacket.cc/viewer.html).

Current implementation supports only Illustrator file conversions with a square matrix of artboards. The next 
implementation will include a user interface to aid in placement of redundant, duplicate squares to fill empty space.

Subsequent updates will provide exports for Photoshop (which I'm fairly familiar with), then GIMP (which I'm not 
familiar with), and then other common image tile formats (Google Earth, etc.).

Export of the basic, square Illustrator-generated map requires a map where artboards were generated in a sequential 
order; roughly resembling the following format:

<p align="center"><img src="https://embers.nicejacket.cc/github/square%20artboard%20structure.png" /></p>

(if the tiles available in Illustrator do not create an even square, stay tuned, all of my maps fall into this 
category; this is coming soon, and my slapdash WIP can be found in dzi_builder.core.tile_filler.py)

Basic execution to generate an html/css/javascript and dzi structure for an Illustrator file with a complete artboard 
matrix is as follows:

    dzi_builder(
        ai_file='C:\\file\\to\\path\\demo.ai',
        vips_path='C:\\Program Files\\vips-dev-8.10\\bin\\',
        offset_right=3000
    )

(There are a number of people who seem to have issues with pyvips. While I'd rather have a clean python implentation, it 
seems that people who use Anaconda or Docker have issues with pyvips, and my overarching philosophy is to make 
implementation as easy as possible, especially for non-technical users.)

Pointing to your target file:

        ai_file='C:\\file\\to\\path\\demo.ai'

Each top-level layer in Illustrator will be treated as a single dzi. Sub-layers will be subsumed into the top level 
layer, which will be treated as a toggle-able layer. Any media you wish to not be toggle-able should be collected under 
a top-level layer named 'base' - though you can change the name of the "always on" layer with the constant BASE_LAYER.  
