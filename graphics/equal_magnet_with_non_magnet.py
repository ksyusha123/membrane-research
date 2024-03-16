import matplotlib.pyplot as plt
import json

from utils import find_median_distances

import argparse
 
parser = argparse.ArgumentParser(description="Draw typical distance with membrane edges")
parser.add_argument("files", nargs='+', type=str, help="filename with simulations info")
    
def draw_median_distances(all_typical_distances, args):
    plt.rcParams.update({'font.size': 20})
    _, ax = plt.subplots(figsize=(9, 7))
    ax.set_xlabel('$t$')

    label_factory = lambda _: f'$\\alpha$={distance_info["alpha"] if "alpha" in distance_info else 0.0}'
    
    ax.set_ylabel('$dist$')
    for distance_info in all_typical_distances:
        ax.plot(distance_info['time'], distance_info["particle_to_center"], label=label_factory(distance_info))
        ax.plot(distance_info['time'], distance_info["top_to_center"], color='black', linestyle='dashed')
        ax.plot(distance_info['time'], distance_info["bottom_to_center"], color='black', linestyle='dashed')
    
    ax.axhline(0, color='black', linewidth=0.5)
    ax.legend()
    

def main(args):
    all_median_distances = []
    for file in args.files:
        with open(file) as f:
            content = json.loads(f.read())
            all_distances = content['experiments']
            median_distances = find_median_distances(all_distances)
            all_median_distances.append(median_distances)

    draw_median_distances(all_median_distances, args)

    plt.savefig(f'eq_magnet_with_non_magnet')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)