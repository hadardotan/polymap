

class Route:
    """
    class represent a route of form "from-to"
    the route is represented in the polymap as a polygon
    polygon centroid chosen by PCA dimension reduction method according to
    a users data
    polygon requested area is the precentage of time the user spend in this
    route, out of all time wasted on routes
    coordinates are the polygon
    current area is the current area according to coordinates
    first coordinates are being picked accoding to voronoi tesseletion
    """

    def __init__(self, from_name, to_name, centroid, requested_area,
                 current_area, coordinates ):
        self.from_name = from_name
        self.to_name = to_name
        self.centroid = centroid
        self.requested_area = requested_area
        self.current_area = current_area
        self.coordinates = coordinates




