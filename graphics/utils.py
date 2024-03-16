import numpy as np
import pathlib


def find_typical_distances(all_distances):
    point = 3.5
    min_d = 1000
    typical_distances = None
    for distances in all_distances:
        if abs(distances['particle_to_center'][0] - point) < min_d:
            min_d = abs(distances['particle_to_center'][0] - point)
            typical_distances = distances
    return typical_distances

def find_median_distances(all_distances):
    n = len(all_distances)
    sum_distances = list(map(lambda x: sum(x['particle_to_center']), all_distances))
    indexed_sums = list(enumerate(sum_distances))
    indexed_sums.sort(key=lambda x: x[1])
    median = indexed_sums[(n - 1) // 2]
    return all_distances[median[0]]

def create_folder(folder_name: str) -> pathlib.Path:
    folder_path = pathlib.Path(folder_name)
    folder_path.mkdir(exist_ok=True)
    return folder_path
