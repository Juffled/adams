from os import listdir
import pandas as pd
import csv
from python.sound_power_calculator import SoundPowerCalculator
from python.fft_creator import FFTCreator


# Remove the # at the start of each extracted data file
list_of_files = listdir(path='data_results_extracted')

for result_file in list_of_files:
    fp_in = f'data_results_extracted/{result_file}'
    fp_out = f'data_results_formatted/formatted_{result_file}'
    with open(fp_in, 'r') as infile, \
        open(fp_out, 'w') as outfile:
        data = infile.read()
        data = data.replace("# ", "")
        outfile.write(data)

# create the fft data for each component in each direction for F and V
list_of_files = listdir(path='data_results_formatted')
for formatted_file in list_of_files:
    my_fft = FFTCreator(filepath=f'data_results_formatted\\{formatted_file}')
    my_fft.fft(window_start=[1.12, 3.52, 5.68], window_end=[1.36, 3.76, 5.92], sample_rate_hz=2000)

#########################
# Calculate Sound Power #
#########################

# open the sim map and get the data into a dataframe
with open('simulation_map.csv', mode='r') as infile:
    dict_reader = csv.DictReader(infile)
    sim_map = list(dict_reader)

df_all = pd.DataFrame()

# Add all the data to the dataframe
# Assign some columns in the dataframe based upon the file name, brg and time window, for future filtering
list_of_files = listdir(path='data_fft')
for file in list_of_files:
    sim = file.split('_')[0]
    window = file.split('_')[1]
    brg = file.split('_')[2]
    component = file.split('_')[3].split('.')[0]
    df = pd.read_csv(f'data_fft/{file}')
    df['sim_id'] = sim
    df['window'] = window
    df['brg'] = brg
    df['component'] = component
    df_all = pd.concat([df_all, df])

my_calculator = SoundPowerCalculator(input_df=df_all, sim_map=sim_map)

############
# Checking #
############
# Export all the different dataframes as .csv for checking
my_calculator.check_data_csv()

############
# Plotting #
############
# https://seaborn.pydata.org/tutorial/color_palettes.html
# and here
# https://matplotlib.org/stable/users/explain/colors/colormaps.html
# for styles
# v_max is the colourbar max
# f_max is the frequency max you wan tto plot (y axis)
my_calculator.plot(cmap_style='viridis', f_max=500, v_max=None)
