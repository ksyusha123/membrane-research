import matplotlib.pyplot as plt
import json

from utils import find_median_distances

import argparse
 
parser = argparse.ArgumentParser(description="Draw typical distance with membrane edges")
parser.add_argument("files", nargs='+', type=str, help="filename with simulations info")
    
def draw_median_distances(all_median_distances, args):
    plt.rcParams.update({'font.size': 20})
    _, ax = plt.subplots(figsize=(9, 7))
    take = 50
    ax.set_xlabel('$t$')
    ax.set_title(f'$\epsilon={all_median_distances[0]["epsilon"]}$')
    label_factory = lambda x: f'$\\alpha$={x["alpha"]}, m={x["moment"]}'

    ax.set_ylabel('$\Delta y$')
    for distance_info in all_median_distances:
        ax.plot(distance_info['time'][:take], distance_info["particle_to_center"][:take], label=label_factory(distance_info))
        ax.plot(distance_info['time'][:take], distance_info["top_to_center"][:take], color='black', linestyle='dashed')
        ax.plot(distance_info['time'][:take], distance_info["bottom_to_center"][:take], color='black', linestyle='dashed')

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

    plt.show()
    # plt.savefig('medians_moments')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)