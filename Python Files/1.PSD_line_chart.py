from scipy.signal import welch
import lightningchart as lc
import numpy as np
import h5py

lc.set_license('my-license-key')

file_path = 'Dataset/rf_dataset.h5'
sample_key = 'sample_0'

# Open the HDF5 file
with h5py.File(file_path, 'r') as f:
    # Access the sample group and attributes
    sample_group = f[sample_key]
    modulation = sample_group.attrs['modulation']
    snr = sample_group.attrs['snr']
    sampling_rate = sample_group.attrs['sampling_rate']
    
    # Extract IQ signal
    iq_signal = sample_group['iq_signal'][:]
    complex_signal = iq_signal[:, 0] + 1j * iq_signal[:, 1]  # Combine I/Q as complex signal

    # Compute Power Spectral Density (PSD) using Welch's method
    fs = sampling_rate
    freqs, psd = welch(complex_signal, fs=fs, nperseg=1024)


chart = lc.ChartXY(
    theme=lc.Themes.Light,
    title=f'Power Spectral Density - {modulation} Modulation, SNR: {snr} dB',
)

line_series = chart.add_line_series()
line_series.add(freqs, psd)

x_axis = chart.get_default_x_axis().set_title('Frequency (Hz)')
chart.get_default_y_axis().set_title('Power Spectral Density (dB/Hz)')

band = x_axis.add_band()
band.set_value_start(-25000)
band.set_value_end(25000)
band.set_color(lc.Color(255, 0, 0, 128))

chart.open()
