import pyvista as pv
import numpy as np
import scipy as sp

import os
import re

from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from create_pvd import *



def file_list_compiler(directory_path):
    """
    Compiles a list of files matching a given pattern within a folder
    
    Args:
        directory_path: absolute path to the directory containing the .vtu files

    Returns:
        file_list: a list containg strings with the absolute paths to all .vtu files within the folder

    """
    file_list = []
    for file_path in directory_path.iterdir():
        # Check if it's a file with a ".vtu" extension and matches the pattern
        if file_path.is_file() and file_path.suffix == '.vtu':
            file_list.append(file_path)

    return file_list


def read_mag_pv(filepath):

    grid = pv.read(filepath)
    
    magnetization = grid.point_data['m']
    
    return magnetization


def natural_key(path):
    """Define key for sorting Path objects that include digits naturally in their filenames."""
    # Convert Path to string and extract the filename
    string = str(path.name)
    return [int(text) if text.isdigit() else text for text in re.split('(\d+)', string)]


#parallelized call of vtu reader
#pyvista is already efficient as is but why not
def process_files(sorted_file_list):
    """Use ThreadPoolExecutor to read and process files concurrently"""

    N_logical_cores = 4 #can be adjusted depending on the machine, uses LOGICAL cores i.e threads.

    with ProcessPoolExecutor(max_workers=N_logical_cores) as executor:
        results = list(executor.map(read_mag_pv, sorted_file_list))

    #Print the shapes for debugging purposes
    print("Results shape:", np.shape(results))
    # Convert list of arrays into a 3D numpy array (stack along the third dimension)
    data = np.stack(results, axis=-1)  
    #Ensure the dimensionality matches your needs
    print("Data shape: ", np.shape(data))
    
    return data

def save_fft_data(mag_data, freqs, original_grid, output_dir):
    """
    Saves FFT data as .vtu files
    
    Args:
        mag_data: FFT data array
        freqs: frequency array
        original_grid: template grid from original data
        output_dir: Path object pointing to output directory
    """
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    freqs = freqs[freqs <= 20e9]

    # Convert frequencies to GHz
    freqs_GHz = freqs * 1e-9

    # For each frequency point, create a .vtu file
    for i, freq in enumerate(freqs_GHz):
        # Create a copy of the original grid
        grid = original_grid.copy()
        
        # Add the FFT data for this frequency
        grid.point_data['fft'] = mag_data[:, :, i]
        
        # Save to file with frequency in the filename
        filename = f'fft_{freq:.2f}GHz.vtu'
        grid.save(output_dir / filename)

    pass

# Modify your main code by adding:
def main():
    path_sim = input("Give FULL simulation path: \n")
    time_step = int(input("Give the time step length of the .vtu files in ps, typical values are 10, 20, 50:\n")) #in ps
    
    path_sim = Path(path_sim)
    file_list = sorted(file_list_compiler(path_sim), key=natural_key)

    # Store the first grid as template
    template_grid = pv.read(file_list[0])
    
    mag_data = process_files(file_list)
    
    freqs = np.fft.rfftfreq(mag_data.shape[-1], 1e-12*time_step)
    
    mag_data = np.abs(sp.fft.rfft(mag_data, axis=-1))**2
    #mag_data = np.average(mag_data, axis=0)

    # Create /fft directory in the simulation path
    fft_dir = path_sim / 'fft'
    
    # Save the FFT data
    save_fft_data(mag_data, freqs, template_grid, fft_dir)

    print(f"FFT data saved to {fft_dir}")

    create_vtk_collection(fft_dir, freqs)

if __name__ == "__main__":
    main()