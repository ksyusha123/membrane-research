import espressomd
import espressomd.observables
import espressomd.accumulators
import espressomd.analyze
import espressomd.interactions
import espressomd.visualization
import espressomd.checkpointing

import numpy as np
import datetime
import sys

from utils import savers, system_functions, vector_functions


membrane_checkpoint = espressomd.checkpointing.Checkpoint(checkpoint_id=f'Lipid_membrane_seed_13')


def init_system(particle_sigma, alpha):
    global system

    membrane_checkpoint.load()

    # Place additional particle
    pos = np.random.random(3) * system.box_l
    pos = [pos[0], 7, pos[2]]
    dip = np.random.random(3)
    dip /= np.linalg.norm(dip)
    additional_particle = system.part.add(pos=pos, type=2, rotation=(True, True, True), dip=dip)
    head_sigma = 0.95
    tail_sigma = 1
    
    system_functions.create_lj_interaction(system, 0, 2, head_sigma, particle_sigma)
    system_functions.create_lj_interaction(system, 1, 2, tail_sigma, particle_sigma)
    system_functions.create_lj_interaction(system, 2, 2, particle_sigma, particle_sigma)

    verlet_skin = 0.4

    # Add magnetic field
    systemtemp = 1.1
    H_dipm = alpha * systemtemp
    H_field = [0, -H_dipm, 0]
    H_constraint = espressomd.constraints.HomogeneousMagneticField(H=H_field)
    system.constraints.add(H_constraint)

    # Warmup
    system.thermostat.turn_off()

    system.time_step = 0.002
    system.cell_system.skin = verlet_skin

    damping = 30
    max_displacement = 0.01
    em_step = 10

    system.integrator.set_steepest_descent(
        f_max=0, gamma=damping, max_displacement=max_displacement)

    energy = system.analysis.energy()['total']
    relative_energy_change = 1.0
    while relative_energy_change > 0.05:
        system.integrator.run(em_step)
        energy_new = system.analysis.energy()['total']
        if energy < sys.float_info.epsilon:
            break
        relative_energy_change = (energy - energy_new) / energy
        print(f'Minimization, relative change in energy: {relative_energy_change:.4f}')
        energy = energy_new

    system.time = 0
    system.time_step = 0.01
    system.integrator.set_vv()
    system.cell_system.skin = verlet_skin

    # Set thermostat
    system.thermostat.set_langevin(kT=systemtemp, gamma=1.0, seed=13)

    system.periodicity = [True, False, True]

    return system, additional_particle, H_field


int_steps = 200
int_n_times = 100

def simulation(particle_sigma, particle, alpha, h_field):
    simulation_start = datetime.datetime.now()
    time = []
    distances_to_center = []

    top_to_center = []
    bottom_to_center = []
    dip_deviations = []

    for i in range(int_n_times):
        print("\rrun %d at time=%.0f " % (i, system.time), end='')
        system.integrator.run(int_steps)
        if i % 10 == 0:
            top, bottom = system_functions.find_membrane_top_and_bottom_y_pos(system)
            center = (top + bottom) / 2
            distance = particle.pos[1] - center
            time.append(int_steps * system.time_step * i)
            distances_to_center.append(distance)

            top_to_center.append(top - center)
            bottom_to_center.append(bottom - center)
            dip_deviations.append(vector_functions.find_angle_between(particle.dip, h_field))

            savers.write_vtk_file(system, f'homogenous_{alpha}', f'vtk_{simulation_start}', i, {0: 0.95, 1: 1, 2: 2.5})

    print(f'\nSimulation has taken {datetime.datetime.now() - simulation_start}')
    return {'epsilon': 1.0,
            'sigma_p': particle_sigma,
            'time': time,
            'alpha': alpha,
            'particle_to_center': distances_to_center,
            'top_to_center': top_to_center,
            'bottom_to_center': bottom_to_center,
            'dip_deviations': dip_deviations}

if __name__ == '__main__':
    particle_sigma = 2.5
    alpha = float(sys.argv[1])
    system, particle, h_field = init_system(particle_sigma, alpha)
    simulation_info = simulation(particle_sigma, particle, alpha, h_field)
    folder_name = 'magnet_homogenous'
    filename_draft = str(alpha).replace('.', '')
    savers.save_distance_as_json(simulation_info, f'{filename_draft}.json', folder_name)
