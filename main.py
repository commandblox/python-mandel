import sys
import threading

import numpy as np
import pygame

iters = int(input("iterations: "))
zoom_pos = [-0.5, 0]
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
    x, y = x / width * 2 - 1, y / height * 2 - 1


    x, y = x / zoom_amt, y / zoom_amt


    x, y = x + zoom_pos[0], y + zoom_pos[1]
    return x, y


def color(val):
    return [-val / 4 + 64, val, val]


def gen_mandel():
    global arr, img, xm, ym

    arr = np.full((width, height, 3), (0, 0, 0))
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            xp, yp = scale(x, y)
            arr[x, y] = color(calcMandel(xp, yp) / iters * 255)
            if stop: return



    img = arr_to_pg(arr)

    xm = 0
    ym = 0


def gen_mandel_thread():
    t = threading.Thread(target=gen_mandel, daemon=True)
    t.start()
    return t


if __name__ == '__main__':
    key = ""

    stop = False

    thread = gen_mandel_thread()
    thread.join()

    window = pygame.display.set_mode(size)

    xm = 0
    ym = 0

    pressed = False

    running = True
    while running:

        window.fill((0, 0, 0))
        window.blit(img, img.get_rect(center=(width/2+xm, height/2+ym)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEWHEEL:
                stop = True
                thread.join()
                stop = False

                if event.y > 0:
                    zoom_amt *= 2
                    thread = gen_mandel_thread()

                    img = pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2))
                elif event.y < 0:
                    zoom_amt /= 2
                    thread = gen_mandel_thread()

                    img = pygame.transform.scale(img, (img.get_width()/2, img.get_height()/2))

            elif event.type == pygame.KEYDOWN:
                key = event.key
            elif event.type == pygame.KEYUP:
                if key == event.key:
                    key = ""


        if key == pygame.K_LEFT:
            stop = True
            thread.join()
            stop = False

            xm += 1
            zoom_pos[0] -= 1/width*2/zoom_amt


            thread = gen_mandel_thread()

        if key == pygame.K_RIGHT:
            stop = True
            thread.join()
            stop = False


            xm -= 1
            zoom_pos[0] += 1/width*2/zoom_amt

            thread = gen_mandel_thread()

        if key == pygame.K_UP:
            stop = True
            thread.join()
            stop = False

            ym += 1
            zoom_pos[1] -= 1/height*2/zoom_amt

            thread = gen_mandel_thread()

        if key == pygame.K_DOWN:
            stop = True
            thread.join()
            stop = False

            ym -= 1
            zoom_pos[1] += 1/height*2/zoom_amt

            thread = gen_mandel_thread()





    pygame.quit()
    sys.exit()
