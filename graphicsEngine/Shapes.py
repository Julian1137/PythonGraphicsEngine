import numpy as np
import graphicsEngine.Geometry1D as Geo1D
import graphicsEngine.Geometry2D as Geo2D
import graphicsEngine.Geometry3D as Geo3D


def Prism(l: float, w: float, h: float, c: np.ndarray) -> Geo3D.Volume:
        '''Create a prism.\n
        Args:
                l = dimension in x,\n
                w = dimension in z,\n
                h = dimension in y,\n
                bc = coordinate of centre'''

        # Vertices
        v1 = np.array([c[0] - l/2, c[1] - h/2, c[2] + w/2])
        v2 = np.array([c[0] + l/2, c[1] - h/2, c[2] + w/2])
        v3 = np.array([c[0] - l/2, c[1] + h/2, c[2] + w/2])
        v4 = np.array([c[0] + l/2, c[1] + h/2, c[2] + w/2])
        v5 = np.array([c[0] - l/2, c[1] - h/2, c[2] - w/2])
        v6 = np.array([c[0] + l/2, c[1] - h/2, c[2] - w/2])
        v7 = np.array([c[0] - l/2, c[1] + h/2, c[2] - w/2])
        v8 = np.array([c[0] + l/2, c[1] + h/2, c[2] - w/2])

        # Lines
        l1  = Geo1D.Line(v1, v2)   
        l2  = Geo1D.Line(v4, v3)   
        l3  = Geo1D.Line(v3, v1)   
        l4  = Geo1D.Line(v2, v4)   
        l5  = Geo1D.Line(v5, v6)   
        l6  = Geo1D.Line(v8, v7)   
        l7  = Geo1D.Line(v7, v5)   
        l8  = Geo1D.Line(v6, v8)  
        l9  = Geo1D.Line(v5, v1)   
        l10 = Geo1D.Line(v2, v6)   
        l11 = Geo1D.Line(v3, v7)  
        l12 = Geo1D.Line(v8, v4)   

        # Faces
        back  = Geo2D.Surface([l1, l4, l2, l3])
        front   = Geo2D.Surface([l5, l8, l6, l7])
        top    = Geo2D.Surface([l2.inv, l12.inv, l6.inv, l11.inv])
        bottom = Geo2D.Surface([l1.inv, l9.inv, l5.inv, l10.inv])
        left   = Geo2D.Surface([l9, l3,  l11, l7])
        right  = Geo2D.Surface([l10, l8, l12, l4])

        return Geo3D.Volume([front, back, top, bottom, left, right])


def Cylinder(r: float, h: np.ndarray, bc: np.ndarray, r_obs: np.ndarray) -> Geo3D.Volume:
        '''Create a cylinder.\n
        Args:
                r = radius,\n
                h = height,\n
                bc = position coordinate of base,\n
                r_obs = position coordinate of observer'''

        nrml = h / np.linalg.norm(h)
        base_circle = Geo1D.Circle(bc, r, nrml)
        top_circle = Geo1D.Circle(bc + h, r, nrml)

        bottom = Geo2D.RadialSurface([base_circle])
        top = Geo2D.RadialSurface([top_circle])

        # Determine visible edges of the curved section
        side = Geo2D.CylindricalSurface(bottom, top, r_obs)

        return Geo3D.Volume([side, bottom, top])


def Semicircle(c: np.ndarray, r: np.ndarray, nrml: np.ndarray) -> Geo3D.Volume:
        '''Create a semicircle.\n
        Args:
                c = centre of semicircle,\n
                r = radius of semicircle,\n
                nrml = normal to plane of semicircle.'''

        nrml = nrml / np.linalg.norm(nrml)
        rounded_edge = Geo1D.Arc(c - r, c + r, nrml)
        flat_edge = Geo1D.Line(c - r, c + r)

        front = Geo2D.RadialSurface([rounded_edge, flat_edge])

        return Geo3D.Volume([front])


def BorderLine(start: np.ndarray, length: np.ndarray) -> Geo3D.Volume:
        '''Create a 3D line.\n
        Args:
                start = start point,\n
                length = length of line in a particular direction'''

        l = Geo1D.Line(start, start + length)

        # Create a 1D face representing the line
        fakeSurface = Geo2D.SurfaceParent([l], lambda xi, zeta: l.p1 + l.dir(xi), fill = False)

        return Geo3D.Volume([fakeSurface])