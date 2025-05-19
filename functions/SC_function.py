import xarray as xr
import numpy as np
import healpy as hp
import easygems.healpix as egh

import cartopy.crs as ccrs

def get_nn_lon_lat_index(nside, lons, lats):
    """
    nside: integer, power of 2. The return of hp.get_nside()
    lons: uniques values of longitudes
    lats: uniques values of latitudes
    returns: array with the HEALPix cells that are closest to the lon/lat grid
    """
    lons2, lats2 = np.meshgrid(lons, lats)
    return xr.DataArray(
        hp.ang2pix(nside, lons2, lats2, nest = True, lonlat = True),
        coords=[("lat", lats), ("lon", lons)],
    )
    
def doubel_itcz_index(lat_bounds , lon_bounds , data_all):

    area_mean_Pn = [] ; area_mean_Ps = [] ;  area_mean_Pe =[]
    area_mean = [area_mean_Pn , area_mean_Ps , area_mean_Pe]
    for lat_pnse , d_mean in zip(lat_bounds , area_mean) :
        
        for data_c in data_all:
            
            lon_part1 = data_c.sel(latitude=lat_pnse, longitude=lon_bounds[0])
            lon_part2 = data_c.sel(latitude=lat_pnse, longitude=lon_bounds[1])

            # Combine both parts
            subset = xr.concat([lon_part1, lon_part2], dim="longitude")
            
            weights = np.cos(np.deg2rad(subset['latitude']))

        # Normalize the weights to sum to 1 across latitude
            weights /= weights.sum()

            # Apply weights across latitude
            weighted_mean = subset.weighted(weights).mean(dim=['latitude', 'longitude'])
            d_mean.append(weighted_mean.data )
    
    all_index = []
    for i in range(5):
        index = (area_mean_Pn[i] + area_mean_Ps[i])/2 - area_mean_Pe[i]
        all_index.append(index)
    return all_index