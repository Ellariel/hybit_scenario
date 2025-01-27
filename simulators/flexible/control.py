from __future__ import annotations

from os.path import abspath
from pathlib import Path
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

META = {
    "api_version": "3.0",
    "type": "hybrid",
    "models": {
        "Ctrl": {
            "public": True,
            "any_inputs": True,
            "any_outputs": True,
            "attrs": []
        }
    },
}

STEP_SIZE = 60*15 

class CtrlSimulator(mosaik_api.Simulator):
    _sid: str
    """This simulator's ID."""
    _step_size: Optional[int]
    """The step size for this simulator. If ``None``, the simulator
    is running in event-based mode, instead.
    """
    sim_params: Dict
    """Simulator parameters specification:
    SIM_PARAMS = {
        'start_date' : '2016-01-01 00:00:00',
        'gen_neg' : True,
    } 
    """

    def __init__(self) -> None:
        super().__init__(META)
    
    def init(self, sid: str, time_resolution: float = 1, step_size: int = STEP_SIZE, sim_params: Dict = {}):
        self.gen_neg = sim_params.get('gen_neg', False)
        self.scenario_type = sim_params.get('scenario_type', 'A')
        self.time_resolution = time_resolution
        self.step_size = step_size
        self.sid = sid
        self.cache = {}
        self.meta["models"]["Ctrl"]["attrs"] += sim_params.get('ctrl_attributes', [])
        return self.meta

    def create(self, num: int, model: str, **model_params: Any) -> List[CreateResult]:
        entities = []
        for n in range(len(self.cache), len(self.cache) + num):
            eid = f"{model}-{n}"
            self.cache[eid] = {}
            entities.append({
                "eid": eid,
                "type": model,
            })
        return entities
    
    def control(self):
        print(self.cache)
        

        result = 0

        if self.gen_neg:
            result = abs(result) * (-1)

        return result

    def step(self, time, inputs, max_advance):
        # {'Ctrl-0': {'P[MW]': {'SteelPlantSim.SteelPlant_0': 9.259042859671064}}}
        for eid, attrs in inputs.items():
            for attr, values in attrs.items():              
                self.cache[eid][attr] = sum(values.values())
        self.control()
        return time + self.step_size
     
    def get_data(self, outputs: OutputRequest) -> OutputData:
        return {eid: {attr: self.cache[eid][attr]
                            for attr in attrs
                               } for eid, attrs in outputs.items()}
