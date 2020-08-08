import numpy as np
from scipy.ndimage import imread
import matplotlib.pyplot as plt

def si1(xl,xr,a,b,ds):     ################# psi(Xs)
	sigma = 1
	res = np.exp((-1./(2*sigma**2))*(xl[i][j]-xr[i][j+ds])**2)
	return res


def si2(ds,dt):           ################## psi(Xs,Xt)
	gama = 1
	delta = 1
	res = np.exp((-1./(2*gama**2))*np.min(((ds-dt)**2,delta**2)))
	return res


def calcmarg(xl,xr,a,b):	################### marginal calculation
	res = np.empty(10)
	k = 1
	for ds in range(0,10):
		total = np.zeros(4)
		temp = si1(xl,xr,a,b,ds)

		for dt in range(0,10): 
			total[0]+= si2(ds,dt)*si1(xl,xr,a+1,b+ds,dt)
		
		for dt in range(0,10): 
			total[1]+= si2(ds,dt)*si1(xl,xr,a,b+ds+1,dt)
		
		for dt in range(0,10): 
			total[2]+= si2(ds,dt)*si1(xl,xr,a,b+ds-1,dt)
		
		for dt in range(0,10): 
			total[3]+= si2(ds,dt)*si1(xl,xr,a-1,b+ds,dt)
		m = k*np.prod(total)
		res[ds] = temp*m
	return res

xl = imread('bwleft.jpg')
xl = xl/255.0
xr = imread('bwright.jpg') 
xr = xr/255.0
N = 200  #################### TAKING 200 PIXELS LENGTH AND BREADTH
res = np.empty([N,N])
n1 = (256-N)/2

for i in range(n1,n1+N):
	for j in range(n1,n1+N):
		mu = calcmarg(xl,xr,i,j)
		res[i-n1][j-n1] = np.argmax(mu)
	print(i-n1)
plt.imshow(res,cmap=plt.cm.gray)
plt.show()


