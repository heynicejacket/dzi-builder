import os
import re


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
