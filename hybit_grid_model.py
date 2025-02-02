import os
import argparse
import pandapower as pp

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)



def make_grid_model(**kwargs):
        base_dir = kwargs.get('dir', './')
        verbose = kwargs.get('verbose', 1)

        data_dir = os.path.join(base_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        grid_file = os.path.join(data_dir, 'grid_model.json')

        net = pp.create_empty_network()
        # https://pandapower.readthedocs.io/en/latest/topology/examples.html

        pp.create_bus(net, name = "Bus-0", vn_kv = 110, type = 'b') # bus 0, 110 kV bar
        pp.create_bus(net, name = "Bus-1", vn_kv = 20, type = 'b') # bus 1, 20 kV bar
        pp.create_ext_grid(net, 0, vm_pu = 1, name = "ExternalGrid-0")
        pp.create_transformer_from_parameters(net, hv_bus=0, lv_bus=1, i0_percent=0.038, pfe_kw=11.6,
                vkr_percent=0.322, sn_mva=40, vn_lv_kv=22.0, vn_hv_kv=110.0, vk_percent=17.8)

        pp.create_bus(net, name = "Bus-2", vn_kv = 20, type = 'b')
        pp.create_bus(net, name = "Bus-3", vn_kv = 20, type = 'b')
        pp.create_bus(net, name = "Bus-4", vn_kv = 20, type = 'b')
        pp.create_bus(net, name = "Bus-5", vn_kv = 20, type = 'b')

        pp.create_bus(net, name = "Bus-6", vn_kv = 20, type = 'b')
        pp.create_bus(net, name = "Bus-7", vn_kv = 20, type = 'b')
        pp.create_bus(net, name = "Bus-8", vn_kv = 20, type = 'b')
        pp.create_bus(net, name = "Bus-9", vn_kv = 20, type = 'b')

        pp.create_line(net, name = "Line-0", from_bus = 1, to_bus = 2, length_km = 1, std_type = "NAYY 4x150 SE")
        pp.create_line(net, name = "Line-1", from_bus = 1, to_bus = 3, length_km = 1, std_type = "NAYY 4x150 SE")
        pp.create_line(net, name = "Line-2", from_bus = 1, to_bus = 4, length_km = 1, std_type = "NAYY 4x150 SE")
        pp.create_line(net, name = "Line-3", from_bus = 1, to_bus = 5, length_km = 1, std_type = "NAYY 4x150 SE")

        pp.create_line(net, name = "Line-0", from_bus = 2, to_bus = 6, length_km = 1, std_type = "NAYY 4x150 SE")
        pp.create_line(net, name = "Line-1", from_bus = 3, to_bus = 7, length_km = 1, std_type = "NAYY 4x150 SE")
        pp.create_line(net, name = "Line-2", from_bus = 4, to_bus = 8, length_km = 1, std_type = "NAYY 4x150 SE")
        pp.create_line(net, name = "Line-3", from_bus = 5, to_bus = 9, length_km = 1, std_type = "NAYY 4x150 SE")

        pp.create_load(net, 2, p_mw = 1, q_mvar = 0.2, name = "Load-0")
        pp.create_sgen(net, 6, p_mw = 1, name = "StaticGen-0")

        pp.create_load(net, 3, p_mw = 1, q_mvar = 0.2, name = "Load-2")
        pp.create_sgen(net, 7, p_mw = 1, name = "StaticGen-2")

        pp.create_load(net, 4, p_mw = 1, q_mvar = 0.2, name = "Load-1")
        pp.create_sgen(net, 8, p_mw = 1, name = "StaticGen-1")

        pp.create_load(net, 5, p_mw = 1, q_mvar = 0.2, name = "Load-3")
        pp.create_sgen(net, 9, p_mw = 1, name = "StaticGen-3")

        pp.runpp(net, numba=False)
        pp.to_json(net, grid_file)
        
        if verbose:
                print("buses", net.bus)
                print("loads", net.load)
                print("sgens", net.sgen)
                print("ext_grid", net.ext_grid)
                print(f"Grid model was saved: {grid_file}")
        


if __name__ == '__main__':

        parser = argparse.ArgumentParser()
        parser.add_argument('--dir', default=None, type=str)
        parser.add_argument('--verbose', default=1, type=int)
        args = parser.parse_args()
        
        if args.dir == None:
                args.dir = os.path.dirname(__file__)
                print('dir:', args.dir)
        
        make_grid_model(**vars(args))