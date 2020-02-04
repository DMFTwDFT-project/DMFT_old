#!/usr/bin/env python
import sys, subprocess, os
import sys
import numpy as np
from scipy import *

#######inputs######################################################################
para_com="mpirun -np 4"
sp=False       #spin polarized
orbitals=False #orbital projected

rom=1000 #omega points

#KPoints_list= [[0,0,0],[0.5,0,0],[0.5,0.5,0],[0,0,0]] # LaNiO3 
#SKPoints=['$\Gamma$','X','M','$\Gamma$']

KPoints_list= [[0,0,0],[0.5,0,0],[0.5,0.5,0],[0,0,0],[0.5,0.5,0.5]] # SrVO3 
SKPoints=['$\Gamma$','X','M','$\Gamma$','R']
nk_band=4000

###################################################################################

print('\n###############################')
print('# DMFT post-processing scheme #')
print('###############################\n')

if sp==True:
	print('Spin Polarized calculation\n')
else:
	print('Non-Spin Polarized Calculation\n')


os.popen("mkdir ./imp.0/plot")
os.popen("cp -r ./imp.0/Sig.out.* ./imp.0/plot/")

print('Averaging self-energies...')
cmd = "saverage.py ./imp.0/Sig.out.* -o sig.inpx"
out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
print('Complete.\n')

#append first line of sig files to sig.inpx
fi=open('./imp.0/plot/Sig.out.0.0','r')
data=fi.readline()
fi.close()
fi=open('sig.inpx','r')
data_sig=fi.readlines()
data_sig.insert(0,data)
fi.close()
fi=open('sig.inpx','w')
fi.writelines(data_sig)
fi.close()
os.popen("mv sig.inpx ./imp.0/plot")

print('Generating sig.inp and sigoo.out...')
cmd2 = "Cmp_Siginp.py ./imp.0/plot/sig.inpx"
out, err = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
print('Complete.\n')
os.popen("mv sig.inp ./imp.0/plot")

print('Analytic Continuation...\n')
cmd3 = "maxent_run.py ./imp.0/plot/sig.inp"
subprocess.Popen(cmd3, shell=True).communicate()
print('Complete.\n')
os.popen("mv Sig.out ./imp.0/plot/Sig1.out")

if sp==True:
	os.popen("cp -r wannier90.chk wannier90.eig INPUT.py ksum.input POSCAR DMFT_mu.out SigMdc.out SigMdc_dn.out ./imp.0/plot")
else:
	os.popen("cp -r wannier90.chk wannier90.eig INPUT.py ksum.input POSCAR DMFT_mu.out SigMdc.out ./imp.0/plot")

if sp==False:
	print('Generating SigMoo_real.out in a denser mesh...')
	cmd = "cd ./imp.0/plot/ && Interp_Sig.py"+" "+str(rom)
	subprocess.Popen(cmd, shell=True).communicate()
	print('Complete.\n')

else:
	print('Generating SigMoo_real.out in a denser mesh for spin up...')
	cmd = "cd ./imp.0/plot/ && Interp_Sig.py"+" "+str(rom)
	subprocess.Popen(cmd, shell=True).communicate()
	print('Complete.\n')

	print('Generating SigMoo_real.out in a denser mesh for spin down...')
	cmd = "cd ./imp.0/plot/ && Interp_Sig_sp.py"+" "+str(rom)
	subprocess.Popen(cmd, shell=True).communicate()
	print('Complete.\n')

#kpath generation
print('Generating k-path...')

def Create_kpath(KPoints,nk_band):
   def dist(a,b): return sqrt(sum((array(a)-array(b))**2))
   # returns the distance of given a and b points
   KPoints=array(KPoints)
   path_len=[]
   for i in range(len(KPoints)-1):
      path_len.append(dist(KPoints[i+1],KPoints[i]))
   path_nk=map(int,nk_band*array(path_len)/sum(path_len))
   klist=[]; dist_K=[0.]; dist_SK=[0.]
   for i,nkk in enumerate(path_nk):
      for n in range(nkk):
         klist.append(KPoints[i]+(KPoints[i+1]-KPoints[i])*n/nkk)
         if len(klist)>1: dist_K.append(dist_K[-1]+dist(klist[-1],klist[-2]))
      dist_SK.append(dist_SK[-1]+path_len[i])
   # Add the ending point
   klist.append(KPoints[-1])
   dist_K.append(dist_K[-1]+dist(klist[-1],klist[-2]))
   return array(klist), array(dist_K), array(dist_SK)

klist, dist_K, dist_SK = Create_kpath(KPoints_list,nk_band)
fi=open('klist.dat','w')
for i in range(nk_band):
  kcheck=0
  for j,d in enumerate(dist_SK):
     if abs(dist_K[i]-d)<1e-4: 
        print >>fi, '%.14f  %.14f  %.14f  %.14f  %s' %(dist_K[i],klist[i][0],klist[i][1],klist[i][2],SKPoints[j])
        kcheck=1
        break
  if kcheck==0:
     print >>fi, '%.14f  %.14f  %.14f  %.14f' %(dist_K[i],klist[i][0],klist[i][1],klist[i][2])   

print('Complete.\n')
os.popen("mv klist.dat ./imp.0/plot/")


#updating ksum.input
fi=open('./imp.0/plot/ksum.input','r')
datax=fi.readlines()
fi.close()
datax[0]=str(nk_band)+"\n"
datax[1]=str(rom)+"\n"
del datax[5]
datax= datax[:-4]
fi=open('./imp.0/plot/ksum.input','w')
fi.writelines(datax)
fi.close()

print('Running dmft_ksum_band...')
cmd = "cd ./imp.0/plot &&"+" "+para_com+" "+"dmft_ksum_band"
out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
print('Complete.\n')

if sp==False:
	print('Plotting...')
	cmd = "cd ./imp.0/plot/ && plot_Gk.py"
	subprocess.Popen(cmd, shell=True).communicate()
	print('Complete.\n')
    os.popen("mv ./imp.0/plot/A_k.eps ./")

else:
	print('Plotting for spin polarized case...')
	cmd = "cd ./imp.0/plot/ && plot_Gk_sp.py"
	subprocess.Popen(cmd, shell=True).communicate()
	print('Complete.\n')
    os.popen("mv ./imp.0/plot/A_k_sp.eps ./")

