import tkinter as tk
from tkinter import filedialog
import numpy as np
import scipy as sp

def get_file_path(initdir):
    # This line will create a root Tk window, but we won't show it
    root = tk.Tk()
    # This line will hide the root window
    root.withdraw()

    # Open file dialog and get the file path
    file_path = filedialog.askopenfilename(initialdir = initdir)

    # Return the selected file path
    return file_path

def get_folder_path():
    # Create a root Tk window (hidden)
    root = tk.Tk()
    root.withdraw()

    # Open folder dialog and get the folder path
    folder_path = filedialog.askdirectory()

    # Return the selected folder path
    return folder_path

def get_folder_path_str(initdir):
    # Create a root Tk window (hidden)
    root = tk.Tk()
    root.withdraw()

    # Open folder dialog and get the folder path
    folder_path = filedialog.askdirectory(initialdir = initdir)

    # Return the selected folder path
    return folder_path 

def cleanfft(ar):
    ar = np.abs(sp.fft.rfft(ar))
    ar = np.abs(ar - ar.mean())**2
    return ar

def findpeaks(ar):
    ln = len(ar)
    peaks = []
    for i in range(1, ln-1):
        if ar[i]>=ar[i-1] & ar[i]>ar[i+1]:
            peaks.append(i)
    return peaks

def stack_peaks(fac, d1, d2, d3):
    peaks_xyz = [[],[],[]]
    d_all = [d1, d2, d3]
    for i in range(0, 3):
        ar, dici = sp.signal.find_peaks(d_all[i], height = fac*np.max(d_all[i])) 
        peaks_xyz[i].append(ar)

    list1 = peaks_xyz[0][0]
    list2 = peaks_xyz[1][0]
    list3 = peaks_xyz[2][0]

    # Determine the maximum length among the lists
    max_length = max(len(list1), len(list2), len(list3))

    # Create arrays with zeros to match the maximum length
    list1 = np.pad(list1, (0, max_length - len(list1)), mode='constant')
    list2 = np.pad(list2, (0, max_length - len(list2)), mode='constant')
    list3 = np.pad(list3, (0, max_length - len(list3)), mode='constant')

    # Combine the lists into a 2D NumPy array
    data = np.column_stack((list1, list2, list3))
    return data