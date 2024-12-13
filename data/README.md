## Data description

There are three CSV profiles of electricity consumption by conventional (electric arc based) full cycle steel manufacturing plants located in South Korea. The total electricity consumption timeseries are available in kW (scaled to 1.15 TW, total per year), with a time interval of 15 minutes:

- profileA_1.15TW.csv
- profileB_1.15TW.csv
- profileС_1.15TW.csv

```python
Time,P[kW]
2018-01-01 00:00:00,4098.425955380552
2018-01-01 00:15:00,3798.833414782559
2018-01-01 00:30:00,4793.480649567898
...
```

## Data preparation
Profiles *A* and *B* initially covered the period from March 1 to September 30, 2019, and were extended by us for the entire year using a normal distribution that preserves weekly consumption patterns. The *C* profile covers all of 2018.

The data preparation pipline is in the file *steel_plant_profiles.ipynb*

Since we have no information about the technology used in these plants, we can only be guided by the information from the original paper (Lee et al., 2021), which says that these are conventional steel manufacturing plants using electric arc and not using DRI.

<img src="https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41597-022-01357-8/MediaObjects/41597_2022_1357_Fig7_HTML.png" alt="Steel manufacturing process" width="300px"/>

## Data sources and references

1. Lee, E., Baek, K. & Kim, J. (2022). Datasets on South Korean manufacturing factories’ electricity consumption and demand response participation. Scientific Data, 9, 227. https://doi.org/10.1038/s41597-022-01357-8 https://doi.org/10.6084/m9.figshare.14822256.v9 https://figshare.com/ndownloader/files/34134648

2. Sathishkumar, V.E., Shin, C., & Cho, Y. (2023). Steel Industry Energy Consumption. UCI Machine Learning Repository. https://doi.org/10.24432/C52G8C https://archive.ics.uci.edu/dataset/851/steel+industry+energy+consumption

3. Sathishkumar, V.E., Shin, C., & Cho, Y. (2020). Efficient energy consumption prediction model for a data analytic-enabled industry building in a smart city. Building Research & Information, 49(1), 127–143. https://doi.org/10.1080/09613218.2020.1809983