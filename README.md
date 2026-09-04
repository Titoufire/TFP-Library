# TFP-Library
Titoufire's Physics Library, contains everything needed to build video games with a customizable physics engine.

# Installation and importation
download the zip file of the latest version, and unzip it in your project folder (same level as your main.py) without creating a folder.  
Then, simply import it with  
`from Tfp.tfp import Tfp`   
if you are having any issues with this, please open an issue  

# How to use
after importing the library, initialize pygame as always, and setup your window. Once done, create a Tfp instance like so:  
`context = Tfp()`  

and a Camera(pos: Vec2, zoom: float)
`camera = context.Camera(Vec2(0, 0), 1)`

then tell give Tfp your window, camera, and number of physics frames per visual frame using Tfp().setup(window: pygame.Surface, camera: Tfp.Camera, physics_frames: int)  
`context.setup(screen, camera, physics_frames=10)`

and you have Tfp setup !

# Functions
