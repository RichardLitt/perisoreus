import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

import matplotlib
import scipy

print(f"NumPy version: {np.__version__}")
print(f"Matplotlib version: {matplotlib.__version__}")
print(f"SciPy version: {scipy.__version__}")

def spectrogram(file_path, start_time=0, end_time=5, min_freq = 0, max_freq = 8000):

    # Load your audio file and process it to create a spectrogram
    fs, data = wavfile.read(file_path)  # Load the audio file
    
    # Clip the audio between start and end times
    data = data[int(fs * start_time):int(fs * end_time)]  # Trim the data to the desired range
    
    # Increase nperseg and noverlap for better resolution
    nperseg = 1024  # Increase for better frequency resolution
    noverlap = 1023  # Set high overlap to maintain time resolution
    
    # Generate spectrogram data
    f, t, Zxx = signal.stft(data, fs, window='bartlett', nperseg=nperseg, noverlap=noverlap)
    Sxx = np.abs(Zxx)  # Use the magnitude of the STFT
    
    # Mask frequencies below 500 Hz by setting them to NaN
    Sxx[f < min_freq, :] = np.nan  # Set values below 500 Hz to NaN

    # Limit the frequency to a maximum of 8000 Hz (8 kHz)
    f_limit_idx = np.where(f <= max_freq)[0]  # Indices of frequencies <= 8000 Hz

    return Sxx, f_limit_idx, f, t

# Create the plot with specific size in inches (500px x 1500px at 100 DPI)
dpi = 100
fig, ax = plt.subplots(1,2, figsize=(900 / dpi, 300 / dpi), dpi=dpi, sharey=True)

# Tailored time bounds
time_bounds = {0:[1,3.5],
               1:[0,2.5]}

# Tailored contrast for visual balance
contrasts = {0:0.15,
             1:0.35}

for i, f_path in enumerate([r"C:\Users\DBetchkal\CODE\GITHUB\perisoreus\558679851.wav", r"C:\Users\DBetchkal\CODE\GITHUB\perisoreus\585940541.wav"]):

    Sxx, f_limit_idx, f, t = spectrogram(f_path, 
                                         start_time=time_bounds[i][0], 
                                         end_time=time_bounds[i][1])
    
    # Display the spectrogram
    ax[i].imshow(
        Sxx[f_limit_idx, :],  # Display only frequencies <= 8000 Hz
        aspect='auto',
        origin='lower',
        extent=[t.min(), t.max(), 0, f[f_limit_idx].max() / 1000],  # Scale frequency to kHz, start y-axis at 0
        cmap='Greys',
        vmax=np.nanmax(Sxx[f_limit_idx, :]) * contrasts[i]  # Adjust vmax to improve visualization
    )

    # Add a time label to both subplots
    ax[i].set_xlabel('Time (s)', labelpad=10)

# Add a frequency lable to the leftmost subplot
ax[0].set_ylabel('Frequency (kHz)', labelpad=15)

# Adjust layout for clarity
plt.tight_layout()

# Save the figure as a PNG file
plt.savefig('spectrogram.png', dpi=dpi, bbox_inches='tight')

# Display the plot
plt.show()

