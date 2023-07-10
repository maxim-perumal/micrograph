import micrograph
import moderngl_window
from pyrr import Quaternion, Matrix44, Vector3
import cProfile

class MainWindow(micrograph.SimWindow):
    def setup(self):
        self.objects = {
            "cube1": micrograph.Cube((2, 2, 2), (1.0, 0.4, 0.0), (0.0, 0.0, 0.0)),
            "sphere1": micrograph.Sphere(2, (0.0, 0.4, 1.0), (0.0, 0.0, 0.0)),
            "quad1": micrograph.Quad((2, 2, 2), (1.0, 0.4, 1.0), (0.0, -5.0, 0.0)),
        }
        self.objects["cube1"].set_rotation_euler_world(0.0, 1.57/2, 0.0)
        self.objects["cube1"].set_translate_xyz_world(-4.0, 0.0, -10.0)

    def update(self, time):
        self.objects["cube1"].rotate_euler(0.001, 0.0, 0.0)
        self.objects["cube1"].translate_xyz(0.01, 0, 0)
        pass

if __name__ == '__main__':
    args = moderngl_window.parse_args()
    if args.profile:
        cProfile.runctx("micrograph.run_window(MainWindow)", globals(), locals(), "output.pstats")
        print("\033[92mProfiling done. Run \033[93m'snakeviz output.pstats'\033[92m to visualize the results.\033[0m")
    else:
        micrograph.run_window(MainWindow)