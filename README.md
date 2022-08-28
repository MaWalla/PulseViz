# PulseViz

FXMode which analyzes a pulseaudio stream and displays it in various ways. Those available are:

- Intensity, which displays an entire color, averaged from the audio stream's different frequencies
- Rainbow Road, which displays a rainbow, scrolling across depending on the bass intensity
- Spectral Stretch, which expands colors on a defined spectrum, depending on their frequency band's volume

The backend is based off [this Project](https://github.com/pckbls/pulseviz.py).

## Compatibility

Given that it's built interfacing Pulseaudio, only Operating Systems using that (so mostly Linux) are supported. 
With that out of the way, both Pulseaudio and PipeWire (which implements it) are supported

## Requirements

[ImmersiveFX](https://github.com/MaWalla/ImmersiveFX)

## Installation

Since this comes as a submodule for ImmersiveFX already, follow the installation steps over there to get it working. ^^

## Configuration

additionally to the config done in the ImmersiveFX README, the following keys can be set in `config.json`:

- `source_name` name of the Pulseaudio source. Can be found by running `pactl list sources` and using the "Name" key. If not or wrongly provided, you're asked to choose an available source at start
- `spectral_stretch_buffer_size` amount of data points to base the color distribution on. A higher number means smoother movements but also less accuracy and increased latency. Must be at least 2 and defaults to 4
- `spectral_stretch_color_map` custom map for color distribution. must be an object with keys ranging from 0 to 32 (as strings) and values being rgb lists like so: `{"0": [255, 0, 0], "1": [255, 192, 0], ..., "32": [128, 16, 255]"}`. Defaults to a rainbow.

## Notes

Both Intensity and Rainbow Road don't work like I'm, wanting them to and require some more tuning.

There is quite some latency along the processing way. While the cycles run fine (and even the more heavy ScreenFX works faster), 
some additional latency may be introduced by Pulseaudio buffering. I hope to find a way around that. At least for Bluetooth it's pretty much in sync.