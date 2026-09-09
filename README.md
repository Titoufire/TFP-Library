# TFP-Library
Titoufire's Physics Library, contains everything needed to build video games with a customizable physics engine.

# Installation and importation
Download the zip file of the latest version, and unzip it in your project folder (same level as your main.py) without creating a folder.  
Then, simply import it with  
`from Tfp.tfp import Tfp`   

This library requires pygame has a dependency. You can use pygame or pygame-ce on newer versions of python.
This library is written for python 3.14.7 therefore using pygame-ce.  
to install pygame, execute in the terminal:  
`pip install pygame` or `pip install pygame-ce` in newer versions  
then import pygame as usual: `import pygame`

if you are having any issues with this, please open an issue  

# How to use
After importing the library, initialize pygame as always, and setup your window. Once done, create a Tfp instance like so:  
`context = Tfp()`  

and a Camera(pos: Vec2, zoom: float)
`camera = context.Camera(Vec2(0, 0), 1)`

then tell give Tfp your window, camera, and number of physics frames per visual frame using Tfp().setup(window: pygame.Surface, camera: Tfp.Camera, physics_frames: int)  
`context.setup(screen, camera, physics_frames=10)`

and you have set up Tfp !

# Functions
#### setup (self, window: pygame.surface, camera: Camera, physics_frames: int=10)
Sets up the tfp context  
***
#### draw (self)
Draws all objects on the window, but DOESN'T update the display  
`Tfp().draw()`
***
#### simulate (self, dt: float)
Does all of the simulation calculations, the chose amount of times (physics_frames)  
`dt` is delta_time in seconds. in pygame it is defined by `pygame.time.Clock().tick() / 1000`  
***
#### set_gravity (self, full: Vec2=None, strenght: float=0, direction: Vec2=None)
Sets or modify gravity with the according parameters. Only use ONE parameter at a time.  
`full` sets the gravity vector to the given one.  
`strength` sets the length of the gravity vector to the given length, without changing the direction.  
`direction` sets the direction of the gravity vector to the given vector, without changing the length.  
***
#### new_line (self, color: str | pygame.Color, start: tuple[int, int], end: tuple[int, int], rest=1, fric=0)
Creates a new line with the given parameters, and returns it. `start` and `end` must be absolute coordinates
***
#### new_ball (self, color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int], rest=1, fric=0, mass=1, floating=False, radius=20)
Creates a new ball with the given parameters, and returns it.
***
#### new_spring (self, color: str | pygame.Color, node1: Ball, node2: Ball, length=None, force=0.5, thickness=None, damp=0.3, dz = 0.01)
Creates a new spring with the given parameters, and returns it.
***
#### new_rigid (self, color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int], vertices: list[tuple[int, int]], edge_color=None, edge_thickness=1, fric=0, rest=1, fixed=False)
Creates a new rigid_body with the given parameters, and returns it.
***
#### say_hello (self)
Says hello in the console
`Tfp().say_hello()`

# Soft bodies
Soft bodies are a collection of balls and springs connecting the balls. They can be built in 4 different ways.

#### build_from_points (points: list[tuple[int, int]], springs: list[tuple[int, int]], color: str | pygame.Color, pos: tuple[int, int], rad: int, force=0.5, fric=0)
Creates new balls in the given order. the coordinates given are relative to `pos`  
Creates springs, each tuple is the index of the two balls the springs should link (in the order they were defined)  
`rad` is the radius of the balls  
`force` is the strength of the springs  
the length of each spring is simply the length between the balls it links, it is not possible to sert a custom length.   
***
#### build_from_balls (balls: list[Ball], springs: list[tuple[int, int]], color: str | pygame.Color, force=0.5)
same as above but does not create the balls, instead it takes Ball objects as argument  
***
#### build_from_preset (preset_name: str, pos: tuple[int, int], color: str | pygame.Color, rad: int, length = 10, width = 10, force=0.5, definition = 8)
builds a soft body from a preset. presets:  
`"square"`: `length` controls the side length of the square, `rad` controls the radius of the balls, `force` controls the strength of the springs  

`"rectangle"`: `length` controls the side length of the rectangle, `width` controls the width of the rectangle, `rad` controls the radius of the balls, `force` controls the strength of the springs  

`"triangle"`: `length` controls the side length of the triangle, `rad` controls the radius of the balls, `force` controls the strength of the springs  

`"circle"`: `length` controls the radius of the circle, `definition` controls the number of balls, `rad` controls the radius of the balls, `force` controls the strength of the springs  
***
### build_from_file (file_path: str)
opens the file at the given path, and creates soft bodies with the instructions within.  
----- USAGE -----  
to create a soft body from a preset:  
start the line with '=' then add you arguments separated by a single white space.   
don't put parenthesies around the coordinates. example:  
`= square 500,300 black 5 length=30`  

to create a soft body from scratch:  
start a line with  '/' to create a new soft body, followed by the center of your soft body,  
optionally followed by the name of that soft body. example:  
`/ 100,50 rainbow square`  

to add vertices, start a line with '+' followed by your arguments separated by a single white space.  
the coordinates are relative to the object's center example:  
`+ red -20,-20 0,0 floating=True radius=10`  

to add springs, start a line with '-' followed by your arguments separated by a single white space.  
for the first and second node, use the index of the the balls you want to join  
(index order is the order to added the vertices). example:  
`+ yellow 0 1 force=0.7`  

to add comments start a line with '#'

example file:  
```
#small black cube
= square 500,300 black 5 length=30

#french flag
/ 300,100 example object
+ blue -40,0 0,0 radius=10 floating=True
+ white 0,0 0,0 radius=10 floating=True
+ red 40,0 0,0 radius=10 floating=True

- white 0 1 thickness=2
- white 1 2 thickness=2
```

# License
Do whatever you want with this, as long as you don't sell a (modified) version of the package. Making games with it and selling them is fine though.
