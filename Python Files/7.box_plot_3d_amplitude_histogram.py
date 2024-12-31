import numpy as np
import h5py
import lightningchart as lc
import time

lc.set_license('my-license-key')

file_path = 'Dataset/rf_dataset.h5'
with h5py.File(file_path, 'r') as f:
    frequencies = []
    amplitudes = []
    for sample_key in f.keys():
        sample_group = f[sample_key]
        freq = sample_group.attrs['carrier_freq']
        iq_data = sample_group['iq_signal'][:]
        amplitude = np.sqrt(iq_data[:, 0]**2 + iq_data[:, 1]**2)
        frequencies.append(freq)
        
        # downsample_rate = 100 
        # amplitude_downsampled = amplitude[::downsample_rate]
        amplitudes.append(amplitude)

# Create a 3D chart
chart = lc.Chart3D(title='3D Amplitude Histogram')
chart.set_animation_zoom(True)

# Add a box series to the chart
box_series = chart.add_box_series()

# Configure axes
chart.get_default_x_axis().set_title('Sample Index')
chart.get_default_y_axis().set_title('Count of Amplitudes') 
chart.get_default_z_axis().set_title('Amplitude')

# Configure a fixed bounding box
chart.set_bounding_box(x=3, y=1, z=1)

# Configure color palette
palette_steps = [
    {"value": 0, "color": lc.Color('blue')},
    {"value": 300, "color": lc.Color('green')},
    {"value": 600, "color": lc.Color('yellow')},
    {"value": 9000, "color": lc.Color('orange')},
    {"value": 1400, "color": lc.Color('red')}, 
]
box_series.set_palette_coloring(steps=palette_steps, look_up_property="y")

chart.add_legend(data=box_series).set_dragging_mode("draggable")
# Open the chart in live mode
chart.open(live=True)

# Function to update the chart dynamically
def update_chart(frame):
    data = []
    for idx, amp in enumerate(amplitudes):
        # Aggregate counts by taking every nth frame for smoother updates
        hist, bins = np.histogram(amp[:frame * 20], bins=10, range=(0, np.max(amp)))  # 10 bins
        for bin_idx in range(len(hist)):
            bin_center = (bins[bin_idx] + bins[bin_idx + 1]) / 2
            bin_size = bins[bin_idx + 1] - bins[bin_idx]
            data.append({
                'xCenter': float(idx),  # Frequency index
                'yCenter': float(hist[bin_idx] / 2),  # Count as height (center)
                'zCenter': float(bin_center),  # Amplitude bin
                'xSize': 0.8,  # Fixed bar width
                'ySize': float(hist[bin_idx]),  # Height of the bar (count value)
                'zSize': float(bin_size)  # Fixed bin width
            })
    box_series.add(data)  # Replace existing data

# Number of frames in the animation
num_frames = max(len(amp) for amp in amplitudes) // 10

for frame in range(1, num_frames + 1):
    update_chart(frame)
    time.sleep(0.2)

chart.close()
