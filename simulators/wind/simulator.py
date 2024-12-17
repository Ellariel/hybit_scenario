"""
@author: original from Fernando Penaherrera and modified by Christoph Stucke and Malte Trauernicht
https://gitlab.com/mosaik/components/energy/mosaik-wind/-/blob/basic_structure/mosaik_components/wind/Simulator.py?ref_type=heads
"""
import mosaik_api_v3
import simulators.wind.wt as wt
import itertools

meta = {
    'models': {
        'WT': {
            'public': True,
            'params': [  # Define the parameters of the related class
                'max_power',  # Max Rated Power
                'power_curve', # Path to pover curve CSV file
            ],
            'attrs': ['P_gen',  # Generated Instant Power
                      'wind_speed',  # Instant Wind Speed
                      ]
        }
    }
}


class Simulator(mosaik_api_v3.Simulator):
    """
    Simulator for the wind turbine
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__(meta)  # Initialise the inherited simulator
        self.sid = None
        self.gen_neg = False
        self.cache = None
        self._entities = {}
        self.eid_counters = {'WT': itertools.count()}
        self.csv_path = ''
        self.step_size = None

    def init(self, sid, time_resolution, power_curve_csv=None, step_size=None, gen_neg=False):
        self.sid = sid
        self.csv_path = power_curve_csv
        if step_size is not None:
            self.step_size = step_size
        else:
            raise RuntimeError('no step size (in seconds) is provided!')
        self.gen_neg = gen_neg
        return self.meta

    def create(self, num, model, **model_params):
        entities = []

        max_power = model_params.get('max_power', 0.1)
        power_curve = model_params.get('power_curve', self.csv_path)
        if power_curve is None:
            raise RuntimeError('no csv data for power curve is given!')

        for i in range(num):
            eid = '%s_%s' % (model, next(self.eid_counters.get('WT')))
            self._entities[eid] = wt.WindTurbine(max_power=max_power, path=power_curve)
            entities.append({'eid': eid, 'type': model, 'rel': []})
        return entities

    def step(self, t, inputs, max_advance):
        self.cache = {}
        for eid, attrs in inputs.items():
            for attr, vals in attrs.items():
                if attr == "wind_speed":
                    wind_speed = list(vals.values())[0]
                    self.cache[eid] = self._entities[eid].power_out(wind_speed)
                    if self.gen_neg:
                        self.cache[eid] *= -1
        return t + self.step_size

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            if eid not in self._entities.keys():
                raise ValueError("Unknown entity ID {}".format(eid))

            data[eid] = {}
            for attr in attrs:
                if attr != "P_gen":
                    raise ValueError("Unknown output attribute {}".format(attr))
                data[eid][attr] = self.cache[eid]
        return data


def main():
    mosaik_api_v3.start_simulation(Simulator(), "Simulator")


if __name__ == '__main__':
    main()
