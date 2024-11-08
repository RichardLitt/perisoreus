import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

import matplotlib
import scipy

# Print library versions
print(f"NumPy version: {np.__version__}")
print(f"Matplotlib version: {matplotlib.__version__}")
print(f"SciPy version: {scipy.__version__}")

# Function to generate spectrogram data
def spectrogram(file_path, start_time=0, end_time=5, min_freq=0, max_freq=8000, nperseg=1024, noverlap=1023):
    # Load the audio file
    fs, data = wavfile.read(file_path)
    
    # Clip the audio between start and end times
    data = data[int(fs * start_time):int(fs * end_time)]
    
    # Generate the spectrogram data using STFT
    f, t, Zxx = signal.stft(data, fs, window='bartlett', nperseg=nperseg, noverlap=noverlap)
    Sxx = np.abs(Zxx)  # Use the magnitude of the STFT

    # Mask frequencies below min_freq by setting them to NaN
    Sxx[f < min_freq, :] = np.nan  # Set values below min_freq to NaN

    # Limit the frequency to a maximum of max_freq
    f_limit_idx = np.where(f <= max_freq)[0]  # Indices of frequencies <= max_freq
    
    return Sxx, f_limit_idx, f, t

# Function to generate and display a single spectrogram
def generate_spectrogram(file_path, start_time=0, end_time=5, min_freq=0, max_freq=8000, nperseg=1024, noverlap=1023, contrast=0.3):
    Sxx, f_limit_idx, f, t = spectrogram(file_path, start_time, end_time, min_freq, max_freq, nperseg, noverlap)
    
    # Create the plot with specified size
    dpi = 300
    fig, ax = plt.subplots(figsize=(10, 4), dpi=dpi)

    # Display the spectrogram
    ax.imshow(
        Sxx[f_limit_idx, :],  # Display only frequencies <= max_freq
        aspect='auto',
        origin='lower',
        extent=[t.min(), t.max(), 0, f[f_limit_idx].max() / 1000],  # Scale frequency to kHz
        cmap='Greys',
        vmax=np.nanmax(Sxx[f_limit_idx, :]) * contrast  # Adjust contrast for visualization
    )

    # Set axis labels
    ax.set_ylabel('Frequency (kHz)')
    ax.set_xlabel('Time (s)')

    # Adjust layout for clarity
    plt.tight_layout()

    # Save the figure as a PNG file
    output_file = file_path.replace('.wav', '_spectrogram.png')
    plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
    plt.show()

# Function to create side-by-side spectrograms for a list of files
def generate_multiple_spectrograms(file_paths, time_bounds, contrasts):
    # Create the plot with specific size and multiple subplots
    dpi = 300
    fig, ax = plt.subplots(1, len(file_paths), figsize=(9, 3), dpi=dpi, sharey=True)

    for i, f_path in enumerate(file_paths):
        # Generate spectrogram data for each file
        Sxx, f_limit_idx, f, t = spectrogram(f_path, 
                                             start_time=time_bounds[i][0], 
                                             end_time=time_bounds[i][1])

        # Display the spectrogram
        ax[i].imshow(
            Sxx[f_limit_idx, :],  # Display only frequencies <= max_freq
            aspect='auto',
            origin='lower',
            extent=[t.min(), t.max(), 0, f[f_limit_idx].max() / 1000],  # Scale frequency to kHz
            cmap='Greys',
            vmax=np.nanmax(Sxx[f_limit_idx, :]) * contrasts[i]  # Adjust contrast for visualization
        )

        # Add labels
        ax[i].set_xlabel(f'Time (s)\nLocation: {"Vermont" if i == 0 else "Oregon"}', labelpad=10)

    # Add a frequency label to the leftmost subplot
    ax[0].set_ylabel('Frequency (kHz)', labelpad=15)

    # Adjust layout for clarity
    plt.tight_layout()

    # Save the figure as a PNG file
    plt.savefig('Figure_3.png', dpi=dpi, bbox_inches='tight')
    plt.show()

# Generate a spectrogram for a single file
generate_spectrogram('585940541.wav', start_time=0, end_time=3, min_freq=1000, max_freq=8000, nperseg=2048, noverlap=1524, contrast=0.3)

# Generate side-by-side spectrograms for multiple files
file_paths = ["558679851.wav", "585940541.wav"]
time_bounds = {0: [1, 3.5], 1: [0, 2.5]}
contrasts = {0: 0.15, 1: 0.35}
generate_multiple_spectrograms(file_paths, time_bounds, contrasts)
