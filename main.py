import micrograph
import moderngl_window
from pyrr import Quaternion, Matrix44, Vector3

class MainWindow(micrograph.SimWindow):
    def setup(self):
        self.objects = {
            "cube1": micrograph.Cube((2, 2, 2), (1.0, 0.4, 0.0), (-4.0, 0.0, -10.0))
        }

    def update(self, time):
        self.objects["cube1"].rotate_euler(0.01, 0.01, 0.01)
        self.objects["cube1"].translate_xyz(0.01, 0, 0)

if __name__ == '__main__':
    args = moderngl_window.parse_args()
    if args.profile:
        cProfile.runctx("micrograph.run_main_window()", globals(), locals(), "output.pstats")
        print("\033[92mProfiling done. Run \033[93m'snakeviz output.pstats'\033[92m to visualize the results.\033[0m")
    else:
        micrograph.run_window(MainWindow)