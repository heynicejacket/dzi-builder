import os
import re


def create_file(file_path, file_name, file_content):
    new_file = open(file_path + file_name, 'w')
    new_file.write(file_content)
    new_file.close()


def create_folder(path, check_folder, verbose=False):
    """
    Given a path (or a path with a file), creates a folder if it doesn't already exist, and returns the path
    :param path:            str, required       folder or file path, e.g. 'C:\\path\\' or 'C:\\path\\to\\file.ai'
    :param check_folder:    str, required       name of folder to be created
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                str                 newly-created folder path, e.g. 'C:\\path\\to\\new\\'
    """
    check_path = path[:path.rfind('\\')+1] + check_folder + '\\'
    if not os.path.isdir(check_path):
        os.makedirs(check_path)
        print('Created {}'.format(check_path)) if verbose else None

    return check_path


def create_folder_structure(layer_path):
    html_path = create_folder(layer_path, 'html\\')
    dzi_path = create_folder(html_path, 'dzi\\')
    osd_path = create_folder(html_path, 'openseadragon\\')

    return html_path, dzi_path, osd_path


def convert_path_to_js(py_path):
    """
    Flips \\ to / to convert string path from Python formatting to Javascript, e.g.:

        C:\\path\\to\\file.ai   -->   C:/path/to/file.ai

    :param py_path:         str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :return:                str                 converted path
    """
    return py_path.replace('\\', '/')


def get_file_list(path):
    """

    :param path:
    :return:
    """
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def get_layer_list(layer_path, verbose=False):
    """
    Given a path to a folder, returns a list of layers. For example, a folder which contains:

        base.png            grid.png
        base-01.png         grid-01.png
        base-02.png         grid-02.png
        base-03.png         grid-03.png

    ...returns a list:

        ['base', 'grid']

    :param layer_path:      str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :param verbose:         bool, optional      if True, prints out details of task
    :return:                list                list of layer names
    """
    print('Creating tile conversion prep list...') if verbose else None
    layer_name_list = list(set([re.sub(r'-\d{1,3}\.\D*|\.\D*', '', i) for i in get_file_list(layer_path)]))

    return layer_name_list


def prefix_path_to_list(path, file_list):
    """
    Given a folder path, creates a list of files with path.
    :param path:            str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :param file_list:       list, required      list of files
    :return:                list                converted list
    """
    return [path + r for r in file_list]
