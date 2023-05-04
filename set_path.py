import geopy.distance
from geopy import Point
from additional_functions import destination
from tkintermapview.canvas_position_marker import CanvasPositionMarker

class wanted_marker():
        def __init__(self) -> None:
            self.d = 0
            self.l =[]
            self.new_marker_1 = []
            self.P1 = []

            

        def set_marker(self, dt, speed):
        #I have already added two points on the map and want to print P1, which is the list points of interest
            if (len(self.new_marker_1)>=3) and (self.new_marker_1[-2][0] != 0) and (self.new_marker_1[-1][0] != 0):
                self.d = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
                if sum(self.l) > float(speed)*float(dt):
                    self.l = []
                    self.l.append(self.d)
                else:
                    self.l.append(self.d)
                if sum(self.l) < float(speed)*float(dt):
                    if self.P1 == []:
                        self.P1.append(self.new_marker_1[1])
                    self.d = sum(self.l)
                if sum(self.l) == float(speed)*float(dt):
                    self.l = []
                    self.P1.append(self.new_marker_1[-1])
                    self.d = 0
                while sum(self.l) > float(speed)*float(dt):
                    endiameso = destination(lat2 = self.new_marker_1[-1][0], long2 = self.new_marker_1[-1][1],
                                        lat1 = self.new_marker_1[-2][0], long1 = self.new_marker_1[-2][1],
                                        kms = float(speed)*float(dt) - sum(self.l[:-1]))
                    self.new_marker_1.insert(-1, (float(endiameso.find_destination().split(",")[0]), float(endiameso.find_destination().split(",")[1])))
                    self.d = geopy.distance.geodesic(self.new_marker_1[-1], self.new_marker_1[-2]).km
                    if self.P1 == []:
                        self.P1 = [self.new_marker_1[1]]
                        
                    self.P1.append((float(endiameso.find_destination().split(",")[0]), float(endiameso.find_destination().split(",")[1])))
                    self.l = [sum(self.l) - float(speed)*float(dt)]

            print("P1 = ", self.P1)
            print("new ", self.new_marker_1)
            print(self.d)
            return self.d, self.new_marker_1, self.P1, self.l   