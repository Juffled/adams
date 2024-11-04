import pandas as pd
import csv


class AdamsTableFormatter():
    def __init__(self, filepath_in, sim, accelerometer_nums, folderpath_out) -> None:
        self.filepath_in = filepath_in
        self.folderpath_out = folderpath_out
        self.sim = sim

        self.num_cols = 216
        self.rated_start = 0
        self.error_start = 72
        self.shock_start = 144

        self.accelerometer_nums = accelerometer_nums

    def sort_data(self):
        for single in self.accelerometer_nums:
            rated = []
            error = []
            shock = []

            outfile = f'{self.folderpath_out}{self.sim}_{single}.csv'

            data_offset = 12*(single - self.accelerometer_nums[0])
            with open(self.filepath_in) as f:
                reader = csv.reader(f)
                for row in reader:
                    rated_data = [row[data_offset + self.rated_start], row[data_offset + self.rated_start + 1], row[data_offset + self.rated_start + 3], row[data_offset + self.rated_start + 5], row[data_offset + self.rated_start + 7], row[data_offset + self.rated_start + 9], row[data_offset + self.rated_start + 11]]
                    if (rated_data[0] !='0') and ((rated_data[1] !='0.0000000000') or (rated_data[1] !='0')):
                        rated.append(rated_data)

                    error_data = [row[data_offset + self.error_start], row[data_offset + self.error_start + 1], row[data_offset + self.error_start + 3], row[data_offset + self.error_start + 5], row[data_offset + self.error_start + 7], row[data_offset + self.error_start + 9], row[data_offset + self.error_start + 11]]
                    if (error_data[0] !='0') and ((error_data[1] !='0.0000000000') or (error_data[1] !='0')):
                        error.append(error_data)

                    shock_data = [row[data_offset + self.shock_start], row[data_offset + self.shock_start + 1], row[data_offset + self.shock_start + 3], row[data_offset + self.shock_start + 5], row[data_offset + self.shock_start + 7], row[data_offset + self.shock_start + 9], row[data_offset + self.shock_start + 11]]
                    if (shock_data[0] !='0') and ((shock_data[1] !='0.0000000000') or (shock_data[1] !='0')):
                        shock.append(shock_data)

            data = rated
            data.extend(error[1:])
            data.extend(shock[1:])
            with pd.option_context('display.precision', 10):
                df = pd.DataFrame(data[1:], columns=rated[0])
                df = df.apply(pd.to_numeric)
                df = df.loc[(df!=0.0).any(axis=1)]
                df.to_csv(outfile, index=False)
        