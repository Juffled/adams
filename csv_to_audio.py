import numpy as np
from scipy import signal
import wave
import struct
import pandas as pd
import time


start_time = time.time()

dt = 5e-5  # Data sampling frequency, assumes constant
SETTLING_TIME = 3
FILEPATH = r'KR-000128-XL-003-A Adams Results Bearing Accelerations.xlsx'

# SHEETS = ['SIM4', 'SIM5', 'SIM6', 'SIM7', 'SIM8', 'SIM9']
SHEETS = ['SIM4_inner', 'SIM5_inner', 'SIM6_inner', 'SIM7_inner', 'SIM8_inner', 'SIM9_inner']
BRGS_INT = ['1', '2', '3', '4', '5', '6', '7']
BRGS_SPLIT = ['1', '2', '3a', '3', '4', '5', '6', '7']
DIRECTIONs = ['X', 'Y', 'Z']

q1 = 0.005
q2 = 0.995

for sheet in SHEETS:
    data = pd.read_excel(FILEPATH, sheet_name=sheet)

    data = data.astype(float)

    data_time_filtered = data[data['Time']>=SETTLING_TIME]

    if sheet == 'SIM4_inner' or sheet == 'SIM5_inner' or sheet == 'SIM6_inner':
        brg_nums = BRGS_INT
    else:
        brg_nums = BRGS_SPLIT

    for brg in brg_nums:

        for direction in DIRECTIONs:

            brg_data = data_time_filtered[f"{sheet}: BRG{brg} - {direction}"]

            trimmed_brg_data = brg_data.clip(lower=brg_data.quantile(q1), upper=brg_data.quantile(q2))

            time_signal = trimmed_brg_data.values.flatten()

            fSample = 1.0 / dt

            scaling_fact = 32767.0 / np.max(np.abs(time_signal))

            wavef = wave.open(f'noise/inner_race/{sheet}_brg{brg}_{direction}.wav', 'w')
            wavef.setnchannels(1)  # mono
            wavef.setsampwidth(2)
            wavef.setframerate(fSample)
            for i in range(len(time_signal)):
                a_val = int(time_signal[i] * scaling_fact)
                data_for_write = struct.pack('<h', a_val)
                wavef.writeframesraw(data_for_write)
            wavef.close()
            
            end_time = time.time()
            print(f'Audio file noise/{sheet}_brg{brg}_{direction}.wav created after {np.round(end_time - start_time, 2)} secs')
