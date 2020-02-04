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

vmm = [0,5.0]
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
print "numk=",numk
nom=int(fi.readline())
print "nom=",nom
fi.close()
A_k=[]
dist_k=[]
om=[]
kpts=[]
fi=open('Gk_up.out','r')
for i in range(numk):
   kpts.append(map(float,fi.readline().split()[1:]))
   A_k.append([]) 
   om.append([]) 
   for j in range(nom):
      line=map(float,fi.readline().split())
      A_k[i].append(-1*line[2]/3.14159265)
      om[i].append(line[0])
   A_k[i]=np.array(A_k[i])
fi.close()
A_k=np.transpose(A_k)[::-1]

#for 2nd dataset
A_k2=[]
dist_k2=[]
om2=[]
kpts2=[]
fi=open('Gk_dn.out','r')
for i2 in range(numk):
   kpts2.append(map(float,fi.readline().split()[1:]))
   A_k2.append([]) 
   om2.append([]) 
   for j2 in range(nom):
      line2=map(float,fi.readline().split())
      A_k2[i2].append(-1*line2[2]/3.14159265)
      om2[i2].append(line[0])
   A_k2[i2]=np.array(A_k2[i2])
fi.close()
A_k2=np.transpose(A_k2)[::-1]

#for 3rd dataset (non spin polarized)
A_k3=[]
dist_k3=[]
om3=[]
kpts3=[]
fi=open('Gk.out','r')
for i3 in range(numk):
   kpts3.append(map(float,fi.readline().split()[1:]))
   A_k3.append([]) 
   om3.append([]) 
   for j3 in range(nom):
      line3=map(float,fi.readline().split())
      A_k3[i3].append(-1*line3[2]/3.14159265)
      om3[i3].append(line3[0])
   A_k3[i3]=np.array(A_k3[i3])
fi.close()
A_k3=np.transpose(A_k3)[::-1]

(ymin,ymax) = (om[0][0],om[0][-1])
(xmin,xmax) = (distk[0],distk[-1])

#subplots
fig = plt.figure()
#no spin
a = fig.add_subplot(1,3,1)
im3=plt.imshow(A_k3,cmap=cm.hot,vmin=vmm[0], vmax=vmm[1], extent=[xmin,xmax,ymin,ymax],aspect='auto' )
a.set_title('No Spin')
#colorbar(im2,orientation='vertical',pad=0.05,shrink=1.0,ticks=arange(0,10.0,1.0))
xticks(SKP,SKPoints)
#xlabel('k-path',fontsize='xx-large')
#ylabel('Energy',fontsize='xx-large')
axhline(y=0,color='black',ls='--')

#spin up
a = fig.add_subplot(1,3,2)
im=plt.imshow(A_k,cmap=cm.hot, vmin=vmm[0], vmax=vmm[1], extent=[xmin,xmax,ymin,ymax],aspect='auto')
a.set_title('Spin Up')
#colorbar(im,orientation='vertical',pad=0.05,shrink=1.0,ticks=arange(0,10.0,1.0))
xticks(SKP,SKPoints)
#xlabel('k-path',fontsize='xx-large')
#ylabel('Energy',fontsize='xx-large')
axhline(y=0,color='black',ls='--')


#spin down
a = fig.add_subplot(1,3,3)
im2=plt.imshow(A_k2,cmap=cm.hot,vmin=vmm[0], vmax=vmm[1], extent=[xmin,xmax,ymin,ymax],aspect='auto' )
a.set_title('Spin Down')
#colorbar(im2,orientation='vertical',pad=0.05,shrink=1.0,ticks=arange(0,10.0,1.0))
xticks(SKP,SKPoints)
#xlabel('k-path',fontsize='xx-large')
#ylabel('Energy',fontsize='xx-large')
axhline(y=0,color='black',ls='--')



#ax1=subplot(111)
#for i in range(18,shape(eigval0)[1]):
#   ax1.plot(k_eig,eigval0[:,i]-7.22220722842 ,color='green')
##ax1.plot([k_eig[319],k_eig[319]], [ymin,ymax], 'w-')
#xticks([0,1,2],['$\Gamma$','X','M'])


# Set common labels
fig.text(0.45, 0.04, 'k-path', ha='center', va='center')
fig.text(0.06, 0.5, 'Energy', ha='center', va='center', rotation='vertical')

#common colorbar
fig.subplots_adjust(right=0.8)
cbar_ax=fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im2,orientation='vertical',pad=0.05,shrink=1.0,ticks=arange(0,10.0,1.0),cax=cbar_ax)

show()
savefig('A_k_all.eps')
exit()


