from __future__ import annotations

from os.path import abspath
from pathlib import Path
from pysimmods.mosaik.pysim_mosaik import PysimmodsSimulator, META
import copy
import pandas as pd
import arrow, os
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple
import mosaik_api_v3 as mosaik_api
from mosaik_api_v3.types import (
    CreateResult,
    CreateResultChild,
    Meta,
    ModelDescription,
    OutputData,
    OutputRequest,
)

class Simulator(PysimmodsSimulator):

    def __init__(self):
        super().__init__()
        self.cached_inputs = {}
        self.cached_outputs = {}
        #self.inputs = {}
        self.previous_timestep = -1
        self.current_timestep = 0
        self.max_advance = 0
        self.meta["type"] = "event-based"

    def step(
        self,
        time: int,
        inputs: Dict[str, Dict[str, Dict[str, Any]]],
        max_advance: int = 0,
    ):
        print('Battery step:', time, inputs)
        self.cached_inputs = copy.deepcopy(inputs)
        # {'Ctrl-0': {'P[MW]': {'SteelPlantSim.SteelPlant_0': 9.259042859671064}}}
        #print('ctrl step:', time)
        #for eid, attrs in inputs.items():
        #    for attr, values in attrs.items():     
        #        if self.current_timestep != time: # first timestep
        #            if attr == 'p_set_mw':
        #                _inputs[eid][attr] = {k: 0 for k, v in values.items()}
        #print(self.meta)
        #self.cached
        self.current_timestep = time
        self.max_advance = max_advance
        super().step(time, inputs, self.max_advance)
        return time + self.step_size

    def get_data(self, outputs: OutputRequest) -> OutputData:
        #_outputs = copy.deepcopy(outputs)
        #
        #for eid in outputs.keys():
        #    _outputs[eid] = ["p_mw", "soc_percent"]
        print('battery get data')
                
        
        #data = {}
        if self.current_timestep != self.previous_timestep:
            print('battery first step')
            self.cached_outputs = super().get_data(outputs)
            #for eid, attrs in outputs.items():
            #data.setdefault(eid, {})
            #    for attr in attrs:
            #        if attr == 'p_mw':
                    #data[eid][attr] *= -1
                    
                        
            for eid, attrs in self.cached_inputs.items():
                for attr, values in attrs.items():     
                    if attr == 'p_set_mw':
                        print(self.cached_inputs)
                        self.cached_inputs[eid][attr] = {k: 0.0 for k, v in values.items()}
                        print(self.cached_inputs)
            super().step(self.current_timestep, self.cached_inputs, self.max_advance)
        self.previous_timestep = self.current_timestep

                

        return self.cached_outputs

        

