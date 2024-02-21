def find_typical_distances(all_distances):
    point = 3.5
    min_d = 1000
    typical_distances = None
    for distances in all_distances:
        if abs(distances['particle_to_center'][0] - point) < min_d:
            min_d = abs(distances['particle_to_center'][0] - point)
            typical_distances = distances
    return typical_distances