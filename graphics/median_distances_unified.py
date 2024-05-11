import matplotlib.pyplot as plt
import json

from utils import find_median_distances

import argparse
 
parser = argparse.ArgumentParser(description="Draw typical distance with membrane edges")
parser.add_argument("files", nargs='+', type=str, help="filename with simulations info")
parser.add_argument("-d", "--dist", action="store_true", help="Show distances to the center")
parser.add_argument("-dip", "--dip_deviation", action="store_true", help="Show dipole deviation from H-field")
parser.add_argument("-lj", "--lennardjones", action="store_true", help="Show parameters epsilon and sigma of LJ interaction in the title")
parser.add_argument("-m", "--magnet", action="store_true", help="Show parameters h of magnet interaction in the title")
    
def draw_median_distances(all_median_distances, args):
    plt.rcParams.update({'font.size': 20})
    _, ax = plt.subplots(figsize=(18, 7))
    ax.set_xlabel('$t$')
    if args.lennardjones:
        label_factory = lambda x: f'$\sigma_p$={x["sigma_p"]}'
        ax.set_title(f'$\epsilon={all_median_distances[0]["epsilon"]}$')
    elif args.magnet:
        label_factory = lambda x: f'$\\alpha$={x["alpha"]}'
    if args.dist:
        ax.set_ylabel('$dist$')
        for distance_info in all_median_distances:
            ax.plot(distance_info['time'], distance_info["particle_to_center"], label=label_factory(distance_info))
            ax.plot(distance_info['time'], distance_info["top_to_center"], color='black', linestyle='dashed')
            ax.plot(distance_info['time'], distance_info["bottom_to_center"], color='black', linestyle='dashed')
        
    if args.dip_deviation:
        ax.set_ylabel('$\\angle (\overrightarrow{m}, \overrightarrow{H})$')
        for distance_info in all_median_distances:
            ax.plot(distance_info['time'], distance_info["dip_deviations"], label=label_factory(distance_info))

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
    if args.dip_deviation:
        fig_name_details.append('dip_deviation')
    if args.lennardjones:
        fig_name_details.append('lj')
    if args.magnet:
        fig_name_details.append('magnet')
    plt.savefig(f'medians_with_edges_{"_".join(fig_name_details)}')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)