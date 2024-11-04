# Python Code
import time
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import numpy as np


start_time = time.time()

dt = 5e-5  # Data sampling frequency, assumes constant
SETTLING_TIME = 3
FILEPATH = r'KR-000128-XL-003-A Adams Results Bearing Accelerations.xlsx'

# read bearing accleration data into python dataframe

list_of_sheet_combos = [['SIM4_inner', 'SIM7_inner'], ['SIM5_inner', 'SIM8_inner'], ['SIM6_inner', 'SIM9_inner']]
list_of_bearings = ['1', '2', '3', '3a', '4', '5', '6', '7']
list_of_directions = ['X', 'Y', 'Z']

#               1               2                   3                   3a                  4                   5                   6                       7
#               X, Y, Z         X, Y, Z             X, Y, Z             X, Y, Z             X, Y, Z             X, Y, Z             X, Y, Z                 X, Y, Z
# list_of_vmax = [0.6, 1.2, 0.7,  0.7, 0.7, 0.2,      1, 0.5, 0.4,        0.7, 0.7, 0.2,      0.5, 0.7, 0.4,      0.25, 2, 0.7,       0.5, 0.5, 0.4,          0.5, 1.6, 1.3,
#                 1.5, 2, 1,      0.7, 0.4, 0.8,      0.2, 0.2, 0.7,      1, 0.4, 0.7,        1, 1.3, 2.5,        1, 0.5, 0.8,        0.5, 0.4, 3,            0.4, 0.5, 1,
#                 2, 2, 2,        2, 2, 2,            2, 2, 2,            2, 2, 2,            2, 2, 2,            2, 2, 2,            2, 2, 2,                2, 2, 2,
#                 ]

# list_of_vmax = [0.3, 1.2, 0.7,  0.7, 0.7, 0.2,      1, 0.5, 0.4,        0.7, 0.7, 0.2,      0.5, 0.7, 0.4,      0.25, 2, 0.7,       0.5, 0.5, 0.4,          0.5, 1.6, 1.3,
#                 1.5, 2, 1,      0.7, 0.4, 0.8,      0.2, 0.2, 0.7,      1, 0.4, 0.7,        1, 1.3, 2.5,        1, 0.5, 0.8,        0.5, 0.4, 3,            0.4, 0.5, 1,
#                 2, 2, 2,        2, 2, 2,            2, 2, 2,            2, 2, 2,            2, 2, 2,            2, 2, 2,            2, 2, 2,                2, 2, 2,
#                 ]

list_of_vmax = [2, 5, 1.5,      3, 5, 2,      1, 0.8, 0.4,        5, 5, 2,      2.5, 6, 2,      4, 2, 2,       0.2, 0.3, 0.4,          2, 10, 3,
                14, 10, 20,      10, 7, 5,      1.5, 2.5, 0.7,      5, 5, 3,        3, 5, 7,        15, 5, 6,        1.5, 1, 4,            0.2, 0.1, 1,
                20, 20, 20,        20, 20, 20,            20, 20, 20,            20, 20, 20,            20, 20, 20,            20, 20, 20,            20, 20, 20,                20, 20, 20,
                ]

i = 0

for sheet_combo in list_of_sheet_combos:
    s1 = sheet_combo[0]
    s2 = sheet_combo[1]

    data_1_all = pd.read_excel(FILEPATH, sheet_name=s1)
    data_1_all = data_1_all.astype(float)
    data_1_time_filter = data_1_all[data_1_all['Time'] >= SETTLING_TIME]

    # read bearing acceleration data into python dataframe
    data_2_all = pd.read_excel(FILEPATH, sheet_name=s2)
    data_2_all = data_2_all.astype(float)
    data_2_time_filter = data_2_all[data_2_all['Time'] >= SETTLING_TIME]

    for bearing in list_of_bearings:
        if bearing == '3a':
            b1 = '2'
        else:
            b1 = bearing
        b2 = bearing
        for direction in list_of_directions:
            d = direction

            # select the data from the dataframe and flatten into a vector
            data_1_selected = data_1_time_filter[f"{s1}: BRG{b1} - {d}"]
            data_1_timesignal = data_1_selected.values.flatten()

            # select the data from the dataframe and flatten into a vector
            data_2_selected = data_2_time_filter[f"{s2}: BRG{b2} - {d}"]
            data_2_timesignal = data_2_selected.values.flatten()

            fSample = 1.0 / dt  # calc sampling frequency

            # plot spectogram
            plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [1, 1]})
            plt.subplot(1, 2, 1)
            f, ts, Sxx = signal.spectrogram(data_1_timesignal, fSample, window=("tukey", 0.05))
            plt.pcolormesh(ts, f, Sxx, cmap='jet', vmin=0, vmax=list_of_vmax[i])
            plt.colorbar().set_label(label='a label',size=10)
            plt.ylabel('Frequency [Hz]')
            plt.xlabel('Time [sec]')
            plt.ylim((0.0, 6333))
            plt.title(s1)

            plt.subplot(1, 2, 2)
            f, ts, Sxx = signal.spectrogram(data_2_timesignal, fSample, window=("tukey", 0.05))
            plt.pcolormesh(ts, f, Sxx, cmap='jet',vmin=0, vmax=list_of_vmax[i])
            plt.colorbar()
            plt.ylabel('Frequency [Hz]')
            plt.xlabel('Time [sec]')
            plt.ylim((0000.0, 6333))
            plt.title(s2)

            if b2 == '3a':
                title_b = '2 and 3a'
            else:
                title_b = b2

            filename = f'bearing_plots/inner_race/{s1}_{s2}_{b2}_{d}.png'

            plt.suptitle(f"Bearing {title_b} Inner Race Acceleration {d}")
            plt.savefig(filename, bbox_inches='tight')
            plt.close()

            i += 1
            end_time = time.time()
            print(f'Plot {filename} created after {np.round(end_time - start_time, 2)} secs')

end_time = time.time()
print(f'Runtime: {np.round(end_time - start_time, 0)} secs')