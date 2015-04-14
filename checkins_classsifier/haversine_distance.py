from math import *

def HaversineDistance (lat1, lon1, lat2, lon2):
	# Radius of the Earth, in km
	R = 6371

	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin (dlat/2)**2 + cos (lat1) * cos (lat2) * sin (dlon/2)**2
	c = 2 * atan2 (sqrt (a), sqrt (1-a))
	d = R * c

	return d