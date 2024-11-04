import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class CMSPlotter():
    def __init__(self, csv_path, start_time, end_time, numbers=['5', '6', '7', '8', '9', '10']) -> None:
        self.csv = csv_path
        self.nums = numbers
        self.start_time = start_time
        self.end_time = end_time

        self.df = pd.read_csv(self.csv)
        self.filtered_df = self.df[self.df['Time'].between(self.start_time, self.end_time)]

        self._text = 'Accelerometer_'

    def plot_all(self):
        for num in self.nums:
            self.plot_single(filtered_df = self.filter_cms(num), num=num)

    def filter_cms(self, num):
        headings = [f"{self._text}{num}.dX", f"{self._text}{num}.dY", f"{self._text}{num}.dZ"]
        df = self.filtered_df[headings]
        df = df.rename(columns={f"{self._text}{num}.dX":"X", f"{self._text}{num}.dY":"Y", f"{self._text}{num}.dZ":"Z"})
        return df

    def plot_single(self, filtered_df, num):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = filtered_df['X']
        y = filtered_df['Y']
        z = filtered_df['Z']
        ax.plot(x, y, z, color = 'tab:blue', linewidth= 1)
        plt.title(f'Accelerometer #{num} Displacement' )
        ax.set_xlabel("X [mm]")
        ax.set_ylabel("Y [mm]")
        ax.set_zlabel("Z [mm]")
        ax.set_aspect('equal', adjustable='box')
        # plt.show()
        plt.savefig(f"C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/disp_plots/CMS{num}.png")


class CMSPlotter2():
    def __init__(self, csv_path, start_time, end_time, multiplier=1.) -> None:
        self.csv = csv_path
        self.num = csv_path.split('_')[-1].split('.')[0]
        self.sim = csv_path.split('_')[-2].split('/')[-1]
        self.start_time = start_time
        self.end_time = end_time

        self._text = 'Accelerometer_'

        with pd.option_context('display.precision', 10):
            self.df = pd.read_csv(self.csv)
            self.filtered_df = self.df[self.df['Time'].between(self.start_time, self.end_time)]

            headings = [f"{self._text}{self.num}.dX", f"{self._text}{self.num}.dY", f"{self._text}{self.num}.dZ"]
            df = self.filtered_df[headings]

            for heading in headings:
                df[heading] = df[heading] * multiplier

            df = df.rename(columns={f"{self._text}{self.num}.dX":"X", f"{self._text}{self.num}.dY":"Y", f"{self._text}{self.num}.dZ":"Z"})

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            x = df['X']
            y = df['Y']
            z = df['Z']
            ax.plot(x, y, z, color = 'tab:blue', linewidth= 1)
            plt.title(f'Simulation {self.sim}, Accelerometer #{self.num} Displacement, Time={self.start_time} - {self.end_time}s' )
            ax.set_xlabel("X [mm]")
            ax.set_ylabel("Y [mm]")
            ax.set_zlabel("Z [mm]")
            ax.set_aspect('equal')
            plt.locator_params(axis='both', tight=True, nbins=5)
            # plt.show()
            plt.savefig(f"C:/Users/george.grant/OneDrive - Hexagon/Documents/code/Python/adams/wtg_adams_to_fft/disp_plots/{self.sim}/{self.sim}_CMS{self.num}_t{self.start_time}-{self.end_time}s.png")
