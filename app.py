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


ttk.Label(tk, text="Complexity").pack(pady=(12, 0))
complexity = ttk.Scale(
    tk,
    from_=1,
    to=120,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
complexity.set(72)
complexity.pack()

ttk.Label(tk, text="Scale").pack(pady=(12, 0))
size = ttk.Scale(
    tk,
    from_=1,
    to=50,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
size.set(20)
size.pack()

ttk.Label(tk, text="Ocean Level").pack(pady=(12, 0))
oceane = ttk.Scale(
    tk,
    from_=1,
    to=100,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
oceane.set(10)
oceane.pack()

ttk.Label(tk, text="Octaves").pack(pady=(12, 0))
octaves = ttk.Scale(
    tk,
    from_=1,
    to=10,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
octaves.set(3)
octaves.pack()

ttk.Label(tk, text="Sand").pack(pady=(12, 0))
sande = ttk.Scale(
    tk,
    from_=1,
    to=100,
    orient=HORIZONTAL,
    command=lambda x: regen(),
)
sande.set(15)
sande.pack()

ttk.Label(tk, text="Choppiness").pack(pady=(12, 0))
tide = ttk.Scale(
    tk,
    from_=1,
    to=100,
    orient=HORIZONTAL,
)
tide.set(16)
tide.pack()

ttk.Label(tk, text="Wave Size").pack(pady=(12, 0))
wave = ttk.Scale(
    tk,
    from_=1,
    to=100,
    orient=HORIZONTAL,
)
wave.set(27)
wave.pack()

ttk.Label(tk, text="Murkiness").pack(pady=(12, 0))
murk = ttk.Scale(
    tk,
    from_=0,
    to=90,
    orient=HORIZONTAL,
)
murk.set(32)
murk.pack()


def reg():
    map.noise = map.PerlinNoise(octaves=octaves.get())
    regen()


but = ttk.Button(tk, text="Regenerate", command=reg, style="Accent.TButton")
but.pack(pady=30)

sv_ttk.set_theme("dark")


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

music = pygame.mixer.music.load("bg.mp3")
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
    m = generate(
        90, 90, ocean=ocean, travel=travel, scale=scale, octaves=octs, sand=sandv
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
            screen.blit(
                img,
                [
                    x * (16 * scale) - y * (16 * scale) + 485,
                    x * (8 * scale) + y * (8 * scale) - z * (16 * scale),
                ],
            )

        elif cell == 1:
            water.set_alpha(255 - ((d / (oceane.get() / 1000)) * (160 - murk.get())))
            rn = n
            z += (watern((
                    ((x*1/15) + rn),
                    (y*1/25)
                )) ** 2) * (wave.get()/ 5)
            
            screen.blit(
                water,
                [
                    x * (16 * scale) - y * (16 * scale) + 485,
                    x * (8 * scale) + y * (8 * scale) - (z) * (16 * scale),
                ],
            )

        elif cell == 2:
            screen.blit(
                sand,
                [
                    x * (16 * scale) - y * (16 * scale) + 485,
                    x * (8 * scale) + y * (8 * scale) - z * (16 * scale),
                ],
            )

    n += tide.get() / 1000
    pygame.display.flip()
    dt = clock.tick(60)  # Change this to FPS
    pygame.display.set_caption(f"Untitled Game | FPS: {round(clock.get_fps(), 2)}")
    tk.update()
    tk.update_idletasks()
pygame.quit()
