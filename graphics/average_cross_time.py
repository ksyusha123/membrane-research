import json
import argparse

from utils import get_cross_time_stat
 
parser = argparse.ArgumentParser(description="Draw typical distance with membrane edges")
parser.add_argument("files", nargs='+', type=str, help="filename with simulations info")
    

def main(args):
    for file in args.files:
        with open(file) as f:
            content = json.loads(f.read())
            all_distances = content['experiments']
            cross_time_stat = get_cross_time_stat(all_distances)
            print(f'Cross time stat when {all_distances[0]["magnet_count"]}')
            print("\n".join(map(lambda kv: f'{kv[0]}: {kv[1]}', cross_time_stat.items())))
            print()

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)