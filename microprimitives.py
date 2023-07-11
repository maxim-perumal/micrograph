from math import radians
from typing import Tuple
from pyrr import Matrix44
from moderngl_window import geometry

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

    def set_rotation_euler_world(self, x: float, y: float,z: float) -> None:
        rotation_matrix = Matrix44.from_eulers((radians(x), radians(y), radians(z)))
        rotation_matrix[3, 0:3] = self.get_translation() # Preserve the current translation
        self.set_transform(rotation_matrix)

    def set_translate_xyz_world(self, x: float, y: float,z: float) -> None:
        translation_matrix = Matrix44.from_translation((x, y, z))
        translation_matrix[0:3, 0:3] = self.get_rotation() # Preserve the current translation
        self.set_transform(translation_matrix)

    def rotate_euler(self, x: float, y: float,z: float):
        rotation_matrix = Matrix44.from_eulers((radians(x), radians(y), radians(z)))
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
    def __init__(self, size: Tuple[int, int, int], color: Tuple[int, int, int], position: Tuple[int, int, int]):
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

class Sphere(SimObject):
    def __init__(self, radius: int, color: Tuple[int, int, int], position: Tuple[int, int, int]):
        super().__init__()
        self.radius = radius
        self.color = color
        self.geometry = geometry.sphere(radius=radius)
        self.set_translate_xyz_world(*position)

    def render(self, prog, window):
        # render the model
        model = self.get_transform() * Matrix44.from_scale((self.radius, self.radius, self.radius))

        prog['model'].write(model.astype('float32').tobytes())

        prog['Color'].value = self.color

        self.geometry.render(prog)

class Quad(SimObject):
    def __init__(self, size: Tuple[int, int, int], color: Tuple[int, int, int], position: Tuple[int, int, int]):
        super().__init__()
        self.size = size
        self.color = color
        self.geometry = geometry.quad_2d(size=self.size[:2])
        self.set_translate_xyz_world(*position)

    def render(self, prog, window):
        # render the model
        model = self.get_transform() * Matrix44.from_scale(self.size)

        prog['model'].write(model.astype('float32').tobytes())

        prog['Color'].value = self.color

        self.geometry.render(prog)