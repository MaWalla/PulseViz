# Uses parts of the code from https://github.com/pckbls/pulseviz.py

from .intensity import Intensity
from .rainbowroad import RainbowRoad
from .spectral_stretch import SpectralStretch

modes = [
    Intensity,
    RainbowRoad,
    SpectralStretch,
]
