import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class SoundPowerCalculator():
    def __init__(self, input_df, sim_map) -> None:
        self.df_raw = input_df
        self.sim_map = sim_map

        self.set_torque_speed()
        self.df_sp_individual = self.calc_component_soundpower(df=self.reformat_raw_df())

        self.df_sp_gearbox_freq = self.calc_gearbox_soundpower_freq(df=self.df_sp_individual)

        self.df_total_sp = self.calc_total_gearbox_soundpower(df=self.df_sp_gearbox_freq)

    def set_torque_speed(self):
        for sim in self.sim_map:
            self.df_raw.loc[self.df_raw['sim_id'] == sim['sim_id'], 'speed_rpm'] = sim['speed_rpm']
            self.df_raw.loc[(self.df_raw['sim_id'] == sim['sim_id']) & (self.df_raw['window'] == 't1'), 'torque_nm'] = sim['torque_nm_1']
            self.df_raw.loc[(self.df_raw['sim_id'] == sim['sim_id']) & (self.df_raw['window'] == 't2'), 'torque_nm'] = sim['torque_nm_2']
            self.df_raw.loc[(self.df_raw['sim_id'] == sim['sim_id']) & (self.df_raw['window'] == 't3'), 'torque_nm'] = sim['torque_nm_3']

    def reformat_raw_df(self):
        df_fx = self.df_raw[(self.df_raw['component'] == 'fx')]
        df_fx = df_fx.rename(columns={'mag': 'fx_mag_N', 'phase_rad': 'fx_phase_rad'})
        df_fx = df_fx.drop(columns=['component'])

        df_fy = self.df_raw[(self.df_raw['component'] == 'fy')]
        df_fy = df_fy.rename(columns={'mag': 'fy_mag_N', 'phase_rad': 'fy_phase_rad'})
        df_fy = df_fy.drop(columns=['component'])

        df_vx = self.df_raw[(self.df_raw['component'] == 'vx')]
        df_vx = df_vx.rename(columns={'mag': 'vx_mag_m/s', 'phase_rad': 'vx_phase_rad'})
        df_vx = df_vx.drop(columns=['component'])

        df_vy = self.df_raw[(self.df_raw['component'] == 'vy')]
        df_vy = df_vy.rename(columns={'mag': 'vy_mag_m/s', 'phase_rad': 'vy_phase_rad'})
        df_vy = df_vy.drop(columns=['component'])

        df1 = pd.merge(df_fx, df_fy, on=['freq_Hz', 'sim_id', 'brg', 'window', 'torque_nm', 'speed_rpm'])
        df2 = pd.merge(df1, df_vx, on=['freq_Hz', 'sim_id', 'brg', 'window', 'torque_nm', 'speed_rpm'])
        df3 = pd.merge(df2, df_vy, on=['freq_Hz', 'sim_id', 'brg', 'window', 'torque_nm', 'speed_rpm'])
        return df3

    def calc_component_soundpower(self, df):
        df['acoustic_power_w_x'] = 0.5 * df['fx_mag_N'] * df['vx_mag_m/s'] * np.absolute(np.sin(df['fx_phase_rad'] - df['vx_phase_rad']))
        df['acoustic_power_w_y'] = 0.5 * df['fy_mag_N'] * df['vy_mag_m/s'] * np.absolute(np.sin(df['fy_phase_rad'] - df['vy_phase_rad']))
        df['acoustic_power_w'] = (df['acoustic_power_w_x']**2 + df['acoustic_power_w_y']**2)**0.5
        return df

    def calc_gearbox_soundpower_freq(self, df):
        df_grouped = df.groupby(['freq_Hz', 'sim_id', 'window', 'torque_nm', 'speed_rpm']).agg({'acoustic_power_w': 'sum'})
        df_grouped = df_grouped.reset_index()
        return df_grouped

    def calc_total_gearbox_soundpower(self, df):
        df_grouped = df.groupby(['sim_id', 'window', 'torque_nm', 'speed_rpm']).agg({'acoustic_power_w': 'sum'})
        df_grouped = df_grouped.reset_index()
        return df_grouped

    def check_data_csv(self):
        self.df_sp_individual.to_csv('sound_power_component.csv', index=False)
        self.df_raw.to_csv('raw_data.csv', index=False)
        self.df_sp_gearbox_freq.to_csv('freq_sound_power_gearbox.csv', index=False)
        self.df_total_sp.to_csv('total_sound_power_gearbox.csv', index=False)

    def plot(self, cmap_style: str, f_max: float =None, v_max: float =None):
        # Plot by simulation
        for layout in self.sim_map:
            sim_id = layout['sim_id']
            speed_rpm = layout['speed_rpm']

            filtered_data = self.df_sp_gearbox_freq[(self.df_sp_gearbox_freq['sim_id'] == sim_id) & (self.df_sp_gearbox_freq['freq_Hz'] <= f_max + 0.1)]
            rounded_filtered_data = filtered_data.round({'freq_Hz':0, 'speed_rpm':1, 'torque_nm':2, 'acoustic_power_W': 6})
            result = rounded_filtered_data.pivot(index='freq_Hz', columns='torque_nm', values='acoustic_power_w')

            x_label = 'Torque [Nm]'
            y_label = 'Frequency [Hz]'
            title = f'Simulation {sim_id}, Speed {speed_rpm}rpm, Acoustic Sound Power [W]'

            if rounded_filtered_data.empty is True:
                pass
            else:
                plt.clf()
                if v_max is not None:
                    ax = sns.heatmap(result, cmap=cmap_style, vmax=v_max)
                else:
                    ax = sns.heatmap(result, cmap=cmap_style)
                ax.set(xlabel=x_label, ylabel=y_label, title=title)
                plt.yticks(rotation=0)
                ax.invert_yaxis()
                plt.savefig(f'./sound_power_plots/{sim_id}.png')

        # Plot by sim and torques
        torque_vals = [self.sim_map[0]['torque_nm_1'], self.sim_map[0]['torque_nm_2'], self.sim_map[0]['torque_nm_3']]

        for layout in set([d[0] for d in (v['sim_id'] for v in self.sim_map)]):
            filtered_data = self.df_sp_gearbox_freq[self.df_sp_gearbox_freq['sim_id'].str.contains(layout)]
            rounded_filtered_data = filtered_data.round({'freq_Hz':0, 'speed_rpm':1, 'torque_nm':2, 'acoustic_power_W': 6})

            for torque in torque_vals:
                filtered_data_2 = rounded_filtered_data[rounded_filtered_data['torque_nm'] == torque]
                result = filtered_data_2.pivot(index='freq_Hz', columns='sim_id', values='acoustic_power_w')

                if rounded_filtered_data.empty is True:
                    pass
                else:
                    x_label = 'Simulation'
                    title = f'Layout {layout}, Speed {speed_rpm}rpm, Torque {torque}Nm, Acoustic Sound Power [W]'
                    plt.clf()
                    if v_max is not None:
                        ax = sns.heatmap(result, cmap=cmap_style, vmax=v_max)
                    else:
                        ax = sns.heatmap(result, cmap=cmap_style)
                    ax.set(xlabel=x_label, ylabel=y_label, title=title)
                    plt.yticks(rotation=0)
                    ax.invert_yaxis()
                    plt.savefig(f'./sound_power_plots/{layout}_{torque}nm.png')

        for tolerance in set([d[1] for d in (v['sim_id'] for v in self.sim_map)]):
            filtered_data = self.df_sp_gearbox_freq[self.df_sp_gearbox_freq['sim_id'].str.contains(tolerance)]
            rounded_filtered_data = filtered_data.round({'freq_Hz':0, 'speed_rpm':1, 'torque_nm':2, 'acoustic_power_W': 6})

            for torque in torque_vals:
                filtered_data_2 = rounded_filtered_data[rounded_filtered_data['torque_nm'] == torque]
                result = filtered_data_2.pivot(index='freq_Hz', columns='sim_id', values='acoustic_power_w')

                if rounded_filtered_data.empty is True:
                    pass
                else:
                    x_label = 'Tolerance Set'
                    title = f'Tolerance Set {tolerance}, Speed {speed_rpm}rpm, Torque {torque}Nm, Acoustic Sound Power [W]'
                    plt.clf()
                    if v_max is not None:
                        ax = sns.heatmap(result, cmap=cmap_style, vmax=v_max)
                    else:
                        ax = sns.heatmap(result, cmap=cmap_style)
                    ax.set(xlabel=x_label, ylabel=y_label, title=title)
                    plt.yticks(rotation=0)
                    ax.invert_yaxis()
                    plt.savefig(f'./sound_power_plots/{tolerance}_{torque}nm.png')
