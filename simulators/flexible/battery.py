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

class BatterySimulator(PysimmodsSimulator):

    def __init__(self):
        super().__init__(META)
        self.cached_inputs = {}

    def step(
        self,
        time: int,
        inputs: Dict[str, Dict[str, Dict[str, Any]]],
        max_advance: int = 0,
    ):
        self.cached_inputs = copy.deepcopy(inputs)
        super().step(time, inputs, max_advance)

    def get_data(self, outputs: OutputRequest) -> OutputData:
        _outputs = copy.deepcopy(outputs)

        for eid in outputs.keys():
            _outputs[eid] = ["p_mw", "soc_percent"]
                
        _data = super().get_data(_outputs)
        data = {}

        for eid, attrs in outputs.items():
            data.setdefault(eid, {})
            for attr in attrs:
                if attr == 'p_mw':
                    data[eid][attr] = _data[eid][attr] * (-1)
                elif attr == 'soc_percent':
                    data[eid][attr] = _data[eid][attr]
                elif attr == 'soc_mw':
                    data[eid][attr] = 0
                elif attr == 'dp_mw':
                    data[eid][attr] = 0
                else:
                    pass

        return data

        

