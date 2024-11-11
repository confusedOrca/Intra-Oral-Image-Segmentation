from os import listdir, makedirs
from os.path import join, exists
import shutil
import config
from utils import BASE_DIR, MODULE_DIR
from concurrent.futures import ThreadPoolExecutor


SRC_UPPER_JAW = join(BASE_DIR, config.SOURCE, config.UPPER_JAW_DIR)
SRC_LOWER_JAW = join(BASE_DIR, config.SOURCE, config.LOWER_JAW_DIR)
DST_DIR = join(MODULE_DIR, "temp_dataset")


def move_contents(src, dst):
    items = listdir(src)
    def copy_item(item):
        src_item = join(src, item)
        dst_item = join(dst, item)
        if not exists(dst_item):
            shutil.copy(src_item, dst_item)

    with ThreadPoolExecutor() as executor:
        executor.map(copy_item, items)


def aggregate():
    if exists(DST_DIR):
        shutil.rmtree(DST_DIR)
    makedirs(DST_DIR)
    
    with ThreadPoolExecutor() as executor:
        executor.submit(move_contents, SRC_LOWER_JAW, DST_DIR)
        executor.submit(move_contents, SRC_UPPER_JAW, DST_DIR)
    
    return DST_DIR