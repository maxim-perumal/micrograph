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

class MainWindow(WindowConfig):
    title = "3D Cube"
    window_size = (1280, 720)
    aspect_ratio = window_size[0] / window_size[1]

    vertex_shader_source = """
    #version 330
    uniform mat4 ModelViewProjection;
    uniform mat4 Model;
    in vec3 in_position;
    in vec3 in_normal;
    in vec2 in_texcoord_0;
    out vec2 uv;
    out vec3 normal;
    void main() {
        gl_Position = ModelViewProjection * vec4(in_position, 1.0);
        uv = in_texcoord_0;
        normal = mat3(Model) * in_normal;
    }
    """

    fragment_shader_source = """
    #version 330
    uniform vec3 Color;
    in vec2 uv;
    in vec3 normal;
    out vec4 fragColor;
    void main() {
        vec3 ambientLight = vec3(0.5, 0.5, 0.5);
        vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
        float l = dot(normalize(normal), lightDir);
        vec3 diffuse = max(l, 0.0) * Color;
        vec3 ambient = ambientLight * Color;
        fragColor = vec4(diffuse + ambient, 1.0);
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.ctx.program(vertex_shader=self.vertex_shader_source, fragment_shader=self.fragment_shader_source)
        self.scale = self.prog['ModelViewProjection']
        self.setup()

    def setup(self):
        self.objects = {
            "cube1": Cube((2, 2, 2), (1.0, 0.4, 0.0), (-4.0, 0.0, -5.0)),
            "cube2": Cube((2, 2, 2), (0.0, 0.4, 1.0), (4.0, 0.0, -5.0)),
            "cube3": Cube((2, 2, 2), (0.0, 0.4, 1.0), (0.0, 0.0, -5.0))
        }

    def update(self, time):
        rotation1 = Matrix44.from_eulers((time * 1, time * 1, time * 1))
        self.objects["cube1"].transform(rotation1)

        rotation2 = Matrix44.from_eulers((time * 0.5, time * 1, time * 1))
        self.objects["cube2"].transform(rotation2)

        self.objects["cube3"].transform(rotation1)

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

def run_main_window():
    moderngl_window.run_window_config(MainWindow)

# Create new argument parser
def new_parse_args(args=None, parser=None):
    if parser is None:
        parser = moderngl_window.create_parser()
    parser.add_argument('--profile', action='store_true', help='Enable the profiler')
    return parser.parse_args(args=args)

# Replace moderngl_window's argument parser with micrograph's
moderngl_window.parse_args = new_parse_args

if __name__ == '__main__':
    args = moderngl_window.parse_args()
    if args.profile:
        cProfile.runctx("run_main_window()", globals(), locals(), "output.pstats")
        print("\033[92mProfiling done. Run \033[93m'snakeviz output.pstats'\033[92m to visualize the results.\033[0m")
    else:
        run_main_window()