from os import listdir
import pandas as pd
import csv
from python.plotter import Plotter
from python.fft_creator import FFTCreator
from python.csv_time_formatter import csvTimeFormatter
from python.csv_unit_formatter import csvUnitFormatter
from python.fft_mag_formatter import fftMagToZero
from python.cms_plotter import CMSPlotter
from python.adams_table_formatter import AdamsTableFormatter


#########################################################
# Remove the # at the start of each extracted data file #
#########################################################

# list_of_files = listdir(path='data_results_extracted')

# for result_file in list_of_files:
#     fp_in = f'data_results_extracted/{result_file}'
#     fp_out = f'data_results_formatted/formatted_{result_file}'
#     with open(fp_in, 'r') as infile, \
#         open(fp_out, 'w') as outfile:
#         data = infile.read()
#         data = data.replace("# ", "")
#         outfile.write(data)

##########################
# AD003A time formatting #
##########################

# ip = 'C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/data_exported/AD003A_CMS_rated_accel.csv'
# op = 'C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/data_results_formatted/ad003a/ad003a_exported.csv'
# a = csvTimeFormatter(in_path=ip, out_path=op)

##########################
# AD003A Unit formatting #
##########################

# ip = 'C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/data_exported/AD003A_rated_CMS_disp.csv'
# op = 'C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/data_results_formatted/ad003a/AD003A_rated_CMS_disp_um.csv'
# a = csvUnitFormatter(in_path=ip, out_path=op, multiplier=1000.)

##############
# AD003A FFT #
##############

# folder_path = 'data_results_formatted/ad003a'
# list_of_files = listdir(path=folder_path)
# for formatted_file in list_of_files:
#     my_fft = FFTCreator(filepath=f'data_results_formatted/ad003a/{formatted_file}', separator=',')
#     my_fft.fft(window_start=120., window_end=121, sample_rate_hz=1.0 / 2.5e-4)
# fftMagToZero(folder_path=folder_path)

################
# FFT Plotting #
################

# df_all = pd.DataFrame()

# fft_path = 'data_fft/ad003a_rated/acc'

# # Add all the data to the dataframe
# # Assign some columns in the dataframe based upon the file name, brg and time window, for future filtering
# list_of_files = listdir(path=fft_path)
# for file in list_of_files:
#     sim = file.split('_')[-5].split('/')[-1] + "_" + file.split('_')[-4]
#     accel = file.split('_')[2]
#     component = file.split('_')[3]
#     prefix = fft_path.split('/')[-1][0]
#     df = pd.read_csv(f'{fft_path}/{file}')
#     df['sim_id'] = sim
#     df['accel'] = accel
#     df['component'] = component
#     df_all = pd.concat([df_all, df])

# my_calculator = Plotter(input_df=df_all)
# my_calculator.plot(cmap_style='jet', f_max=1000, plot=False, interactive_matplotlib=True, interactive_plotly=True, prefix=prefix)


################
# CMS Plotting #
################

# disp_filepath = "C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/data_results_formatted/ad003a/AD003A_rated_CMS_disp.csv"
# cms = CMSPlotter(csv_path=disp_filepath, start_time=122, end_time=122.1)
# cms.plot_all()