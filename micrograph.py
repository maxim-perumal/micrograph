import struct
import moderngl
import numpy as np
from pyrr import Quaternion, Matrix44, Vector3
from moderngl_window import geometry
from moderngl_window import WindowConfig
from moderngl_window.opengl.vao import VAO
import cProfile
import pstats
import moderngl_window
import argparse
import os
import time as tm

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
        self.set_transform(self.get_transform() * rotation_matrix)

    def translate_xyz(self, x: float, y: float,z: float):
        translation_matrix = Matrix44.from_translation((x, y, z))
        self.set_transform(translation_matrix * self.get_transform())

    def scale_xyz(self, x: float, y: float,z: float):
        scale_matrix = Matrix44.from_scale((x, y, z))
        self.set_transform(scale_matrix * self.get_transform())

    def render(self, prog, window):
        raise NotImplementedError("Subclasses should implement this method.")

class Cube(SimObject):
    def __init__(self, size, color, position):
        super().__init__()
        self.size = size
        self.color = color
        self.geometry = geometry.cube(size=self.size)
        self.set_translate_xyz_world(*position)

    def render(self, prog, window):
        model = self.get_transform() * Matrix44.from_scale(self.size)

        prog['Model'].write(model.astype('float32').tobytes())
        projection = Matrix44.perspective_projection(75, window.aspect_ratio, 1, 100)

        matrix44 = projection * model
        flattened_matrix44 = matrix44.flatten().tolist()

        window.scale.value = flattened_matrix44
        prog['Color'].value = self.color

        self.geometry.render(prog)

class SimWindow(WindowConfig):
    title = "3D Cube"
    window_size = (1280, 720)
    aspect_ratio = window_size[0] / window_size[1]

    # Load in the shader source code
    file = open("shaders/vertex_shader.glsl")
    vertex_shader_source = file.read()
    file = open("shaders/fragment_shader.glsl")
    fragment_shader_source = file.read()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.ctx.program(vertex_shader=self.vertex_shader_source, fragment_shader=self.fragment_shader_source)
        self.scale = self.prog['ModelViewProjection']
        self.setup()

    def setup(self):
        pass

    def update(self, time):
        pass

    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.9, 0.9, 0.9)
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.update(time)
        for obj in self.objects.values():
            obj.render(self.prog, self)

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)

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
