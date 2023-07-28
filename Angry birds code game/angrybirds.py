import pygame
import random

pygame.init()

# Inicializace fontu a velikosti textu
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Funkce pro kontrolu překrytí dvou obdélníků
def check_overlap(rect1, rect2):
    return rect1.colliderect(rect2)

# Parametry okna
HEIGHT = 720
WIDTH = 1280

# FPS
FPS = 60
FPS_CLOCK = pygame.time.Clock()

# Vytvoreni okna
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
#Jmeno okna
pygame.display.set_caption("Angry Birds")

#================================================================================================
# Načtení a přizpůsobení obrázku pozadí
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Zmenšení obrázku země na výšku 100 pixelů a přizpůsobení šířky okna
ground = pygame.image.load("Ground.png").convert()
ground = pygame.transform.scale(ground, (WIDTH, 100))

# # nacteni a umisteni hrace
bird = pygame.image.load("bird.png").convert_alpha()
bird = pygame.transform.scale(bird, (50, 50))
bird_rect = bird.get_rect()
bird_x = WIDTH // 10
bird_y = HEIGHT - ground.get_height() - 75
bird_speed = 10

# nacteni a umisteni tanku
tank = pygame.image.load("tank.png").convert_alpha()
tank = pygame.transform.scale(tank, (80, 80))
tank_rect = tank.get_rect()
tank_x = WIDTH // 10
tank_y = HEIGHT - ground.get_height() - 60
tank_speed = 10

# proměnné pro "shell.png"
shell_speed = 5
shell_fired = False
shell = pygame.image.load("shell.png").convert_alpha()
shell = pygame.transform.scale(shell, (30, 30))
shell_rect = shell.get_rect()
shell_x = tank_x + 100
shell_y = tank_y + 15
shells = []  # seznam pro uložení všech strel

