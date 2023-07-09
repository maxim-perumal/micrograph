import micrograph
import moderngl_window
from pyrr import Matrix44

class MainWindow(micrograph.SimWindow):
    def setup(self):
        self.objects = {
            "cube1": micrograph.Cube((2, 2, 2), (1.0, 0.4, 0.0), (-4.0, 0.0, -5.0)),
            "cube2": micrograph.Cube((2, 2, 2), (0.0, 0.4, 1.0), (4.0, 0.0, -5.0)),
            "cube3": micrograph.Cube((2, 2, 2), (0.0, 0.4, 1.0), (0.0, 0.0, -5.0)),
            "cube4": micrograph.Cube((2, 2, 2), (0.0, 0.4, 1.0), (0.0, 2.5, -5.0))
        }

    def update(self, time):
        rotation1 = Matrix44.from_eulers((time * 1, time * 1, time * 1))
        self.objects["cube1"].transform(rotation1)

        rotation2 = Matrix44.from_eulers((time * 0.5, time * 4, time * 1))
        self.objects["cube2"].transform(rotation2)

        self.objects["cube3"].transform(rotation1)

if __name__ == '__main__':
    args = moderngl_window.parse_args()
    if args.profile:
        cProfile.runctx("micrograph.run_main_window()", globals(), locals(), "output.pstats")
        print("\033[92mProfiling done. Run \033[93m'snakeviz output.pstats'\033[92m to visualize the results.\033[0m")
    else:
        micrograph.run_window(MainWindow)