import struct
import moderngl
import numpy as np
from pyrr import Matrix44
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
    def __init__(self, size, color, position):
        self.size = size
        self.color = color
        self.position = position
        self.rotation = Matrix44.identity()

    def transform(self, transformation):
        self.rotation = transformation

    def render(self, prog, window):
        pass

class Cube(SimObject):
    def __init__(self, size, color, position):
        super().__init__(size, color, position)
        self.geometry = geometry.cube(size=self.size)

    def render(self, prog, window):
        model = self.rotation * Matrix44.from_scale((1, 1, 1))
        translation = Matrix44.from_translation(self.position)

        prog['Model'].write(model.astype('float32').tobytes())
        modelview = translation * model
        projection = Matrix44.perspective_projection(75, window.aspect_ratio, 1, 100)

        matrix44 = projection * modelview
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
