from geopy.distance import geodesic
from geopy import Point
import numpy
import math

class destination:
    def __init__(self, lat1 = 0, lat2 = 0, long1 = 0, long2 = 0, kms = 1):
        self.lat1 = lat1
        self.lat2 = lat2
        self.long1 = long1
        self.long2 = long2
        self.kms = kms

    def get_bearing(self):
        dLon = (self.long2 - self.long1)
        x = math.cos(math.radians(self.lat2)) * math.sin(math.radians(dLon))
        y = math.cos(math.radians(self.lat1)) * math.sin(math.radians(self.lat2)) - math.sin(math.radians(self.lat1)) * math.cos(math.radians(self.lat2)) * math.cos(math.radians(dLon))
        brng = numpy.arctan2(x,y)
        brng = numpy.degrees(brng)
        return brng

    def find_destination(self):
        coords = geodesic(kilometers=self.kms).destination(Point(self.lat1, self.long1), self.get_bearing()).format_decimal()
        return coords #(float(coords.split(",")[0]) , float(coords.split(",")[1]))

# print(get_bearing(40.693441180545996, 22.851500848046868, 40.655425024320344, 22.950377801171868))
# ob1 = destination(lat1 = 40.668840911211134, long1 = 22.87388052282508, lat2 = 40.64562656008282, long2 = 22.93004419945957, kms =2)
# distance = geodesic((40.670009126290765, 22.880339959374993), (40.64562656008282, 22.93004419945957)).km
# print(distance)
# print(ob1.find_destination())

