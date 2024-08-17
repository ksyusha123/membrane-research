import numpy as np

def find_membrane_top_and_bottom_y_pos(system):
    membrane_edge_particles = np.array(list(filter(lambda particle: particle.type == 0, system.part.all())))
    y_positions_of_membrane_edge = np.sort(np.array(list(map(lambda p: p.pos[1], membrane_edge_particles))))
    upper = np.median(y_positions_of_membrane_edge[:-len(membrane_edge_particles) // 2 :-1])
    lower = np.median(y_positions_of_membrane_edge[:len(membrane_edge_particles) // 2])
    return upper, lower

def find_membrane_bottom_y_pos(system):
    membrane_edge_particles = np.array(list(filter(lambda particle: particle.type == 0, system.part.all())))
    y_positions_of_membrane_edge = np.sort(np.array(list(map(lambda p: p.pos[1], membrane_edge_particles))))
    lower = np.median(y_positions_of_membrane_edge[:len(membrane_edge_particles) // 2])
    return lower

def create_wca_interaction(system, type1, type2, sigma1, sigma2):
    sigma = (sigma1 + sigma2) / 2
    system.non_bonded_inter[type1, type2].lennard_jones.set_params(
        epsilon=1, sigma=sigma, cutoff=2.0**(1.0 / 6.0) * sigma, shift='auto')

def create_lj_interaction(system, type1, type2, sigma1, sigma2, epsilon=1):
    sigma = (sigma1 + sigma2) / 2
    system.non_bonded_inter[type1, type2].lennard_jones.set_params(
        epsilon=epsilon, sigma=sigma, cutoff=2.5 * sigma, shift='auto')

def create_lj_cos2_interaction(system, type1, type2, sigma1, sigma2):
    sigma = (sigma1 + sigma2) / 2
    system.non_bonded_inter[type1, type2].lennard_jones_cos2.set_params(
        epsilon=1, sigma=sigma, width=1.6 * sigma)