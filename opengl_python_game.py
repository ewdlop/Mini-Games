try:
    import pygame
except ImportError:
    print("Error: Unable to import 'pygame'. Please make sure it is installed.")

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    print("Error: Unable to import OpenGL modules. Please make sure PyOpenGL is installed.")

try:
    import numpy as np
except ImportError:
    print("Error: Unable to import 'numpy'. Please make sure it is installed.")

# 初始化 Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("OpenGL 3D Game")

# 设置视角
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# 定义立方体的顶点
vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

# 定义立方体的边
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_cube()
    
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
