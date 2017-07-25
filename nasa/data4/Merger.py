from os import listdir
from os.path import isfile, join
import sys
import re

# path = sys.argv[1]
path = 'C:\\Barak\\WorldWithoutMalaria\\nasa\\example_data'

m = re.search("MERRA2_300.(.*)_2d_slv_Nx.([0-9]{4})([0-9]{4}).txt", "MERRA2_300.statD_2d_slv_Nx.20041207.txt")
type = m.group(1)
year = m.group(2)

print("Merging directory " +path)
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

groups = {}
for f in onlyfiles:
    m = re.search("MERRA2_[0-9]00.(.*)_2d_slv_Nx.([0-9]{4})([0-9]{4}).txt", f)
    if m is None:
        continue
    type = m.group(1)
    year = m.group(2)
    day = m.group(3)
    if groups.get(year) is None:
        groups[year]={}
    yearGroup = groups[year]
    if yearGroup.get(day) is None:
        yearGroup[day] = {}
    yearGroup[day][type] = f


for year, dic in groups.items():
    print("Merging year " + year)
    with open(year + '.txt', 'a') as outFile:
        for day, data in dic.items():
            sdate = [year + "-" + day[:2] + "-" + day[2:]]
            with open(join(path, data["tavg1"]),'r') as tavg1:
                with open(join(path, data["statD"]), 'r') as statD:
                    for line in tavg1:
                        sRow = statD.readline().split(',')
                        tRow = line.split(',')
                        out = sdate + [str(e) for e in sRow + tRow[2:]]
                        s=','.join(out)
                        outFile.write(s)
