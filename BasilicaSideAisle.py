import numpy as np
import matplotlib.pyplot as plt
import graphicsEngine.PerspectiveRenderer as rn
import graphicsEngine.Geometry3D as Geo3D
import graphicsEngine.Templates as Architecture
import graphicsEngine.Shapes as Shapes


# Initialise observer and perspective method in engine
# obs = rn.Observer(np.array([0, 2, 0]), np.array([0, -10, 0]), 60, 45)          # centred view
obs = rn.Observer(np.array([2, 2, 0]), np.array([-20, 0, 0]), 60, 45)           # offset view

eye = rn.Perspective('human_eye', f = 22e-3)
engine = rn.Renderer(obs, eye)

scene = Geo3D.Scene()

# Structural parameters
side_aisle_w = 5                # width of side aisle, i.e. arch diameter
col_h = 5.5                     # height of columns
col_w = col_h/8                 # diameter of columns, according to Vitruvian proportion
total_h = 12                    # height above arches
ncols = 7                       # number of columns
window_height = 6               # height of windows
window_width = 3                # width of windows

# Define geometry according to pattern over the number of columns
for i in range(ncols):
    # Uncomment to enable square pillars
    # scene.add_solid(Shapes.SquareColumn(col_w, col_h, np.array([-(side_aisle_w+col_w)/2, 0, (side_aisle_w+col_w)*i])))
    # scene.add_solid(Shapes.SquareColumn(col_w, col_h, np.array([(side_aisle_w+col_w)/2, 0, (side_aisle_w+col_w)*i])))

    # Rounded cylindrical columns
    scene.add_solid(Architecture.CorinthianColumn(col_w/2, np.array([0, col_h, 0]), 
                                             np.array([-(side_aisle_w+col_w)/2, 0, (side_aisle_w+col_w)*i]), obs.pos))

    scene.add_solid(Architecture.CorinthianColumn(col_w/2, np.array([0, col_h, 0]), 
                                             np.array([(side_aisle_w+col_w)/2, 0, (side_aisle_w+col_w)*i]), obs.pos))
    
    # Arch across aisle
    scene.add_solid(Architecture.Arch(np.array([0, col_h, (side_aisle_w+col_w)*i+col_w/2]), np.array([side_aisle_w, 0, 0]), 
                             side_aisle_w + 2*col_w, total_h - col_h, np.array([0, 0, col_w])))
    scene.add_solid(Architecture.AnnularArc(np.array([0, col_h, (side_aisle_w+col_w)*i - 1.000001*col_w/2]), 
                                      np.array([side_aisle_w/2, 0, 0]), np.array([0, 0, 1]), 0.5))
    
    # Show wall corner at bottom

    if i == ncols - 1:
        break

    # Arch on left side
    scene.add_solid(Architecture.Arch(np.array([-side_aisle_w/2, col_h, (side_aisle_w+col_w)*(i+0.5)]), np.array([0, 0, -side_aisle_w]), 
                            side_aisle_w + 2*col_w, total_h - col_h, np.array([col_w, 0, 0]), show_ends = False, split_left = False))
    scene.add_solid(Architecture.AnnularArc(np.array([-side_aisle_w/2+0.000001, col_h, (side_aisle_w+col_w)*(i+0.5)]), 
                                      np.array([0, 0, side_aisle_w/2]), np.array([-1, 0, 0]), 0.5))
    
    # Arch on right side
    scene.add_solid(Architecture.Arch(np.array([side_aisle_w/2, col_h, (side_aisle_w+col_w)*(i+0.5)]), np.array([0, 0, side_aisle_w]), 
                        side_aisle_w + 2*col_w, total_h - col_h, np.array([-col_w, 0, 0]), show_ends = False, split_right = False))
    scene.add_solid(Architecture.AnnularArc(np.array([side_aisle_w/2-0.000001, col_h, (side_aisle_w+col_w)*(i+0.5)]), 
                                      np.array([0, 0, side_aisle_w/2]), np.array([-1, 0, 0]), 0.5))    
    
    # Window and bottom corner of wall
    scene.add_surfaces(Architecture.DoubleArchedWindow(np.array([-side_aisle_w/2-col_w, 1, (side_aisle_w+col_w)*(i+0.5)]), 
                                              np.array([0, 0, window_width]), np.array([0, window_height, 0])))
    scene.add_solid(Shapes.BorderLine(np.array([-(side_aisle_w)/2-col_w, 0, (side_aisle_w+col_w)*i+col_w/2]), side_aisle_w*np.array([0, 0, 1])))
    scene.add_solid(Shapes.BorderLine(np.array([-(side_aisle_w)/2-col_w, 0, (side_aisle_w+col_w)*i-col_w/2]), col_w*np.array([0, 0, 1])))

    # Vault (ceiling)
    scene.add_solid(Architecture.Vault([np.array([-side_aisle_w/2, col_h+1.7, (side_aisle_w+col_w)*i + col_w/2]), 
                                  np.array([side_aisle_w/2, col_h+1.7, (side_aisle_w+col_w)*(i + 1) - col_w/2])], 
                                 [np.array([side_aisle_w/2, col_h+1.7,(side_aisle_w+col_w)*i + col_w/2]), 
                                  np.array([-side_aisle_w/2, col_h+1.7,(side_aisle_w+col_w)*(i + 1) - col_w/2])]))

# Plot
engine.render(scene)

plt.tight_layout()
plt.show()