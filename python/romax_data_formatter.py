import pandas as pd
import numpy as np


class RomaxData():
    def __init__(self, speed_rpm, dataframe, ignore_orders, factor: bool, max_order: int =64, min_magnitude_factor: float =0.05, min_magnitude: float =0) -> None:
        self.ignore_orders = ignore_orders
        self.top_order_num = max_order
        self.order_1 = speed_rpm / 60
        self.order_max = self.order_1 * self.top_order_num

        self.factor = factor
        self._min_magnitude_factor = min_magnitude_factor
        self._min_magnitude = min_magnitude

        self.all_data = dataframe
        self.components = ['fx', 'fy']

        self.data_process()

    def data_process(self):
        df = self.all_data
        df['linear phase'] = np.rad2deg(df['phase_rad'])
        df['Harmonic Index'] = df['freq_Hz'] / self.order_1
        df['linear amplitude'] = df['mag_N']
        df = df[df['Harmonic Index'] < self.top_order_num + 0.5]

        list_of_sims = df['sim_id'].unique()

        for sim in list_of_sims:
            df_sim = df[df['sim_id'] == sim]
            floor_value = max(df_sim['mag_N'].max() * self._min_magnitude_factor, self._min_magnitude)

            df_romax = df_sim[['Harmonic Index', 'linear amplitude', 'linear phase', 'component']]

            df_romax = df_romax.round({'Harmonic Index': 2})

            df_romax_x = df_romax[df_romax['component'] == 'fx']
            df_romax_y = df_romax[df_romax['component'] == 'fy']
            df_romax_z = df_romax[df_romax['component'] == 'fz']

            df_romax_x = df_romax_x.drop(columns=['component'])
            df_romax_y = df_romax_y.drop(columns=['component'])
            df_romax_z = df_romax_z.drop(columns=['component'])

            df_romax_x = df_romax_x.rename(columns={'linear amplitude': 'linear amplitude x', 'linear phase': 'linear phase x'})
            df_romax_y = df_romax_y.rename(columns={'linear amplitude': 'linear amplitude y', 'linear phase': 'linear phase y'})
            df_romax_z = df_romax_z.rename(columns={'linear amplitude': 'linear amplitude z', 'linear phase': 'linear phase z'})

            df_romax_sim = pd.merge(df_romax_x, df_romax_y, how='inner', on=['Harmonic Index'])
            df_romax_sim = df_romax_sim.merge(df_romax_z, how='inner', on=['Harmonic Index'])

            df_filtered_data = df_romax_sim[(df_romax_sim['linear amplitude x'] > floor_value) | (df_romax_sim['linear amplitude y'] > floor_value) | (df_romax_sim['linear amplitude z'] > floor_value)]

            df_filtered_data = df_filtered_data[~df_filtered_data['Harmonic Index'].isin(self.ignore_orders)]
            
            df_filtered_data.to_csv(f'6_romax_inputs/for_romax_{sim}_fxfyfz.csv', index=False)

            df_x = df_filtered_data[['Harmonic Index', 'linear amplitude x', 'linear phase x']].copy()
            df_y = df_filtered_data[['Harmonic Index', 'linear amplitude y', 'linear phase y']].copy()

            df_x.to_csv(f'6_romax_inputs/for_romax_{sim}_fx.csv', index=False)
            df_y.to_csv(f'6_romax_inputs/for_romax_{sim}_fy.csv', index=False)

            if df_filtered_data['linear amplitude z'].max() > floor_value:
                df_z = df_filtered_data[df_filtered_data['Harmonic Index', 'linear amplitude z', 'linear phase z']].copy()
                df_z.to_csv(f'6_romax_inputs/for_romax_{sim}_fz.csv', index=False)
