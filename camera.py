from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians
from enum import Enum

class CameraMouvement(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4

class Camera(object):
    def __init__(self, 
                camera_pos: Vector3=Vector3([0.0, 0.0, 0.0]),
                camera_front: Vector3=Vector3([0.0, 0.0, -1.0]),
                camera_up: Vector3=Vector3([0.0, 1.0, 0.0]),
                camera_right: Vector3=Vector3([1.0, 0.0, 0.0]),
                mouse_sensitivity: float=0.1,
                speed: float=10.0) -> None:

        self.camera_pos = camera_pos
        self.camera_front = camera_front
        self.camera_up = camera_up
        self.camera_right = camera_right
        self.WorldUp = camera_up

        self.mouse_sensitivity = mouse_sensitivity
        self.speed = speed
        self.yaw = -90.0
        self.pitch = 0.0

        self.updateCameraVectors()
    
    # Returns the view matrix
    def GetViewMatrix(self) -> matrix44:
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    # Processes input received from mouse
    def ProcessMouseMouvement(self, xoffset: float, yoffset: float, constrainPitch: bool=True) -> None:
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.yaw += xoffset
        self.pitch -= yoffset

        # Constrain pitch to prevent screen flipping
        if constrainPitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0
        
        # Update all the vectors
        self.updateCameraVectors()

    # Processes input received from keyboard
    def ProcessKeyboard(self, direction: str, deltaTime: float) -> None:
        velocity = self.speed * deltaTime
        if direction == CameraMouvement.FORWARD:
            self.camera_pos += self.camera_front * velocity
        if direction == CameraMouvement.BACKWARD:
            self.camera_pos -= self.camera_front * velocity
        if direction == CameraMouvement.LEFT:
            self.camera_pos -= self.camera_right * velocity
        if direction == CameraMouvement.RIGHT:
            self.camera_pos += self.camera_right * velocity
        

    def ProcessMouseScroll(self):
        pass

    def updateCameraVectors(self) -> None:
        # Compute the new Front vector
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.camera_front = vector.normalise(front)

        # Re-compute the camera_right and camera_up vectors
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, self.WorldUp))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))
