"""
The WindData Files dowloaded from DWD are beeing prepared for usage as wind-speed input for the wind simulator.
"""
import csv

delimiter = ','

# specify the path to the datafile to be read and determine row count
datafile_path = '../../data/WDforPV-2301-01.csv'
in_file = open(datafile_path)
row_count = sum(1 for eor in in_file)
print(row_count)

# open the file for reading
datafile = open(datafile_path)
header = next(datafile).strip().split(delimiter)
columns = next(datafile).strip().split(delimiter)
print(header)

# specify and open the datafile to be written
newfile_path = '../../data/WDforPV-2301-01_Oldenburg.csv'
title = ['WeatherData']
header = ['Date','t_air_deg_celsius','bh_w_per_m2','dh_w_per_m2']

with open(newfile_path, 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(title)
    filewriter.writerow(header)

    # loop through rows of existing datafile to add date and temp+solar-data to new file
    days = 31  # how many days should be extracted?
    row_count = 1 + 144 * days
    for xi in range(1, row_count):
        nextRow = next(datafile).strip().split(delimiter)
        oldDate = str(nextRow[0])
        #year = '2022'
        year = oldDate[6:10]
        month = oldDate[3:5]
        day = oldDate[0:2]
        hour = oldDate[11:13]
        minute = oldDate[14:16]
        date = year+'-'+month+'-'+day+' '+hour+':'+minute+':00'

        t_air = nextRow[1]
        bh_w = nextRow[2]
        dh_w = nextRow[3]

        newRow = [date, t_air, bh_w, dh_w]  # combine date, air temperature and solar data to a new row
        filewriter.writerow(newRow)  # & add thew new row







# make a new variable - c - for Python's CSV reader object -
#c = csv.reader(csvfile)

# read whatever you want from the reader object
# print it or use it any way you like
#for row in c:
#    print( row[1] + ", " + row[5])

# save and close the file
datafile.close()
