import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio


class Plotter():
    def __init__(self, input_df) -> None:
        self.df_raw = input_df

    def plot(self, cmap_style: str, f_max: float =None, z_max: float =None, plot: bool =True, interactive_plotly: bool =False, interactive_matplotlib: bool =False,prefix='a', multiplier=1.):
        if prefix == 'a':
            z_label = "Acceleration [m/s²]"
            sub_title = "accel"
        elif prefix == 'd':
            z_label = "Displacement [um]"
            sub_title = "disp"

        # Plot by accelerometer
        for sim_id in self.df_raw['sim_id'].unique():
            for cms in self.df_raw['accel'].unique():
                
                with pd.option_context('display.precision', 12):

                    filtered_data = self.df_raw[(self.df_raw['accel'] == cms) & (self.df_raw['freq_Hz'] <= f_max + 0.0001) & (self.df_raw['prefix'] == prefix)]
                    rounded_filtered_data = filtered_data.round({'freq_Hz':2, 'phase':2})
                    rounded_filtered_data['mag'] = rounded_filtered_data['mag'] * multiplier
                    result = rounded_filtered_data.pivot(index='freq_Hz', columns='component', values='mag')

                    x_label = "Component"
                    y_label = "Frequency [Hz]"
                    title = f"Accelerometer #{cms[3:]}"

                    if interactive_plotly is True:
                        fig = px.imshow(result, title=title, labels=dict(x=x_label, y=y_label, color=z_label), color_continuous_scale=cmap_style, zmax=z_max)
                        fig.update_yaxes(autorange=True)
                        fig.update_layout(title_x=0.5)
                        fig.show()
                        # fig.write_image(f'{save_path}{sim_id}_{cms}.png')

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
                        ytick_labels = [int(f * f_max / 10) for f in range(len(ytick_pos))]
                        ax.set_yticks(ytick_pos)
                        ax.set_yticklabels(ytick_labels)
                        ax.set(xlabel=x_label, ylabel=y_label, title=title)

                        if interactive_matplotlib is True:
                            plt.show()

                        if plot is True:
                            plt.savefig(f'./fft_plots/{sim_id}/{sim_id}_{cms}_{sub_title}.png')
