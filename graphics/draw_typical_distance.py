import matplotlib.pyplot as plt
import json
import sys

from utils import find_typical_distances

def draw_typical_distances(all_typical_distances):
    plt.rcParams.update({'font.size': 20})
    _, ax = plt.subplots(figsize=(9, 7))
    ax.set_xlabel('$t$')
    ax.set_ylabel('$dist$')
    ax.set_title(f'$\epsilon$=1')
    for distance_info in all_typical_distances:
        ax.plot(distance_info['time'], distance_info["distances"], label=f'$\sigma_p$={distance_info["sigma_p"]}')
    ax.legend()
    ax.axhline(0, color='black', linewidth=0.5)
    

def main(filenames):
    all_typical_distances = []
    for file in filenames:
        with open(file) as f:
            content = json.loads(f.read())
            all_distances = content['experiments']
            typical_distances = find_typical_distances(all_distances)
            all_typical_distances.append(typical_distances)


    plt.rcParams.update({'font.size': 20})
    _, ax = plt.subplots(figsize=(9, 7))
    ax.set_xlabel('$t$')
    ax.set_ylabel('$dist$')
    ax.set_title(f'$\epsilon$=1')
    for distance_info in all_typical_distances:
        ax.plot(distance_info['time'], distance_info["particle_to_center"], label=f'$\sigma_p$={distance_info["sigma_p"]}')
    ax.legend()
    ax.axhline(0, color='black', linewidth=0.5)

    plt.show()

if __name__ == '__main__':
    main(sys.argv[1:])