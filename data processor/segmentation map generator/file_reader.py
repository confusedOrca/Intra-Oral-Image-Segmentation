def read_txt_file(file_path):
    data = []
    
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            class_id = int(values[0])
            coordinates = list(map(float, values[1:]))
            data.append([class_id] + coordinates)
    
    data.sort(key=lambda x: x[0])
    return data
