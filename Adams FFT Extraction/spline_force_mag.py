import pandas as pd
import numpy as np


class FFT_Processor():
    def __init__(self, speed: int, mag_path: str, phase_path: str, 
                 max_order: int =38, min_magnitude: float =5.0, frequency_error: float = 0.05) -> None:
        self.speed_rpm = speed
        self.top_order_num = max_order
        self.order_1 = self.speed_rpm / 60
        self.order_max = self.order_1 * self.top_order_num
        self._min_magnitude = min_magnitude
        self._freq_error = frequency_error

        self._mag_path = mag_path
        self._phase_path = phase_path

        self._heading_mag = ['freq_Hz', 'mag_N']
        self._heading_phase = ['freq_Hz', 'phase_deg']

        self._order_range = self.order_range_calculator()

        self.data = self.data_process()

    def order_range_calculator(self):
        order_range = []
        for i in range(0, self.top_order_num):
            order = i + 1
            spread = [order * self.order_1 * (1 - self._freq_error), order * self.order_1 * (1 + self._freq_error), order]
            order_range.append(spread)
        return order_range

    def data_read(self, path, heading):
        df = pd.read_csv(path, sep='\t')
        df.columns = heading
        return df

    def data_process(self):
        df_mag = self.data_read(self._mag_path, self._heading_mag)
        df_phase = self.data_read(self._phase_path, self._heading_phase)

        df_combined = pd.merge(df_mag, df_phase, on=self._heading_mag[0], how='inner')
        df_combined['order'] = df_combined['freq_Hz'] / self.order_1

        df_mag_filtered = df_combined[df_combined[self._heading_mag[1]] >= self._min_magnitude]

        dataset_dict = df_mag_filtered.to_dict('records')

        data_filter_pass_1 = []

        for data_row in dataset_dict:
            for data_range in self._order_range:
                lower_range = data_range[0]
                upper_range = data_range[1]
                order = data_range[2]

                if lower_range <= data_row['freq_Hz'] <= upper_range:
                    data_row['order'] = int(round(data_row['order'],0))
                    data_row['order_error_%'] = np.round(100 * np.abs(1 - data_row['freq_Hz'] / (self.order_1 * order)),3)
                    data_filter_pass_1.append(data_row)

        data_filter_pass_2 = [data_filter_pass_1[0]]

        for data in data_filter_pass_1:
            if data['order'] == data_filter_pass_2[-1]['order']:
                if data['order_error_%'] <= data_filter_pass_2[-1]['order_error_%']:
                    data_filter_pass_2[-1] = data
            else:
                data_filter_pass_2.append(data)

        df1 = pd.DataFrame(data_filter_pass_2)
        df2 = df1[['order', 'mag_N', 'phase_deg', 'freq_Hz', 'order_error_%']]

        return df2
