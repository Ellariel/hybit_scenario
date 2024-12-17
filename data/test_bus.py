import pandapower as pp
import numpy as np
import matplotlib.pyplot as plt
#import simbench as sb
#import pandapower.auxiliary
import copy
import os
import warnings
warnings.filterwarnings("ignore", "", FutureWarning, "simbench")

#pandapower.auxiliary._check_if_numba_is_installed = lambda x: x


def calculate_voltage_stability_limit(net, bus, load_index, step_size):
    results = []
    p_load = 0.0
    while True:
        try:
            net.load.loc[load_index, 'p_mw'] = p_load
            pp.runpp(net)
            voltage = net.res_bus.vm_pu.at[bus]
            results.append((p_load, voltage))
            p_load += step_size
        except pp.LoadflowNotConverged:
            break
    return np.array(results)


def plot_voltage_stability_curve(bus, results, p_min, label=None):
    plt.plot(results[:, 0], results[:, 1], label=f'Bus {bus}' if not label else label)
    plt.scatter(results[-1, 0], results[-1, 1], color='red', marker='x')
    plt.axvline(x=results[-1, 0], color='green', linestyle='--', label=f'P_vsl = {results[-1, 0]} MW')
    plt.xlabel('P Load (MW)')
    plt.ylabel('Voltage (pu)')
    plt.title(f'Voltage Stability Curve')
    plt.legend()
    plt.grid(True)


def main():
    GRID_FILE = 'hybit_egrid_cell1.json'
    base_dir = './'
    data_dir = os.path.join(base_dir, 'data')
    grid_file = os.path.join(data_dir, GRID_FILE)
    grid_model = pp.from_json(grid_file)
    pp.runpp(grid_model, numba=False)
    print(f"Grid model of {len(grid_model.load)} loads,\
    {len(grid_model.sgen)} sgens,\
    {len(grid_model.bus)} buses,\
    {len(grid_model.line)} lines,\
    {len(grid_model.trafo)} trafos,\
    {len(grid_model.ext_grid)} ext_grids")

    buses = grid_model.bus[grid_model.bus.name.str.contains('SteelPlant') |\
                           grid_model.bus.name.str.contains('mvb01-switchgear')]
    
    print(buses)
    # List of buses for which you want to plot voltage_profile stability curves
    buses_to_analyze = [i for i, b in buses.iterrows()]  # Replace with your list of buses

    # Step size for increasing the load
    P_min = 10.0  # in MW Replace with your desired step size

    for bus in buses_to_analyze:
        net_ = copy.deepcopy(grid_model)
        load_index = pp.create_load(net_, bus=bus, p_mw=P_min, q_mvar=0)  # Create a load at the specified bus
        results = calculate_voltage_stability_limit(net_, bus, load_index, P_min)
        label = net_.bus.loc[bus, 'name']
        plot_voltage_stability_curve(bus, results, P_min, label)

    plt.show()


if __name__ == "__main__":
    main()
