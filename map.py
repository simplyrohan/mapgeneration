from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=3)


def generate(width, height, ocean, travel=1/100, scale=20, octaves=3, sand=0.015):
    noise.octaves = octaves
    map = []
    for x in range(width):
        for y in range(height):
            z = (noise([x * travel, y * travel]) ** 2) * scale + 5
            if ocean < (z - 5)/scale <= ocean+sand:
                map.append([x, y, z+1, 2, None])
                
            elif (z - 5) / scale <= ocean:
                map.append([x, y, z+1, 2, None])
                map.append([x, y, ocean * scale + 5, 1, (z - 5) / scale])
            else:
                map.append([x, y, z, 0, None])

    return map
