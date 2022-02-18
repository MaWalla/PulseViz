import numpy as np

from immersivefx import Core
from .bands import Bands, calculate_octave_bands
from .pacmd import list_sources


class PulseViz(Core):
    name = 'PulseViz'

    target_versions = ['1.1']
    target_platforms = ['linux']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        bands_data = {
            'source_name': self.get_source_name(),
            'sample_frequency': 44100,
            'sample_size': 8192,
            'window_size': 1024,
            'window_overlap': 0.5,
            'window_function': 'hanning',
            'weighting': 'Z',
            'band_frequencies': calculate_octave_bands(fraction=3)
        }

        self.pulseviz_bands = Bands(**bands_data)
        self.start_bands()
        self.start_threads()

    def splash(self):
        print('Welcome to ----------------------------- by MaWalla')
        print('        ███ █  █ █    ██ ███ █   █ ███ ████        ')
        print('        █ █ █  █ █   █   █   █   █  █     █        ')
        print('        ███ █  █ █    █  ██  ██ ██  █   ██         ')
        print('        █   █  █ █     █ █    ███   █  █           ')
        print('        █    ██  ███ ██  ███   █   ███ ████        ')
        print('-- backend: https://github.com/pckbls/pulseviz.py -')

    def get_source_name(self):
        """
        Choice menu for the used pulseaudio source,
        can also be set statically by setting a "source_name" key in the config.
        Options can be manually obtained with pactl list sources | grep 'Name:'
        """
        sources = list_sources()
        chosen_source = self.config.get('source_name')
        while chosen_source not in sources:
            print('---------------------------------------------------')
            print('PulseViz requires an audio source but no source_name was defined ')
            print('or the source isn\'t available right now. Pick another source please:\n')
            for index, source in enumerate(sources):
                print(f'{index}: {source}')

            choice = input()

            try:
                chosen_source = list(sources)[int(choice)]
            except (IndexError, ValueError):
                print(f'Invalid choice! It must be a number bigger than 0 and smaller than {len(sources)}, try again!')

        return chosen_source

    def start_bands(self):
        self.pulseviz_bands.start()

    def stop_bands(self):
        self.pulseviz_bands.stop()

    @property
    def converted_values(self):
        """
        takes the raw pulseviz data and puts all bands weight on a scale from 0.0 to 1.0
        """
        # I intentionally reassign with np.array() so that the variable can't change while the loop cycle runs
        values = np.array(self.pulseviz_bands.values)

        return np.array([
            (value - values.min()) / (values.max() - values.min())
            if not np.isinf(value) else 0
            for value in values
        ])
