import lightningchart as lc
import numpy as np
import h5py

lc.set_license('my-license-key')

file_path = 'Dataset/rf_dataset.h5'
sample_key = 'sample_0'

with h5py.File(file_path, 'r') as f:
    amplitudes = []
    # Access the sample group and attributes
    sample_group = f[sample_key]
    modulation = sample_group.attrs['modulation']
    snr = sample_group.attrs['snr']
    sampling_rate = sample_group.attrs['sampling_rate']

    # Extract IQ signal
    iq_signal = sample_group['iq_signal'][:]
    complex_signal = iq_signal[:, 0] + 1j * iq_signal[:, 1]  # Combine I/Q as complex signal

    fs = sampling_rate
    symbol_period = int(sampling_rate / (fs / 1000)) 
    i_data = iq_signal[:, 0]
    q_data = iq_signal[:, 1]

# # Calculate histogram
counts_In_phase, bin_edges_In_phase = np.histogram(i_data, bins=100)
counts_Quadrature, bin_Quadrature = np.histogram(q_data, bins=100)

# Preparing data
bar_data_In_phase = [
    {"category": f"{bin_edges_In_phase[i]:.2f}–{bin_edges_In_phase[i+1]:.2f}", "value": int(count)}
    for i, count in enumerate(counts_In_phase)
]

bar_data_Quadrature = [
    {"category": f"{bin_Quadrature[i]:.2f}–{bin_Quadrature[i+1]:.2f}", "value": int(count)}
    for i, count in enumerate(counts_Quadrature)
]

dashboard = lc.Dashboard(
    columns=2,
    rows=1,
    theme=lc.Themes.Light,    
)


chart_In_phase = dashboard.BarChart(
    row_index=0,
    column_index=0
)
chart_In_phase.set_title('In-phase (I) Amplitude Distribution')
chart_In_phase.set_data(bar_data_In_phase)
chart_In_phase.set_sorting('disabled')
chart_In_phase.set_bars_color(lc.Color('cyan'))

chart_Quadrature = dashboard.BarChart(
    row_index=0,
    column_index=1
)
chart_Quadrature.set_title('Quadrature (Q) Amplitude Distribution')
chart_Quadrature.set_data(bar_data_Quadrature)
chart_Quadrature.set_sorting('disabled')
chart_Quadrature.set_bars_color(lc.Color(255, 178, 102))

dashboard.open()