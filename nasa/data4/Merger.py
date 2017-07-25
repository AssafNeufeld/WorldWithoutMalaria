from os import listdir
from os.path import isfile, join
import sys
import re

#sys.argv=["Merger.py", "c:\\malaria" ,"19980101", "19980104"]
path = sys.argv[1]
startDate = sys.argv[2]
endDate = sys.argv[3]

print("Merging directory " +path + "between " + startDate + " and " + endDate)
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

groups = {}
for f in onlyfiles:
    m = re.search("MERRA2_[0-9]00.(.*)_2d_slv_Nx.([0-9]{4})([0-9]{4}).txt", f)
    if m is None:
        continue
    type = m.group(1)
    year = m.group(2)
    day = m.group(3)
    yd= year+day
    if yd < startDate or yd > endDate:
        continue

    if groups.get(year) is None:
        groups[year]={}
    yearGroup = groups[year]
    if yearGroup.get(day) is None:
        yearGroup[day] = {}
    yearGroup[day][type] = f


for year, dic in groups.items():
    print("Merging year " + year)
    firstLineInYear = True
    with open(year + '.txt', 'w') as outFile:
        for day, data in dic.items():
            firstLineInDay = True
            sdate = [year + "-" + day[:2] + "-" + day[2:]]
            if data.get("tavg1") is None or data.get("statD") is None:
                continue
            with open(join(path, data["tavg1"]),'r') as tavg1:
                with open(join(path, data["statD"]), 'r') as statD:
                    for line in tavg1:
                        sRow = statD.readline().strip('\n').split(',')
                        tRow = line.strip('\n').split(',')
                        out = sdate + [str(e) for e in sRow + tRow[2:]]
                        s=','.join(out)+'\n'
                        if firstLineInDay:
                            if firstLineInYear:
                                outFile.write(s)
                                firstLineInYear=False

                            firstLineInDay = False
                            continue
                        outFile.write(s)
