import sys

import numpy as np
import pygame

iters = int(input("iterations: "))
zoom_pos = -0.5, 0
zoom_amt = 0.5

size = width, height = 500, 500


def arr_to_pg(arr):
    return pygame.pixelcopy.make_surface(arr)


def calcMandel(x, y):
    c = complex(x, y)
    z = 0
    for i in range(iters):
        z = z ** 2 + c
        if abs(z) > 10:
            break

    return i


def scale(x, y):
    x, y = x / width * 2 - 1, y / width * 2 - 1


    x, y = x / zoom_amt, y / zoom_amt


    x, y = x + zoom_pos[0], y + zoom_pos[1]
    return x, y


def color(val):
    return [-val / 4 + 64, val, val]


def gen_mandel():
    global arr, img

    arr = np.full((width, height, 3), (0, 0, 0))
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            xp, yp = scale(x, y)
            arr[x, y] = color(calcMandel(xp, yp) / iters * 255)

    img = arr_to_pg(arr)


if __name__ == '__main__':
    gen_mandel()

    window = pygame.display.set_mode(size)

    pressed = False

    running = True
    while running:

        window.fill((0, 0, 0))
        window.blit(img, img.get_rect())
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        oldpressed = pressed
        if pygame.mouse.get_pressed()[0]:
            pressed = True
        else:
            pressed = False

        if oldpressed != pressed and pressed is True:
            mx, my = pygame.mouse.get_pos()
            zoom_pos = scale(mx, my)
            zoom_amt *= 2
            print(zoom_amt, zoom_pos)
            gen_mandel()

    pygame.quit()
    sys.exit()
