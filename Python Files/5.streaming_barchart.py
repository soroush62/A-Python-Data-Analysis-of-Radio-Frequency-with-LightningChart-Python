# Real-time Streaming Using LightningChart Bar Chart
import h5py
import numpy as np
import lightningchart as lc
import time
from scipy.fftpack import fft

lc.set_license('my-license-key')

# Load dataset
file_path = 'Dataset/rf_dataset.h5'  # Adjust your dataset path
sample_key = 'sample_0'  # Adjust based on your dataset

with h5py.File(file_path, 'r') as f:
    sample_group = f[sample_key]
    iq_signal = sample_group['iq_signal'][:]  # Extract signal data
    sampling_rate = sample_group.attrs.get('sampling_rate', 1e6)  # Default 1 MHz

# Combine IQ signal
signal = iq_signal[:, 0] + 1j * iq_signal[:, 1]

# Set up BarChart
chart = lc.BarChart(
    title="Frequency Spectrum Equalizer Streaming",
    theme=lc.Themes.Dark,
)
chart.set_animation_values(True)  # Enable smooth animation for bar updates
chart.set_animation_category_position(True)
chart.set_sorting("disabled")
chart.set_value_label_display_mode("hidden")
chart.set_label_rotation(45)

# Define data streaming parameters
frame_size = 200  # Samples per frame
frame_interval = 0.05  # Interval between frames (seconds)
num_bars = frame_size // 2  # Only positive frequencies

# Initialize bar categories (frequency bins)
frequencies = np.fft.rfftfreq(frame_size, d=1 / sampling_rate)
categories = [f"{freq / 1e3:.0f} kHz" for freq in frequencies]
chart.set_data([{"category": cat, "value": 0} for cat in categories])

chart.set_palette_colors(
    steps=[
        {"value": 0.0, "color": lc.Color("blue")},
        {"value": 0.1, "color": lc.Color("yellow")},
        {"value": 0.3, "color": lc.Color("orange")},
        {"value": 0.5, "color": lc.Color("red")},
    ],
    percentage_values=False,
)

# Streaming function
def stream_data():
    total_samples = len(signal)
    num_frames = total_samples // frame_size

    for frame_idx in range(num_frames):
        start_idx = frame_idx * frame_size
        end_idx = start_idx + frame_size
        frame_signal = signal[start_idx:end_idx]

        # Compute FFT and normalize
        spectrum = np.abs(fft(frame_signal)[:len(frequencies)])
        spectrum = spectrum / np.max(spectrum)  # Normalize to [0, 1]

        # Prepare data for bars
        bar_data = [{"category": cat, "value": spectrum[i]} for i, cat in enumerate(categories)]

        # Update chart
        chart.set_data(bar_data)

        # Wait for the next frame
        time.sleep(frame_interval)

# Start streaming in a separate thread
from threading import Thread
streaming_thread = Thread(target=stream_data)
streaming_thread.start()

chart.open(live=True)