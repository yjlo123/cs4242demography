import math

def HaversineDistance (lat1, lon1, lat2, lon2):
	# Radius of the Earth, in km
	R = 6371

	# Delta longidute and latitude
	dlon = math.radians (lon2 - lon1) 
	dlat = math.radians (lat2 - lat1)


	a = math.sin (dlat/2)**2 + math.cos (lat1) * math.cos (lat2) * math.sin (dlon/2)**2 
	c = 2 * math.atan2 (math.sqrt(a), math.sqrt(1-a)) 
	d = R * c

	return d