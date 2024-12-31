import h5py
import numpy as np
import lightningchart as lc

lc.set_license('my-license-key')

file_path = 'Dataset/rf_dataset.h5'

# Open the HDF5 file and read a sample
with h5py.File(file_path, 'r') as f:
    sample_key = 'sample_0'
    sample_group = f[sample_key]
    
    # Extract metadata
    carrier_freq = sample_group.attrs['carrier_freq']
    modulation = sample_group.attrs['modulation']
    sampling_rate = sample_group.attrs['sampling_rate']
    snr = sample_group.attrs['snr']
    
    # Load I/Q signal data
    iq_signal = sample_group['iq_signal'][:]
    i_data = iq_signal[:, 0]  # In-phase component
    q_data = iq_signal[:, 1]  # Quadrature component

# Downsample data to lighten the visualization
downsample_factor = 100 
i_data_downsampled = i_data[::downsample_factor]
q_data_downsampled = q_data[::downsample_factor]
time_axis_downsampled = np.arange(len(i_data_downsampled)) / (sampling_rate / downsample_factor)

# Create a LightningChart dashboard
dashboard = lc.Dashboard(
    theme=lc.Themes.Light, 
    columns=1,
    rows=2 
)

# 1. Plot I/Q Waveform
waveform_chart = dashboard.ChartXY(row_index=0, column_index=0)
waveform_chart.set_title(f'I/Q Signal Waveform - {modulation} Modulation, SNR: {snr} dB')

legend = waveform_chart.add_legend()
# Add I data series
i_series = waveform_chart.add_line_series()
i_series.set_name('In-phase (I)')
i_series.add(time_axis_downsampled.tolist(), i_data_downsampled.tolist())

# Add Q data series
q_series = waveform_chart.add_line_series()
q_series.set_name('Quadrature (Q)')
q_series.add(time_axis_downsampled.tolist(), q_data_downsampled.tolist())

legend.add(i_series)
legend.add(q_series)

# Configure axes
waveform_chart.get_default_x_axis().set_title('Time (s)')
waveform_chart.get_default_y_axis().set_title('Amplitude')

# 2. Constellation Plot (I vs. Q)
constellation_chart = dashboard.ChartXY(row_index=1, column_index=0)
constellation_chart.set_title(f'Constellation Plot - {modulation} Modulation')

# Add scatter series for constellation points
scatter_series = constellation_chart.add_point_series()
scatter_series.add(i_data_downsampled.tolist(), q_data_downsampled.tolist())

constellation_chart.get_default_x_axis().set_title('In-phase (I)')
constellation_chart.get_default_y_axis().set_title('Quadrature (Q)')

dashboard.open()
