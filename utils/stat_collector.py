from utils import system_functions
from utils import vector_functions


class StatCollector:
    def __init__(self, system, particle, int_steps, epsilon, particle_sigma, alpha, magnet_count, moment) -> None:
        self.time = []
        self.distances_to_center = []
        self.top_to_center = []
        self.bottom_to_center = []
        self.dip_deviations = []
        self.membrane_center = []
        self.membrane_top = []
        self.membrane_bottom = []
        self.particle_coord = []
        self.f = []

        self.system = system
        self.particle = particle
        self.int_steps = int_steps

        self.epsilon = epsilon
        self.particle_sigma = particle_sigma
        self.alpha = alpha
        self.magnet_count = magnet_count

        self.moment = moment

    def collect(self, i):
        top, bottom = system_functions.find_membrane_top_and_bottom_y_pos(self.system)
        center = (top + bottom) / 2
        distance = self.particle.pos[1] - center
        self.time.append(self.int_steps * self.system.time_step * i)
        self.distances_to_center.append(distance)

        self.top_to_center.append(top - center)
        self.bottom_to_center.append(bottom - center)

        self.membrane_center.append(center)
        self.membrane_top.append(top)
        self.membrane_bottom.append(bottom)

        self.particle_coord.append(self.particle.pos[1])

        f = self.particle.f
        self.f.append([f[0], f[1], f[2]])

        # visualizer.update()
        self.dip_deviations.append(vector_functions.find_angle_between(self.particle.dip, [0, -1, 0]))

    def stat(self):
        return {'epsilon': self.epsilon,
            'sigma_p': self.particle_sigma,
            'time': self.time,
            'alpha': self.alpha,
            'particle_to_center': self.distances_to_center,
            'top_to_center': self.top_to_center,
            'bottom_to_center': self.bottom_to_center,
            'dip_deviations': self.dip_deviations,
            'magnet_count': self.magnet_count,
            'membrane_center': self.membrane_center,
            'particle_coord': self.particle_coord,
            'f': self.f,
            'moment': self.moment}
