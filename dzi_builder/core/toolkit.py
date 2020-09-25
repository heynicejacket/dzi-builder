import os


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
    output_list = get_file_list(layer_path)
    layer_name_list = list(set([l.split('-', 1)[0] for l in output_list]))

    return layer_name_list


def prefix_path_to_list(path, file_list):
    """
    Given a folder path, creates a list of files with path.
    :param path:            str, required       folder and file path, e.g. 'C:\\path\\to\\file.ai'
    :param file_list:       list, required      list of files
    :return:                list                converted list
    """
    return [path + r for r in file_list]
