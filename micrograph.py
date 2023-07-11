import os
import imgui
import pstats
import struct
import cProfile
import moderngl
import argparse
import time as tm
import numpy as np
import moderngl_window
from typing import Tuple
from pyrr import Matrix44
from moderngl_window import WindowConfig
from camera import Camera, CameraMouvement
from moderngl_window.opengl.vao import VAO
from moderngl_window.integrations.imgui import ModernglWindowRenderer

class SimWindow(WindowConfig):
    # Window parameters
    title = "3D Cube"
    window_size = (1280, 720)
    aspect_ratio = window_size[0] / window_size[1]

    # Camera
    camera = Camera()

    # Mouse parameters
    cursor = True

    # Load in the shader source code
    file = open("shaders/vertex_shader.glsl")
    vertex_shader_source = file.read()
    file = open("shaders/fragment_shader.glsl")
    fragment_shader_source = file.read()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        imgui.create_context()
        self.wnd.ctx.error
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.wnd.mouse_exclusivity = True
        self.prog = self.ctx.program(vertex_shader=self.vertex_shader_source, fragment_shader=self.fragment_shader_source)
        self.setup()

        # Setup time
        self.deltaTime = 0.0
        self.previousTime = 0.0

    def setup(self):
        pass

    def update(self, time: float):
        pass

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
        
        # Render imgui's windows
        # self.render_ui()
    
    def render_ui(self):
        imgui.new_frame()
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)
                
                imgui.end_menu()
            imgui.end_main_menu_bar()
        
        imgui.show_test_window()

        imgui.begin("Custom Micrograph", True)
        imgui.text("Cube")
        imgui.text("Sphere")
        imgui.text("Quad")
        imgui.text_colored("Micrograph", 0.2, 1., 0.)
        imgui.end()

        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    def resize(self, width: int, height: int) -> None:
        self.ctx.viewport = (0, 0, width, height)
        # Projection matrix
        projection = Matrix44.perspective_projection(75, self.wnd.aspect_ratio, 1, 100)
        self.prog['projection'].write(projection.astype('float32').tobytes())

        self.imgui.resize(width, height)
    
    def mouse_position_event(self, x: int, y:int, dx: int, dy: int) -> None:
        self.imgui.mouse_position_event(x, y, dx, dy)

        # if self.wnd.mouse_states.left:
        self.camera.ProcessMouseMouvement(dx, dy)
    
    def mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)
    
    def ProcessInput(self):
        if not self.wnd.mouse_states.left:
            pass
            
        if self.wnd.is_key_pressed(self.wnd.keys.W):
            self.camera.ProcessKeyboard(CameraMouvement.FORWARD, self.deltaTime)
        if self.wnd.is_key_pressed(self.wnd.keys.S):
            self.camera.ProcessKeyboard(CameraMouvement.BACKWARD, self.deltaTime)
        if self.wnd.is_key_pressed(self.wnd.keys.A):
            self.camera.ProcessKeyboard(CameraMouvement.LEFT, self.deltaTime)
        if self.wnd.is_key_pressed(self.wnd.keys.D):
            self.camera.ProcessKeyboard(CameraMouvement.RIGHT, self.deltaTime)
        if self.wnd.is_key_pressed(self.wnd.keys.Q):
            self.camera.ProcessKeyboard(CameraMouvement.UP, self.deltaTime)
        if self.wnd.is_key_pressed(self.wnd.keys.E):
            self.camera.ProcessKeyboard(CameraMouvement.DOWN, self.deltaTime)

    def key_event(self, key, action, modifiers):
        self.imgui.key_event(key, action, modifiers)

        keys = self.wnd.keys

        if action == keys.ACTION_PRESS:
            if key == keys.ESCAPE:
                self.wnd.close()

            if key == keys.M:
                self.wnd.mouse_exclusivity = not self.wnd.mouse_exclusivity
    
    def unicode_char_entered(self, char):
        self.imgui.unicode_char_entered(char)
        
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
