import matplotlib.pyplot as plt
import json

from utils import find_median_distances

import argparse
 
parser = argparse.ArgumentParser(description="Draw typical distance with membrane edges")
parser.add_argument("files", nargs='+', type=str, help="filename with simulations info")
parser.add_argument("-d", "--dist", action="store_true", help="Show distances to the center")
parser.add_argument("-m", "--magnet", action="store_true", help="Show parameters h of magnet interaction in the title")
    
def draw_median_distances(all_median_distances, args):
    plt.rcParams.update({'font.size': 20})
    _, ax = plt.subplots(figsize=(18, 7))
    ax.set_xlabel('$t$')
    if args.dist:
        ax.set_ylabel('$y$')
        for distance_info in all_median_distances:
            take = len(distance_info['time']) // 2
            ax.plot(distance_info['time'][:take], distance_info["particle_coord"][:take], label='particle')
            ax.plot(distance_info['time'][:take], distance_info["membrane_center"][:take], label='membrane')
        
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

    fig_name_details = []
    if args.dist:
        fig_name_details.append('dist')
    if args.magnet:
        fig_name_details.append('magnet')
    plt.savefig(f'membrane_and_particle')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)