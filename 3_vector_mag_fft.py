#Script for the Fourier Transform on the average per point

from magnumpi import *
import numpy as np
import scipy as sp

import os
import re

from pathlib import Path

from utils import *
from read_vtu import *


def do_vfft(data, stepfreq, depin):
    """
    Performs the vector FFT.

    Takes in the data array and performs the FFT along the time axis and then averages for every spatial component.

    Args:
        data (ndarray): array containg the magnetization data in 4D for every point.
        stepfreq (int): parameter for writing the frequencies
        depin (str): directory path for writing the necessary files
    """
    #shape0 is the points
    #shape1 is the 3dims
    #shape2 is the time points

    freqs = np.fft.rfftfreq(data.shape[-1], 1e-12*stepfreq)
    data = np.abs(sp.fft.rfft(data))**2
    data = np.average(data, axis = 0)

    output_dir = Path(depin) / "images"
    output_dir.mkdir(parents=True, exist_ok=True)


    np.savetxt(output_dir / "PSD_freq.txt", freqs)
    np.savetxt(output_dir / "PSD_data.txt", data.T)


    print("\nPSD completed")

    return None

def init_path(depin):
    """
    Initializes the path to the directory.

    Formats the given path to a directory to be passed down in the appropriate format.

    Args:
        depin (string): absolute path to simulation directory
    Returns:
        directory_path (Path): formatted path
        stepfreq (int): parameter for generating the right frequency array
    """

    os.makedirs(depin+"/images", exist_ok=True)
    print("\nReading data from: \n"+depin)

    directory_path = Path(depin)

    #stepfreq = int(input("\nSet the step size for the fields in ps: "))
    stepfreq = 10
    print("\nfftfreq resolution will be: ", 1e-12*stepfreq)

    return directory_path, stepfreq

def v_fft(depin):
    """
    Core function to perform vector fft on given data.

    This function calls a set of functions to perform the vector fft for a given simulation.

    Args:
        depin (string): absolute path to the simulation directory containing .vtu files
    """

    directory_path, stepfreq = init_path(depin)

    file_list = file_list_compiler(directory_path)

    file_list = sorted(file_list, key=natural_key)

    data_real = process_files(file_list)

    print("After processed and read: ", np.shape(data_real))

    do_vfft(data_real, stepfreq, depin)

    pass

if __name__ == '__main__' :

    path = input("Give the absolute path to the simulation data folder: \n")

    t0 = time.time()

    v_fft(path)

    delt = int(time.time() - t0)
    f_t = time_f(delt)
    print("Time elapsed: ", f_t)
    