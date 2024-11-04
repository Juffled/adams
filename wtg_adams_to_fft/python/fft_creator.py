import numpy as np  
import matplotlib.pyplot as plt 
import pandas as pd
import scipy.fftpack
from scipy.fft import rfft, rfftfreq

plt.style.use("seaborn")


class FFTCreator():
    def __init__(self, filepath, separator) -> None:
        self._filepath = filepath
        self.sim = filepath.split('_')[-2].split('/')[-1]
        self.raw_df = pd.read_csv(filepath)
        self.prefix = self.raw_df.columns[-1].split('.')[-1][0]
        self.processed_df = None
        self.process_data()

        self.list_of_data_requests = ['acc5_x','acc5_y', 'acc5_z',
                                      'acc6_x','acc6_y', 'acc6_z',
                                      'acc7_x','acc7_y', 'acc7_z',
                                      'acc8_x','acc8_y', 'acc8_z',
                                      'acc9_x','acc9_y', 'acc9_z',
                                      'acc10_x','acc10_y', 'acc10_z']

    def process_data(self):
        self.raw_df['time'] = self.raw_df['Time']

        self.raw_df['acc5_x'] = self.raw_df[f'Accelerometer_5.{self.prefix}X']
        self.raw_df['acc5_y'] = self.raw_df[f'Accelerometer_5.{self.prefix}Y']
        self.raw_df['acc5_z'] = self.raw_df[f'Accelerometer_5.{self.prefix}Z']

        self.raw_df['acc6_x'] = self.raw_df[f'Accelerometer_6.{self.prefix}X']
        self.raw_df['acc6_y'] = self.raw_df[f'Accelerometer_6.{self.prefix}Y']
        self.raw_df['acc6_z'] = self.raw_df[f'Accelerometer_6.{self.prefix}Z']

        self.raw_df['acc7_x'] = self.raw_df[f'Accelerometer_7.{self.prefix}X']
        self.raw_df['acc7_y'] = self.raw_df[f'Accelerometer_7.{self.prefix}Y']
        self.raw_df['acc7_z'] = self.raw_df[f'Accelerometer_7.{self.prefix}Z']

        self.raw_df['acc8_x'] = self.raw_df[f'Accelerometer_8.{self.prefix}X']
        self.raw_df['acc8_y'] = self.raw_df[f'Accelerometer_8.{self.prefix}Y']
        self.raw_df['acc8_z'] = self.raw_df[f'Accelerometer_8.{self.prefix}Z']

        self.raw_df['acc9_x'] = self.raw_df[f'Accelerometer_9.{self.prefix}X']
        self.raw_df['acc9_y'] = self.raw_df[f'Accelerometer_9.{self.prefix}Y']
        self.raw_df['acc9_z'] = self.raw_df[f'Accelerometer_9.{self.prefix}Z']

        self.raw_df['acc10_x'] = self.raw_df[f'Accelerometer_10.{self.prefix}X']
        self.raw_df['acc10_y'] = self.raw_df[f'Accelerometer_10.{self.prefix}Y']
        self.raw_df['acc10_z'] = self.raw_df[f'Accelerometer_10.{self.prefix}Z']

        self.processed_df = self.raw_df[['time',
                                         'acc5_x','acc5_y', 'acc5_z',
                                         'acc6_x','acc6_y', 'acc6_z',
                                         'acc7_x','acc7_y', 'acc7_z',
                                         'acc8_x','acc8_y', 'acc8_z',
                                         'acc9_x','acc9_y', 'acc9_z',
                                         'acc10_x','acc10_y', 'acc10_z']] 

        self.processed_df.round({'time': 6})

    def fft(self, window_start, window_end, sample_rate_hz: int):
        for data_request in self.list_of_data_requests:
            duration = window_end - window_start
            n = int(np.round(sample_rate_hz * duration, 0))
            # filter for the window
            filtered_df = self.processed_df[self.processed_df['time'].between(window_start, window_end)]

            # fft
            signal = filtered_df[data_request].values
            spectrum = rfft(signal)

            # data we want from the fft
            fft_freq = rfftfreq(n, 1 / sample_rate_hz)
            magnitude = np.abs(spectrum) * 2 / n
            phase = np.angle(spectrum)

            # put it somewhere
            df = pd.DataFrame.from_dict({'freq_Hz': fft_freq, 'mag': magnitude, 'phase_rad': phase})  # , orient='columns'
            df.to_csv(f'data_fft/{self.sim}/{self.sim}_{data_request}_{self.prefix}.csv', index=False)




class FFTCreator2():
    def __init__(self, filepath, separator, window_start, window_end, sample_rate_hz: int) -> None:
        self._filepath = filepath
        self.sim = filepath.split('_')[-2].split('/')[-1]
        self.accel_num = filepath.split('_')[-1].split('.')[0]
        self.list_of_data_requests = ['dX', 'dY', 'dZ', 'aX', 'aY', 'aZ']

        with pd.option_context('display.precision', 10):
            self.raw_df = pd.read_csv(filepath, sep=separator)
            self.raw_df['time'] = self.raw_df['Time']

            self.raw_df['aX'] = self.raw_df[f'Accelerometer_{self.accel_num}.aX']
            self.raw_df['aY'] = self.raw_df[f'Accelerometer_{self.accel_num}.aY']
            self.raw_df['aZ'] = self.raw_df[f'Accelerometer_{self.accel_num}.aZ']

            self.raw_df['dX'] = self.raw_df[f'Accelerometer_{self.accel_num}.dX']
            self.raw_df['dY'] = self.raw_df[f'Accelerometer_{self.accel_num}.dY']
            self.raw_df['dZ'] = self.raw_df[f'Accelerometer_{self.accel_num}.dZ']


            self.processed_df = self.raw_df[['time', 'aX','aY', 'aZ', 'dX','dY', 'dZ']] 

            self.processed_df.round({'time': 6})
            self.processed_df['time'] = pd.to_numeric(self.processed_df['time'])
            self.fft(window_start=window_start, window_end=window_end, sample_rate_hz=sample_rate_hz)

    def fft(self, window_start, window_end, sample_rate_hz: int):
        for data_request in self.list_of_data_requests:
            duration = window_end - window_start
            n = int(np.round(sample_rate_hz * duration, 0))
            # filter for the window
            filtered_df = self.processed_df[self.processed_df['time'].between(window_start, window_end)]

            # fft
            signal = filtered_df[data_request].values
            spectrum = rfft(signal)

            # data we want from the fft
            fft_freq = rfftfreq(n, 1 / sample_rate_hz)
            magnitude = np.abs(spectrum) * 2 / n
            phase = np.angle(spectrum)

            # put it somewhere
            df = pd.DataFrame.from_dict({'freq_Hz': fft_freq, 'mag': magnitude, 'phase_rad': phase})  # , orient='columns'
            df.to_csv(f'data_fft/{self.sim}/{self.sim}_CMS{self.accel_num}_{data_request}.csv', index=False)
