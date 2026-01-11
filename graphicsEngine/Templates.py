import numpy as np
import graphicsEngine.Geometry1D as Geo1D
import graphicsEngine.Geometry2D as Geo2D
import graphicsEngine.Geometry3D as Geo3D


def SquarePillar(w: float, h: float, bc: np.ndarray) -> Geo3D.Volume:
        '''Create a pillar with a square cross section.\n
        Args:
            w = pillar width,\n
            h = pillar height,\n
            bc = coordinate of centre of bottom of pillar'''

        b = bc.reshape((3, 1))         # centroid of base

        # Bottom face vertices
        p1 = b + np.array([w/2, 0, w/2]).reshape((3, 1))
        p2 = b + np.array([-w/2, 0, w/2]).reshape((3, 1))
        p3 = b + np.array([-w/2, 0, -w/2]).reshape((3, 1))
        p4 = b + np.array([w/2, 0, -w/2]).reshape((3, 1))

        # Top face vertices
        p5 = b + np.array([w/2, h, w/2]).reshape((3, 1))
        p6 = b + np.array([-w/2, h, w/2]).reshape((3, 1))
        p7 = b + np.array([-w/2, h, -w/2]).reshape((3, 1))
        p8 = b + np.array([w/2, h, -w/2]).reshape((3, 1))

        l1 = Geo1D.Line(p1, p2)
        l2 = Geo1D.Line(p2, p3)
        l3 = Geo1D.Line(p3, p4)
        l4 = Geo1D.Line(p4, p1)

        l5 = Geo1D.Line(p5, p6)
        l6 = Geo1D.Line(p6, p7)
        l7 = Geo1D.Line(p7, p8)
        l8 = Geo1D.Line(p8, p5)

        l9 = Geo1D.Line(p1, p5)
        l10 = Geo1D.Line(p2, p6)
        l11 = Geo1D.Line(p3, p7)
        l12 = Geo1D.Line(p4, p8)

        bottom = Geo2D.Surface([l1, l2, l3, l4])
        top = Geo2D.Surface([l5, l6, l7, l8])
        front = Geo2D.Surface([l1, l10, l5.inv, l9.inv])
        right = Geo2D.Surface([l2, l10, l6, l11.inv])
        back = Geo2D.Surface([l3, l12, l7.inv, l11.inv])
        left = Geo2D.Surface([l4, l9, l8.inv, l12.inv])

        return Geo3D.Volume([bottom, top, front, right, back, left])


def ColumnCapital(c: np.ndarray, r: np.ndarray, axis: np.ndarray = np.array([0, 1, 0])) -> Geo3D.Volume:
    '''Create a simplified trapezoidal capital for a column.\n
    Args:
        c = position of centre of the top of the column,\n
        r = width of column at its base, given as a in-plane vector to the cross section,\n
        axis = unit vector in the axial direction of the column'''

    r_mag = np.linalg.norm(r)
    h = 2*r_mag

    dir1 = r/r_mag
    dir2 = np.cross(r.reshape(3), axis.reshape(3))
    dir2 = dir2/np.linalg.norm(dir2)

    # Obtain points along bottom face
    ch = c + h*axis
    p1 = ch + r_mag*dir1 + r_mag*dir2
    p2 = ch + r_mag*dir1 - r_mag*dir2
    p3 = ch - r_mag*dir1 - r_mag*dir2
    p4 = ch - r_mag*dir1 + r_mag*dir2

    # Obtain points along top face
    r_top = 5.5/6.5*r_mag                               # from Vitruvian proportions
    p5 = c + (r_top*dir1 + r_top*dir2)/np.sqrt(2)
    p6 = c + (r_top*dir1 - r_top*dir2)/np.sqrt(2)
    p7 = c - (r_top*dir1 + r_top*dir2)/np.sqrt(2)
    p8 = c + (-r_top*dir1 + r_top*dir2)/np.sqrt(2)

    l1 = Geo1D.Line(p1, p2)
    l2 = Geo1D.Line(p2, p3)
    l3 = Geo1D.Line(p3, p4)
    l4 = Geo1D.Line(p4, p1)

    l5 = Geo1D.Line(p1, p5)
    l6 = Geo1D.Line(p2, p6)
    l7 = Geo1D.Line(p3, p7)
    l8 = Geo1D.Line(p4, p8)

    arc1 = Geo1D.Arc(p5, p6, axis, r = r_top, visible=False)
    arc2 = Geo1D.Arc(p6, p7, axis, r = r_top, visible=False)
    arc3 = Geo1D.Arc(p7, p8, axis, r = r_top, visible=False)
    arc4 = Geo1D.Arc(p8, p5, axis, r = r_top, visible=False)

    diag1 = Geo1D.Line(p6, p1, visible=False)
    diag2 = Geo1D.Line(p7, p2, visible=False)
    diag3 = Geo1D.Line(p8, p3, visible=False)
    diag4 = Geo1D.Line(p5, p4, visible=False)

    # Form trapezoidal volume from 8 triangles
    side1a = Geo2D.Surface.Triangle([l1, l6, diag1])
    side1b = Geo2D.Surface.Triangle([l5.inv, diag1.inv, arc1.inv])
    side2a = Geo2D.Surface.Triangle([l2, l7, diag2])
    side2b = Geo2D.Surface.Triangle([l6.inv, diag2.inv, arc2.inv])
    side3a = Geo2D.Surface.Triangle([l3, l8, diag3])
    side3b = Geo2D.Surface.Triangle([l7.inv, diag3.inv, arc3.inv])
    side4a = Geo2D.Surface.Triangle([l4, l5, diag4])
    side4b = Geo2D.Surface.Triangle([l8.inv, diag4.inv, arc4.inv])

    return [side1a, side1b, side2a, side2b, side3a, side3b, side4a, side4b]


