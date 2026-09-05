# TFP-Library
Titoufire's Physics Library, contains everything needed to build video games with a customizable physics engine.

# Installation and importation
Download the zip file of the latest version, and unzip it in your project folder (same level as your main.py) without creating a folder.  
Then, simply import it with  
`from Tfp.tfp import Tfp`   
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
#### setup (window: pygame.surface, camera: Camera, physics_frames: int=10)
Sets up the tfp context

***
#### draw ()
Draws all objects on the window, but DOESN'T update the display

***
#### simulate (dt: float)
Does all of the simulation calculations, the chose amount of times (physics_frames)  
`dt` is delta_time in seconds. in pygame it is defined by `pygame.time.Clock().tick() / 1000`
***
#### set_gravity (full: Vec2=None, strenght: float=0, direction: Vec2=None)
Sets or modify gravity with the according parameters. Only use ONE parameter at a time.  
`full` sets the gravity vector to the given one.  
`strength` sets the length of the gravity vector to the given length, without changing the direction.  
`direction` sets the direction of the gravity vector to the given vector, without changing the length.  
***
#### new_line (color: str | pygame.Color, start: tuple[int, int], end: tuple[int, int], rest=1, fric=0)
Creates a new line with the given parameters, and returns it. `start` and `end` must be absolute coordinates
***
#### new_ball (color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int], rest=1, fric=0, mass=1, floating=False, radius=20)
Creates a new ball with the given parameters, and returns it.
***
#### new_spring (color: str | pygame.Color, node1: Ball, node2: Ball, length=None, force=0.5, thickness=None, damp=0.3, dz = 0.01)
Creates a new spring with the given parameters, and returns it.
***
#### new_rigid (color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int], vertices: list[tuple[int, int]], edge_color=None, edge_thickness=1, fric=0, rest=1, fixed=False)
Creates a new rigid_body with the given parameters, and returns it.
***
#### say_hello ()
Says hello in the console

# License
Do whatever you want with this, as long as you don't sell a (modified) version of the package. Making games with it and selling them is fine though.
