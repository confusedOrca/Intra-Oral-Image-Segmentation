import os

def update_class_id_in_txt_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()

                updated_lines = []
                for line in lines:
                    parts = line.strip().split()
                    if parts and parts[0] == '1':
                        parts[0] = '0'
                    updated_lines.append(' '.join(parts))

                with open(file_path, 'w') as f:
                    f.write('\n'.join(updated_lines) + '\n')

if __name__ == "__main__":
    directory = "dataset\det_dataset_after_split"
    update_class_id_in_txt_files(directory)
