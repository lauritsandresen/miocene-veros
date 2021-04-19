import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

#This script can be used to rotate maps around a given point (rc1,rc2) by a given angle (beta)

map_file2 = xr.open_dataset('mmco_topo_bathy_v1_0.nc')
#map_file2 = xr.open_dataset('mmco_veg_v1_0.nc')

lat = map_file2.lat.data
lon = map_file2.lon.data
topo = map_file2.topo.data
#topo = map_file2.veg.data


def old_angle(vin1,vin2,rc1,rc2,beta):
    #Function that finds the angel that you get, when you rotate "back"
    rc1 = np.radians(rc1)
    rc2 = np.radians(90 - rc2)
    beta = -np.radians(beta)
    vin1 = np.radians(vin1)
    vin2 = np.radians(90 - vin2)
    k = np.array([np.sin(rc2)*np.cos(rc1),np.sin(rc2)*np.sin(rc1),np.cos(rc2)])
    a = np.array([np.sin(vin2)*np.cos(vin1),np.sin(vin2)*np.sin(vin1),np.cos(vin2)])
    b = np.cos(beta)*a + np.sin(beta)*np.cross(k,a) + np.dot(k,a)*(1 - np.cos(beta))*k
    vin1_old = np.degrees(np.arctan2(b[1],b[0]))
    if vin1_old < 0:
        vin1_old = 360 + vin1_old
    r = np.sqrt(np.square(b[0]) + np.square(b[1]))
    c = np.degrees(np.arctan( r/b[2]))
    #print(c)
    vin2_old = -90 - c
    if c > 0:
        vin2_old = 90 - c
    return vin1_old,vin2_old

def find_closest(vin1,vin2,lat,lon):
    #Find the grid point closest to the angel found in previous function
    min_lat = np.absolute(lat - vin2)
    min_lon = np.absolute(lon - vin1)
    min_lat = np.where(min_lat == np.min(min_lat))
    min_lon = np.where(min_lon == np.min(min_lon))
    return min_lat[0],min_lon[0]

def rot_map(rc1,rc2,beta,topo):
    #Put all grid points together in new map
    topo_new =np.zeros_like(topo)
    n = 0
    for x in lat:
        m = 0
        for y in lon:
            vin1_old,vin2_old = old_angle(y,x,rc1,rc2,beta)
            min_lat, min_lon = find_closest(vin1_old,vin2_old,lat,lon)
            dum = topo[min_lat,min_lon]
            topo_new[n,m] =dum[0]
            m = m + 1
        n = n +1
        print(n)
    return topo_new

#Call rot_map to rotate map. Use like: rot_map(x-position you rotate around, y-position you roate around, numbers of degree you rotate, old topography)

#topo_new = rot_map(180+78.55,45.23,3.99,topo)
topo_new = rot_map(180+78.55,45.23,45,topo)



plt.figure()
plt.imshow(np.flipud(topo_new),cmap='RdBu')
plt.colorbar()
#plt.clim(-8200,8200)
plt.show()

