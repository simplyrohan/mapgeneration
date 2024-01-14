from perlin_noise import PerlinNoise
from scipy.interpolate import interp1d

noise = PerlinNoise(octaves=3)
spline_points = [(-1, -0.8), (0, 0), (0.35, 0.35), (0.37, 0.75), (0.5, 0.8), (2, 1.1)]
x, y = zip(*spline_points)


def generate(
    width,
    height,
    ocean,
    travel=1 / 100,
    scale=20,
    octaves=3,
    sand=0.015,
    points=spline_points,
):
    x, y = zip(*points)
    interp = interp1d(x, y, kind="linear")
    noise.octaves = octaves
    map = []
    for x in range(width):
        for y in range(height):
            z = noise([x * travel, y * travel])
            z = interp(z)
            z *= scale
            if ocean < (z) / scale <= ocean + sand:
                map.append([x, y, z + 1, 2, None])
            elif (z) / scale <= ocean:
                map.append([x, y, z + 1, 2, None])
                map.append([x, y, ocean * scale, 1, (z) / scale])

            else:
                for i in range(int(z)):
                    map.append([x, y, i + (z - int(z)), 4, None])
                map.append([x, y, z, 0, None])

    return map


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    interp = interp1d(x, y, kind="linear")
    d = [((x - 100) / 100, interp((x - 100) / 100)) for x in range(200)]
    xd, yd = zip(*d)
    plt.plot(xd, yd)
    plt.show()
