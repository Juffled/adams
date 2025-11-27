import pandas as pd
import matplotlib.pyplot as plt


class TrajectoryPlotter():
    def __init__(self, filepath, separator='    ') -> None:
        self._filepath = filepath
        self.sim = filepath.split('_')[-2]
        self.raw_df = pd.read_csv(filepath, sep=separator, lineterminator='\r')

        self.formatted_df = self.process_data()
        
    def process_data(self):
        df = pd.DataFrame()
        df['time'] = self.raw_df['time.TIME']
        df['rotorspline_dx'] = self.raw_df['rotor_spline_relative_ground.DX']
        df['rotorspline_dy'] = self.raw_df['rotor_spline_relative_ground.DY']
        df['inputspline_dx'] = self.raw_df['input_spline_relative_ground.DX']
        df['inputspline_dy'] = self.raw_df['input_spline_relative_ground.DY']
        df['sim_id'] = self.sim
        return df

    def plot(self, start_time, end_time):
        filtered_df = self.formatted_df[self.formatted_df['time'].between(start_time, end_time)]
        r_x = filtered_df['rotorspline_dx']
        r_y = filtered_df['rotorspline_dy']
        
        i_x = filtered_df['inputspline_dx']
        i_y = filtered_df['inputspline_dy']
        plt.clf()
        plt.plot(r_x, r_y, label='Rotor Shaft Spline')
        plt.plot(i_x, i_y, label='Input Shaft Spline')

        plt.title(f'{self.sim}: Spline Trajectory' )
        plt.xlabel("X [mm]")
        plt.ylabel("Y [mm]")
        plt.legend(loc="upper left", fancybox=True)
        plt.gca().set_aspect('equal')
        plt.savefig(f"./8_trajectory_plots/{self.sim}_trajectory.png")
