import json

def update(objects, path):
    data = read(path)
        
    data.update(objects)

    with open(path, "w") as file:
        json.dump(data, file, indent=2, sort_keys=True)
        file.close()


def read(path):
    try:
        with open(path, "r") as file:
            data = json.load(file)
            if not data:
                data = {}
    except FileNotFoundError:
        data = {}
        with open(path, "w") as file:
            json.dump(data, file)
    
    return data


def test(path):
    data = read(path)

    for obj in data:
        print(obj)