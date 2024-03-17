#SBCS

import numpy as np
import pygame
import tempfile
import os
import time
from scipy.io.wavfile import write

# Initialize Pygame Mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1)

def generate_sine_wave(frequency, duration=1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note = np.sin(frequency * t * 2 * np.pi)
    return note