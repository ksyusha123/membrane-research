import matplotlib.pyplot as plt
import json
import pathlib
import numpy as np

from utils import find_median_distances

import argparse
 
parser = argparse.ArgumentParser(description="Draw typical distance with membrane edges")
parser.add_argument("folders", nargs='+',type=str, help="folder with .json results")

plt.rcParams.update({'font.size': 20})


def draw_median_distances(all_median_distances):
    _, ax = plt.subplots(figsize=(9, 7))
    # take = 50
    ax.set_xlabel('$t$')
    ax.set_title(f'$\epsilon={all_median_distances[0]["epsilon"]}, m={all_median_distances[0]["moment"]}$')
    label_factory = lambda x: f'$\\alpha$={x["alpha"]}'

    ax.set_ylabel('$\Delta y$')
    for distance_info in all_median_distances:
        lengths = [np.linalg.norm(f) for f in distance_info["f"]]
        ax.plot(distance_info['time'], lengths, label=label_factory(distance_info))

    ax.axhline(0, color='black', linewidth=0.5)
    ax.legend()
    

def main(args):
    
    for folder in args.folders:
        all_median_distances = []
        files = [f for f in pathlib.Path(folder).iterdir() if f.is_file()]
        for file in files:
            with open(file) as f:
                content = json.loads(f.read())
                all_distances = content['experiments']
                median_distances = find_median_distances(all_distances)
                all_median_distances.append(median_distances)

        draw_median_distances(all_median_distances)
        plt.savefig(f'forces_{folder}.png')

    # plt.show()
    # plt.savefig('medians_moments')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)