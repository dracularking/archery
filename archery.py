import pygame
import sys
import random

# 初始化Pygame
pygame.init()

# 设置窗口大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("射箭游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 设置靶子的参数
target_width = 50
target_height = 100
target_x = SCREEN_WIDTH - target_width - 20
target_y = SCREEN_HEIGHT // 2 - target_height // 2
target_speed = 0.1
target_hit = False
hit_count = 0
arrow_count = 0

# 设置箭的参数
arrow_width = 20
arrow_height = 10
arrow_x = 50
arrow_y = SCREEN_HEIGHT // 2 - arrow_height // 2
arrow_speed = 0.5
arrow_direction = "right"
arrow_fired = False

# 设置计时器
clock = pygame.time.Clock()
FPS = 60

# 初始化内置声音
hit_sound = pygame.mixer.Sound("sound/beep.mp3")
shoot_sound = pygame.mixer.Sound("sound/shoot.mp3")


# 绘制靶子
def draw_target():
    pygame.draw.rect(screen, RED, (target_x, target_y, target_width, target_height))


# 绘制箭
def draw_arrow():
    pygame.draw.rect(screen, BLUE, (arrow_x, arrow_y, arrow_width, arrow_height))


# 检查箭是否击中靶子
def check_hit():
    global target_hit, hit_count, arrow_count
    if not target_hit and arrow_x + arrow_width >= target_x and arrow_y + arrow_height >= target_y and arrow_y <= target_y + target_height:
        target_hit = True
        hit_count += 1
        # 播放音效
        hit_sound.play()


# 显示箭支数和成功率
def show_hit_info():
    global arrow_count, hit_count
    font = pygame.font.SysFont(None, 25)
    text = font.render("Hits: " + str(hit_count), True, BLACK)
    screen.blit(text, (10, 50))
    if arrow_count > 0:
        hit_rate = hit_count / arrow_count * 100
    else:
        hit_rate = 0
    text = font.render("Hit Rate: {:.2f}%".format(hit_rate), True, BLACK)
    screen.blit(text, (10, 90))


# 显示击中次数
def show_arrow_count():
    font = pygame.font.SysFont(None, 25)
    text = font.render("Arrows: " + str(arrow_count), True, BLACK)
    screen.blit(text, (10, 10))


# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not arrow_fired:
                arrow_fired = True
                arrow_count += 1
                shoot_sound.play()

    # 清屏
    screen.fill(WHITE)

    # 绘制靶子
    draw_target()

    # 绘制箭
    draw_arrow()

    # 移动靶子
    target_y += target_speed * clock.get_time()
    if target_y <= 0:
        target_speed = abs(target_speed)
    elif target_y >= SCREEN_HEIGHT - target_height:
        target_speed = -abs(target_speed)

    # 移动箭
    if arrow_fired:
        if arrow_direction == "right":
            arrow_x += arrow_speed * clock.get_time()
            if arrow_x >= SCREEN_WIDTH:
                arrow_fired = False
                target_hit = False
                arrow_x = 50
        elif arrow_direction == "left":
            arrow_x -= arrow_speed * clock.get_time()
            if arrow_x <= 0:
                arrow_fired = False
                target_hit = False
                arrow_x = 50

    # 检查箭是否击中靶子
    check_hit()

    # 如果箭击中靶子，显示成功，并计数
    if target_hit:
        font = pygame.font.SysFont(None, 36)
        text = font.render("Hit!", True, GREEN)
        screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
        target_y = 0
        target_speed = random.uniform(0.1, 0.9)

    # 显示击中次数
    show_hit_info()

    # 显示箭支数和成功率
    show_arrow_count()

    # 更新画面
    pygame.display.flip()

    # 控制帧率
    clock.tick(FPS)
