from collections import namedtuple

### Define namedtuple
User = namedtuple ("User", ["userId", "gender", "ageGroup"])
Location = namedtuple ("Location", ["address", "context", "latitude", "longidute"])
CheckInFeature = namedtuple ("CheckInFeature", ["user", "location"])
ClassifyResult = namedtuple ("ClassifyResult", ["result", "confident"])