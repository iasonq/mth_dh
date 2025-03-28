# soldes
# ifft + superimposing, only requires fft to be done
from magnumpi import *
import numpy as np

import os
import re

from pathlib import Path

from utils import *
from read_vtu import *


def simulation_inv_super(path, stepsize, snapshot_list, boost=1):
    """
    Performs the inverse FFT (iFFT) on selected snapshots from a set of FFT-generated .vtu files,
    superimposes the result on the original data, and saves the final output.

    Args:
        path (str): Absolute path to the folder containing the simulation data.
        stepsize (int): The time step size for the fields in picoseconds.
        snapshot_list (list of int): List of snapshot indices to process.
        boost (int, optional): A multiplier to enhance the signal during superimposition. Defaults to 1.

    Returns:
        pass
    """
    t0 = time.time()
    directory = Path(path)

    print("Reading files from: ", directory)

    # Compile a list of .vtu files
    print("\nCompiling filenames")
    file_list = file_list_compiler(directory)

    # Sort the file list based on the extracted numbers
    print("\nSorting the FFT list")
    sorted_file_list = sorted(file_list, key=natural_key)

    print("\nReading the functions data")
    data_real = process_files(sorted_file_list)

    # Initialize FFT data array
    print("\nPerforming FFT, along last axis (time axis)")
    data_fft = np.fft.rfft(data_real)
    data_real = None

    # Read the first file to determine the data shape
    m0 = read_function(Path(path) / "fields_0.vtu")
    ms = read_function(Path(path) / "fields_0.vtu")

    sl = len(sorted_file_list)
    t = np.arange(0, sl) * 1e-12 * stepsize

    print("\nFFT data reading completed")

    for sn_iter in snapshot_list:
        data_fft_sn = data_fft.copy()

        # Isolate the selected frequency
        print(f"\nIsolating frequency for snapshot: {sn_iter}")
        data_fft_sn[:, :, 0:sn_iter] = 0
        data_fft_sn[:, :, sn_iter+1:] = 0

        # Perform iFFT
        print("\nPerforming iFFT")
        data_ifft = np.fft.irfft(data_fft_sn)
        data_fft_sn = None
        
        # Superimpose and save the results
        output_dir = Path(path) / f"superimposed_{sn_iter}b{boost}_proper"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "super.pvd"
        
        print(f"\nSuperimposing and writing data to: {output_path}")
        f = File(str(output_path))
        for i in range(sl):
            ms.dat.data[:, :] = m0.dat.data + data_ifft[:, :, i] * boost
            f.write(ms, time=t[i])
            print_progress_bar(i + 1, len(t), t0)

        data_ifft = None

        delt = int(time.time() - t0)
        f_t = time_f(delt)
        print(f"\nSuperimposing for snapshot {sn_iter} completed in {f_t}")

    print("All snapshots processed")

# MAIN EXECUTION
if __name__ == "__main__":
    print("Initializing parameters")
    path = input('Give the absolute path to the simulation directory: \n')
    stepsize = int(input("Input stepsize, typical values are 10, 20, 50: "))
    print("\nfftfreq resolution will be: ", 1e-12 * stepsize)

    snapshot_list = []
    print("\nReading snapshots")
    print("0 to exit, avoid the last frame as input.")
    while True:
        sn = int(input("Snapshot: "))
        if sn != 0:
            snapshot_list.append(sn)
        else:
            break

    boost = int(input("Enter a boost value, default is 1: "))
    simulation_inv_super(path, stepsize, snapshot_list, boost)
