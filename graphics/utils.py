import pathlib
from typing import Union


def find_median_distances(all_distances):
    n = len(all_distances)
    sum_distances = list(map(lambda x: sum(x['particle_to_center']), all_distances))
    indexed_sums = list(enumerate(sum_distances))
    indexed_sums.sort(key=lambda x: x[1])
    median = indexed_sums[(n - 1) // 2]
    print(median[0])
    return all_distances[median[0]]

def create_folder(folder_name: str) -> pathlib.Path:
    folder_path = pathlib.Path(folder_name)
    folder_path.mkdir(exist_ok=True)
    return folder_path

def find_cross_time(distances) -> Union[int, None]:
    for i in range(len(distances)):
        if distances['particle_to_center'][i] < 0:
            return distances['time'][i]
    return None

def get_cross_time_stat(all_distances):
    n = 0
    cross_time_sum = 0
    for experiment in all_distances:
        cross_time = find_cross_time(experiment)
        if cross_time:
            cross_time_sum += cross_time
            n += 1
    return {'average cross time': cross_time_sum / n, 'cross miss': len(all_distances) - n}
