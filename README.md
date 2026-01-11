# Python Graphics Engine
This project presents a modular implementation to convert 3D geometrical information in the 'real world' to accurate 2D visualisations. 
A fully analytical method has been employed to model lines, circular arcs and surfaces formed by them. 
A first principles approach has been taken, deriving all underlying mathematics from observations of the real world.

## How it works
### Observer
The observations of an environment are encapsulated in the `Observer` and `Perspective` classes. 
The `Observer` class is dependent on the observer's position and viewing angle (as determined by Euler angles).
The `Perspective` class chooses the method of projection. 
Linear perspective, typically found in art may be achieved through the `human_eye` option, whereas more distorted images can be obtained with nonlinear perspective.

### Geometry
A 1D geometrical feature such as a line, arc or circle can be constructed from points in 3D space. 
A convention has been established where the *x* axis corresponds to the lateral direction, the *y* axis to the vertical direction and the *z* axis to depth. 
The points along 1D geometrical features are described by a non-dimensionalised shape function of the variable ξ ∈ [0, 1]. 
This approach reduces all 1D geometry to have the same properties allowing for a high level of modularity in the code.

From a series of bounding 1D geometrical features, a 2D surface may be constructed. Simple rectangular and triangular surfaces are captured by the `Surface` class. 
Using the bounding lines, these surfaces can be described analytically from the variables ξ ∈ [0, 1] and ζ ∈ [0, 1]. 
More complex surfaces requiring definitions in polar or cylindrical coordinates can be achieved through the `RadialSurface` and `CylindricalSurface` classes, respectively.

A series of faces can be grouped as a 3D solid in the `Volume` class, however, the rendering method is applied directly to faces and this class exists primarily for conceptual grouping.
Solids can be defined manually by a user through points, lines and surfaces, however, common shapes and architectural features can be found in `Shapes` and `Templates`. 

### Rendering Process
A set of solids or faces form the scene composition. These faces must be rendered in the correct order to produce an accurate image. 
A simple Painter's algorithm method is used, where the furthest away faces are rendered first.
To achieve this, the analytical formulas for each surface are used to calculate the minimum distance from the observer to the face. 
After determining the minimum distance to each face, they are plotted in descending order. 

## Examples
* `SimpleDemo.py` shows a simple implementation of a cube, cylinder and arch into the composition space.
* `BasilicaSideAisle.py` employs conventions detailed by the Roman engineer Vitruvius in his treatise *De Architectura* to construct the side aisle of a Renaissance basilica. 
Corinthian columns, arches and windows combine to form a stunning scene. 
