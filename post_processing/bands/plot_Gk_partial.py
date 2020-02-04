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


#inputs
wan_orbs=[4]

#wan_orbs=[xxx+1 for xxx in range(28)]

#################################
vmm = [0,10]
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

fi_gk=open('Gk_partial.out','r')
data=re.findall('k=\s*[0-9E+-.\sorb=\s]*',fi_gk.read())
fi_gk.close()
filtered_orbs=[]
  
for i in range(numk):    
   #kpts.append(list(map(float,data[i].split('\n')[0].split()[1:]))) 
         
   
   for orbs in wan_orbs:          
       filtered_orbs.append(data[i].split('\n')[1:][(orbs-1)*nom+orbs:orbs*nom+orbs])
       
for orb_counter in range(numk*len(wan_orbs)):
   for j in range(nom): 
       A_k.append(-1*float(filtered_orbs[orb_counter][j].split()[2])/3.14159265)
       om.append(float(filtered_orbs[orb_counter][j].split()[0]))

A_k=np.array(A_k)
A_k=A_k.reshape(numk,nom*len(wan_orbs))     

#method 1
#A_k=np.transpose(A_k)[::-1]

#method 2 & 3
A_kblend=np.zeros((len(wan_orbs),numk,nom))
A_ktotal=np.zeros((numk,nom))

nom_counter=0
for orb in range(len(wan_orbs)):
    A_kblend[orb,:,:] = A_k[:,nom_counter:nom_counter+nom]
    nom_counter=nom_counter+nom
    A_ktotal=A_ktotal+A_kblend[orb,:,:]

    
#method 3    
A_ktotal = np.transpose(A_ktotal)[::-1]    


om=np.array(om)
om=om.reshape(numk,nom*len(wan_orbs))


(ymin,ymax) = (om[0][0],om[0][-1]) #500x100 energy matrix
(xmin,xmax) = (distk[0],distk[-1])

#method 1
#im=plt.imshow(np.transpose(A_kblend[0,:,:])[::-1],cmap=cm.hot, vmin=vmm[0], vmax=vmm[1], extent=[xmin,xmax,ymin,ymax],aspect='auto',alpha=0.5)

#method2
#alpha_count=linspace(0.9,0.1,len(wan_orbs))
#for plot_count in range(len(wan_orbs)):
#    im=plt.imshow(np.transpose(A_kblend[plot_count,:,:])[::-1],cmap=cm.hot, vmin=vmm[0], vmax=vmm[1], extent=[xmin,xmax,ymin,ymax],aspect='auto',alpha=alpha_count[plot_count])

#method 3
im = plt.imshow(A_ktotal,cmap=cm.hot,extent=[xmin,xmax,ymin,ymax],aspect='auto',vmin=vmm[0],vmax=vmm[1])

colorbar(im,orientation='vertical',pad=0.05,shrink=1.0,ticks=arange(0,10.0,1.0))
xticks(SKP,SKPoints)
xlabel('k-path',fontsize='xx-large')
ylabel('Energy',fontsize='xx-large')
axhline(y=0,color='black',ls='--')


plt.show()
plt.savefig('A_k_partial.eps')



