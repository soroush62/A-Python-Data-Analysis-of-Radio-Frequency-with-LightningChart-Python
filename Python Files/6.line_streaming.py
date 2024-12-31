
import h5py
import numpy as np
import lightningchart as lc
from scipy.fftpack import fft
import time

lc.set_license('my-license-key')

file_path = 'Dataset/rf_dataset.h5' 
sample_key = 'sample_0' 

with h5py.File(file_path, 'r') as f:
    sample_group = f[sample_key]
    iq_signal = sample_group['iq_signal'][:]  # Extract signal data
    sampling_rate = sample_group.attrs.get('sampling_rate', 1e6)  # Default to 1 MHz

# Combine IQ signal
signal = iq_signal[:, 0] + 1j * iq_signal[:, 1]

# Chart setup for real-time visualization
chart = lc.ChartXY(
    title="Frequency Spectrum (Streaming)",
    theme=lc.Themes.Dark
)

line_series = chart.add_line_series()

# Customize Axes
chart.get_default_x_axis().set_title("Frequency (Hz)")
chart.get_default_y_axis().set_title("Amplitude")

# Define streaming parameters
frame_size = 1000  # Number of samples per frame
frame_interval = 0.5  # Time interval between frames (in seconds)

# Start streaming data
def stream_data():
    total_samples = len(signal)
    num_frames = total_samples // frame_size
    frequencies = np.fft.rfftfreq(frame_size, d=1 / sampling_rate)

    max_amplitude = np.max(np.abs(signal))  # Maximum amplitude for color scaling

    for frame_idx in range(num_frames):
        # Extract the current frame
        start_idx = frame_idx * frame_size
        end_idx = start_idx + frame_size
        frame_signal = signal[start_idx:end_idx]

        # Compute FFT for the frame
        spectrum = np.abs(fft(frame_signal)[:len(frequencies)])

        # Prepare data for the line chart
        line_data = [{"x": frequencies[i], "y": spectrum[i]} for i in range(len(frequencies))]

        # Update chart
        line_series.clear()
        line_series.add(data=line_data)

        # Configure the gradient color palette
        gradient_steps = [
        {"value": np.min(spectrum), "color": lc.Color("#0000FF")},  # Deep Blue
        {"value": np.percentile(spectrum, 20), "color": lc.Color("#0080FF")},  # Light Blue
        {"value": np.percentile(spectrum, 40), "color": lc.Color("#00FF00")},  # Green
        {"value": np.percentile(spectrum, 60), "color": lc.Color("#FFFF00")},  # Yellow
        {"value": np.percentile(spectrum, 80), "color": lc.Color("#FF8000")},  # Orange
        {"value": np.max(spectrum), "color": lc.Color("#FF0000")},  # Red
]

        line_series.set_palette_line_coloring(
            steps=gradient_steps,
            interpolate=True,
            look_up_property="y"
        )

        # Wait for the next frame
        time.sleep(frame_interval)

chart.open(live=True)

stream_data()






