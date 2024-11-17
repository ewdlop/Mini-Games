import random
import pygame
import sys
import locale

# 设置区域设置
locale.setlocale(locale.LC_ALL, '')

# 初始化pygame
pygame.init()

# 定义颜色
白色 = (255, 255, 255)
黑色 = (0, 0, 0)
红色 = (213, 50, 80)
绿色 = (0, 255, 0)
蓝色 = (50, 153, 213)

# 定义常量
游戏标题 = '贪食蛇游戏'
游戏结束信息 = "游戏结束! 按C继续或按Q退出"
分数前缀 = "分数: "

# 设置游戏窗口
宽度 = 600
高度 = 400
游戏窗口 = pygame.display.set_mode((宽度, 高度))
pygame.display.set_caption(游戏标题)

时钟 = pygame.time.Clock()

# 蛇的初始设置
蛇块 = 10
蛇速度 = 15

# 字体设置
字体样式 = pygame.font.SysFont("Kai", 25)
分数字体 = pygame.font.SysFont("Kai", 35)

def 显示分数(score):
    分数显示 = 分数字体.render(f"{分数前缀}{locale.format_string('%d', score, grouping=True)}", True, 黑色)
    游戏窗口.blit(分数显示, [0, 0])

def 绘制蛇(蛇块参数, 蛇列表):
    """绘制蛇的每个部分"""
    for x in 蛇列表:
        pygame.draw.rect(游戏窗口, 绿色, [x[0], x[1], 蛇块参数, 蛇块参数])

def 游戏循环():
    游戏结束 = False
    游戏超时 = False

    x1 = 宽度 / 2
    y1 = 高度 / 2

    x1变化 = 0
    y1变化 = 0

    蛇列表 = []
    蛇长度 = 1

    食物x = round(random.randrange(0, 宽度 - 蛇块) / 10.0) * 10.0
    食物y = round(random.randrange(0, 高度 - 蛇块) / 10.0) * 10.0

    while not 游戏结束:

        while 游戏超时:
            游戏窗口.fill(白色)
            信息 = 字体样式.render(游戏结束信息, True, 红色)
            游戏窗口.blit(信息, [宽度 / 6, 高度 / 3])
            显示分数(蛇长度 - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        游戏结束 = True
                        游戏超时 = False
                    if event.key == pygame.K_c:
                        游戏循环()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                游戏结束 = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1变化 = -蛇块
                    y1变化 = 0
                elif event.key == pygame.K_RIGHT:
                    x1变化 = 蛇块
                    y1变化 = 0
                elif event.key == pygame.K_UP:
                    y1变化 = -蛇块
                    x1变化 = 0
                elif event.key == pygame.K_DOWN:
                    y1变化 = 蛇块
                    x1变化 = 0

        if x1 >= 宽度 or x1 < 0 or y1 >= 高度 or y1 < 0:
            游戏超时 = True

        x1 += x1变化
        y1 += y1变化
        游戏窗口.fill(白色)
        pygame.draw.rect(游戏窗口, 蓝色, [食物x, 食物y, 蛇块, 蛇块])
        蛇头 = []
        蛇头.append(x1)
        蛇头.append(y1)
        蛇列表.append(蛇头)
        if len(蛇列表) > 蛇长度:
            del 蛇列表[0]

        for x in 蛇列表[:-1]:
            if x == 蛇头:
                游戏超时 = True

        绘制蛇(蛇块, 蛇列表)
        显示分数(蛇长度 - 1)

        pygame.display.update()

        if x1 == 食物x and y1 == 食物y:
            食物x = round(random.randrange(0, 宽度 - 蛇块) / 10.0) * 10.0
            食物y = round(random.randrange(0, 高度 - 蛇块) / 10.0) * 10.0
            蛇长度 += 1

        时钟.tick(蛇速度)

    pygame.quit()
    sys.exit()

游戏循环()
