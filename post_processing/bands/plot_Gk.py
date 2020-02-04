#!/usr/bin/env python

from scipy import *
import matplotlib
matplotlib.use('ps')
from matplotlib.font_manager import fontManager, FontProperties
from pylab import *
import scipy.interpolate
import re
import matplotlib.pyplot as plt
import numpy as np

vmm = [0,10]
nk=0
SKP=[]
SKPoints=[]
distk=[]
kpts=[]
fi=open('klist.dat','r')
for line in fi.readlines():
   line=line.split()
   distk.append(float(line[0]))
   kpts.append([float(line[1]),float(line[2]),float(line[3])])
   if len(line)==5:
      SKP.append(float(line[0]))
      SKPoints.append(line[4])
fi.close() 

fi=open('ksum.input','r')
numk=int(fi.readline())
print("numk=",numk)
nom=int(fi.readline())
print("nom=",nom)
fi.close()
A_k=[]
dist_k=[]
om=[]
kpts=[]
fi=open('Gk.out','r')
for i in range(numk):
   kpts.append(list(map(float,fi.readline().split()[1:])))
   A_k.append([]) 
   om.append([]) 
   for j in range(nom):
      line=list(map(float,fi.readline().split()))
      A_k[i].append(-1*line[2]/3.14159265)
      om[i].append(line[0])
   A_k[i]=np.array(A_k[i])
fi.close()

A_k=np.transpose(A_k)[::-1]

(ymin,ymax) = (om[0][0],om[0][-1])
(xmin,xmax) = (distk[0],distk[-1])

im=plt.imshow(A_k,cmap=cm.hot, vmin=vmm[0], vmax=vmm[1], extent=[xmin,xmax,ymin,ymax],aspect='auto')
colorbar(im,orientation='vertical',pad=0.05,shrink=1.0,ticks=arange(0,10.0,1.0))
xticks(SKP,SKPoints)
xlabel('k-path',fontsize='xx-large')
ylabel('Energy',fontsize='xx-large')
axhline(y=0,color='black',ls='--')

show()
savefig('A_k.eps')



