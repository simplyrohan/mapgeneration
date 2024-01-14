import pygame
from math import sin
import perlin_noise
from map import generate
import map
import threading
from tkinter import *
from tkinter import ttk
import sv_ttk

tk = Tk()
tk.title("Options")
tk.geometry("300x600")


def regen(*args, **kwargs):
    pass


ttk.Label(tk, text="Complexity").pack(pady=(6, 0))
complexity = ttk.Scale(
    tk,
    from_=1,
    to=120,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
complexity.set(72)
complexity.pack()

ttk.Label(tk, text="Scale").pack(pady=(6, 0))
size = ttk.Scale(
    tk,
    from_=1,
    to=50,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
size.set(20)
size.pack()

ttk.Label(tk, text="Ocean Level").pack(pady=(6, 0))
oceane = ttk.Scale(
    tk,
    from_=-5,
    to=50,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
oceane.set(10)
oceane.pack()

ttk.Label(tk, text="Octaves").pack(pady=(6, 0))
octaves = ttk.Scale(
    tk,
    from_=1,
    to=10,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
octaves.set(3)
octaves.pack()

ttk.Label(tk, text="Sand").pack(pady=(6, 0))
sande = ttk.Scale(
    tk,
    from_=1,
    to=100,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
sande.set(15)
sande.pack()

ttk.Label(tk, text="Choppiness").pack(pady=(6, 0))
tide = ttk.Scale(
    tk,
    from_=1,
    to=100,
    orient=HORIZONTAL,
)
tide.set(16)
tide.pack()

ttk.Label(tk, text="Wave Size").pack(pady=(6, 0))
wave = ttk.Scale(
    tk,
    from_=1,
    to=100,
    orient=HORIZONTAL,
)
wave.set(27)
wave.pack()

ttk.Label(tk, text="Murkiness").pack(pady=(6, 0))
murk = ttk.Scale(
    tk,
    from_=0,
    to=90,
    orient=HORIZONTAL,
)
murk.set(32)
murk.pack()

ttk.Label(tk, text="Mountain Threshold").pack(pady=(6, 0))
mountthres = ttk.Scale(
    tk,
    from_=0,
    to=100,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
mountthres.set(35)
mountthres.pack()

ttk.Label(tk, text="Mountain Gradient").pack(pady=(6, 0))
mountgrad = ttk.Scale(
    tk,
    from_=0,
    to=100,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
mountgrad.set(20)
mountgrad.pack()

ttk.Label(tk, text="Mountain Height").pack(pady=(6, 0))
mountheight = ttk.Scale(
    tk,
    from_=0,
    to=120,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
mountheight.set(38)
mountheight.pack()

ttk.Label(tk, text="Snow Threshold").pack(pady=(6, 0))
snow_thresh = ttk.Scale(
    tk,
    from_=0,
    to=120,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
snow_thresh.set(80)
snow_thresh.pack()


def reg():
    map.noise = map.PerlinNoise(octaves=octaves.get())
    regen()


but = ttk.Button(tk, text="Regenerate", command=reg, style="Accent.TButton")
but.pack(pady=12)

sv_ttk.set_theme("dark")


# end of Tkinter


watern = perlin_noise.PerlinNoise(octaves=1)

pygame.init()

screen = pygame.display.set_mode([1000, 600])
pygame.display.set_caption("Untitled Game")

clock = pygame.time.Clock()

dt = 0

scale = 0.4

img = pygame.transform.scale(pygame.image.load("tile.png"), [32 * scale, 32 * scale])
sand = pygame.transform.scale(pygame.image.load("sand.png"), [32 * scale, 32 * scale])
water = pygame.transform.scale(pygame.image.load("water.png"), [32 * scale, 32 * scale])
water.set_alpha(140)
stone = pygame.transform.scale(pygame.image.load("stone.png"), [32 * scale, 32 * scale])
snow = pygame.transform.scale(pygame.image.load("snow.png"), [32 * scale, 32 * scale])

music = pygame.mixer.music.load("bg.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

m = generate(180, 180, ocean=0.1, travel=1 / 48, scale=20, octaves=3)
n = 0


def regen():
    global m
    travel = 1 / (120 - complexity.get())
    scale = size.get()
    ocean = oceane.get() / 1000
    octs = octaves.get()
    sandv = sande.get() / 1000
    spline_points = [
        (-1, -0.5),
        (0, 0),
        (mountthres.get() / 100, mountthres.get() / 100),
        (
            mountthres.get() / 100 + (mountgrad.get() / 100),
            mountthres.get() / 100 + (mountheight.get() / 100),
        ),
        (2, 1.1),
    ]
    m = generate(
        90,
        90,
        ocean=ocean,
        travel=travel,
        scale=scale,
        octaves=octs,
        sand=sandv,
        points=spline_points,
    )


reg()


running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((160, 180, 200))  # Background Color

    # Content to draw
    for tile in m:
        x, y, z, cell, d = tile
        if cell == 0:
            if z > snow_thresh.get():
                screen.blit(
                    snow,
                    [
                        x * (16 * scale) - y * (16 * scale) + 485,
                        x * (8 * scale) + y * (8 * scale) - z * (16 * scale) + 100,
                    ],
                )
            else:
                screen.blit(
                    img,
                    [
                        x * (16 * scale) - y * (16 * scale) + 485,
                        x * (8 * scale) + y * (8 * scale) - z * (16 * scale) + 100,
                    ],
                )
        elif cell == 4:
            screen.blit(
                stone,
                [
                    x * (16 * scale) - y * (16 * scale) + 485,
                    x * (8 * scale) + y * (8 * scale) - z * (16 * scale) + 100,
                ],
            )

        elif cell == 1:
            water.set_alpha(
                255 * ((abs(d - (oceane.get() / 1000))) / 0.1 + (murk.get() / 100))
            )
            rn = n
            z += (watern((((x * 1 / 15) + rn), (y * 1 / 25))) ** 2) * (wave.get() / 5)

            screen.blit(
                water,
                [
                    x * (16 * scale) - y * (16 * scale) + 485,
                    x * (8 * scale) + y * (8 * scale) - (z) * (16 * scale) + 100,
                ],
            )

        elif cell == 2:
            screen.blit(
                sand,
                [
                    x * (16 * scale) - y * (16 * scale) + 485,
                    x * (8 * scale) + y * (8 * scale) - z * (16 * scale) + 100,
                ],
            )

    n += tide.get() / 1000
    pygame.display.flip()
    dt = clock.tick(60)  # Change this to FPS
    pygame.display.set_caption(f"Untitled Game | FPS: {round(clock.get_fps(), 2)}")
    tk.update()
    tk.update_idletasks()
pygame.quit()
