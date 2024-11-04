import numpy as np  
import matplotlib.pyplot as plt 
import pandas as pd
import scipy.fftpack
from scipy.fft import rfft, rfftfreq

plt.style.use("seaborn")


class FFTCreator():
    def __init__(self, filepath) -> None:
        self._filepath = filepath
        self.sim = filepath.split('_')[-2]
        self.raw_df = pd.read_csv(filepath, sep='    ', lineterminator='\r', engine='python')
        self.processed_df = None

        self.process_data()

        self.list_of_data_requests = ['b1_fx','b1_vx',
                                      'b2_fx','b2_vx',
                                      'b3_fx','b3_vx',
                                      'b4_fx','b4_vx',
                                      'b5_fx','b5_vx',
                                      'b6a_fx','b6a_vx',
                                      'b6b_fx','b6b_vx',
                                      'b7_fx','b7_vx',
                                      'b1_fy','b1_vy',
                                      'b2_fy','b2_vy',
                                      'b3_fy','b3_vy',
                                      'b4_fy','b4_vy',
                                      'b5_fy','b5_vy',
                                      'b6a_fy','b6a_vy',
                                      'b6b_fy','b6b_vy',
                                      'b7_fy','b7_vy']

    def process_data(self):
        self.raw_df['time'] = self.raw_df['time.TIME']

        self.raw_df['b1_fx'] = self.raw_df['B1_Bearing_Forces.Radial_X']
        self.raw_df['b1_fy'] = self.raw_df['B1_Bearing_Forces.Radial_Y']
        self.raw_df['b1_vx'] = self.raw_df['HSG_B1_B2_velocity.VX_B1']
        self.raw_df['b1_vy'] = self.raw_df['HSG_B1_B2_velocity.VY_B1']

        self.raw_df['b2_fx'] = self.raw_df['B2_Bearing_Forces.Radial_X']
        self.raw_df['b2_fy'] = self.raw_df['B2_Bearing_Forces.Radial_Y']
        self.raw_df['b2_vx'] = self.raw_df['HSG_B1_B2_velocity.VX_B2']
        self.raw_df['b2_vy'] = self.raw_df['HSG_B1_B2_velocity.VY_B2']

        self.raw_df['b3_fx'] = self.raw_df['B3_Bearing_Forces.Radial_X']
        self.raw_df['b3_fy'] = self.raw_df['B3_Bearing_Forces.Radial_Y']
        self.raw_df['b3_vx'] = self.raw_df['HSG_B3_B4_velocity.VX_B3']
        self.raw_df['b3_vy'] = self.raw_df['HSG_B3_B4_velocity.VY_B3']

        self.raw_df['b4_fx'] = self.raw_df['B4_Bearing_Forces.Radial_X']
        self.raw_df['b4_fy'] = self.raw_df['B4_Bearing_Forces.Radial_Y']
        self.raw_df['b4_vx'] = self.raw_df['HSG_B3_B4_velocity.VX_B4']
        self.raw_df['b4_vy'] =  self.raw_df['HSG_B3_B4_velocity.VY_B4']

        self.raw_df['b5_fx'] = self.raw_df['B5_Bearing_Forces.Radial_X']
        self.raw_df['b5_fy'] = self.raw_df['B5_Bearing_Forces.Radial_Y']
        self.raw_df['b5_vx'] = self.raw_df['HSG_B5_B6_velocity.VX_B5']
        self.raw_df['b5_vy'] = self.raw_df['HSG_B5_B6_velocity.VY_B5']

        self.raw_df['b6a_fx'] = self.raw_df['B6_a_pos_Bearing_Forces.Radial_X'] + self.raw_df['B6_a_neg_Bearing_Forces.Radial_X']
        self.raw_df['b6a_fy'] = self.raw_df['B6_a_pos_Bearing_Forces.Radial_Y'] + self.raw_df['B6_a_neg_Bearing_Forces.Radial_Y']
        self.raw_df['b6a_vx'] = self.raw_df['HSG_B5_B6_velocity.VX_B6']
        self.raw_df['b6a_vy'] = self.raw_df['HSG_B5_B6_velocity.VY_B6']

        self.raw_df['b6b_fx'] = self.raw_df['B6_b_pos_Bearing_Forces.Radial_X'] + self.raw_df['B6_b_neg_Bearing_Forces.Radial_X']
        self.raw_df['b6b_fy'] = self.raw_df['B6_b_pos_Bearing_Forces.Radial_Y'] + self.raw_df['B6_b_neg_Bearing_Forces.Radial_Y']
        self.raw_df['b6b_vx'] = self.raw_df['HSG_B5_B6_velocity.VX_B6']
        self.raw_df['b6b_vy'] = self.raw_df['HSG_B5_B6_velocity.VY_B6']

        self.raw_df['b7_fx'] = self.raw_df['B7_pos_Bearing_Forces.Radial_X']
        self.raw_df['b7_fy'] = self.raw_df['B7_pos_Bearing_Forces.Radial_Y']
        self.raw_df['b7_vx'] = self.raw_df['HSG_B7_velocity.VX_B7']
        self.raw_df['b7_vy'] = self.raw_df['HSG_B7_velocity.VY_B7']

        self.processed_df = self.raw_df[['time',
                                         'b1_fx','b1_vx',
                                         'b2_fx','b2_vx',
                                         'b3_fx','b3_vx',
                                         'b4_fx','b4_vx',
                                         'b5_fx','b5_vx',
                                         'b6a_fx','b6a_vx',
                                         'b6b_fx','b6b_vx',
                                         'b7_fx','b7_vx',
                                         'b1_fy','b1_vy',
                                         'b2_fy','b2_vy',
                                         'b3_fy','b3_vy',
                                         'b4_fy','b4_vy',
                                         'b5_fy','b5_vy',
                                         'b6a_fy','b6a_vy',
                                         'b6b_fy','b6b_vy',
                                         'b7_fy','b7_vy']] 
        self.processed_df.round({'time': 6})

    def fft_numpy(self, window_start, window_end, sample_rate_hz):
        i = 1
        for start, end in zip(window_start, window_end):
            for data_request in self.list_of_data_requests:
                duration = end - start
                n = int(sample_rate_hz * duration)
                # filter for the window
                filtered_df = self.processed_df[self.processed_df['time'].between(start, end)]

                # fft
                signal = filtered_df [data_request]
                time = filtered_df['time']
                spectrum = np.fft.rfft(signal, norm='ortho')
                spectrum[0] = 0

                # data we want from the fft
                fft_freq = np.fft.rfftfreq(len(signal))*len(signal)/(time.max()-time.min())
                magnitude = np.abs(spectrum) * 2
                phase = np.angle(spectrum)

                # put it somewhere
                df = pd.DataFrame.from_dict({'freq_Hz': fft_freq, 'mag': magnitude, 'phase_rad': phase})
                pos_df = df.loc[df['freq_Hz'] >= 0]
                pos_df.to_csv(f'data_fft/{self.sim}_t{i}_{data_request}.csv', index=False)
            i += 1

    def fft(self, window_start, window_end, sample_rate_hz: int):
        i = 1
        for start, end in zip(window_start, window_end):
            for data_request in self.list_of_data_requests:
                duration = end - start
                n = int(np.round(sample_rate_hz * duration, 0))
                # filter for the window
                filtered_df = self.processed_df[self.processed_df['time'].between(start, end)]

                # fft
                signal = filtered_df[data_request].values
                spectrum = rfft(signal)

                # data we want from the fft
                fft_freq = rfftfreq(n, 1 / sample_rate_hz)
                magnitude = np.abs(spectrum) * 2 / n
                phase = np.angle(spectrum)

                # put it somewhere
                df = pd.DataFrame.from_dict({'freq_Hz': fft_freq, 'mag': magnitude, 'phase_rad': phase})  # , orient='columns'
                df.to_csv(f'data_fft/{self.sim}_t{i}_{data_request}.csv', index=False)
            i += 1

            # Y = scipy.fftpack.fftshift(scipy.fftpack.fft(signal))
            # f = scipy.fftpack.fftshift(scipy.fftpack.fftfreq(n, 1 / sample_rate))
            # m = np.abs(Y)
            # p = np.angle(Y)
            # fig = plt.figure()
            # ax1=fig.add_subplot(2,1,1)
            # ax2=fig.add_subplot(2,1,2)
            # pos_df['mag'].plot(ax=ax1)
            # pos_df['phase'].plot(ax=ax2)
            # plt.show()
