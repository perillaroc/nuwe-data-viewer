# coding: utf-8
import datetime

import nuwe_pyeccodes
import numpy as np

from nuwe_data_viewer.plugin.plot_renderer.grid_data import GridData


class GribPlotter(object):
    def __init__(self):
        pass

    @classmethod
    def generate_plot_data(cls, grib_message: nuwe_pyeccodes.GribMessageHandler) -> GridData:
        print('get lon/lat begin:', datetime.datetime.utcnow())
        left_lon = grib_message.getDouble('longitudeOfFirstGridPointInDegrees')
        right_lon = grib_message.getDouble('longitudeOfLastGridPointInDegrees')
        lon_step = grib_message.getDouble('iDirectionIncrementInDegrees')
        nx = grib_message.getLong('Ni')
        lon_array = np.arange(left_lon, right_lon + lon_step / 2, lon_step)

        top_lat = grib_message.getDouble('latitudeOfFirstGridPointInDegrees')
        bottom_lat = grib_message.getDouble('latitudeOfLastGridPointInDegrees')
        lat_step = grib_message.getDouble('jDirectionIncrementInDegrees')
        ny = grib_message.getLong('Nj')
        lat_array = np.arange(top_lat, bottom_lat - lat_step / 2, -lat_step)

        lons, lats = np.meshgrid(lon_array, lat_array)

        print('get values begin:', datetime.datetime.utcnow())
        values = grib_message.getDoubleArray('values')
        grid_values = values.reshape(ny, nx)

        print('get values end:', datetime.datetime.utcnow())
        return GridData(lons, lats, grid_values)
