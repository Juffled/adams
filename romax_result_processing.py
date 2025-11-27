import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
from tkinter import MULTIPLE
from python.romax_result_check import RomaxResult

romax_designed_results_folder = "C:\\Users\\george.grant\\Desktop\\Mobis Tech Transfer\\results\\9_romax_outputs\\nominal_gear"
romax_designed_results = RomaxResult(romax_designed_results_folder)
romax_designed_results.import_data()

romax_measured_results_folder = "C:\\Users\\george.grant\\Desktop\\Mobis Tech Transfer\\results\\9_romax_outputs\\measured_gear"
romax_measured_results = RomaxResult(romax_measured_results_folder)
romax_measured_results.import_data()

models = list(romax_designed_results.results.keys())

def update_graph(selected_model, selected_orders,graph_adjusted = True):
    # Clear the previous graph
    ax.clear()
    print(selected_orders)
    # Get data for the selected model and orders
    for i, order in enumerate(romax_designed_results.results[selected_model]['Orders']):
        if order in selected_orders:
            frequencies = romax_designed_results.results[selected_model]['Input_Speed'][i]
            #frequencies = frequencies[1:]
            frequencies = [float(j) for j in frequencies]
            #frequencies.pop(0)

            erp = romax_designed_results.results[selected_model]['ERP_result'][i]
            #erp.pop(0)
            #erp = erp[1:]
            erp = [float(j) for j in erp]
            print(f"The Max ERP value for {selected_model} - {order} is: {max(erp)}")
            # Update the graph
            ax.plot(frequencies, erp, label=f"{selected_model} - {order}-AD")
        if order in romax_measured_results.results[selected_model]['Orders']and order in selected_orders:
            frequencies = romax_measured_results.results[selected_model]['Input_Speed'][i]
            #frequencies = frequencies[1:]
            frequencies = [float(j) for j in frequencies]
            #frequencies.pop(0)

            erp = romax_measured_results.results[selected_model]['ERP_result'][i]
            #erp.pop(0)
            #erp = erp[1:]
            erp = [float(j) for j in erp]

            # Update the graph
            ax.plot(frequencies, erp, linestyle='dashed', label=f"{selected_model} - {order}-AM")

    ax.set_title(f"Rotor Shaft Speed vs ERP for {selected_model}")
    ax.set_xlabel("Rotor Shaft Speed (rpm) ")
    ax.set_ylabel("Equivalent Radiated Power (ERP) (dB re 1.0e-12W)")
    #ax.set_xlim(0, 10000)
    #ax.set_ylim(0, 100)
    #ax.set_xticks(range(0,10_001,1000))
    ax.set_xticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000])
    ax.set_xticklabels(range(0,10001,1000))
    ax.set_yscale('log')
    
    
    if graph_adjusted == False:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.75, box.height])
    elif graph_adjusted == True:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width, box.height])
    if len(selected_orders)>15:
        ax.legend(loc = "center left", bbox_to_anchor = (1,0.5),fancybox = True,
              shadow=True, fontsize='small', ncol = 2)#, ncol=len(selected_orders))
    else:
        ax.legend(loc = "center left", bbox_to_anchor = (1,0.5),fancybox = True,
              shadow=True, fontsize='small', ncol = 1)#, ncol=len(selected_orders))
        
    # Refresh the canvas
    canvas.draw()

def on_model_select(event):
    selected_model = model_selector.get()
    available_orders = list(romax_designed_results.results[selected_model]['Orders'])
    order_selector.delete(0, tk.END)
    for order in available_orders:
        order_selector.insert(tk.END, order)
    select_all_var.set(0)
    update_graph(selected_model, available_orders)

def on_order_select(event):
    selected_model = model_selector.get()
    selected_orders = [order_selector.get(idx) for idx in order_selector.curselection()]
    if not selected_orders:
        selected_orders = list(romax_designed_results.results[selected_model]['Orders'])
    update_graph(selected_model, selected_orders)

def toggle_select_all():
    selected_model = model_selector.get()
    available_orders = list(romax_designed_results.results[selected_model]['Orders'])
    if select_all_var.get():
        order_selector.select_set(0, tk.END)
        update_graph(selected_model, available_orders)
    else:
        order_selector.select_clear(0, tk.END)
        update_graph(selected_model, [])

# Initialize Tkinter window
root = tk.Tk()
root.title("Model and Order Selection with ERP Graph")

# Create a frame for the UI
frame = ttk.Frame(root)
frame.pack(side=tk.LEFT, padx=10, pady=10)

# Dropdown menu for model selection
label = ttk.Label(frame, text="Select a Model:")
label.pack(pady=5)

model_selector = ttk.Combobox(frame, values=models, state="readonly")
model_selector.pack(pady=5)
model_selector.bind("<<ComboboxSelected>>", on_model_select)

# Checkbox for select all orders
select_all_var = tk.IntVar()
select_all_checkbox = ttk.Checkbutton(frame, text="Select All Orders", variable=select_all_var, command=toggle_select_all)
select_all_checkbox.pack(pady=5)

# Listbox for order selection
label_orders = ttk.Label(frame, text="Select Orders:")
label_orders.pack(pady=2)

order_selector = tk.Listbox(frame, selectmode=MULTIPLE, height=10)
order_selector.pack(pady=2)
order_selector.bind("<<ListboxSelect>>", on_order_select)

# Matplotlib figure setup
fig, ax = plt.subplots(figsize=(13, 15))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, padx=2, pady=2)

# Add interactive toolbar
toolbar_frame = ttk.Frame(root)
toolbar_frame.pack(side=tk.TOP, fill=tk.X)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

# Initialize with the first model and all orders
update_graph(models[0], romax_designed_results.results[models[0]]['Orders'][0], graph_adjusted = False)
model_selector.set(models[0])
for order in romax_designed_results.results[models[0]]['Orders']:
    order_selector.insert(tk.END, order)

# Run the Tkinter main loop
root.mainloop()