def CorinthianColumn(r: float, h: np.ndarray, bc: np.ndarray, obs: np.ndarray) -> Geo3D.Volume:
    '''Create a simplified Corinthian column composed of a cylindrical body
    and trapezoidal capital, with tapering. Vitruvian proportions are followed.\n
    Args:
        r = radius of column,\n
        h = height of column in the axial direction,\n
        bc = position of the base of the column,\n
        obs = position of the observer, required for determining visible edges'''

    h_mag = np.linalg.norm(h)
    necking_factor = 5.5/6.5            # from Vitruvian proportions for column necking
    body_proportion = 1 - 2*r/h_mag     # from Vitruvian proportions for capital size

    nrml = h / h_mag
    base_circle = Geo1D.Circle(bc, r, nrml)
    top_circle = Geo1D.Circle(bc + body_proportion*h, necking_factor*r, nrml)

    # Faces of column
    bottom = Geo2D.RadialSurface([base_circle])
    top = Geo2D.RadialSurface([top_circle])
    side = Geo2D.CylindricalSurface(bottom, top, obs)

    # Capital trapezoid
    capital = ColumnCapital(bc + body_proportion*h, np.array([r, 0, 0]))

    return Geo3D.Volume([side, *capital])


def Arch(c: np.ndarray, dia: np.ndarray, w_ovr: float, h: float, dpth: np.ndarray, 
                 show_ends = True, split_right = False, split_left = False) -> Geo3D.Volume:
    '''Create a semicircular arch with supports. Front face of the arch is split into three faces
    corresponding to the semicircular and two rectangular sections. \n
    Args:
        c = centre of the arch on its front face plane,\n
        dia = diameter of the arch as a vector parallel to the semicircle end points,\n
        w_ovr = overall width of the arch including the semicircular span and support width,\n
        h = height of the arch,\n
        dpth = depth of the arch in corresponding direction,\n
        show_ends = boolean for displaying the end edges of the arch,\n
        split_right = boolean for displaying the edge between central and right face,\n
        split_left = boolean for displaying the edge between the central and left face'''

    c = c.reshape((3, 1))
    dia = dia.reshape((3, 1))
    dpth = dpth.reshape((3, 1))

    # Semicircle end points on front face
    p1 = c - dia/2
    p2 = c + dia/2

    # Semicircle end points on back face
    p3 = p1 - dpth
    p4 = p2 - dpth
 
    # Obtain direction vector parallel to front face
    vert = np.cross(dia.reshape(3), dpth.reshape(3))
    vert = np.abs(vert)/np.linalg.norm(vert)
    vert = vert.reshape((3, 1))
    nrml = dpth / np.linalg.norm(dpth)

    Arc1 = Geo1D.Arc(p1, p2, nrml)
    Arc2 = Geo1D.Arc(p3, p4, nrml)    

    # Determine all other front face points
    p5 = c - w_ovr * dia/np.linalg.norm(dia)/2
    p6 = c + w_ovr * dia/np.linalg.norm(dia)/2

    p7 = p5 + vert*h
    p8 = p6 + vert*h

    l1 = Geo1D.Line(p5, p1)

    l2 = Geo1D.Line(p2, p6)
    l3 = Geo1D.Line(p6, p8, visible = show_ends)
    l4 = Geo1D.Line(p8, p7)
    l5 = Geo1D.Line(p7, p5, visible = show_ends)

    # Determine all other back face points
    p9 = p5 - dpth
    p10 = p6 - dpth
    p11 = p7 - dpth
    p12 = p8 - dpth

    p13 = p1 + vert*h
    p14 = p2 + vert*h
    p15 = p13 - dpth
    p16 = p14 - dpth

    l6 = Geo1D.Line(p9, p3)
    l7 = Geo1D.Line(p4, p10)
    l8 = Geo1D.Line(p10, p12, visible = show_ends)
    l9 = Geo1D.Line(p12, p11)
    l10 = Geo1D.Line(p11, p9, visible = show_ends)

    l11 = Geo1D.Line(p5, p9)
    l12 = Geo1D.Line(p1, p3)
    l13 = Geo1D.Line(p2, p4)
    l14 = Geo1D.Line(p6, p10)
    l15 = Geo1D.Line(p8, p12)
    l16 = Geo1D.Line(p7, p11)

    l17 = Geo1D.Line(p1, p13, visible = split_left)
    l18 = Geo1D.Line(p2, p14, visible = split_right)
    l19 = Geo1D.Line(p3, p15, visible = split_left)
    l20 = Geo1D.Line(p4, p16, visible = split_right)
    l21 = Geo1D.Line(p13, p7, visible = True)
    l22 = Geo1D.Line(p14, p13, visible = True)
    l23 = Geo1D.Line(p8, p14, visible = True)
    l24 = Geo1D.Line(p15, p11)
    l25 = Geo1D.Line(p16, p15)
    l26 = Geo1D.Line(p12, p16)

    # Define faces from lines
    frontL = Geo2D.Surface([l21, l5, l1, l17, l21])
    frontC = Geo2D.Surface([l22, l17.inv, Arc1, l18])
    frontR = Geo2D.Surface([l23, l18.inv, l2, l3])
    backL = Geo2D.Surface([l24, l10, l6, l19])
    backC = Geo2D.Surface([l25, l19.inv, Arc2, l20])
    backR = Geo2D.Surface([l26, l20.inv, l7, l8])
    
    right = Geo2D.Surface([l14, l8, l15.inv, l3.inv])
    left = Geo2D.Surface([l5.inv, l11, l10, l16.inv])
    top = Geo2D.Surface([l4, l16, l9.inv, l15.inv])
    botL = Geo2D.Surface([l1, l12, l6.inv, l11.inv])
    botR = Geo2D.Surface([l2, l14, l7.inv, l13.inv])
    ventral = Geo2D.Surface([Arc1, l13, Arc2.inv, l12.inv])

    return Geo3D.Volume([frontL, frontC, frontR, right, backL, backC, backR, left, top, ventral])


