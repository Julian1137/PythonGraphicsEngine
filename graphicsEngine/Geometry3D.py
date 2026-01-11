import numpy as np
import graphicsEngine.Geometry2D as Geo2D


class Volume:

    def __init__(self, faces: list):
        '''Group a series of surfaces as a single solid.\n
        Args:
            faces = list of surface objects'''

        self.faces = faces


class Scene:

    def __init__(self):
        '''Initialise composition space.'''
        
        self.surfaces = []
        self.solids = []


    def add_solid(self, sol: Volume):
        '''Add a solid volume to the composition space.\n
        Args:
            sol = volume object'''

        self.solids.append(sol)

        for i in range(len(sol.faces)):
            self.surfaces.append(sol.faces[i])


    def add_surfaces(self, surf: list[Geo2D.Surface]):
        '''Add a surface to the composition space.\n
        Args:
            surf = list of surface objects'''

        for face in surf:
            self.surfaces.append(face)


    def order_faces(self, obs_r: np.ndarray) -> np.ndarray:
        '''Apply the painter's algorithm to decide rendering order 
        of all surfaces present in the composition space.\n
        Args:
            obs_r = position coordinate of observer
        Returns:
            order = array of indices from surfaces attribute in descending order of distance.'''
       
        dist = np.zeros(len(self.surfaces))

        for i in range(len(self.surfaces)):
                dist[i] = self.surfaces[i].min_dist(obs_r)     

        order = np.argsort(dist)[::-1]

        return order