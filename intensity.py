import threading
import numpy as np

from .main import PulseViz


class Intensity(PulseViz):
    name = 'PulseViz (Intensity)'

    def __init__(self, *args, **kwargs):
        last_frames = kwargs.get('config', dict()).get('last_frames', 2)
        if last_frames > 0:
            self.last_frames = last_frames + 1
        else:
            self.last_frames = 1
        self.color_values = np.zeros([self.last_frames, 3])

        self.sub_bass_color = np.array((255, 0, 96))
        self.kick_color = np.array((255, 0, 0))
        self.snare_color = np.array((192, 255, 0))
        self.mid_color = np.array((0, 255, 128))
        self.high_color = np.array((0, 128, 255))

        super().__init__(*args, **kwargs)

    @staticmethod
    def post_process_color(value, color):
        value *= 255 / (color.max() or 1)

        return value

    def device_processing(self, device, device_instance):
        return [self.raw_data for _ in range(device_instance.leds)]

    def data_processing(self, *args, **kwargs):
        values = self.pulseviz_bands.values

        all_converted_values = np.array([
            self.data_conversion(value, values.min(), values.max()) if not np.isinf(value) else 0
            for value in values
        ])

        calculated_color = np.array([
            all_converted_values[:4].mean() * self.sub_bass_color * 0.5,
            all_converted_values[4:8].mean() * self.kick_color,
            all_converted_values[9:13].mean() * self.snare_color,
            all_converted_values[13:-6].mean() * self.mid_color * 0.75,
            all_converted_values[-6:].mean() * self.high_color * 0.75,
        ]).mean(axis=0)

        self.color_values = np.roll(self.color_values, -1, axis=0)
        self.color_values[self.last_frames - 1] = calculated_color

        color = self.color_values.mean(axis=0)

        self.raw_data = np.clip([
            self.post_process_color(rgb, color) for rgb in color
        ], 0, 255).astype(int).tolist()