def Vault(diagonal1: list[np.ndarray], diagonal2: list[np.ndarray]) -> Geo3D.Volume:
        '''Create a vault with semicircular arcs across diagonals. All points assumed 
        to lie in the xz plane\n
        Args:
            diagonal1 = list of points of first diagonal,\n
            diagonal2 = list of points of second diagonal'''

        # Determine normal vecotrs for semicircular arcs
        nrml1 = np.array([-(diagonal1[0][0] - diagonal1[1][0]), 0, 1])
        nrml1 = -nrml1 / np.linalg.norm(nrml1)
        nrml2 = np.array([-(diagonal2[0][0] - diagonal2[1][0]), 0, 1])
        nrml2 = nrml2 / np.linalg.norm(nrml2)

        dia_mag = np.linalg.norm(diagonal1[0] - diagonal1[1])/2

        arc1 = Geo1D.Arc(diagonal1[0], diagonal1[1], nrml1, r = dia_mag)
        arc2 = Geo1D.Arc(diagonal2[0], diagonal2[1], nrml2, r = dia_mag)

        # Create 1D surfaces for the lines, faces not filled in for efficiency
        FakeSurface1 = Geo2D.SurfaceParent([arc1], lambda xi, zeta: arc1.p1 + arc1.dir(xi), fill = False)
        FakeSurface2 = Geo2D.SurfaceParent([arc2], lambda xi, zeta: arc2.p1 + arc2.dir(xi), fill = False)

        return Geo3D.Volume([FakeSurface1, FakeSurface2])


