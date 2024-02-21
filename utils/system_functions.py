import numpy as np

def find_membrane_top_and_bottom_y_pos(system):
    membrane_edge_particles = np.array(list(filter(lambda particle: particle.type == 0, system.part.all())))
    y_positions_of_membrane_edge = np.sort(np.array(list(map(lambda p: p.pos[1], membrane_edge_particles))))
    upper = np.median(y_positions_of_membrane_edge[:-len(membrane_edge_particles) // 2 :-1])
    lower = np.median(y_positions_of_membrane_edge[:len(membrane_edge_particles) // 2])
    return upper, lower