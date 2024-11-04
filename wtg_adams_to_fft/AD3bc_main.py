from os import listdir
import pandas as pd
import csv
from python.plotter import Plotter
from python.fft_creator import FFTCreator2
from python.csv_time_formatter import csvTimeFormatter
from python.csv_unit_formatter import csvUnitFormatter
from python.fft_mag_formatter import fftMagToZero
from python.cms_plotter import CMSPlotter2
from python.adams_table_formatter import AdamsTableFormatter


############################
# AD003B/C Data Formatting #
############################

# adams_tab_path = 'C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/adams_table/disp'
# folder_path_out = 'C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/data_exported/ad003bc/disp/'
# list_of_files = listdir(path=adams_tab_path)
# accel_nums = [5, 6, 7, 8, 9, 10]
# for file in list_of_files:
#     sim = file.split('_')[0]
#     my_adams_data = AdamsTableFormatter(filepath_in=f'adams_table/disp/{file}', sim=sim, accelerometer_nums=accel_nums, folderpath_out=folder_path_out)
#     my_adams_data.sort_data()

# ip = 'C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/data_exported/ad003bc/disp'
# op = 'C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/data_results_formatted/ad003bc/disp/'
# list_of_files = listdir(path=ip)
# for file in list_of_files:
#     csvTimeFormatter(in_path=f'data_exported/ad003bc/{file}', out_path=f'{op}{file}')


#######
# FFT #
#######

# folder_path = 'data_results_formatted/ad003bc'
# list_of_files = listdir(path=folder_path)
# for formatted_file in list_of_files:
#     my_fft = FFTCreator2(filepath=f'data_results_formatted/ad003bc/{formatted_file}', separator=',', window_start=90., window_end=100, sample_rate_hz=1.0 / 2.5e-4)

# fftMagToZero(folder_path='data_fft/ad3b')
# fftMagToZero(folder_path='data_fft/ad3c')

################
# FFT Plotting #
################

df_all = pd.DataFrame()

fft_path = 'data_fft/ad3c/acc'

# Add all the data to the dataframe
# Assign some columns in the dataframe based upon the file name, brg and time window, for future filtering
list_of_files = listdir(path=fft_path)
with pd.option_context('display.precision', 12):
    for file in list_of_files:
        df = pd.read_csv(f'{fft_path}/{file}')
        df['prefix'] = fft_path.split('/')[-1][0]
        df['sim_id'] = file.split('_')[-3].split('/')[-1]
        df['accel'] = file.split('_')[-2]
        df['component'] = file.split('_')[-1].split('.')[0]
        df_all = pd.concat([df_all, df])

    my_calculator = Plotter(input_df=df_all)
    my_calculator.plot(cmap_style='jet', f_max=100, plot=True, interactive_matplotlib=False, interactive_plotly=False, prefix='a')


# ###############
# CMS Plotting #
# ###############

# disp_folderpath = "C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/data_results_formatted/ad003bc"
# list_of_files = listdir(path=disp_folderpath)
# for file in list_of_files:
#     cms = CMSPlotter2(csv_path=f'{disp_folderpath}/{file}', start_time=91.0, end_time=92., multiplier=1000)
