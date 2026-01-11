import numpy as np
import matplotlib.pyplot as plt
import graphicsEngine.PerspectiveRenderer as rn
import graphicsEngine.Geometry3D as Geo3D
import graphicsEngine.Shapes as Shapes
import graphicsEngine.Templates as Architecture


# Initialise observer and perspective method in engine
obs = rn.Observer(np.array([0, 2, 0]), np.array([0, 0, 0]), 60, 45)
eye = rn.Perspective('human_eye', f = 22e-3)
engine = rn.Renderer(obs, eye)

scene = Geo3D.Scene()

# Generate a cube
scene.add_solid(Shapes.Prism(1, 1, 1, np.array([-2, 1, 10])))

# Generate a cylinder
scene.add_solid(Shapes.Cylinder(0.5, np.array([0, 1, 0]), np.array([2, 0, 7]), obs.pos))

# Generate arch
scene.add_solid(Architecture.Arch(np.array([1, 2, 12]), np.array([2, 0, 0]), 3, 2, np.array([0, 0, 1])))

# Show horizon
obs.plot_horizon(engine.ax)

# Render scene
engine.render(scene)

plt.tight_layout()
plt.show()