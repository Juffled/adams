import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class SoundPowerProcessor():
    def __init__(self, power_data_list: list) -> None:
        self.data = self._add_power_data(power_data_list=power_data_list)

    def _add_power_data(self, power_data_list: list[pd.DataFrame]):
        df = pd.DataFrame()

        for power_data in power_data_list:
            df = pd.concat([df, power_data[['freq_Hz', 'order', 'acoustic_power_W', 'speed_rpm', 'torque_nm']]])

        cols = ['freq_Hz', 'speed_rpm', 'torque_nm']

        df1 = df.groupby(cols)[['acoustic_power_W']].sum().add_prefix('total_')
        df2 = df.join(df1, on=cols)
        df3 = df2.groupby(cols, as_index=False).agg({'order' : 'max', 'total_acoustic_power_W': 'max'})
        return df3

    def plot(self, frequency_limit=None, speed_rpm= None, torque_nm= None, x_speed: bool = False, x_torque: bool =False, title: str ='Acoustic Power [W]'):
        filtered_data = self.data
        if frequency_limit is not None:
            filtered_data = filtered_data[(filtered_data['freq_Hz'] < frequency_limit)]

        if speed_rpm is not None:
            filtered_data = filtered_data[(filtered_data['speed_rpm'] == speed_rpm)]

        if torque_nm is not None:
            filtered_data = filtered_data[(filtered_data['torque_nm'] == torque_nm)]

        rounded_filtered_data = filtered_data.round({'freq_Hz':0, 'speed_rpm':1, 'torque_nm':2, 'total_acoustic_power_W': 3, 'order': 3})

        if x_speed is True:
            result = rounded_filtered_data.pivot(index='freq_Hz', columns='speed_rpm', values='total_acoustic_power_W')
            x_label = "Rotational Speed [rpm]"
        elif x_torque is True:
            result = rounded_filtered_data.pivot(index='freq_Hz', columns='torque_nm', values='total_acoustic_power_W')
            x_label = "Torque [Nm]"

        ax = sns.heatmap(result, fmt="g", cmap='viridis')
        ax.set(xlabel=x_label, ylabel="Frequency [Hz]", title=title)
        plt.yticks(rotation=0)
        ax.invert_yaxis()
        plt.show()
