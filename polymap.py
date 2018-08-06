import route
import data_processing
import numpy as np



class Polymap:
    """
    class represnt the the polymap
    each polygon represent a route

    """


    def __init__(self, routes, all_coordinates):
        self.routes = routes
        self.all_coordinates = all_coordinates



    def calc_poly_area(self, poly):
        """

        :param poly: route object
        :return:
        """
        coords = poly.coordinates
        # The trick is that the first coordinate should also be last
        coords.append(coords[0])

        t = 0
        for count in range(len(coords) - 1):
            y = coords[count + 1][1] + coords[count][1]
            x = coords[count + 1][0] - coords[count][0]
            z = y * x
            t += z
        return abs(t / 2.0)





def main():

    polymap = Polymap([],[])
    polymap.routes