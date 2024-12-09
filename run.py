import os
import sys
import glob
import argparse
import itertools
import pandas as pd
from massca.utils import MAX_CONVERGENCE_ERROR



def run_scenarios(**kwargs):
    
    base_dir = kwargs.get('dir', './')
    use_os = kwargs.get('use_os', True) 
    verbose = kwargs.get('verbose', 1)
    
    alg = ['swarm'] # 'default', 'cohda', 
    data_dir = os.path.join(base_dir, 'data')
    results_dir = os.path.join(base_dir, 'results')

    STEPS = 1
    SEED = 13
    START_DATE = '2016-01-01 00:00:00'
    STEP_SIZE = 60*15
    END = STEPS * STEP_SIZE    
    
    ######## Refreshing grid model, profiles and results
    
    [os.remove(f) for f in glob.glob(results_dir+"/*.csv")]
    
    if use_os:
        os.system(f'python {os.path.join(base_dir, "hybit_grid_model.py")} --dir "{base_dir}" --verbose {verbose}')
        os.system(f'python {os.path.join(base_dir, "hybit_grid_profiles.py")} --dir "{base_dir}" --start "{START_DATE}" --end {END} --step {STEP_SIZE} --seed {SEED} --verbose {verbose}')
    else:
        from hybit_grid_model import make_grid_model
        make_grid_model(dir=base_dir, verbose=verbose)
        
        from hybit_grid_profiles import make_grid_profiles
        make_grid_profiles(dir=base_dir,
                           verbose=verbose,
                           start=START_DATE,
                           end=END,
                           step=STEP_SIZE,
                           seed=SEED)

    ######## Run scenario with different parameteres

    max_error = {}
    for i, j in itertools.product(alg, repeat=2):
        if (j == 'cohda') or (i == 'cohda'):
            max_error[(i, j)] = 1.0 # for COHDA as it is more flexible..
        else:
            max_error[(i, j)] = MAX_CONVERGENCE_ERROR
        
        if use_os:
            command = f'python {os.path.join(base_dir, "hybit_scenario.py")} --within {i} --between {j} --performance True --dir "{base_dir}" --start "{START_DATE}" --end {END} --step {STEP_SIZE} --max_error {max_error[(i, j)]} --verbose {verbose} --seed {SEED}'
            if verbose:
                print(command)
            os.system(command)
        else:
            if verbose:
                print(kwargs)
            from hybit_scenario import run_scenario
            run_scenario(dir=base_dir,
                         verbose=verbose,
                         within=i, between=j,
                         performance=True,
                         start=START_DATE,
                         end=END,
                         step=STEP_SIZE,
                         seed=SEED,
                         max_error=max_error[(i, j)])

    ####### Analysis part

    s = lambda x: f"{x:.3f}"
    prof_file = os.path.join(data_dir, 'grid_profiles.csv')
    profiles = pd.read_csv(prof_file, skiprows=1)

    for i, j in itertools.product(alg, repeat=2):
        f = os.path.join(results_dir, f"{i}_{j}_results.csv")
        if os.path.exists(f):
            df = pd.read_csv(f).rename(columns={
                'MASSCA-0.root_agent-steptime': 'steptime',
                'MASSCA-0.root_agent-convergence_attempts': 'convergence_attempts',
                'GridSim-0.ExternalGrid-0-value': 'ExternalGrid',
            })

            bus = {int(c.split('Bus-')[1].split('-')[0]) : c for c in df.columns if 'Bus' in c}
            sim = {int(c.split('FLSim-')[1].split('-')[0]) : c for c in df.columns if 'FLSim' in c} 
            load = {int(c.split('.value')[0].split('-')[1]) : c for c in profiles.columns if 'Load' in c and 'value' in c} 
            gen = {int(c.split('.value')[0].split('-')[1]) : c for c in profiles.columns if 'StaticGen' in c and 'value' in c}  
            agt = {int(c.split('Agent_')[1].split('-')[0]) : c for c in df.columns if 'Agent_' in c} 

            for (_, r), (_, p) in zip(df.iterrows(), profiles.iterrows()):
                print('step:', r['date'])
                print(f'within: {i}, between: {j}')
                
                # Loads
                print(sim[0], '=', s(r[sim[0]]), bus[2], '=', s(r[bus[2]]), agt[5], '=', s(r[agt[5]]), load[0], '=', s(p[load[0]]))
                print(sim[1], '=', s(r[sim[1]]), bus[3], '=', s(r[bus[3]]), agt[6], '=', s(r[agt[6]]), load[2], '=', s(p[load[2]]))
                print(sim[2], '=', s(r[sim[2]]), bus[4], '=', s(r[bus[4]]), agt[7], '=', s(r[agt[7]]), load[1], '=', s(p[load[1]]))
                print(sim[3], '=', s(r[sim[3]]), bus[5], '=', s(r[bus[5]]), agt[8], '=', s(r[agt[8]]), load[3], '=', s(p[load[3]]))
                print()
                
                # Gens
                print(sim[4], '=', s(r[sim[4]]), bus[6], '=', s(r[bus[6]]), agt[9], '=', s(r[agt[9]]), gen[0], '=', s(p[gen[0]]))
                print(sim[5], '=', s(r[sim[5]]), bus[7], '=', s(r[bus[7]]), agt[10], '=', s(r[agt[10]]), gen[2], '=', s(p[gen[2]]))
                print(sim[6], '=', s(r[sim[6]]), bus[8], '=', s(r[bus[8]]), agt[11], '=', s(r[agt[11]]), gen[1], '=', s(p[gen[1]]))
                print(sim[7], '=', s(r[sim[7]]), bus[9], '=', s(r[bus[9]]), agt[12], '=', s(r[agt[12]]), gen[3], '=', s(p[gen[3]]))
                
                sim_prod = abs(r[sim[4]] + r[sim[5]] + r[sim[6]] + r[sim[7]])
                bus_prod = abs(r[bus[6]] + r[bus[7]] + r[bus[8]] + r[bus[9]])
                agt_prod = abs(r[agt[9]] + r[agt[10]] + r[agt[11]] + r[agt[12]])

                sim_cons = abs(r[sim[0]] + r[sim[1]] + r[sim[2]] + r[sim[3]])
                bus_cons = abs(r[bus[2]] + r[bus[3]] + r[bus[4]] + r[bus[5]])
                agt_cons = abs(r[agt[5]] + r[agt[6]] + r[agt[7]] + r[agt[8]])

                print('sim_prod', s(sim_prod), 'bus_prod', s(bus_prod), 'agt_prod', s(agt_prod))
                print('sim_cons', s(sim_cons), 'bus_cons', s(bus_cons), 'agt_cons', s(agt_cons))

                sim_diff = sim_prod - sim_cons
                bus_diff = bus_prod - bus_cons
                agt_diff = agt_prod - agt_cons

                diff = r['ExternalGrid'] + sim_diff

                print('sim_diff', s(sim_diff), 'bus_diff', s(bus_diff), 'agt_diff', s(agt_diff))
                print('ExternalGrid', s(r['ExternalGrid']), 'total balance(', s(diff), ') <= 0.95')
                print()

                assert int(r['convergence_attempts']) == 2 # perfect case
                assert s(sim_prod) == s(bus_prod) == s(agt_prod)
                assert s(sim_cons) == s(bus_cons) == s(agt_cons)
                assert s(sim_diff) == s(bus_diff) == s(agt_diff)
                assert abs(diff) <= 1.0 # just out of blue
        else:
            raise AttributeError(f'No results for setup: within - {i}, between - {j}!')



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default=None, type=str)
    parser.add_argument('--use_os', default=False, type=bool)
    parser.add_argument('--verbose', default=1, type=int)
    args = parser.parse_args()    
    
    if args.dir == None:
        args.dir = os.path.dirname(__file__)
        sys.path.append(args.dir)
        print('dir:', args.dir)
    
    run_scenarios(**vars(args))