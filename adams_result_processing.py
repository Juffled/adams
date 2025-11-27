from os import listdir
import numpy as np
import pandas as pd
from python.fft_creator import FFTCreator
from python.romax_data_formatter import RomaxData
from python.fft_plotter import  FFTPlotter
from python.traj_plotter import TrajectoryPlotter


#############
# Variables #
#############

adams_timestep = 5e-5
fft_window_start = 2.5
factors = 5  # Tuner for getting FFT frequency to match, probably leave at 5
rotating_speed_rpm = 5000
romaxdt_max_order = 64  # max order for romaxDT magnitude export, 2x spline teeth

factor_switch = True  # switch to choose between min_magnitude/floor value or floor factor
min_magnitude_factor = 0.01 # the floor value as a factor of the maximum magnitude e.g. 0.01 * max value
min_magnitude = 2  # the floor value for RomaxDT inputs

fft_plot_max_freq = 5400 # set y axis of fft
fft_plot_colourmap = 'YlOrRd'  # https://matplotlib.org/stable/gallery/color/colormap_reference.html

trajectory_start_time = 2.5  # start time for trajectory plotting
num_trajectory_rotations = 5  # number of rotations to plot

##############################################################
################### LEAVE BELOW THIS ALONE ###################
##############################################################

#########
# Calcs #
#########

rotating_hz = rotating_speed_rpm / 60
rotation_time = 1 / rotating_hz
freq_step = factors * rotating_hz /1000
fft_window_end = np.round(fft_window_start + freq_step,2)
trajectory_end_time = trajectory_start_time + rotation_time * num_trajectory_rotations

#########################################################
# Remove the # at the start of each extracted data file #
#########################################################

list_of_files = listdir(path='3_data_results_extracted')

for result_file in list_of_files:
    fp_in = f'3_data_results_extracted/{result_file}'
    fp_out = f'4_data_results_formatted/formatted_{result_file}'
    with open(fp_in, 'r') as infile, \
        open(fp_out, 'w') as outfile:
        data = infile.read()
        data = data.replace("# ", "")
        outfile.write(data)

#######
# FFT #
#######

list_of_files = listdir(path='4_data_results_formatted')
for formatted_file in list_of_files:
    my_fft = FFTCreator(filepath=f'4_data_results_formatted/{formatted_file}', separator='    ')
    my_fft.fft(window_start=fft_window_start, window_end=fft_window_end, sample_rate_hz=1.0 / adams_timestep)

###############
# FFT Plotter #
###############

df_all = pd.DataFrame()

fft_path = '5_data_fft/'

# Add all the data to the dataframe
# Assign some columns in the dataframe based upon the file name, brg and time window, for future filtering
list_of_files = listdir(path=fft_path)
for file in list_of_files:
    sim = file.split('_')[0]
    component = file.split('_')[-1].split('.')[0]
    df = pd.read_csv(f'{fft_path}/{file}')
    df['sim_id'] = sim
    df['component'] = component
    df_all = pd.concat([df_all, df])

my_calculator = FFTPlotter(input_df=df_all)
my_calculator.plot(cmap_style=fft_plot_colourmap, freq_max=fft_plot_max_freq) # z_max = 200 << put this in the call if you want to limit the z axis

##############
# Romax Data #
##############
fft_path = '5_data_fft/'
list_of_files = listdir(path='5_data_fft')
all_data = pd.DataFrame()
for fft_file in list_of_files:
    sim = fft_file.split('_')[0]
    component = fft_file.split('_')[-1].split('.')[0]
    df = pd.read_csv(f'{fft_path}/{fft_file}')
    df['sim_id'] = sim
    df['component'] = component
    all_data = pd.concat([all_data, df])

my_romax_data = RomaxData(dataframe=all_data, speed_rpm = rotating_speed_rpm, ignore_orders=[19, 38, 57],
                          max_order=romaxdt_max_order, factor = factor_switch, min_magnitude_factor=min_magnitude_factor, min_magnitude=min_magnitude)

#####################
# Spline Trajectory #
#####################

list_of_files = listdir(path='4_data_results_formatted')
for formatted_file in list_of_files:
    my_trajectory = TrajectoryPlotter(filepath=f'4_data_results_formatted/{formatted_file}', separator='    ')
    my_trajectory.plot(start_time=trajectory_start_time, end_time=trajectory_end_time)
