import matplotlib.pyplot as plt
import json
import sys

def main(filename):
    with open(filename) as f:
        content = json.loads(f.read())

    plt.rcParams.update({'font.size': 20})
    _, ax = plt.subplots(figsize=(9, 7))
    ax.set_xlabel('$t$')
    ax.set_ylabel('$\Delta y$')
    ax.set_title(f'$\epsilon$={content["experiments"][0]["epsilon"]}, $\sigma_p$={content["experiments"][0]["sigma_p"]}')

    for distance_info in content['experiments']:
        ax.plot(distance_info['time'], distance_info["distances"])

    ax.axhline(0, color='black', linewidth=0.5)

    plt.savefig(filename.replace('json', ''))

if __name__ == '__main__':
    main(sys.argv[1])