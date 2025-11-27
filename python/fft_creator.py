import numpy as np  
import pandas as pd
from scipy.fft import rfft, rfftfreq


class FFTCreator():
    def __init__(self, filepath, separator) -> None:
        self._filepath = filepath
        self.sim = filepath.split('_')[-2]
        self.raw_df = pd.read_csv(filepath, sep=separator, lineterminator='\r')
        self.processed_df = None
        self.process_data()

        self.list_of_data_requests = ['spline_fx','spline_fy', 'spline_fz']

    def process_data(self):
        self.raw_df['time'] = self.raw_df['time.TIME']
        self.raw_df['spline_fx'] = self.raw_df['rotor_spline_global_forces.Fx']
        self.raw_df['spline_fy'] = self.raw_df['rotor_spline_global_forces.Fy']
        self.raw_df['spline_fz'] = self.raw_df['rotor_spline_global_forces.Fz']

        self.processed_df = self.raw_df[['time',
                                         'spline_fx','spline_fy', 'spline_fz']] 

        self.processed_df.round({'time': 6})
        self.processed_df.drop(self.processed_df.tail(1).index,inplace=True)
        if self.processed_df.iloc[1]['time'] == 0.0:
            self.processed_df.drop(self.processed_df.head(1).index,inplace=True)


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

            # Remove static/rigid body stuff
            magnitude[0] = 0.0

            # put it somewhere
            df = pd.DataFrame.from_dict({'freq_Hz': fft_freq, 'mag_N': magnitude, 'phase_rad': phase})  # , orient='columns'
            df.to_csv(f'5_data_fft/{self.sim}_{data_request}.csv', index=False)
