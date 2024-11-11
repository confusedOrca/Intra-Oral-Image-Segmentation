from os import getcwd, walk
from os.path import dirname, join, exists
import shutil
import config
from concurrent.futures import ThreadPoolExecutor

CWD = getcwd()
SRC = join(CWD, config.SOURCE)
DST = join(dirname(SRC), config.NAME)
LABELS = join(DST, config.LABEL_SRC)


def bbox_format(data):
    values = list(map(float, data.split()))
    class_id = int(values[0])
    
    if class_id not in config.CLASSES:
        return None
    
    x_coo = values[1::2]
    y_coo = values[2::2]
    x_center = (min(x_coo) + max(x_coo)) / 2
    y_center = (min(y_coo) + max(y_coo)) / 2
    height = max(y_coo) - min(y_coo)
    width = max(x_coo) - min(x_coo)
    return f"{class_id} {x_center:.5f} {y_center:.5f} {width:.5f} {height:.5f}"
    
    
def transform(text):
    lines = text.strip().splitlines()
    results = []
    
    with ThreadPoolExecutor() as executor:
        tasks = [executor.submit(bbox_format, line) for line in lines]
        
        for task in tasks:
            result_line = task.result()
            if result_line:
                results.append(result_line)
                
    return "\n".join(results)


def process_file(txt_file, transform_func):
    try:
        with open(txt_file, 'r') as file:
            content = file.read()
            
        new_content = transform_func(content)

        with open(txt_file, 'w') as file:
            file.write(new_content)
            
    except Exception as e:
        print(f"An error occurred: {e}")

    
def main():
    if exists(DST):
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)
    
    txt_files = [
        join(root, file)
        for root, _, files in walk(LABELS)
        for file in files if file.endswith('.txt')
    ]

    with ThreadPoolExecutor() as executor:
        tasks = [
            executor.submit(process_file, file_path, transform)
            for file_path in txt_files
        ]

        for task in tasks:
            try:
                task.result()
            except Exception as e:
                print(f"An error occurred while processing a file: {e}")

if __name__ == "__main__":
    main()