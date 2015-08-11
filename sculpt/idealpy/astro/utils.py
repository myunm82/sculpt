import ephem
import types
import datetime
from sculpt.utils import SculptArgumentError
from astrolib import coords
import numpy

def _check_angle(angle):
    if isinstance(angle, ephem.Angle) or type(angle) == types.StringType or type(angle) == types.FloatType:
        return ephem.degrees(angle)
    else:
        raise IdealPyArgumentError('angle', "angle should be of type ephem.Angle or string or float")
    
def azel2radec(az, el, latitude, longitude, date=None):
    """
    Given the azimuth and elevation of an object in radians
    (its horizontal coordinates), and the latitude and longitude
    (in degrees) of the observer's location, returns the
    Right Ascension and Declination in ephem.Angle units.
    Simply rendering them as __str__ will give the right stringified
    representation of RA and Dec.

    Example Usage:

       >>> ra, dec = azel2radec('135:23', '75.0', '42.38028', '-72.52361')
       >>> print ra, dec
       >>> (17:48:05.94, 31:00:06.1)
       
    @param az: Azimuth of the source given in radians typically. If
       azimuth is given as a float it is interpreted as radians. It can
       also be specified as a string like: '170:23:20'. Or it can be
       specified as ephem.Angle.
    @type az: ephem.Angle units or string or floating point (radians)
    @param el: Elevation of the source given in radians typically. If
       elevation is given as a float it is interpreted as radians. It can
       also be specified as a string like: '60:23:20'. Or it can be
       specified as ephem.Angle.
    @type el: ephem.Angle units or string or floating point (radians)
    @param latitude: Latitude of the source given in radians typically. If
       latitude is given as a float it is interpreted as radians. It can
       also be specified as a string like: '60:23:20'. Or it can be
       specified as ephem.Angle.
    @type latitude: ephem.Angle units or string or floating point (radians)    
    @param longitude: Longitude of the source given in radians typically. If
       longitude is given as a float it is interpreted as radians. It can
       also be specified as a string like: '60:23:20'. Or it can be
       specified as ephem.Angle. Longitudes west of GMT should be given as
       negative numbers.
    @type longitude: ephem.Angle units or string or floating point (radians)
    @param date: a datetime.date or datetime.datetime instance of date. This is
       an optional entry. If not given, it will assume current time
    @type date: datetime.date or datetime.datetime instance
    @return: a tuple of RA and Dec of the source for the given observer
       location. Units of RA and Dec are ephem.Angle units.
    """
    obs = ephem.Observer()
    latitude = _check_angle(latitude)
    longitude = _check_angle(longitude)
    obs.lat, obs.long = latitude, longitude
    az = _check_angle(az)
    el = _check_angle(el)
    if date is not None and (isinstance(date, datetime.datetime) or isinstance(date, datetime.date)):
        date = date
    else:
        date = datetime.datetime.now()
    obs.date = date
    return obs.radec_of(az=az, alt=el)

        
def jprecess(ra, dec, epoch='1950.0'):
    """
    Given RA and Dec in degrees for a given epoch (default 1950.0), returns
    the precessed RA and Dec in degrees in J2000 coordinates

    Example Usage:

       >>> ra = ten('4:23:43')*360/24.
       >>> dec = ten('65:42:55')
       >>> ra2000, dec2000 = jprecess(ra, dec)
       >>> print ra2000, dec2000

    @param ra: Right Ascension in degrees. Or you can give a vector or list
       of RA coordinates.
    @type ra: float in degrees
    @param dec: Declination in degrees. Or you can give a vector or list of
       Dec coordinates
    @type dec: float in degrees
    @param epoch: Scalar giving epoch of original observations, default 1950.0
    @type epoch: string or float
    @return: a tuple of RA and Dec or list of tuples (if input is a vector)
       precessed to FK5 system of J2000. Angles are in degrees.
    """
    if epoch in ('1950.0', '1950.', '1950', 'B1950'):
        epoch = 1950.0
    if type(ra) in (types.ListType, types.TupleType, numpy.ndarray):
        vect = True
        if type(dec) not in (types.ListType, types.TupleType, numpy.ndarray) or len(ra) != len(dec):
            raise SculptArgumentError('dec', "dec should be of same type as RA, and have same length")            
    else:
        vect = False
    if vect:
        ret = []
        for i, r in enumerate(ra):
            pos = coords.Position((r, dec[i]), equinox=epoch)
            ret.append(pos.j2000())
    else:
        pos = coords.Position((ra,dec), equinox=epoch)
        ret = pos.j2000()
    return ret


    
def bprecess(ra, dec, epoch='2000.0'):
    """
    Given RA and Dec in degrees for a given epoch (default 2000.0), returns
    the precessed RA and Dec in degrees in B1950 coordinates (FK4)

    Example Usage:

       >>> ra = ten('4:23:43')*360/24.
       >>> dec = ten('65:42:55')
       >>> ra1950, dec1950 = jprecess(ra, dec)
       >>> print ra1950, dec1950

    @param ra: Right Ascension in degrees. Or you can give a vector or list
       of RA coordinates.
    @type ra: float in degrees
    @param dec: Declination in degrees. Or you can give a vector or list of
       Dec coordinates
    @type dec: float in degrees
    @param epoch: Scalar giving epoch of original observations, default 2000.0
    @type epoch: string or float
    @return: a tuple of RA and Dec or list of tuples (if input is a vector)
       precessed to FK4 system of B1950. Angles are in degrees.
    """
    if epoch in ('2000.0', '2000.', '2000', 'J2000'):
        epoch = 2000.0
    if type(ra) in (types.ListType, types.TupleType, numpy.ndarray):
        vect = True
        if type(dec) not in (types.ListType, types.TupleType, numpy.ndarray) or len(ra) != len(dec):
            raise SculptArgumentError('dec', "dec should be of same type as RA, and have same length")            
    else:
        vect = False
    if vect:
        ret = []
        for i, r in enumerate(ra):
            pos = coords.Position((r, dec[i]), equinox=epoch)
            ret.append(pos.b1950())
    else:
        pos = coords.Position((ra,dec), equinox=epoch)
        ret = pos.b1950()
    return ret


    
