# import the CSV result files from folder
# import csv excitation files from folder
# extract the excitation order from the results 
# extract the excitation orders from the excitations
# compare the results 

import pandas as pd
from os import listdir
from numpy import delete, isnan, array
import math
# from scipy.interpolate import interp1d
        
def parse_folder(folder_path) -> list:
    return listdir(folder_path)

class RomaxResult():
    def __init__(self, romax_results_path) -> None:
        print("Initialising Romax result")
        self.folder_path = romax_results_path

    def import_data(self):
        self.files = parse_folder(self.folder_path)
        self.results = {}
        self.erp_sum_result = {}
        self.create_dict()
    
    def read_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.path)
    
    def create_dict(self):
        print("Creating dictionary for results based on file name")
        for i in self.files:
            if i != 'Gear Excitations':
                j = i.split("_")
                k = j[1].split(".")
                model_name = k[0]
            else:
                model_name = i
            #print(f"Romax results model name {model_name}")
            orders,input_speed, erp_result = self.extract_orders(i)
            self.results[model_name] = {
                "Orders": orders,
                "Input_Speed": input_speed,
                "ERP_result": erp_result
            }
            

    def extract_orders(self,file) -> list:
        #print("extracting the erp results and seperating by order for each file")
        orders = []
        input_speed = []
        erp_result = []
        if file != 'Gear Excitations':
            file_path = self.folder_path + "\\" + file
            df = pd.read_csv(file_path, delimiter=None, header=None, skiprows=1)
            df.columns = df.iloc[0]
            df = df.iloc[1:]
            
            for column_title in df.columns:
                string_split = column_title.split(" ")
                if string_split[1] == "Equivalent":
                    #print(f"Order: {string_split[8]}")
                    orders.append(string_split[8])
                    erp_result.append(df[column_title])
                else:
                    freq = df[column_title]
                    if type(freq) == pd.Series:
                        input_speed.append(freq)    
                    elif type(freq) == pd.DataFrame:
                        input_speed.append(freq.iloc[:,0])
            sum_erp_result = []# equivalent summation of ERP
            for i in range(len(erp_result[0])):
                if i == 0:
                    sum_erp_result.append(0.00)
                else:
                    sum_erp_result.append(self.decibel_addition(self.return_nth_subvalue(erp_result,i)))
                
            orders.append("ERP summation")
            input_speed.append(input_speed[0])
            erp_result.append(sum_erp_result)
                    
        else:
            gear_ERP_files = parse_folder(self.folder_path+ "\\" + file)
            gear_ERP_files = [f for f in gear_ERP_files if f.endswith('.csv')]
            #gear_order_list = []
            #gear_erp_list = []
            #gear_frequency_list = []
            for gear in gear_ERP_files:
                text_split = gear.split(" ")
                gear_order_with_ext = text_split[2].split(".")
                gear_order = float(gear_order_with_ext[0])
                
                file_path = self.folder_path + "\\" + file + "\\" + gear
                df = pd.read_csv(file_path, delimiter=None)
                erp = df[df.columns[0]].values
                erp = delete(erp, 0)
                
                freq = df.index.values
                freq = delete(freq, 0)
                
                orders.append(gear_order)
                erp_result.append(erp.tolist())
                input_speed.append(freq.tolist())
            
            sum_erp_result = []# equivalent summation of ERP
            include_orders = [19*1, 19*2, 19*3]#only include the 19th order and harmonics for ERP summation
            include_erp = []
            for i, order in enumerate(orders):
                if order in include_orders:
                    include_erp.append(erp_result[i])
            for i in range(len(include_erp[0])):
                if i == 0:
                    sum_erp_result.append(0.00)
                else:
                    sum_erp_result.append(self.decibel_addition(self.return_nth_subvalue(include_erp,i)))
                
            orders.append("ERP summation")
            input_speed.append(input_speed[0])
            erp_result.append(sum_erp_result)

        """input_speed_list = range(0,5001,20) #list of 251 values

        #orders - list of all orders
        #erp_result - list of all the erp results 
        #input_speed - same list repeated for all results 
        erp_speed = []
        for i,order in enumerate(orders):
            erp = erp_result[i]
            freq = input_speed[i]
            order = float(order)

            #freq/order *60
            speed = [float(f)/order*60 for f in freq]
            interp_func = interp1d(speed,erp)
            new_erp = interp_func(array(input_speed_list))
            erp_speed.append(new_erp)

        """


        return [orders,input_speed,erp_result]
    
    def return_largest_order(self):
        order_list = []
        for model in self.results:
            orders = (self.results[model]['Orders'][:-1])
            for i in orders:
                order_list.append(float(i))
        return max(order_list)


    
    def return_nth_subvalue(self,list_of_lists,n):

        return [float(subvalue[n]) for subvalue in list_of_lists]
    
    def decibel_addition(self,db_values):
        """
        Perform decibel addition for a list of dB values.

        Parameters:
            db_values (list): A list of decibel values.

        Returns:
            float: The resulting decibel value after addition.
        """
        # Convert dB values to linear scale
        #linear_values = [10**(db/10) for db in db_values]
        linear_values = [10**(db/10) if not isnan(db) else 0 for db in db_values]

        # Sum linear values
        linear_sum = sum(linear_values)

        if linear_sum <= 0:
            linear_sum = 1

        # Convert back to dB
        result_db = 10 * math.log10(linear_sum)

        return result_db
    
    def summation_output_results(self):

        key_list = ['EM Rotor Speed (rpm)']
        results_list = []
        output_data = {}


        for model in self.equiv_results.keys():
            if results_list == []:
                output_data['EM Rotor Speed (rpm)'] = self.results[model]['Frequency_Range'][0]
            if model != 'Gear Excitations':
                output_data[model] = self.results[model]['ERP_result'][-1]
                key_list.append(model)
                results_list.append(self.results[model]['ERP_result'][-1])
    
        self.erp_sum_df = pd.DataFrame(output_data)




