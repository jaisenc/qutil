import os
import logging
import shutil


def clear_and_init_folder(folder: str):
    """

    :param folder:
    :return:
    """
    if os.path.isdir(folder):
        shutil.rmtree(folder)
        logging.debug("Folder already exist, removing {}".format(folder))
    if not os.path.isdir(folder):
        os.makedirs(folder, True)


def uzip_all_files(src: str, dst: str):
    """
    Unzip all the zip files in the src folder to the dst folder

    :param src:
    :param dst:
    :return:
    """
    for f in os.listdir(src):
        if f.endswith('.zip'):
            zip_ref = zipfile.ZipFile(os.path.join(src, f), 'r')
            zip_ref.extractall(dst)
            zip_ref.close()
