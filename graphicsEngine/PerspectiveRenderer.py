import numpy as np
import graphicsEngine.Geometry3D as Geo3D
import matplotlib.pyplot as plt


class Perspective:

    def __init__(self, method: str = "human_eye", f: float = 22e-3):
        '''Initialise perspective module for projection of 3D geometry to 2D coordinates.\n
        Args:
            method = type of perspective used for projection:\n
                        "human_eye" = same lens with same focal length as the human eye,\n
                        "nonlinear" = no lens simulation leading to nonlinear perspective,\n
                        "lens" = an arbitary lens with focal length f\n
            f = focal length (default set to human eye)'''

        self.mode = method

        if method == 'human_eye':
            self.projection = self.lens
            self.f = 22e-3
        elif method == 'nonlinear':
            self.projection = self.nonlinear
        elif method == 'lens':
            self.projection = self.lens
            self.f = f
        else:
            raise Exception("Error: Invalid projection method")


    @ staticmethod
    def nonlinear(r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        '''Produce 2D image from 3D geometry without lens effects. Image is hyperbolic.\n
        Args:
            r = 3xn array of points of edges
        Returns:
            theta_x = image x coordinate,\n
            theta_y = image y coordinate'''

        lngth = np.shape(r)[1]
        theta_x = np.zeros(lngth)
        theta_y = np.zeros_like(theta_x)

        for i in range(lngth):
            r_dash = np.sqrt(r[2, i]**2 + r[0, i]**2)
            theta_x[i] = np.arctan2(r[0, i], r[2, i])
            theta_y[i] = np.arctan2(r[1, i], r_dash)

        theta_x = np.rad2deg(theta_x)
        theta_y = np.rad2deg(theta_y)

        return theta_x, theta_y


    def lens(self, r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        '''Produce 2D image of 3D geometry through a lens.
        Args:
            r = 3xn array of points along edges,\n
            f = focal length of lens
        Returns:
            px = image x coordinate,\n
            py = image y coordinate'''

        px = self.f * r[0]/np.abs(r[2])
        py = self.f * r[1]/np.abs(r[2])

        return px, py
    

class Observer:

    def __init__(self, pos: np.ndarray, euler_angles: np.ndarray, 
                 fov_x: float, fov_y: float):
        '''Initialise an observer at a given position and orientation.\n
        Args:
            pos = position of observer,\n
            euler_angles = yaw, pitch and roll of observer,\n
            fov_x = field of view in the horizontal direction (degrees),\n
            fov_y = field of view in the vertical direction (degrees)'''

        self.pos = pos.reshape((3, 1))
        self.eul = np.deg2rad(euler_angles)
        self.fov_x = fov_x
        self.fov_y = fov_y
    

    def plot_horizon(self, ax):
        '''Plot the horizon line according to the observer's orientation.\n
        Args:
            ax = axis for plotting'''

        x = [-self.fov_x/2, self.fov_x/2]
        y = [0, 0]

        ax.plot(x, y, alpha = 0.25, color = 'black')


    def euler_rot_matrix(self) -> np.ndarray:
        '''Apply yaw, pitch and roll angles for coordinate transformation matrix.'''

        psi = self.eul[0]
        theta = self.eul[1]
        phi = self.eul[2]

        R_yaw = np.array([
            [np.cos(psi), 0, np.sin(psi)],
            [0, 1, 0],
            [-np.sin(psi), 0, np.cos(psi)]])

        R_pitch = np.array([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta)],
            [0, np.sin(theta), np.cos(theta)]])
        
        R_roll = np.array([
            [np.cos(phi), -np.sin(phi), 0],
            [np.sin(phi), np.cos(phi), 0],
            [0, 0, 1]])
        
        return R_roll @ R_pitch @ R_yaw


class Renderer:

    def __init__(self, obs: Observer, method: Perspective):
        '''Initialise rendering engine.\n
        Args:
            obs = observer object,\n
            method = perspective object'''
        
        self.obs = obs
        self.method = method
        self.create_viewspace()


    def create_viewspace(self):
        '''Create the viewing space according to the limits of the observer's FOV.'''
        
        self.fig, self.ax = plt.subplots()

        if self.method.mode == "nonlinear":
            self.ax.set_xlim(-self.obs.fov_x/2, self.obs.fov_x/2)
            self.ax.set_ylim(-self.obs.fov_y/2, self.obs.fov_y/2)

        else:
            self.ax.set_xlim(-np.tan(np.deg2rad(self.obs.fov_x/2))*self.method.f, 
                             np.tan(np.deg2rad(self.obs.fov_x/2))*self.method.f)
            self.ax.set_ylim(-np.tan(np.deg2rad(self.obs.fov_y/2))*self.method.f, 
                             np.tan(np.deg2rad(self.obs.fov_y/2))*self.method.f)

        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])


    def render(self, scene: Geo3D.Scene):
        '''Render entire 3D scene composition into 2D image space.\n
        Args:
            scene = scene object containing all solids and faces'''

        order = scene.order_faces(self.obs.pos)         # obtain plotting order via Painter's algorithm
        nfaces = len(order)

        for i in range(nfaces):
            r, r_edge = scene.surfaces[order[i]].discretise()
            r = self.obs.euler_rot_matrix().T @ (r - self.obs.pos)
            tx, ty = self.method.projection(r)

            # Plot face
            if scene.surfaces[order[i]].fill == True:
                self.ax.fill(tx, ty, edgecolor = None, alpha = 1, zorder = 1, facecolor = 'white')

            # Plot face edges
            for j in range(len(r_edge)):
                r = self.obs.euler_rot_matrix().T @ (r_edge[j] - self.obs.pos)
                tx, ty = self.method.projection(r)
                self.ax.plot(tx, ty, color = 'black', zorder = 1, linewidth = 0.75)