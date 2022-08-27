import colorsys
import numpy as np

from .main import PulseViz


class SpectralStretch(PulseViz):
    name = 'PulseViz (Spectral Stretch)'

    def __init__(self, *args, **kwargs):
        self.scale = 360
        self.band_amount = 33
        self.raw_data = np.zeros(self.band_amount)
        self.data_buffer = np.array([self.raw_data for _ in range(4)])

        rainbow_map = {
            index + 3: [
                int(color * 255)
                for color in colorsys.hsv_to_rgb((self.scale * index / self.band_amount - 6) / self.scale, 1, 1)
            ]
            for index in range(self.band_amount - 6)
        }

        self.first_color, *_ = rainbow_map.values()
        *_, self.last_color = rainbow_map.values()

        self.rainbow_map = {
            **{index: self.first_color for index in range(3)},
            **rainbow_map,
            **{index: self.last_color for index in range(self.band_amount - 3, self.band_amount)}
        }

        super().__init__(*args, **kwargs)

    def data_processing(self, *args, **kwargs):
        raw_data = np.array(self.converted_values)

        total_volume = 0
        for number in raw_data:
            total_volume += number

        first_dataset, *datasets = self.data_buffer

        if total_volume:
            self.data_buffer = np.array([*datasets, raw_data / total_volume])
        else:
            self.data_buffer = np.array([*datasets, raw_data])

        self.raw_data = self.data_buffer.mean(axis=0)

    def device_processing(self, device, device_instance):
        led_numbers = [round(number) for number in (self.raw_data * device_instance.leds)]

        output = []

        for index in range(self.band_amount):
            for _ in range(led_numbers[index]):
                output = [*output, self.rainbow_map[index]]

        if not output:
            output = [
                [
                    int(color * 255)
                    for color in colorsys.hsv_to_rgb((self.scale * index / device_instance.leds) / self.scale, 1, 1)
                ]
                for index in range(device_instance.leds)
            ]

        return output
