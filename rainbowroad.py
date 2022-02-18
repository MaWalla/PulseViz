import colorsys
import threading
import numpy as np

from .main import PulseViz


class RainbowRoad(PulseViz):
    name = 'PulseViz (Rainbow Road)'

    def __init__(self, *args, **kwargs):
        self.rainbow_offset = 0
        self.scale = 360
        self.raw_data = 0

        super().__init__(*args, **kwargs)

    def data_processing(self, *args, **kwargs):
        converted_values = self.converted_values

        converted_values = converted_values - converted_values.mean()

        self.raw_data = np.array([
            converted_values[:4].mean() * 0.75,
            converted_values[4:8].mean() * 2,
            converted_values[9:13].mean(),
            converted_values[13:-6].mean() * 0.33,
            converted_values[-6:].mean() * 0.2,
            ]).mean(axis=0) * 12

    def device_processing(self, device, device_instance):
        movement = self.raw_data
        if movement > 0:
            self.rainbow_offset += movement

        if self.rainbow_offset > self.scale:
            self.rainbow_offset -= self.scale

        return [
            [
                int(color * 255) for color in colorsys.hsv_to_rgb(
                    ((self.scale * index / device_instance.leds) + self.rainbow_offset) / self.scale, 1, 1
                )
            ] for index in range(device_instance.leds)
        ]