class SplineOrders():
    def __init__(self, folder:str) -> None:
        print("initialising the SplineOrders class ")
        self.folder_path = folder
        self.files = parse_folder(self.folder_path)
        self.filter_files()
    
    def create_ammend_dict(self, vector:str, dictonary:dict = {}) -> dict:
        dictonary[vector] = []
        return dictonary
    
    def find_model_name_vector(self, file_name:str):
        j = file_name.split("_")
        k = j[3].split(".")
            
        model_name = j[2]
        vector = k[0]

        return [model_name,vector]

    def find_orders_from_file(self, model_name, vector, file):
        #print("pulling all the orders from the files")
            results = pd.read_csv(self.folder_path + "\\" +file)
            self.results[model_name][vector] = results[results.columns[0]]

    def filter_files(self):
        print("Pulling all the model names from the title of the files")
        self.results = {}
        model_running_list = []
        for i in self.files:
            model_name, vector = self.find_model_name_vector(i)

            #print(f"model is {model_name} and vector is {vector}")

            if len(model_running_list) == 0:
                model_running_list.append(model_name)
                vectors = self.create_ammend_dict(vector)
                self.results[model_running_list[0]] = vectors
            elif len(model_running_list) == 1:
                if model_running_list[0] == model_name:
                    vectors = self.create_ammend_dict(vector,vectors)
                elif model_running_list[0] != model_name:
                    model_running_list.clear()
                    model_running_list.append(model_name)
                    #vectors = self.create_ammend_dict(vector)
                    self.results[model_running_list[0]] = {vector: {}}
                    #self.results[model_running_list[0]] = self.create_ammend_dict(vector)
            elif len(model_running_list) > 1:
                print(f"model running list has too many values. len model_running_list = {len(model_running_list)}")
            self.find_orders_from_file(model_name,vector,i)

        
def main():

    spline_harmonics_folder = "I:\\Projects\\KR-000130 MSC- Hyundai Mobis NVH Layout Study\\05 - Analysis\\07 - Python\\kr130_adams_python\\6_romax_inputs"

    romax_results_folder = "I:\\Projects\\KR-000130 MSC- Hyundai Mobis NVH Layout Study\\05 - Analysis\\07 - Python\\kr130_adams_python\\9_romax_outputs\\nominal_gear"


    spline_harmonics = SplineOrders(spline_harmonics_folder)
    #print(spline_harmonics.results)

    romax_results = RomaxResult(romax_results_folder)
    romax_results.import_data()
    print(f"Max Order from data is: ", romax_results.return_largest_order())

    #spline_harmonics.find_orders_from_file()



    for model_name in spline_harmonics.results.keys():
        if model_name in romax_results.results.keys():
            pass
        else:
            print(f"This model {model_name} is not in Romax results ")

    spline_orders = []
    erp_orders = []
    model_list = []
    error_counter = 0
    for model in spline_harmonics.results:
        spline_orders.append(spline_harmonics.results[model]['fx'].values)
        model_list.append(model)
        erp_orders.append(romax_results.results[model]['Orders'])
        for order in spline_harmonics.results[model]['fx'].values:
            erp_list = [float(i) for i in romax_results.results[model]['Orders'][:-1]]
            if not (order in erp_list):
                print(f"No ERP resutls for Model: {model} Order: {order}")
                error_counter =+ 1

    if error_counter == 0:
        print("no errors have been found, all Spline orders in ERP results")
    else:
        print("Errors found please check results")


    print("hello")

if __name__ == "__main__":
    main()