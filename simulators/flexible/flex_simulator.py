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
        "FLSim": {
            "public": True,
            "any_inputs": True,
            "trigger" : ['delta_signal'],
            "attrs": ["P[MW]",           # input/output active power [MW]
                      'delta_signal'],   # input of modifier from ctrl
        }
    },
}

STEP_SIZE = 60*15 
CACHE_DIR = Path(abspath(__file__)).parent
DATE_FORMAT = "YYYY-MM-DD HH:mm:ss"

class Simulator(mosaik_api.Simulator):
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
    
    def init(self, sid: str, time_resolution: float = 1, step_size: int = STEP_SIZE, csv_file = None, sim_params: Dict = {}):
        self.gen_neg = sim_params.get('gen_neg', False)
        self.date = arrow.get(sim_params.get('start_date', '2016-01-01 00:00:00'), DATE_FORMAT)

        self.csv_file = None
        if csv_file and os.path.exists(csv_file):
            self.csv_file = pd.read_csv(csv_file, compression='zip')
            self.csv_file['Time'] = pd.to_datetime(self.csv_file['Time'], format='mixed', utc=True)
            self.csv_file.set_index('Time',inplace=True)

        self.time_resolution = time_resolution
        self.step_size = step_size
        self.current_time = -1
        self.sid = sid
        self.entities = {}
        self.delta_signal = {}
        return self.meta

    def create(self, num: int, model: str, **model_params: Any) -> List[CreateResult]:
        entities = []
        for n in range(len(self.entities), len(self.entities) + num):
            eid = f"{model}-{n}"
            self.entities[eid] = 0
            self.delta_signal[eid] = 0 # Default value

            if isinstance(self.csv_file, pd.DataFrame):
                self.entities[eid] = self.csv_file[eid]

            entities.append({
                "eid": eid,
                "type": model,
            })
        return entities
    
    def _get_data(self, eid, attr):
        if attr == 'delta_signal':
            return self.delta_signal[eid]
        
        if isinstance(self.entities[eid], pd.Series):
            idx = self.entities[eid].index.get_indexer([self.date.datetime], method='ffill')[0]
            result = self.entities[eid].iloc[idx]
        else:
            result = self.entities[eid]

        result += self.delta_signal[eid]

        if self.gen_neg:
            result = abs(result) * (-1)

        return result

    def step(self, time, inputs, max_advance):
        if self.current_time > -1 and self.current_time != time:
            self.date = self.date.shift(seconds=self.step_size)
            self.delta_signal = {k: 0 for k, v in self.delta_signal.items()}               
        self.current_time = time
        for eid, attrs in inputs.items():
            for attr, values in attrs.items():
                v = sum(values.values())
                if attr == 'P[MW]':
                    if not isinstance(self.entities[eid], pd.Series):
                        self.entities[eid] = v
                elif attr == 'delta_signal':
                    self.delta_signal[eid] = v
                else:
                    pass

        return time + self.step_size
     
    def get_data(self, outputs: OutputRequest) -> OutputData:
        return {eid: {attr: self._get_data(eid, attr) 
                            for attr in attrs
                                } for eid, attrs in outputs.items()}
    
def main():
    """Run our simulator"""
    return mosaik_api.start_simulation(Simulator(), 'Flexible Load/Gen Simulator')

if __name__ == '__main__':
    main()