import route
import data_processing
import shapley
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import voronoi_polygons
import numpy as np



class Polymap:
    """
    class represnt the the polymap
    each polygon represent a route

    """


    def __init__(self, centroids, polys_points, polys_names, requested_areas, current_areas):
        """

        :param centroids: np array
        :param polys_points: np array of np arrays
        :param polys_names:
        :param requested_areas: np array
        :param current_areas: np array
        """
        self.polys_names = polys_names
        self.num_of_polys = centroids.size
        self.centroids = centroids
        self.polys_points = polys_points
        self.requested_areas = requested_areas
        self.current_areas = self.get_current_areas()

    def calc_poly_area(self, poly_points):
        """

        :param poly_points : current polygon's points np array
        :return:
        """
        # xs = poly_points[:,0]
        # ys = poly_points[:,1]

        #the first and last elements are for +1 -1 to work at end of range
        xs = poly_points[-1:,0]
        xs = np.append(xs,poly_points[:,0])
        xs = np.append(xs,poly_points[:1,0])

        ys = poly_points[-1:,1]
        ys = np.append(ys,poly_points[:,1])
        ys = np.append(ys,poly_points[:1,1])

        #for i in range(1, len(xs)-1):
        #    print ("digesting x, y+1, y-1 points: {0}/{1}/{2}".format(xs[i], ys[i+1], ys[i-1]))

        #https://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon
        area = sum(xs[i]*(ys[i+1]-ys[i-1]) for i in range(1, len(xs)-1))/2.0
        # centroid_x =  sum((xs[i]+xs[i+1])*(xs[i]*ys[i+1] - xs[i+1]*ys[i]) for i in range(1, len(xs)-1))/(6.0*area)
        # centroid_y =  sum((ys[i]+ys[i+1])*(xs[i]*ys[i+1] - xs[i+1]*ys[i]) for i in range(1, len(xs)-1))/(6.0*area)

        return area



    def get_current_areas(self):

        # init np array in size of num of polys
        current_areas = np.zero(self.num_of_polys)

        for i in range(self.num_of_polys):
            current_areas[i] = self.calc_poly_area(self.polys_points[i])

        return current_areas


def voro():
    rand_points = np.random.rand(5, 2)
    bounding_box = np.array([[0., 1.], [0., 0.],[1,1],[1,0]])
    print(bounding_box)
    points = np.concatenate((rand_points,bounding_box), axis=0)

    # compute Voronoi tesselation
    vor = Voronoi(rand_points, qhull_options='Qbb Qc Qx')



    print(vor.vertices)

    voronoi_plot_2d(vor)



    plt.show()


voro()




