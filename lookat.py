from astropy.io import fits
import glob
from matplotlib.colors import LogNorm
from IPython import get_ipython
ipython=get_ipython()

ipython.magic('pylab')

path='/home/ih64/Desktop/NovaMusca/fitsimages/Iband/'
images= glob.glob(path+'*.fits')

with open('weirdos.txt','w') as f:
	for image in images:
		hdu_list=fits.open(image)
		image_data=hdu_list[0].data
		hdu_list.close()
		imshow(image_data, cmap='gray', norm=LogNorm())
		print(image.split('/')[-1])
		print('does this look weird or OK?')
		response=input('press 1 for weird, 2 to view next image, or 3 to quit')
		if response==1:
			f.write(image+' ')
		elif response==2:
			pass
		elif response==3:
			break
		else:
			print('your response was not recognized. Please try again')
			response=input('press w for weird, n to view next image, or q to quit')