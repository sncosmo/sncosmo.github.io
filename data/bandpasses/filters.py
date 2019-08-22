import glob,os,sys,sncosmo
from astropy.table import Table
import numpy as np

try:
	sncosmo.get_bandpass('asdf')
except Exception as e:
	bandlist=str(e)

bandlist=[x.strip() for x in bandlist[bandlist.rfind('names:')+7:].split(',')]
bandlist=[x.strip("'") for x in bandlist]


for folder in ['UVIS',"IR"]:
	files=glob.glob(os.path.join('/Users','jpierel','Downloads',folder,'*.csv'))
	for filename in files:
		band=os.path.basename(filename)[:os.path.basename(filename).find('_')]
		if band.lower() not in bandlist and 'm' not in band.lower() and 'w' not in band.lower() and 'lp' not in band.lower():
			print(band)
			continue
		dat=Table.read(filename)
		dat.remove_column('col0')
		if folder=='UVIS':
			dat['Wavelength']=np.average([dat['Chip 1 Wave (Angstroms)'],dat['Chip 2 Wave (Angstroms)']],axis=0)
			dat['Throughput']=np.average([dat['Chip 1 Throughput'],dat['Chip 2 Throughput']],axis=0)
			dat.remove_column('Chip 1 Wave (Angstroms)')
			dat.remove_column('Chip 1 Throughput')
			dat.remove_column('Chip 2 Wave (Angstroms)')
			dat.remove_column('Chip 2 Throughput')
		minind=np.min(np.where(dat['Throughput']>0)[0])
		maxind=np.max(np.where(dat['Throughput']>0)[0])
		dat=dat[minind-1:maxind+2]
		with open(os.path.join('wfc3-'+folder.lower(),band.lower()+'.tab'),'w') as f:
			f.write('# STSCI '+folder+' Throughput data from http://www.stsci.edu/hst/instrumentation/wfc3/performance/throughputs\n')
			f.write('# Downloaded 08/22/2019\n')
			f.write('# Wavelength (Angstrom) Throughput (0-1)\n')
			for row in dat:
				f.write(' '.join([str(x) for x in row])+'\n')
		#dat.write('test.dat',format='ascii',overwrite=True)
		#sys.exit()