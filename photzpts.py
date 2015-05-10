import glob
import numpy as np
import pandas as pd

#get a listing of the files suzane made that have the photometric zero points
#i saved them locally under /home/ih64/Desktop/PhotResults
#the ones I computed are there too, but they are put together in the ipython notebook
suzpts=glob.glob('/home/ih64/Desktop/PhotResults/RESULTS.200[6-9]_*')+glob.glob('/home/ih64/Desktop/PhotResults/RESULTS.201[0-1]_*') + glob.glob('/home/ih64/Desktop/PhotResults/RESULTS.2012_0[0-6]')

rowdict={'date':[], 'star':[], 'b':[], 'v':[],'r':[],'i':[],
	'cb':[],'cv':[],'cr':[],'ci':[],
	'xb':[],'xv':[],'xr':[],'xi':[]}

headerdelim='======================================================================================================================='

for month in suzpts:
	#they're not super machine-readable-friendly, we have to take them apart and yank out what we need
	with open(month,'r') as f:
		text=f.read()

	#header info is in the first two sections above the delimiter
	data=text.split(headerdelim)[2]

	#each date is broken up by a long string of hyphens
	dates=data.split('-----------------------------------------------------------------------------------------------------------------------')

	#go up to the second to last element in the list dates, the last one is just an empty string
	for day in dates[0:-2]:
		words=day.strip().split()
		if words[0][0:2]=='20':
			rowdict['date'].append(float(words[0][2:]))
			rowdict['star'].append(words[1])
			rowdict['b'].append(words[2])
			rowdict['v'].append(words[3])
			rowdict['r'].append(words[4])
			rowdict['i'].append(words[5])
			rowdict['xb'].append(words[6])
			rowdict['xv'].append(words[7])
			rowdict['xr'].append(words[8])
			rowdict['xi'].append(words[9])
			rowdict['cb'].append(words[10])
			rowdict['cv'].append(words[11])
			rowdict['cr'].append(words[12])
			rowdict['ci'].append(words[13])

#shove all the data into a pandas dataframe
table=pd.DataFrame(rowdict)
#force the datatype for the dates to be ints, they were made from strings to floats above
table['date']=table['date'].values.flatten().astype(int)
#the mirror was cleaned on 110921, this note sneaks in and screws up the data frame
table=table.drop(table[table['date']==110921].index)
#suzane filled in the string 'na' if the data was not determined. change these to np NaNs in our dataframe
table=table.replace('na',np.nan)
#sometimes the string '---' was used if the data were not determined, swap these out for nans too
table=table.replace('---',np.nan)
table=table.replace('----',np.nan)
#finally, sometimes 0.0 were used if the data were not determined
table=table.replace(0.0,np.nan)
#foce the datatype for the values to floats, they are currently strings.
table[['b','v','r','i','xb','xv','xr','xi','cb','cv','cr','ci']]=table[['b','v','r','i','xb','xv','xr','xi','cb','cv','cr','ci']].astype(float)
#the extinction coef for V was .14 before 200905 and .144 after
def excoefV(date):
    if date < 90500:
        return .14
    else:
        return .144
table['excoefV']=table['date'].apply(lambda x: excoefV(x))
#likewise the extinction coef for I was .066 before 200905 and .056 after
def excoefI(date):
    if date < 90500:
        return .066
    else:
        return .056
table['excoefI']=table['date'].apply(lambda x: excoefI(x))
table.to_pickle('suzpts')
table.to_csv('suzpts.csv')