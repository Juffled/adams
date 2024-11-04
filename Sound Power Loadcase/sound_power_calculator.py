import pandas as pd
import numpy as np


class SoundPowerCalculator():
    def __init__(self, speed_rpm: int, torque_nm: float, f_mag_path: str, f_phase_path: str, v_mag_path: str, v_phase_path: str,
                 frequency_error: float = 0.05) -> None:
        self.speed_rpm = speed_rpm
        self.torque_nm = torque_nm
        self.order_1 = self.speed_rpm / 60
        self._freq_error = frequency_error

        self.f_mag_path = f_mag_path
        self.f_phase_path = f_phase_path
        self.v_mag_path = v_mag_path
        self.v_phase_path = v_phase_path

        self.f_heading_mag = ['freq_Hz', 'f_mag_N']
        self.f_heading_phase = ['freq_Hz', 'f_phase_deg']
        self.v_heading_mag = ['freq_Hz', 'v_mag_m/s']
        self.v_heading_phase = ['freq_Hz', 'v_phase_deg']

        self.data = self.data_process()

    def data_read(self, path, heading):
        df = pd.read_csv(path, sep='\t')
        df.columns = heading
        return df

    def data_process(self):
        f_mag = self.data_read(self.f_mag_path, self.f_heading_mag)
        f_phase = self.data_read(self.f_phase_path, self.f_heading_phase)

        v_mag = self.data_read(self.v_mag_path, self.v_heading_mag)
        v_phase = self.data_read(self.v_phase_path, self.v_heading_phase)

        df_combined_f = pd.merge(f_mag, f_phase, on=self.f_heading_mag[0], how='inner')
        df_combined_v = pd.merge(v_mag, v_phase, on=self.v_heading_mag[0], how='inner')
        df_combined = pd.merge(df_combined_f, df_combined_v, on=self.f_heading_mag[0], how='inner')
        df_combined['order'] = df_combined['freq_Hz'] / self.order_1
        df_combined['acoustic_power_W'] = 0.5 * df_combined['f_mag_N'] * df_combined['v_mag_m/s'] * np.absolute(np.sin(np.radians(df_combined['f_phase_deg']) - np.radians(df_combined['v_phase_deg'])))
        df_combined['speed_rpm'] = self.speed_rpm
        df_combined['torque_nm'] = self.torque_nm
        return df_combined
