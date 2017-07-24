import os

#import necessary modules
import numpy as np
import netCDF4 as nc4
import sys

#This finds the user's current path so that all hdf4 files can be found
def readparamsFromFile(FILE_NAME, params):
    try:
        #read in the data
        merraData = nc4.Dataset(FILE_NAME, 'r')
        variables=set(merraData.variables)
        desiredVariables=set(params)
        desiredVariables=set([x.lower() for x in desiredVariables])
        var1=variables.intersection(desiredVariables)
        desiredVariables=set([x.upper() for x in desiredVariables])
        var2=variables.intersection(desiredVariables)
        fileVars=list(var1.union(var2))
        print('Saving the following SDS from current file: \n')
        [print('(' + str(fileVars.index(x)) + ')',x) for x in fileVars]

        #extract lat and lon info. These are just vectors in the dataset so they're repeated to accommodate the data array
        lats=merraData.variables['lat'][108:252]
        lons=merraData.variables['lon'][260:372]
        totalLon=np.tile(lons,len(lats))
        totalLat=lats.repeat(len(lons))
        #create a matrix the same size as the lat/lon datasets to save everything
        output=np.zeros((totalLat.shape[0],len(fileVars)+2))
        output[:,0]=totalLat
        output[:,1]=totalLon
        #can't combine string and floats in an array, so a list of titles is made
        tempOutput=[]
        tempOutput.append('Latitude')
        tempOutput.append('Longitude')
        index=2
        for SDS_NAME in fileVars:
            try:
                #read merra data as a vector
                data=merraData.variables[SDS_NAME][:]
            except:
                print('There is an issue with your MERRA file (might be the wrong MERRA file type). Skipping...')
                continue
            if len(data.shape) ==4:
                level=data.shape[1]-1
                data=data[0,level,108:252,260:372]
            elif len(data.shape) == 3:
                level=data.shape[0]-1
                data=data[level,108:252,260:372]
            data=data.ravel()
            #save variable
            output[:,index]=data
            tempOutput.append(SDS_NAME)
            index+=1
        #stacks the titles on the data array to be saved to file
        output=np.row_stack((tempOutput,output))
        #create the name of the file from the filename
        outputName='{0}.txt'.format(FILE_NAME[:-4])
        #save the file
        np.savetxt(outputName,output,delimiter=',',fmt='%s')
    except:
        pass

for year in range(1997, 2002):
    for month in range(1, 13):
        for day in range(1, 32):
            try:
                month = str(month).zfill(2)
                day = str(day).zfill(2)
                year = str(year)
                url = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2SDNXSLV.5.12.4/' + year + '/' + month + '/MERRA2_200.statD_2d_slv_Nx.' + year + month + day + '.nc4'
                filename = 'MERRA2_200.statD_2d_slv_Nx.' + year + month + day + '.nc4'
                os.system('wget --user=barakyaari --password=malariaPass1 ' + url)
                readparamsFromFile(filename, {"T2MMAX", "T2MMIN", "T2MMEAN"})
                os.system('rm ' + filename)
            except:
                pass


