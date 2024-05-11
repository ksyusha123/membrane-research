# Computer simulation of the magnetomechanical interaction of nanoparticles and cell membranes 

Author: Astakhova Kseniia. Telegram: @kast0.

## Description  
A collection of scripts used in the study of the interaction of cell membranes and nanoparticles. Scripts are using ESPResSo. 

## Installation 
Firstly one needs to install [ESPResSo](https://espressomd.github.io/doc4.2.1/installation.html). Then install matplotlib. This repository uses matplotlib-3.6.3.

## Structure  
```
|-- graphics
|   |-- wca.py
|   |-- average_cross_time.py
|   |-- utils.py
|   |-- equal_magnet_with_non_magnet.py
|   |-- membrane_move.py
|   |-- median_distances_unified.py
|   |-- all_distances.py
|   |-- lj.py
|   |-- lj_cos2.py
|-- membrane_and_magnet_particle_homogenous.py
|-- utils
|   |-- vector_functions.py
|   |-- stat_collector.py
|   |-- savers.py
|   |-- system_functions.py
|-- membrane_and_magnet_particle_gradient.py
|-- membrane_and_particle.py
|-- membrane_self_assembly.py
```
At the root of the repository are the scripts themselves, which are run using espresso. The graphics folder contains scripts for plotting statistics collected during the simulation. The `utils` folder and the `graphics/utils.py` file contain common functions used in the corresponding folder. 

## How to use  
The scripts have help: `script.py -h`
To run the script you should use the `pypresso` command provided with ESPResSo: `./pypresso script.py`

## Useful details  
For visualizing magnetic moment you can pass option `director_arrows=True` to the openGLLive visualizer. Also you will need to adapt the code in `src/python/espressomd/visualization.py` to draw dipole moment vectors. As a quick workaround, you can replace `particle_data.director` by `particle_data.dip` to change the behavior of `director_arrows=True`.

