import lightningchart as lc
import numpy as np
import h5py

lc.set_license('my-license-key')

file_path = 'Dataset/rf_dataset.h5'

with h5py.File(file_path, 'r') as f:
    sample_key = 'sample_0'
    sample_group = f[sample_key]
    
    carrier_freq = sample_group.attrs['carrier_freq']
    modulation = sample_group.attrs['modulation']
    sampling_rate = sample_group.attrs['sampling_rate']
    snr = sample_group.attrs['snr']
    
    # Load I/Q signal data
    iq_signal = sample_group['iq_signal'][:]
    i_data = iq_signal[:, 0]  # In-phase component
    q_data = iq_signal[:, 1]  # Quadrature component

# Time axis for plotting the waveform
time_axis = np.arange(len(i_data)) / sampling_rate

# Calculate magnitude and phase for bubble size and color
magnitude = np.sqrt(i_data**2 + q_data**2)  # Intensity of the signal
phase = np.arctan2(q_data, i_data)  # Phase of the signal

# Normalize magnitude and phase
magnitude_normalized = (magnitude - np.min(magnitude)) / (np.max(magnitude) - np.min(magnitude))
phase_normalized = (phase - np.min(phase)) / (np.max(phase) - np.min(phase))

chart = lc.Chart3D(
    theme=lc.Themes.Light,
    title=f'3D Bubble Chart - {modulation} Modulation, SNR: {snr} dB'
)

chart.get_default_x_axis().set_title('Time (s)')
chart.get_default_y_axis().set_title('In-Phase (I)')
chart.get_default_z_axis().set_title('Quadrature (Q)')

series = chart.add_point_series(
    render_2d=False,
    individual_lookup_values_enabled=True,
    individual_point_color_enabled=True,
    individual_point_size_axis_enabled=True,
    individual_point_size_enabled=True,
)
series.set_point_shape('sphere')
series.set_palette_point_colors(
    steps=[
        {'value': 0.0, 'color': lc.Color(255, 128, 0)},  # Orange for low phase
        {'value': 0.5, 'color': lc.Color(255, 255, 0)},  # Yellow for medium phase  
        {'value': 1.0, 'color': lc.Color(0, 128, 255)},  # Blue for high phase
    ],
    look_up_property='value',
    interpolate=True,
    percentage_values=True
)

# Prepare the bubble data
data = []
for t, i, q, mag, ph in zip(
    time_axis[:], i_data[:], q_data[:1000], magnitude_normalized[:1000], phase_normalized[:1000]
):  # Limit data to 1000 points for clarity
    data.append({
        'x': float(t),         # Time as X-axis
        'y': float(i),         # In-phase (I) as Y-axis
        'z': float(q),         # Quadrature (Q) as Z-axis
        'size': mag * 16 + 4,  # Scale magnitude to bubble size (range: 4 to 20)
        'value': ph            # Phase determines the color (normalized 0 to 1)
    })

series.add(data)
chart.add_legend(data=series).set_dragging_mode("draggable")

chart.open()
