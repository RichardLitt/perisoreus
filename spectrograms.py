import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

import matplotlib
import scipy

print(f"NumPy version: {np.__version__}")
print(f"Matplotlib version: {matplotlib.__version__}")
print(f"SciPy version: {scipy.__version__}")

# Load your audio file and process it to create a spectrogram
file = '558679851.wav'  # specify your audio file
fs, data = wavfile.read(file)  # Load the audio file

# Clip the audio between 1 second and 4 seconds
start_time = 1  # Start at 1 second
end_time = 4    # End at 4 seconds
data = data[int(fs * start_time):int(fs * end_time)]  # Trim the data to the desired range

# Increase nperseg and noverlap for better resolution
nperseg = 2048  # Increase for better frequency resolution
noverlap = 1524  # Set high overlap to maintain time resolution

# Generate spectrogram data
f, t, Zxx = signal.stft(data, fs, window='bartlett', nperseg=nperseg, noverlap=noverlap)
Sxx = np.abs(Zxx)  # Use the magnitude of the STFT

# Mask frequencies below 500 Hz by setting them to NaN
min_freq = 500  # Minimum frequency to display (ignore frequencies below 500 Hz)
Sxx[f < min_freq, :] = np.nan  # Set values below 500 Hz to NaN

# Limit the frequency to a maximum of 8000 Hz (8 kHz)
max_freq = 8000  # 8 kHz
f_limit_idx = np.where(f <= max_freq)[0]  # Indices of frequencies <= 8000 Hz

# Create the plot with specific size in inches (500px x 1500px at 100 DPI)
dpi = 100
fig, ax = plt.subplots(figsize=(1000 / dpi, 400 / dpi), dpi=dpi)

# Display the spectrogram
ax.imshow(
    Sxx[f_limit_idx, :],  # Display only frequencies <= 8000 Hz
    aspect='auto',
    origin='lower',
    extent=[t.min(), t.max(), 0, f[f_limit_idx].max() / 1000],  # Scale frequency to kHz, start y-axis at 0
    cmap='Greys',
    vmax=np.nanmax(Sxx[f_limit_idx, :]) * 0.3  # Adjust vmax to improve visualization
)

# Set axis labels and title
ax.set_ylabel('Frequency (kHz)')
ax.set_xlabel('Time (s)')

# Adjust layout for clarity
plt.tight_layout()

# Save the figure as a PNG file
plt.savefig('spectrogram.png', dpi=dpi, bbox_inches='tight')

# Display the plot
plt.show()
