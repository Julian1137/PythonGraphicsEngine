import numpy as np
from scipy.optimize import minimize
import graphicsEngine.Geometry1D as Geo1D


class SurfaceParent:

    def __init__(self, bounds: list, map, fill: bool = True):
        '''Define a surface given bounding 1D geometry.\n
        Args:
            bounds = list of 1D geometry boundaries,\n
            map = two-variable function defining the surface,\n
            fill = whether to colour in the surface when rendered.'''

        self.ln = bounds
        self.nseg = len(bounds)
        self.map = map
        self.fill = fill
        

    def discretise(self) -> tuple[np.ndarray, list]:
        '''Discretise a surface into points along the boundaries.\n
        Returns:
            all_pts = all boundary points,\n
            visible_edges = boundary points grouped by edge'''

        all_pts = self.ln[0].generate_points()
        visible_edges = []

        if self.ln[0].visible == True:
            visible_edges.append(all_pts)

        if self.nseg > 1:
            for i in range(1, self.nseg):
                pts = self.ln[i].generate_points()
                all_pts = np.concatenate([all_pts, pts], axis = 1)

                if self.ln[i].visible == True:
                    visible_edges.append(pts)

        return all_pts, visible_edges


    def min_dist(self, r: np.ndarray):
        '''Determine the minimum distance from a surface to a point.\n
        Args:
            r = reference point'''

        def dist(params):
            return np.linalg.norm(r - self.map(params[0], params[1]))

        guess = [0.5, 0.5]
        result = minimize(dist, guess, bounds = [[0, 1], [0, 1]])

        return result.fun


class Surface(SurfaceParent):

    def __init__(self, bounds: list, fill: bool = True):
        '''Define simple rectangular or cylindrical surface.\n
        Args:
            bounds = 1D boundaries of surface,\n
            fill = whether to colour in surface'''

        self.ln = bounds
        self.nseg = len(bounds)
        self.fill = fill

        # Parametric definition of surface
        self.map = lambda xi, zeta: self.ln[0].p1 + self.ln[0].dir(xi) + self.ln[1].dir(zeta)


    @classmethod
    def Triangle(cls, bounds, fill = True):
        '''Define triangular surface.\n
            Args:
                bounds = 1D boundaries of surface forming a triangle,\n
                fill = whether to colour in surface'''

        surf = cls(bounds, fill)
        surf.map = lambda xi, zeta: surf.ln[0].p1 + surf.ln[0].dir(xi) + surf.ln[1].dir(xi*zeta)
        
        return surf


class RadialSurface(SurfaceParent):

    def __init__(self, bounds: list, fill: bool = True):
        '''Define a surface according to radial coordinates.\n
        Args:
            bounds = list of bounding 1D geometries with the first item being an Arc or Circle,\n
            fill = whether to colour in surface'''

        self.ln = bounds
        self.nseg = len(bounds)
        self.fill = fill
        self.map = lambda xi, zeta: bounds[0].radial(xi, zeta)
               

class CylindricalSurface(SurfaceParent):

    def __init__(self, face1: RadialSurface, face2: RadialSurface, 
                 r_obs: np.ndarray, fill: bool = True):
        '''Define a surface according to cylindrical coordinates.\n
        Args:
            face1 = starting surface defined in radial coordinates,\n
            face2 = terminating surface defined in radial coordinates,\n
            r_obs = observer position,\n
            fill = whether to colour in surface'''

        self.fill = fill
        self.nseg = 4
        self.r1 = face1.ln[0].r
        self.r2 = face2.ln[0].r

        axis = face2.ln[0].c - face1.ln[0].c
        self.ln = self.find_tangent_boundaries(face1, face2, r_obs)                     # obtain visible boundaries
        self.map = lambda xi, eta: self.ln[0].radial(xi, self.radius(eta)) + eta*axis   # parametric definition of surface


    def radius(self, eta: float) -> float:
        '''Calculate the radius of the cylindrically defined object at a given height.\n
        Args:
            eta = non-dimensionalised height coordinate
        Returns:
            r = radius magnitude'''

        r = 1 + eta*(self.r2/self.r1 - 1)

        return r
    

    def find_tangent_boundaries(self, face1: RadialSurface, face2: RadialSurface, 
                                r_obs: np.ndarray) -> list[Geo1D.Arc, Geo1D.Line, Geo1D.Arc, Geo1D.Line]:
        '''Determine the tangent plane to a cylindrical surface passing through the observer 
        and generate boundary lines. \n
        Args:
            face1 = starting face,\n
            face2 = terminating face,\n
            r_obs = position of observer
        Returns:
            list of boundaries forming visible part of cylindrical surface.'''

        r_obs = r_obs.reshape(3)
        c_1 = face1.ln[0].c
        c_2 = face2.ln[0].c
        axial_dir = c_2 - c_1

        # Parametric form of curved surface between faces
        surf_map = lambda xi, eta: face1.ln[0].radial(xi, self.radius(eta)) + eta*axial_dir      

        # Function equal to 0 when tangent to the cylindrical surface
        def tangency(params):

            r = surf_map(*params).reshape(3)
            c = c_1 + params[1]*axial_dir
            c = c.reshape(3)

            return np.abs(np.linalg.norm(r)**2 + np.dot(c, r_obs)- np.dot(r.reshape(3), r_obs + c))
        
        sols = []

        # Check for multiple solutions
        for i in range(9):
            guess = [0.125*i, 0.5]
            result = minimize(tangency, guess, bounds = [[0, 1], [0, 1]]).x
            sols.append(result[0])

        r_obs = r_obs.reshape((3, 1))
        unique_sol = []
        temp_storage = []

        # Extract unique solutions
        for xi in sols:
            if round(xi, 2) not in temp_storage:
                temp_storage.append(round(xi, 2))
                unique_sol.append(xi)

        unique_sol = unique_sol[1:]     # remove trivial solution

        # Find end points of tangent boundary lines
        botL = face1.ln[0].radial(unique_sol[0], 1)
        topL = face2.ln[0].radial(unique_sol[0], 1)
        botR = face1.ln[0].radial(unique_sol[1], 1)
        topR = face2.ln[0].radial(unique_sol[1], 1)

        l1 = Geo1D.Line(botL, topL)
        l2 = Geo1D.Line(botR, topR)

        # Create both possible arcs given the boundary lines
        normal = axial_dir / np.linalg.norm(axial_dir)
        face1_arc = Geo1D.Arc(botL, botR, normal, r = self.r1)
        face1_rev = Geo1D.Arc(botL, botR, -normal, r = self.r1)

        # Calculate distance to midpoint of each possible arc
        d_1 = np.linalg.norm(face1_arc.parametric(0.5) - r_obs)
        d_rev = np.linalg.norm(face1_rev.parametric(0.5) - r_obs)

        # Choose arc which is closest, i.e. visible
        if d_rev < d_1:
            normal = -normal
            face1_arc = face1_rev

        face2_arc = Geo1D.Arc(topL, topR, normal, r = self.r2)

        return [face1_arc, l2, face2_arc.inv, l1.inv]