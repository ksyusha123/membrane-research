import matplotlib.pyplot as plt
import json
import pathlib

from utils import find_median_distances, create_folder

import argparse
 
parser = argparse.ArgumentParser(description="Draw typical distance with memebrane edges")
parser.add_argument("filename", type=str, help="filename with simulations info")
parser.add_argument("-lj", "--lennardjones", action="store_true", help="Show parameters epsilon and sigma of LJ interaction in the title")
parser.add_argument("-m", "--magnet", action="store_true", help="Show parameters h of magnet interaction in the title")
    

def main(filename, show_lj, show_magnet):
    median_distances = []
    with open(filename) as f:
        content = json.loads(f.read())
        all_distances = content['experiments']
        median_distances = find_median_distances(all_distances)


    plt.rcParams.update({'font.size': 20})
    _, ax = plt.subplots(figsize=(9, 7))
    ax.set_xlabel('$t$')
    ax.set_ylabel('$dist$')
    title = []
    if show_lj:
        title.append(f'$\epsilon$={median_distances["epsilon"]}, $\sigma_p$={median_distances["sigma_p"]}')
    if show_magnet:
        title.append(f'$\\alpha={median_distances["alpha"]}$')
    ax.set_title('\n'.join(title))
    ax.plot(median_distances['time'], median_distances["particle_to_center"])
    ax.plot(median_distances['time'], median_distances["top_to_center"], color='black', linestyle='dashed')
    ax.plot(median_distances['time'], median_distances["bottom_to_center"], color='black', linestyle='dashed')
    ax.axhline(0, color='black', linewidth=0.5)

    folder_path = create_folder('median_with_edge')
    plt.savefig(folder_path / f'{filename.replace("json", "")}')

if __name__ == '__main__':
    args = parser.parse_args()
    filename = args.filename
    main(filename, args.lennardjones, args.magnet)