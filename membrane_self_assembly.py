import espressomd
import espressomd.observables
import espressomd.accumulators
import espressomd.analyze
import espressomd.interactions
import espressomd.visualization
import espressomd.checkpointing

import numpy as np
import datetime
import threading
import random
import sys

seed = 13

random.seed(seed)
np.random.seed(seed)

checkpoint = espressomd.checkpointing.Checkpoint(checkpoint_id=f"Lipid_membrane_seed_{seed}")

def use_checkpoint(init_system_func):
    def wrapper():
        if not checkpoint.has_checkpoints():
            init_system_func()
            checkpoint.register('system')
            checkpoint.save()
        else:
            checkpoint.load()
            system.integrator.run(2, reuse_forces=True)
        return system
    return wrapper


@use_checkpoint
def init_system():
    global system

    mol_num = 320
    box_l = [14.0, 14.0, 14.0]
    system = espressomd.System(box_l=box_l)

    # Set bonded interactions
    fene = espressomd.interactions.FeneBond(k=30, d_r_max=1.5)
    hb = espressomd.interactions.HarmonicBond(k=10.0, r_0=4.0)

    system.bonded_inter.add(fene)
    system.bonded_inter.add(hb)

    # Set non-bonded interactions
    lj_eps = 1.0
    lj_sigmah = 0.95
    lj_sigma = 1.0
    lj_offset = 0.0

    system.non_bonded_inter[0, 0].lennard_jones.set_params(
        epsilon=lj_eps, sigma=lj_sigmah, cutoff=1.1225 * lj_sigmah,
        shift=0.25 * lj_eps, offset=lj_offset)

    system.non_bonded_inter[0, 1].lennard_jones.set_params(
        epsilon=lj_eps, sigma=lj_sigmah, cutoff=1.1225 * lj_sigmah,
        shift=0.25 * lj_eps, offset=lj_offset)

    system.non_bonded_inter[1, 1].lennard_jones_cos2.set_params(
        epsilon=lj_eps, sigma=lj_sigma, offset=lj_offset, width=1.6)

    # Place molecules randomly
    particle_types = [0, 1, 1]
    bond_l = 1.0
    for i in range(mol_num):
        tail_pos = np.random.random(3) * system.box_l
        orient = 2 * np.random.random(3) - 1
        orient /= np.linalg.norm(orient)
        for j in range(len(particle_types)):
            cur_part_id = i * len(particle_types) + j
            particle_position = tail_pos + (len(particle_types) - j - 1) * bond_l * orient
            system.part.add(id=cur_part_id, type=particle_types[j], pos=particle_position)
            if j > 0:
                system.part.by_id(cur_part_id - 1).add_bond((fene, cur_part_id))
            if j > 1:
                system.part.by_id(cur_part_id - 2).add_bond((hb, cur_part_id))

    verlet_skin = 0.4
    
    # Warmup
    system.time_step = 0.002
    system.cell_system.skin = verlet_skin

    damping = 30
    max_displacement = 0.01 * lj_sigmah
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
    systemtemp = 1.1
    system.thermostat.set_langevin(kT=systemtemp, gamma=1.0, seed=seed)

system = init_system()

visualizer = espressomd.visualization.openGLLive(system, bond_type_radius=[0], background_color=[255,255,255])

def simulation():
    int_steps = 200
    int_n_times = 1500
    simulation_start = datetime.datetime.now()
    for i in range(int_n_times):
        print("\rrun %d at time=%.0f " % (i, system.time), end='')
        system.integrator.run(int_steps)
        visualizer.update()
        if i % 100 == 0:
            checkpoint.save()
    
    checkpoint.save()
    print(f'\nSimulation has taken {datetime.datetime.now() - simulation_start}')

thread = threading.Thread(target=simulation)
thread.daemon = True
thread.start()
visualizer.start()