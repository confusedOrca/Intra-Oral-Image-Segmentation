import os

def count_labels(folder_path):
    folder_path = os.path.join(os.getcwd(), folder_path)
    count_array = [0, 0, 0, 0]

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r') as file:
                for line in file:
                    first_number = int(line.split()[0])
                    count_array[first_number] += 1

    return count_array

if __name__ == "__main__":
    train_lbl_path = "dataset_v1.4/labels/train"
    print(f"Train label counts = {count_labels(train_lbl_path)}")
    
    test_lbl_path = "dataset_v1.4/labels/test"
    print(f"Test label counts = {count_labels(test_lbl_path)}")
    
    valid_lbl_path = "dataset_v1.4/labels/val"
    print(f"Valid label counts = {count_labels(valid_lbl_path)}")