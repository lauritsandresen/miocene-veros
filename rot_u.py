import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from scipy import interpolate



map_file2 = xr.open_dataset('mmco_topo_bathy_v1_0.nc')
lat = map_file2.lat.data
lon = map_file2.lon.data
z_b = map_file2.topo.data

topo_new =np.zeros_like(z_b)

x_b = np.linspace(0, 1, z_b.shape[0])
y_b = np.linspace(0, 1, z_b.shape[1])


def old_angle(vin1,vin2,rc1,rc2,beta):
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
    min_lat = np.absolute(lat - vin2)
    #print('hej')
    #print(vin2)
    #print(np.min(min_lat))
    min_lon = np.absolute(lon - vin1)
    min_lat = np.where(min_lat == np.min(min_lat))
    min_lon = np.where(min_lon == np.min(min_lon))
    return min_lat[0],min_lon[0]

def rot_map(rc1,rc2,beta,zu):
    n = 0
    for x in lat:
        m = 0
        for y in lon:
            #print(x)
            vin1_old,vin2_old = old_angle(y,x,rc1,rc2,beta)
            min_lat, min_lon = find_closest(vin1_old,vin2_old,lat,lon)
            dum = z_u[min_lat,min_lon]
            topo_new[n,m] =dum[0]
            m = m + 1
        n = n +1
        print(n)
    return topo_new



#####Utrecht topography AHS

map_file1 = xr.open_dataset('OF_20Ma_AHS_WORLD.nc')

z_u = map_file1.z.data
z_u = z_u.reshape((1801,3601))
z_u = np.delete(z_u,1800,0)

x_u = np.linspace(0, 1, z_u.shape[0])
y_u = np.linspace(0, 1, z_u.shape[1])

#Interpolate

f = interpolate.interp2d(y_u, x_u, z_u, kind='cubic')
z_u = f(y_b, x_b)

z_u = np.roll(z_u, 360, axis=1)

topo_new = rot_map(180+78.55,45.23,3.99,z_u)





####Utrecht topography PMAG
map_file1 = xr.open_dataset('OF_20Ma_PMAG_WORLD.nc')

z_uP = map_file1.z.data
z_uP = z_uP.reshape((1801,3601))
z_uP = np.delete(z_uP,1768,0)

x_uP = np.linspace(0, 1, z_uP.shape[0])
y_uP = np.linspace(0, 1, z_uP.shape[1])

f = interpolate.interp2d(y_uP, x_uP, z_uP, kind='cubic')
z_uP = f(y_b, x_b)

z_uP = np.roll(z_uP, 360, axis=1)

print(z_uP)


plt.figure()
plt.imshow(topo_new - z_uP,cmap='RdBu')
#plt.imshow(z_uP,cmap='RdBu')

plt.colorbar()
plt.clim(-8200,8200)
plt.show()

