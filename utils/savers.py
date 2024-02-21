import pathlib
import json


def save_distance_as_json(distance_info, filename):
    if not pathlib.Path(filename).is_file():
        current = {'experiments': []}
    else:
        with open(filename) as f:
            current_str = f.read()
            current = json.loads(current_str)
    
    current['experiments'].append(distance_info)

    with open(filename, 'w') as f:
        f.write(json.dumps(current, indent=2))