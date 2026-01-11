import numpy as np


class Curve:

    def generate_points(self) -> np.ndarray:
        '''Generate a series of points along a curve.'''

        if self.curved == True:
            nx = self.nx_curved
        else:
            nx = self.nx_linear

        # Create non-dimensionalised local coordinate space
        lcl_coords = np.linspace(0, 1, nx).reshape((1, nx))

        p = self.parametric(lcl_coords)

        return p
    
    @ property
    def nx_linear(self) -> int:
        return 50
    
    @ property
    def nx_curved(self) -> int:
        return 360


class Line(Curve):

    def __init__(self, start: np.ndarray, end: np.ndarray, visible: bool = True):
        '''Define a line given two points.\n
        Args:
            start = line start point,\n
            end = line end point,\n
            visible = visibility of line when rendered'''

        self.p1 = start.reshape((3, 1))
        self.p2 = end.reshape((3, 1))
        self.visible = visible
        self.curved = False

        # Parametric definitions of direction vector and line
        self.dir = lambda xi: (self.p2 - self.p1) * xi
        self.parametric = lambda xi: self.p1 + self.dir(xi)


    @ property
    def inv(self):
        '''Reverse direction of line.'''

        return self.__class__(self.p2, self.p1, visible = self.visible)


class Arc(Curve):

    def __init__(self, start: np.ndarray, end: np.ndarray, normal: np.ndarray, 
                 r: float = 0, visible: bool = True):
        '''Define an arc between two points.\n
        Args:
            start = start point,\n
            end = end point,\n
            normal = unit vector normal to the arc's plane,\n
            r = radius of arc (half the distance between the points by default),\n
            visible = visibility of the arc when rendered
            '''

        self.p1 = start.reshape((3,1))
        self.p2 = end.reshape((3,1))
        self.n  = normal.reshape((3,1))
        self.curved = True
        self.visible = visible

        d = np.linalg.norm(self.p2 - self.p1)

        # Define in-plane unit vectors
        u = (self.p2 - self.p1) / d         
        v = np.cross(self.n.reshape(3), u.reshape(3)).reshape((3,1))

        if r == 0:
            self.r = np.linalg.norm(self.p2 - self.p1)/2
            self.c = self.p1 + (self.p2 - self.p1)/2
 
        else:
            # Calculate centre for non-default radius
            m = (self.p1 + self.p2) / 2
            h = np.sqrt(max(r**2 - (d/2)**2, 0))
            self.r = r
            self.c = m + h * v

        # Calculate angular arguments of end points
        theta1 = np.arctan2((self.p1 - self.c).T @ v, (self.p1 - self.c).T @ u)[0,0]
        theta2 = np.arctan2((self.p2 - self.c).T @ v, (self.p2 - self.c).T @ u)[0,0]

        # Define map from non-dimensionalised coordinate to angle on arc
        self.shape = lambda zeta: (theta2 - theta1) * zeta + theta1

        # Parametric definitions of arc
        self.radial = lambda xi, zeta: self.c + zeta*self.r*(np.cos(self.shape(xi))*u + np.sin(self.shape(xi))*v)
        self.parametric = lambda xi: self.radial(xi, 1)
        self.dir = lambda xi: self.parametric(xi) - self.p1
                  
            
    @ property    
    def inv(self):
        '''Reverse direction of arc.'''

        return self.__class__(self.p2, self.p1, -self.n, self.r, visible = self.visible)
    

    @ property
    def max(self) -> np.ndarray:
        '''Calculate point maximum distance from end points.'''

        return self.parametric(0.5)
    

    @ property
    def length(self) -> float:
        '''Calculate total length of arc.'''

        return self.r*self.shape(1)


class Circle(Curve):

    def __init__(self, centre: np.ndarray, r: float, normal: np.ndarray, visible: bool = True):
        '''Define a circle given a centre and radius.\n
        Args:
            centre = coordinate of circle centre,\n
            r = radius of circle,\n
            normal = unit vector normal to the plane of the circle,\n
            visible = visibility of the circular edge when rendered'''

        self.curved = True
        self.c = centre.reshape((3, 1))
        self.nrml = normal
        self.r = r
        self.visible = visible

        # Calculate in-plane direction vectors
        temp = np.array([1, 1, 1])
        u = np.cross(temp, self.nrml)
        u = u / np.linalg.norm(u)
        v = np.cross(self.nrml, u)
        v = v / np.linalg.norm(v)
        u = u.reshape((3, 1))
        v = v.reshape((3, 1))

        # Parametric definitions
        self.radial = lambda xi, zeta: self.c + zeta*self.r*(u*np.cos(xi*(2*np.pi)) + v*np.sin(xi*(2*np.pi)))
        self.parametric = lambda xi: self.radial(xi, 1)
        self.dir = lambda xi: self.parametric(xi) - self.c
        self.p1 = self.c