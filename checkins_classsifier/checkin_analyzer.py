import time
import requests
import json
from params import *
from namedtuple import *

class CheckinAnalyzer:
	def __init__ (self):
		self.__api__ = "https://api.foursquare.com/v2/search/recommendations"

	def __initialize_new_payload__ (self, location = None):
		self.__payload__ = {
			"ll"			: None,
			"limit"			: FS_ANALYZER_LIMIT,
			"radius"		: FS_ANALYZER_RADIUS,
			"intent"		: "bestnearby",
			"client_id"		: "SUDHF5BMGBVUMEHBQV2GNSERUH3WABBVDLILRLK0WWXKSY5K",
			"client_secret" : "GDP32ZN2USAPBYLW4CGWVYJQSJBGGNYC4KWT5S2S0N34E5ZB",
			"v"				: time.strftime("%Y%m%d")
		}

		if location != None:
			self.__payload__["ll"] = location

	def analyze (self, location):
		# Check for invalid location
		if location.latitude == None or location.longidute == None:
			print "Invalid location!"
			return

		# Set up request payload
		ll = str (location.latitude) + "," + str (location.longidute)
		self.__initialize_new_payload__ (ll)

		# Send the request
		response = requests.get (self.__api__, params = self.__payload__)
		response = response.json ()

		group = response["response"]["group"]
		total_result = group["totalResults"]

		# Try to count the number of recommenders, based on gender
		maleCount = 0
		femaleCount = 0
		total = 0
		results = group["results"]
		for result in results:
			items = result["snippets"]["items"]
			total += len (items)
			for item in items:
				try:
					gender = item["detail"]["object"]["user"]["gender"]
					if gender == "male":
						maleCount += 1
					elif gender == "female":
						femaleCount += 1
				except KeyError:
					gender = None

		result = []
		result.append (ClassifyResult ("male", float (maleCount) / total))
		result.append (ClassifyResult ("female", float (femaleCount) / total))

		return result