import numpy as np
from scipy.ndimage import filters
from numba import autojit, prange

@autojit
def CubeMap(arr, multi_marker=True):
	nx, ny, nz = arr.shape
	Nx, Ny, Nz = 2*nx-1,2*ny-1,2*nz-1#2*nx,2*ny,2*nz#
	cubemap    = np.zeros((Nx,Ny,Nz))
	markers    = 1, 1, 1, 1
	if multi_marker: markers = 1, 2, 3, 4
	## Vertices
	for i in prange(nx):
		for j in xrange(ny):
			for k in xrange(nz):
				if arr[i,j,k]: cubemap[i*2,j*2,k*2] = markers[0]

	## Edges 
	for i in prange(Nx):
		for j in xrange(Ny):
			for k in xrange(Nz):
				if cubemap[i,j,k] == 0:
					if cubemap[(i-1)%Nx,j,k] and cubemap[(i+1)%Nx,j,k]: cubemap[i,j,k] = markers[1]
					elif cubemap[i,(j-1)%Ny,k] and cubemap[i,(j+1)%Ny,k]: cubemap[i,j,k] = markers[1]
					elif cubemap[i,j,(k-1)%Nz] and cubemap[i,j,(k+1)%Nz]: cubemap[i,j,k] = markers[1]

	## Faces 
	for i in prange(Nx):
		for j in xrange(Ny):
			for k in xrange(Nz):
				if cubemap[i,j,k] == 0:
					if cubemap[(i-1)%Nx,j,k] and cubemap[(i+1)%Nx,j,k] and cubemap[i,(j-1)%Ny,k] and cubemap[i,(j+1)%Ny,k]: cubemap[i,j,k] = markers[2]
					elif cubemap[i,(j-1)%Ny,k] and cubemap[i,(j+1)%Ny,k] and cubemap[i,j,(k-1)%Nz] and cubemap[i,j,(k+1)%Nz]: cubemap[i,j,k] = markers[2]
					elif cubemap[i,j,(k-1)%Nz] and cubemap[i,j,(k+1)%Nz] and cubemap[(i-1)%Nx,j,k] and cubemap[(i+1)%Nx,j,k]: cubemap[i,j,k] = markers[2]
	
	## Cubes
	for i in prange(Nx):
		for j in xrange(Ny):
			for k in xrange(Nz):
				if cubemap[i,j,k] == 0:
					if cubemap[(i-1)%Nx,j,k] and cubemap[(i+1)%Nx,j,k]: 
						if cubemap[i,(j-1)%Ny,k] and cubemap[i,(j+1)%Ny,k]: 
							if cubemap[i,j,(k-1)%Nz] and cubemap[i,j,(k+1)%Nz]: cubemap[i,j,k] = markers[3]

	return cubemap	


@autojit
def EulerCharacteristic_seq(A):
	chi = 0;
	nx,ny,nz = A.shape
	for x in prange(nx):
		  for y in xrange(ny):
			for z in xrange(nz):
				if(A[x,y,z] == 1):
					if (x+y+z)%2 == 0: chi += 1
					else: chi -= 1
	return chi 

