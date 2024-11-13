from os import listdir, makedirs
from os.path import join, exists
import shutil
import config
from utils import BASE_DIR, MODULE_DIR
from concurrent.futures import ThreadPoolExecutor, as_completed


SRC_UPPER_JAW = join(BASE_DIR, config.SOURCE, config.UPPER_JAW_DIR)
SRC_LOWER_JAW = join(BASE_DIR, config.SOURCE, config.LOWER_JAW_DIR)
DST_DIR = join(MODULE_DIR, "temp_dataset")


def move_contents(src, dst, items):
    for item in items:
        src_item = join(src, item)
        dst_item = join(dst, item)
        if not exists(dst_item):
            shutil.copy(src_item, dst_item)


def aggregate():
    if exists(DST_DIR):
        shutil.rmtree(DST_DIR)
    makedirs(DST_DIR)

    lower_jaw_items = listdir(SRC_LOWER_JAW)
    upper_jaw_items = listdir(SRC_UPPER_JAW)
    all_items = lower_jaw_items + upper_jaw_items

    with ThreadPoolExecutor() as executor:
        tasks = [
            executor.submit(move_contents, SRC_LOWER_JAW, DST_DIR, lower_jaw_items),
            executor.submit(move_contents, SRC_UPPER_JAW, DST_DIR, upper_jaw_items)
        ]

        for task in as_completed(tasks):
            task.result()

    return DST_DIR