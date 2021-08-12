import threading
import numpy as np

from .main import PulseViz


class Intensity(PulseViz):
    name = 'PulseViz (Intensity)'

    def __init__(self, *args, **kwargs):
        self.band_mapping = {
            0: [255, 0, 0],
            1: [255, 0, 0],
            2: [255, 0, 0],
            3: [255, 0, 0],
            4: [255, 0, 0],
            5: [255, 0, 0],
            6: [255, 0, 0],
            7: [255, 0, 0],
            8: [255, 0, 0],
            9: [255, 128, 0],
            10: [255, 255, 0],
            11: [255, 255, 0],
            12: [255, 255, 0],
            13: [255, 255, 0],
            14: [255, 255, 0],
            15: [128, 255, 0],
            16: [0, 255, 0],
            17: [0, 255, 0],
            18: [0, 255, 0],
            19: [0, 255, 0],
            20: [0, 255, 0],
            21: [0, 255, 128],
            22: [0, 255, 255],
            23: [0, 255, 255],
            24: [0, 255, 255],
            25: [0, 255, 255],
            26: [0, 255, 255],
            27: [0, 128, 255],
            28: [0, 0, 255],
            29: [0, 0, 255],
            30: [0, 0, 255],
            31: [0, 0, 255],
            32: [0, 0, 255],
            33: [0, 0, 255],
        }

        super().__init__(*args, **kwargs)

    @staticmethod
    def post_process_color(value, color):
        if value != color.max():
            value *= 0.8

        value *= 255 / (color.max() or 1)

        return value

    def device_processing(self, device, device_instance):
        return [self.raw_data for _ in range(device_instance.leds)]

    def data_processing(self, *args, **kwargs):
        values = self.pulseviz_bands.values

        converted_values = [[
            self.data_conversion(value, values.min(), values.max()) * color if not np.isinf(value) else 0
            for color in self.band_mapping[num]
        ] for num, value in enumerate(values)]

        color = np.array(converted_values).mean(axis=0)

        self.raw_data = np.clip([
            self.post_process_color(rgb, color) for rgb in color
        ], 0, 255).astype(int).tolist()
