import pygame
import pygame.gfxdraw
import math

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("3D Effect Game")

# 定义立方体的顶点
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# 定义立方体的边
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# 旋转角度
angle_x = 0
angle_y = 0
angle_z = 0

def rotate(vertices, angle_x, angle_y, angle_z):
    rotated_vertices = []
    for x, y, z in vertices:
        # 旋转 X 轴
        y, z = y * math.cos(angle_x) - z * math.sin(angle_x), y * math.sin(angle_x) + z * math.cos(angle_x)
        # 旋转 Y 轴
        x, z = x * math.cos(angle_y) + z * math.sin(angle_y), -x * math.sin(angle_y) + z * math.cos(angle_y)
        # 旋转 Z 轴
        x, y = x * math.cos(angle_z) - y * math.sin(angle_z), x * math.sin(angle_z) + y * math.cos(angle_z)
        rotated_vertices.append((x, y, z))
    return rotated_vertices

def project(vertices, width, height, fov, viewer_distance):
    projected_vertices = []
    for x, y, z in vertices:
        factor = fov / (viewer_distance + z)
        x = x * factor + width / 2
        y = -y * factor + height / 2
        projected_vertices.append((x, y))
    return projected_vertices

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # 旋转立方体
    rotated_vertices = rotate(vertices, angle_x, angle_y, angle_z)
    projected_vertices = project(rotated_vertices, 800, 600, 256, 4)

    # 绘制立方体的边
    for edge in edges:
        pygame.draw.line(screen, (255, 255, 255), projected_vertices[edge[0]], projected_vertices[edge[1]], 1)

    pygame.display.flip()

    # 更新旋转角度
    angle_x += 0.01
    angle_y += 0.01
    angle_z += 0.01

pygame.quit()