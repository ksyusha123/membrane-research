import numpy as np
import math

def find_angle_between(a, b):
    cos_angle = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return math.degrees(np.arccos(cos_angle))