# nacteni a umisteni nepritele
enemy = pygame.image.load("piggy.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (50, 50))
enemy_rect = enemy.get_rect()
# spawnování po pravé polovině okna hráče
enemy_x = random.randint(WIDTH // 2, WIDTH - enemy.get_width())
# umístění na zemi "Ground.png"
enemy_y = HEIGHT - ground.get_height() - enemy.get_height()



#================================================================================================

# Počet ostrovů, které chceme spawnovat
num_islands = 3
# Inicializace seznamu ostrovů
islands = []
# Spawnování ostrovů
for i in range(num_islands):
    island = pygame.image.load("Ground2.png").convert_alpha()
    island = pygame.transform.scale(island, (180, 100))

    # Náhodné určení pozice po pravé polovině okna hráče
    island_x = random.randint(WIDTH // random.randint(2, 3), WIDTH - island.get_width())
    island_y = HEIGHT // random.randint(2, 3)

    # Kontrola překrývání ostrovů
    island_rect = pygame.Rect(island_x, island_y, island.get_width(), island.get_height())
    overlap = True
    while overlap:
        overlap = False
        for other_island in islands:
            other_rect = pygame.Rect(other_island[1], other_island[2], other_island[0].get_width(), other_island[0].get_height())
            if check_overlap(island_rect, other_rect):
                overlap = True
                island_x = random.randint(WIDTH // random.randint(2, 3), WIDTH - island.get_width())
                island_y = HEIGHT // random.randint(2, 3)
                island_rect = pygame.Rect(island_x, island_y, island.get_width(), island.get_height())
                break

    islands.append((island, island_x, island_y))

# inicializujeme seznam nepřátel
enemies = []

# přidáme 3 nepřátel do seznamu???
for i in range(2):
    enemy = pygame.image.load("piggy.png").convert_alpha()
    enemy = pygame.transform.scale(enemy, (50, 50))
    enemy_rect = enemy.get_rect()
    enemy_x = random.randint(WIDTH // 2, WIDTH - enemy_rect.width)
    enemy_y = HEIGHT - ground.get_height() - enemy_rect.height
    enemies.append((enemy, enemy_x, enemy_y))

while any(abs(enemy_x - x) < enemy_rect.width for _, x, _ in enemies):
    enemy_x = random.randint(WIDTH // 2, WIDTH - enemy_rect.width)

enemies.append((enemy, enemy_x, enemy_y))

# Výpočet pozice, na které chcete umístit bird.png v rámci tank.png
bird_position = (tank_rect.width // 2 - bird_rect.width // 2, tank_rect.height // 2 - bird_rect.height // 2)

player_pos = [WIDTH // 2, HEIGHT - ground.get_height() - 50]

# Skóre hráče
score = 0
font = pygame.font.SysFont(None, 48)
score_text = font.render(f"Score: {score}", True, (255, 255, 255))
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

for island in islands:
    # Pokud jsme ještě nepřekročili limit nepřátel na ostrově, spawnujeme dalšího nepřítele
    if len([e for e in enemies if e[2] == island[2]]) < 2:
        enemy = pygame.image.load("piggy.png").convert_alpha()
        enemy = pygame.transform.scale(enemy, (50, 50))
        enemy_rect = enemy.get_rect()
        enemy_x = random.randint(island[1], island[1] + island[0].get_width() - enemy_rect.width)
        enemy_y = island[2] - 10
        enemies.append((enemy, enemy_x, enemy_y))




running = True

# game loop
while running:

    # for loop through the event queue
    for event in pygame.event.get():

        # Kdyz zmacknu ESCAPE nebo zmacknu krizek vypne se 'hra'
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # přidání nové šipky na pozici tanku
            shells.append(pygame.Rect(tank_x + 100, tank_y + 15, shell.get_width(), shell.get_height()))

            if event.key == pygame.K_ESCAPE:
                running = False
            # Zvyšování skóre, když hráč zmáčkne mezerník
            if event.key == pygame.K_p:
                score += 10
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))


            # Zvyšování skóre, když hráč zmáčkne mezerník
            if event.key == pygame.K_SPACE:
                score += 10
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                shell_x = tank_x


    #===============================================================================================================
    # Nakreslení pozadí a zeme
    displaysurface.blit(background, (0, 0))

    # Získání seznamu stisknutých kláves
    keys = pygame.key.get_pressed()

    # Pohyb hráče
    if keys[pygame.K_LEFT] and bird_x > 0:
        bird_x -= bird_speed
    if keys[pygame.K_RIGHT] and bird_x < WIDTH - bird.get_width() - 30:
        bird_x += bird_speed

        # Pohyb tanku
    if keys[pygame.K_LEFT] and tank_x > 0:
        # vymažeme starou pozici tanku
        displaysurface.blit(background, (tank_x, tank_y), (tank_x, tank_y, tank.get_width(), tank.get_height()))
        tank_x -= tank_speed
    if keys[pygame.K_RIGHT] and tank_x < WIDTH - tank.get_width():
        # vymažeme starou pozici tanku
        displaysurface.blit(background, (tank_x, tank_y), (tank_x, tank_y, tank.get_width(), tank.get_height()))
        tank_x += tank_speed
        # Stisknutím mezerníku vytvoří novou šipku
    if keys[pygame.K_SPACE] and not shell_rect:
            shell_x = tank_x + 50
            shell_y = tank_y + 15
            shell_rect = shell.get_rect()

    # smyčka pro každou šipku v seznamu
    for shell_rect in shells:
            displaysurface.blit(background, shell_rect, shell_rect)
            shell_rect.move_ip(shell_speed, 0)  # posun šipky dopředu
            displaysurface.blit(shell, shell_rect)

            # detekce kolize mezi šipkou a nepřítelem
            if shell_rect.colliderect(enemy_rect):
                score += 50
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                enemy_x = random.randint(WIDTH // 2, WIDTH - enemy.get_width())
                enemy_y = HEIGHT - ground.get_height() - enemy.get_height()
                shells.remove(shell_rect)  # odebrání šipky ze seznamu

            # detekce, zda se šipka dostala až na konec okna
            if shell_rect.right > WIDTH:
                shells.remove(shell_rect)  # odebrání šipky ze seznamu



    displaysurface.blit(score_text, score_rect)


    displaysurface.blit(ground, (0, HEIGHT - ground.get_height()))

    displaysurface.blit(bird, (bird_x, bird_y))

    displaysurface.blit(tank, (tank_x, tank_y))



# ===============================================================================================================
    for island, island_x, island_y in islands:
        displaysurface.blit(island, (island_x, island_y))

    for enemy, enemy_x, enemy_y in enemies:
        displaysurface.blit(enemy,(enemy_x,enemy_y))

    for enemy in enemies:
        displaysurface.blit(enemy[0], (enemy[1], enemy[2]))



    # Update okna
    pygame.display.update()

    # Omezení FPS na hodnotu FPS
    FPS_CLOCK.tick(FPS)