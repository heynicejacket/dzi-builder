from win32com.client import Dispatch, GetActiveObject, pywintypes
import os
import time

from dzi_builder.javascript.illustrator_js import (
    js_create_artboards,
    js_convert_to_svg
)


def prefix_path_to_list(path, file_list):
    """
    Given a folder path, creates a list of files with path.
    :param path:            str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :param file_list:       list, required      list of files
    :return:                list                converted list
    """
    return [path + r for r in file_list]


def convert_path_to_js(py_path):
    """
    Flips \\ to / to convert string path from Python formatting to Javascript, e.g.:

        C:\\path\\to\\file.ai   -->   C:/path/to/file.ai

    :param py_path:         str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :return:                str                 converted path
    """
    return py_path.replace('\\', '/')


def get_illustrator(verbose=False):
    """
    Targets an open instance of Illustrator, or opens Illustrator.
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                obj                 reference to Illustrator (type win32com.client.CDispatch)
    """
    print('Targeting or opening Illustrator...') if verbose else None
    try:
        app = GetActiveObject('Illustrator.Application')
    except pywintypes.com_error:
        app = Dispatch('Illustrator.Application')

    return app


def open_illustrator_file(app, file):
    """
    Opens an illustrator file.
    :param app:             COM obj, required   reference to Illustrator (type win32com.client.CDispatch)
    :param file:            str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :return:
    """
    # my machine takes 5-10 seconds to load Illustrator; could replace with sleep(), this is probably better
    go = False
    while not go:
        try:
            ai_doc = app.Open(file)                             # open the Illustrator file
            go = True
        except pywintypes.com_error:
            pass

    return ai_doc


def create_artboards(app, doc, ai_path, width, height=0.0, transparent_png=True, verbose=False):
    """
    Given an Illustrator file, generates files from individual artboards.
    Setting transparent_png to False will return .svg files. Setting transparent_png to True, will, if the Illustrator
    (top-level) layer would have negative space (be able to see an empty artboard background), the output file will
    have transparency.
    :param app:             COM obj, required   reference to Illustrator (type win32com.client.CDispatch)
    :param doc:             COM obj, required   reference to Illustrator file (type win32com.client.CDispatch)
    :param ai_path:         str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :param width:           float, required     width of output png file            TODO: should be optional if svg
    :param height:          float, optional     height of output png file
    :param transparent_png: bool, optional      if True, saves tiles as .png with transparency
    :param verbose:         bool, optional      if True, prints out details of task
    :return:
    """
    js_transparent_png = 1 if transparent_png else 0
    h = width if height == 0.0 else height
    print('Creating artboards from individual layers...') if verbose else None
    js_create_artboards(app, convert_path_to_js(ai_path), js_transparent_png, width, h)        # generate tiles

    doc.Save()                                                  # saving the last file left open provides silent exit
    doc.Close()


def ai_to_svg(app, layer_path, verbose=False):
    """
    Given a path to a folder, converts all files with the .ai extension into SVG files.
    :param app:             COM obj, required   reference to Illustrator (type win32com.client.CDispatch)
    :param layer_path:      str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                list                list of layer names
    """
    print('Creating tile conversion prep list...') if verbose else None
    output_list = [f for f in os.listdir(layer_path) if os.path.isfile(os.path.join(layer_path, f))]
    rem_list_pre = [l for l in output_list if l.find('-') == -1]

    rem_list = prefix_path_to_list(layer_path, rem_list_pre)
    tile_list_pre = prefix_path_to_list(layer_path, output_list)
    tile_list = [f for f in tile_list_pre if f not in rem_list]

    [os.remove(r) for r in rem_list]                            # unsure why illustrator creates these, but, unneeded

    print('Converting *.ai to *.svg...') if verbose else None
    for t in tile_list:
        print('...{}'.format(t)) if verbose else None
        ai_tile = app.Open(t)

        js_convert_to_svg(app, layer_path.replace('\\', '/'))

        ai_tile.Save()
        ai_tile.Close()
        os.remove(t)
        time.sleep(2)                                           # keeps illustrator from overloading memory


def get_layer_list(layer_path, verbose=False):
    """
    Given a path to a folder, returns a list of layers. For example, a folder which contains:

        base.ai             grid.ai
        base-01.ai          grid-01.ai
        base-02.ai          grid-02.ai
        base-03.ai          grid-03.ai

    ...returns a list:

        ['base', 'grid']

    :param layer_path:      str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                list                list of layer names
    """
    print('Creating tile conversion prep list...') if verbose else None
    output_list = [f for f in os.listdir(layer_path) if os.path.isfile(os.path.join(layer_path, f))]
    layer_name_list = list(set([l.split('-', 1)[0] for l in output_list]))

    return layer_name_list


def create_folder(path, new_folder):
    """
    Given a path (or a path with a file), creates a folder if it doesn't already exist, and returns the path
    :param path:            str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :param new_folder:      str, required       name of folder to be created
    :return:                str                 newly-created folder path, e.g. 'C:\\path\\to\\new\\'
    """
    orig_path = path[:path.rfind('\\')+1]
    new_path = orig_path + new_folder + '\\'
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    return new_path


def generate_tiles(file, tile_width, transparency):
    """
    Generate SVG or PNG tiles from an illustrator file with multiple layers and multiple artboards.

    # transparent layer implementation:
    # https://embers.nicejacket.cc/blog/2018/06/16/transparent-layers-for-openseadragon-with-libvips/

    # non-transparent layer implementation:
    # https://embers.nicejacket.cc/blog/2018/06/14/making-large-maps-with-openseadragon/

    :param file:            str, required       folder and file path, e.g. 'C:\path\to\file.ai'
    :param tile_width:      float, required     width of output tiles
    :param transparency:    bool, required      if True, tiles are generated with transparency in negative space
    :return:                list                list of layer names
    """
    tile_path = create_folder(file, 'layers')

    app = get_illustrator()
    doc = open_illustrator_file(app, file)
    create_artboards(app=app, doc=doc, ai_path=tile_path, width=tile_width, transparent_png=transparency)
    layer_name_list = get_layer_list(tile_path)

    if not transparency:
        ai_to_svg(app, tile_path, verbose=True)

    print(layer_name_list)

    app.Quit()

    return layer_name_list
