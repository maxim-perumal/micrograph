import os
import pstats
import struct
import cProfile
import moderngl
import argparse
import time as tm
import numpy as np
import moderngl_window
from typing import Tuple
from camera import Camera, CameraMouvement
from pyrr import Matrix44
from moderngl_window import geometry
from moderngl_window import WindowConfig
from moderngl_window.opengl.vao import VAO

class SimObject:
    def __init__(self):
        self.transform_state = Matrix44.identity()

    def get_transform(self):
        return self.transform_state

    def set_transform(self, transformation):
        self.transform_state = transformation # Extract the current translation

    def get_translation(self):
        return self.get_transform()[3, 0:3]

    def get_rotation(self):
        return self.get_transform()[0:3, 0:3]

    def set_rotation_euler_world(self, x: float, y: float,z: float):
        rotation_matrix = Matrix44.from_eulers((x, y, z))
        rotation_matrix[3, 0:3] = self.get_translation() # Preserve the current translation
        self.set_transform(rotation_matrix)

    def set_translate_xyz_world(self, x: float, y: float,z: float):
        translation_matrix = Matrix44.from_translation((x, y, z))
        translation_matrix[0:3, 0:3] = self.get_rotation() # Preserve the current translation
        self.set_transform(translation_matrix)

    def rotate_euler(self, x: float, y: float,z: float):
        rotation_matrix = Matrix44.from_eulers((x, y, z))
        self.set_transform(rotation_matrix * self.get_transform())

    def translate_xyz(self, x: float, y: float,z: float):
        translation_matrix = Matrix44.from_translation((x, y, z))
        self.set_transform(translation_matrix * self.get_transform())

    def scale_xyz(self, x: float, y: float,z: float):
        scale_matrix = Matrix44.from_scale((x, y, z))
        self.set_transform(scale_matrix * self.get_transform())

    def render(self, prog, window):
        raise NotImplementedError("Subclasses should implement this method.")

class Cube(SimObject):
    def __init__(self, size: Tuple[int, int], color: Tuple[int, int, int], position: Tuple[int, int, int]):
        super().__init__()
        self.size = size
        self.color = color
        self.geometry = geometry.cube(size=self.size)
        self.set_translate_xyz_world(*position)

    def render(self, prog, window):
        # render the model
        model = self.get_transform() * Matrix44.from_scale(self.size)

        prog['model'].write(model.astype('float32').tobytes())

        prog['Color'].value = self.color

        self.geometry.render(prog)

class SimWindow(WindowConfig):
    title = "3D Cube"
    camera = Camera()
    window_size = (1280, 720)
    aspect_ratio = window_size[0] / window_size[1]
    lastX, lastY = window_size[0]/2, window_size[1]/2
    firstMouse = True
    cursor = False

    # Load in the shader source code
    file = open("shaders/vertex_shader.glsl")
    vertex_shader_source = file.read()
    file = open("shaders/fragment_shader.glsl")
    fragment_shader_source = file.read()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.ctx.program(vertex_shader=self.vertex_shader_source, fragment_shader=self.fragment_shader_source)
        self.setup()
        self.deltaTime = 0.0
        self.previousTime = 0.0

    def setup(self):
        pass

    def update(self, time: float):
        pass

    def ProcessInput(self):
        if self.wnd.is_key_pressed(self.wnd.keys.W):
            self.camera.ProcessKeyboard(CameraMouvement.FORWARD, self.deltaTime)
        if self.wnd.is_key_pressed(self.wnd.keys.S):
            self.camera.ProcessKeyboard(CameraMouvement.BACKWARD, self.deltaTime)
        if self.wnd.is_key_pressed(self.wnd.keys.A):
            self.camera.ProcessKeyboard(CameraMouvement.LEFT, self.deltaTime)
        if self.wnd.is_key_pressed(self.wnd.keys.D):
            self.camera.ProcessKeyboard(CameraMouvement.RIGHT, self.deltaTime)

    def render(self, time: float, frame_time: float):
        # Process input keyboard
        self.ProcessInput()

        self.ctx.clear(0.9, 0.9, 0.9)
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.deltaTime = time - self.previousTime
        self.previousTime = time

        # Projection matrix
        projection = Matrix44.perspective_projection(75, self.aspect_ratio, 1, 100)

        # View matrix
        view = self.camera.GetViewMatrix()

        # Set uniform variable from shader
        self.prog['projection'].write(projection.astype('float32').tobytes())
        self.prog['view'].write(view.astype('float32').tobytes())

        self.update(time)
        for obj in self.objects.values():
            obj.render(self.prog, self)

    def resize(self, width: int, height: int) -> None:
        self.ctx.viewport = (0, 0, width, height)
    
    def mouse_position_event(self, x: int, y:int, dx: int, dy: int) -> None:
        if self.firstMouse:
            self.lastX = x
            self.lastY = y
            self.firstMouse = False

        xoffset = self.lastX - x
        yoffset = self.lastY - y

        self.lastX = x
        self.lastY = y

        self.camera.ProcessMouseMouvement(xoffset, yoffset)
    
    def mouse_scroll_event(self, x_offset: float, y_offset: float) -> None:
        pass
    
    def key_event(self, key, action, modifiers):
        if self.wnd.keys.ESCAPE == key:
            self.wnd.close()
        
def run_window(window):
    moderngl_window.run_window_config(window)

# Create new argument parser
def new_parse_args(args=None, parser=None):
    if parser is None:
        parser = moderngl_window.create_parser()
    parser.add_argument('--profile', action='store_true', help='Enable the profiler')
    return parser.parse_args(args=args)

# Replace moderngl_window's argument parser with micrograph's
moderngl_window.parse_args = new_parse_args
