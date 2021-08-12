import colorsys
import threading
import numpy as np

from .main import PulseViz


class RainbowRoad(PulseViz):
    name = 'PulseViz (Rainbow Road)'

    def __init__(self, *args, **kwargs):
        self.rainbow_offset = 0
        self.acceleration_weight = {
            0: 0.25,
            1: 0.33,
            2: 0.5,
            3: 0.75,
            4: 0.83,
            5: 1,
            6: 1,
            7: 0.75,
            8: 0.5,
            9: 0.33,
            10: 0.1,
            11: 0.05,
            **{index + 12: 0 for index in range(21)},
        }

        self.scale = 360

        super().__init__(*args, **kwargs)

    def data_processing(self, *args, **kwargs):
        self.raw_data = self.pulseviz_bands.values

    def device_processing(self, device, device_instance):
        values = self.raw_data

        movement = np.sum([
            self.data_conversion(value, values.min(), values.max()) * self.acceleration_weight[index]
            for index, value in enumerate(values)
        ])

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
