import os


def get_base_dir() -> str:
    return os.getcwd()


def create_dir_if_not_exist(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def get_library_dir() -> str:
    """Get base path of the library"""
    internal_dir = os.path.dirname(__file__)
    upper_dir = os.path.join(internal_dir, "..")
    library_dir = os.path.realpath(upper_dir)

    assert library_dir.endswith("noted")
    return library_dir
