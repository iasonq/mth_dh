### VARIOUS FUNCTIONS FOR EVALUATIONS ###

#PROGRESSBAR
import time
import sys

def print_progress_bar(iteration, total, t0, bar_length=50):
    """Prints a progress bar in th terminal"""
    progress = (iteration / total)
    arrow = '-' * int(round(progress * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    t = time.time()


    sys.stdout.write('\r[{}] {}% {} {}'.format(arrow + spaces, 
                                                            int(round(progress * 100)), 
                                                            str(iteration)+"/"+str(total), 
                                                            time_f(int(t-t0))
                                                                ) )
    sys.stdout.flush()

    pass

#TIME FORMATTER
def time_f(t):
    """Formats time in human readable form"""
    h, r = divmod(t, 3600)  # 3600 seconds in an hour
    m, s = divmod(r, 60)  # 60 seconds in a minute
    t_f = f"{h:02d}:{m:02d}:{s:02d}"  #use f-string formatting
    return t_f    

#SORTER
import re
def natural_key(path):
    """Define key for sorting Path objects that include digits naturally in their filenames."""
    # Convert Path to string and extract the filename
    string = str(path.name)
    return [int(text) if text.isdigit() else text for text in re.split('(\d+)', string)]


#FILEPATH GUI
import tkinter as tk
from tkinter import filedialog

def get_file_path():
    # This line will create a root Tk window, but we won't show it
    root = tk.Tk()
    # This line will hide the root window
    root.withdraw()

    # Open file dialog and get the file path
    file_path = filedialog.askopenfilename()

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