def ArchedWindow(c: np.ndarray, w: np.ndarray, h: np.ndarray) -> Geo3D.Volume:
        '''Create an arched window, composed of rectangular and semicircular sections.\n
        Args:
            c = centre of the bottom edge of the window,\n
            w = width of the window,\n
            h = height of the window'''

        # Bottom vertices
        v1 = c - w/2
        v2 = c + w/2

        h_rect = np.linalg.norm(h) - np.linalg.norm(w)/2
        h_vec = h / np.linalg.norm(h)

        v3 = v1 + h_rect*h_vec
        v4 = v2 + h_rect*h_vec

        # Rectangular section boundaries
        l1 = Geo1D.Line(v1, v2)
        l2 = Geo1D.Line(v2, v4)
        l3 = Geo1D.Line(v4, v3, visible=False)
        l4 = Geo1D.Line(v3, v1)

        # Define semicircular section
        nrml = np.cross(h.reshape(3), w.reshape(3))
        nrml = nrml/np.linalg.norm(nrml)
        arc1 = Geo1D.Arc(v4, v3, nrml)

        rect_face = Geo2D.Surface([l1, l2, l3, l4], fill = False)
        semicirc_face = Geo2D.RadialSurface([arc1, l3.inv], fill = False)

        return Geo3D.Volume([rect_face, semicirc_face])


def DoubleArchedWindow(c: np.ndarray, w: np.ndarray, h: np.ndarray) -> Geo3D.Volume:
        '''Create a double arched window with two main semicircular panes and a 
        circular pane in the top centre.\n
        Args:
            c = centre of the bottom of the window,\n
            w = width of the window,\n
            h = height of the window'''

        major_arch = ArchedWindow(c, w, h)

        h_vec = h / np.linalg.norm(h)
        h_minor_mag = np.linalg.norm(h) - np.linalg.norm(w)/2

        w_vec = w / np.linalg.norm(w)

        nrml = np.cross(w.reshape(3), h.reshape(3))
        nrml = nrml/np.linalg.norm(nrml)

        ratio = 15

        w_minor_mag = np.linalg.norm(w)/(2 + 3/ratio)
        t = w_minor_mag/ratio
        h_minor_mag += w_minor_mag/2 - t
        
        # Create two smaller arched windows within the main window
        c_minor = c + t*h_vec
        minor_arch_1 = ArchedWindow(c_minor - 0.5*(w_minor_mag + t)*w_vec, w_minor_mag*w_vec, h_minor_mag*h_vec)
        minor_arch_2 = ArchedWindow(c_minor + 0.5*(w_minor_mag + t)*w_vec, w_minor_mag*w_vec, h_minor_mag*h_vec)

        # Create a circular window at the top
        circle_border = Geo1D.Circle(c + (np.linalg.norm(h) - np.linalg.norm(w)/4 + 2*t)*h_vec, 0.25 * w_minor_mag, nrml)
        circular_window = Geo2D.RadialSurface([circle_border], fill = False)

        faces = major_arch.faces + minor_arch_1.faces + minor_arch_2.faces + [circular_window]

        return faces


def AnnularArc(c: np.ndarray, r_inner: np.ndarray, nrml: np.ndarray, t: float) -> Geo3D.Volume:
    '''Create an annular arc, commonly used to show the edge of an arch.\n
    Args:
        c = centre of the arc,\n
        r_inner = inner radius of the arc, i.e. the radius of the arch,\n
        nrml = unit normal vector in the direction of the arc,\n
        t = thickness of the arch's border'''

    inner_arc = Geo1D.Arc(c - r_inner, c + r_inner, nrml)

    vert = -np.cross(r_inner.reshape(3), nrml.reshape(3))
    vert = vert/np.linalg.norm(vert)

    r_in = np.linalg.norm(r_inner)
    theta = np.arccos(r_in/(r_in + t))
    h = (r_in + t) * np.sin(theta) * vert

    outer_arc = Geo1D.Arc(c - r_inner + h, c + r_inner + h, -nrml, r = r_in + t)

    l1 = Geo1D.Line(c - r_inner, c - r_inner + h)
    l2 = Geo1D.Line(c + r_inner, c + r_inner + h)

    front = Geo2D.RadialSurface([inner_arc, l2, outer_arc.inv, l1.inv])

    return Geo3D.Volume([front])