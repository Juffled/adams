import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class FFTPlotter():
    def __init__(self, input_df) -> None:
        self.df_raw = input_df

    def plot(self, cmap_style: str, freq_max: float =None, z_max: float =None):
        for sim_id in self.df_raw['sim_id'].unique():
            filtered_data = self.df_raw[(self.df_raw['freq_Hz'] <= freq_max + 0.0001) & (self.df_raw['sim_id'] == sim_id)]
            rounded_filtered_data = filtered_data.round({'freq_Hz':2, 'mag_N':4})
            result = rounded_filtered_data.pivot(index='freq_Hz', columns='component', values='mag_N')

            x_label = "Component"
            y_label = "Frequency [Hz]"
            z_label = "Force [N]"
            title = f"{sim_id} - Spline Force FFT"

            if rounded_filtered_data.empty is True:
                pass
            else:
                plt.clf()
                if z_max is not None:
                    ax = sns.heatmap(result, cmap=cmap_style, vmax=z_max, cbar_kws={'label': z_label})
                else:
                    ax = sns.heatmap(result, cmap=cmap_style, cbar_kws={'label': z_label})
                ax.invert_yaxis()
                ymin, ymax = ax.get_ylim()
                ytick_pos = np.linspace(ymin, ymax, 11)
                ytick_labels = [int(f * freq_max / 10) for f in range(len(ytick_pos))]
                ax.set_yticks(ytick_pos)
                ax.set_yticklabels(ytick_labels)
                ax.set(xlabel=x_label, ylabel=y_label, title=title)

                plt.savefig(f'./7_fft_plots/{sim_id}_spline_force_fft.png')
