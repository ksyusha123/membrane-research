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
import threading

from utils import savers, system_functions, stat_collector

import argparse
 
parser = argparse.ArgumentParser(description="Modelling of lipid membrane and charged particle interaction using gradient magnetic field")
parser.add_argument("-a", "--alpha", type=float, help="The magnitude of the magnetic moment of fixed magnets")
parser.add_argument("-m", "--moment", type=float, help="The magnitude of the magnetic moment of particle")
parser.add_argument("-c", "--count", type=int, help="Count of fixed magnets")
parser.add_argument("-e", "--epsilon", type=float, help="Epsilon")
parser.add_argument("-v", "--visualize", action="store_true", help="Visualize modelling using GL")

seed = 13

membrane_checkpoint = espressomd.checkpointing.Checkpoint(checkpoint_id=f'Lipid_membrane_seed_13')
particle_sigma = 2.5


def place_charged_particles(system, dip, count = 1):
    charged_particles = []
    lower_y_pos = system_functions.find_membrane_bottom_y_pos(system)
    start_x = system.box_l[0] / 2 - count // 2
    for i in range(count):
        cp = system.part.add(pos=[start_x, lower_y_pos - 2, 7], fix=[True, True, True], rotation=[False, False, False], type=3, dip=[0, -dip, 0])
        charged_particles.append(cp)
        print(start_x)
        start_x += 1
    return charged_particles


def init_system(cp_dip, magnet_count, particle_dip_modulus, epsilon):
    global system

    membrane_checkpoint.load()

    # Place additional particle
    pos = np.random.random(3) * system.box_l
    pos = [pos[0], 7, pos[2]]
    dip = np.random.random(3)
    dip /= np.linalg.norm(dip)
    dip *= particle_dip_modulus
    additional_particle = system.part.add(pos=pos, type=2, rotation=(True, True, True), dip=dip)
    head_sigma = 0.95
    tail_sigma = 1
    
    system_functions.create_lj_interaction(system, 0, 2, head_sigma, particle_sigma, epsilon)
    system_functions.create_lj_interaction(system, 1, 2, tail_sigma, particle_sigma, epsilon)
    system_functions.create_lj_interaction(system, 2, 2, particle_sigma, particle_sigma, epsilon)

    verlet_skin = 0.4

    systemtemp = 1.1

    # Warmup
    system.thermostat.turn_off()

    actor = espressomd.magnetostatics.DipolarDirectSumCpu(prefactor=1.)
    system.magnetostatics.solver = actor

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
    system.thermostat.set_langevin(kT=systemtemp, gamma=1.0, seed=seed)

    system.periodicity = [True, False, True]

    charged_particles = place_charged_particles(system, cp_dip, magnet_count)

    system_functions.create_lj_interaction(system, 3, 3, 2, 2)
    system_functions.create_lj_interaction(system, 2, 3, 2, particle_sigma)

    return system, additional_particle, charged_particles

def save_results(magnet_count, results, moment, epsilon):
    folder_name = f'magnet_gradient_{epsilon}_'
    filename_draft = f'{str(cp_dip)}_{str(moment)}'
    savers.save_distance_as_json(results, f'{filename_draft}.json', folder_name)


int_steps = 200
int_n_times = 300

def simulation(particle, cp_dip, magnet_count, moment, epsilon, visualize=False):
    simulation_start = datetime.datetime.now()
    statistics = stat_collector.StatCollector(system, particle, int_steps, epsilon, particle_sigma, cp_dip, magnet_count, moment)

    for i in range(int_n_times):
        print("\rrun %d at time=%.0f " % (i, system.time), end='')
        system.integrator.run(int_steps)
        if i % 10 == 0:
            statistics.collect(i)
            # savers.write_vtk_file(system, f'gradient_{cp_dip}', f'vtk_{simulation_start}_{magnet_count}', i, {0: 0.95, 1: 1, 2: 2.5, 3: 1})

            if visualize:
                visualizer.update()

    print(f'\nSimulation has taken {datetime.datetime.now() - simulation_start}')
    results = statistics.stat()
    save_results(magnet_count, results, moment, epsilon)
    return results

if __name__ == '__main__':
    args = parser.parse_args()
    cp_dip = args.alpha
    moment = args.moment
    epsilon = args.epsilon
    fixed_magnet_count = args.count

    system, particle, charged_particles = init_system(cp_dip, fixed_magnet_count, moment, epsilon)

    if args.visualize:

        visualizer = espressomd.visualization.openGLLive(system, bond_type_radius=[0], background_color=[255,255,255], director_arrows=True)
    
        thread = threading.Thread(target=simulation, args=(particle, cp_dip, fixed_magnet_count, moment, True))
        thread.daemon = True
        thread.start()
        visualizer.start()
        
    else:
        simulation_info = simulation(particle, cp_dip, fixed_magnet_count, moment, epsilon)
