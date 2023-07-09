import moderngl
import numpy as np
from pyrr import Matrix44
from moderngl_window import geometry
from moderngl_window import WindowConfig
import cProfile
import moderngl_window
import argparse

class SimObject:
    def __init__(self, size, color, position, geometry):
        self.size = size
        self.color = color
        self.position = position
        self.rotation = Matrix44.identity(dtype='f4')
        self.geometry = geometry
        self.model = Matrix44.identity(dtype='f4')

    def transform(self, transformation):
        self.rotation = transformation

    def update(self):
        self.model = self.rotation * Matrix44.from_scale(self.size, dtype='f4')

    def render(self, prog, window):
        model = self.model
        translation = Matrix44.from_translation(self.position, dtype='f4')
        prog['Model'].write(model.astype('float32').tobytes())
        modelview = translation * model
        projection = window.projection
        matrix44 = projection * modelview
        prog['ModelViewProjection'].write(matrix44.astype('float32').tobytes())
        prog['Color'].value = self.color
        self.geometry.render(prog)

class MainWindow(WindowConfig):
    title = "3D Cube"
    window_size = (1280, 720)
    aspect_ratio = window_size[0] / window_size[1]
    projection = Matrix44.perspective_projection(75, aspect_ratio, 1, 100, dtype='f4')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.ctx.program(vertex_shader='Shader/vertex_shader.glsl', fragment_shader='Shader/fragment_shader.glsl')
        self.geometry = geometry.cube(size=(2, 2, 2))
        self.setup()

    def setup(self):
        self.objects = [
            SimObject((2, 2, 2), (1.0, 0.4, 0.0), (-4.0, 0.0, -5.0), self.geometry),
            SimObject((2, 2, 2), (0.0, 0.4, 1.0), (4.0, 0.0, -5.0), self.geometry),
            SimObject((2, 2, 2), (0.0, 0.4, 1.0), (0.0, 0.0, -5.0), self.geometry)
        ]

    def update(self, time):
        rotation1 = Matrix44.from_eulers((time * 1, time * 1, time * 1), dtype='f4')
        rotation2 = Matrix44.from_eulers((time * 0.5, time * 1, time * 1), dtype='f4')

        self.objects[0].transform(rotation1)
        self.objects[0].update()

        self.objects[1].transform(rotation2)
        self.objects[1].update()

        self.objects[2].transform(rotation1)
        self.objects[2].update()

    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.9, 0.9, 0.9)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.update(time)
        for obj in self.objects:
            obj.render(self.prog, self)

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)

    def key_event(self, key, action, modifiers):
        if self.wnd.keys.ESCAPE == key:
            self.wnd.close()

def run_main_window():
    moderngl_window.run_window_config(MainWindow)

def new_parse_args(args=None, parser=None):
    if parser is None:
        parser = moderngl_window.create_parser()
    parser.add_argument('--profile', action='store_true', help='Enable the profiler')
    return parser.parse_args(args=args)

moderngl_window.parse_args = new_parse_args

if __name__ == '__main__':
    args = moderngl_window.parse_args()
    if args.profile:
        cProfile.runctx("run_main_window()", globals(), locals(), "output.pstats")
        print("\033[92mProfiling done. Run \033[93m'snakeviz output.pstats'\033[92m to visualize the results.\033[0m")
    else:
        run_main_window()