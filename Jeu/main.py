import pygame
import random
from pygame.locals import *
from Class_folder import enemy, projectile, rect_color

# Position initiale du joueur
player_position_x = 10
player_position_y = 10
# Taille de la fenêtre en pixel
window_width = 700
window_height = 700
# Listes de projectiles
bullets_right = []
bullets_left = []
bullets_up = []
bullets_down = []
# Liste d'ennemies
enemies = []
# Vitesse du joueur
player_speed = 2 
# Vitesse du projetile
bullet_speed = 10
# Valeurs aléatoires x et y du point d'apparition de l'ennemi
random_x = 0
random_y = 0
# Liste d'ennemies
enemy_list = []
# Variable qui check si l'ennemi est dans un mur avant de le faire apparaître
enemy_is_valide = False
# Index qui indique la direction dans lequel le projectile doit aller
direction_index = 1

clock = pygame.time.Clock() # Permet de limiter les FPS, équivalent au time.deltaTime en C#

# Dessine des rectangles marrons représentant les murs 
def displayWalls():
    
    global walls
    global wall0
    global wall1
    global wall2
    global wall3
    global wall4
    global wall5
    global wall6
    global wall7
    global wall8
   
    wall0 = pygame.draw.rect(surface, rect_color.BROWN, (250, 75, 200, 100)) 
    wall1 = pygame.draw.rect(surface, rect_color.BROWN, (75, 75, 100, 100))
    wall2 = pygame.draw.rect(surface, rect_color.BROWN, (525, 75, 100, 100))
    wall3 = pygame.draw.rect(surface, rect_color.BROWN, (75, 525, 100, 100))
    wall4 = pygame.draw.rect(surface, rect_color.BROWN, (525, 525, 100, 100))
    wall5 = pygame.draw.rect(surface, rect_color.BROWN, (75, 250, 100, 200))
    wall6 = pygame.draw.rect(surface, rect_color.BROWN, (525, 250, 100, 200))
    wall7 = pygame.draw.rect(surface, rect_color.BROWN, (250, 525, 200, 100))
    wall8 = pygame.draw.rect(surface, rect_color.BROWN, (250, 250, 200, 200))

    walls = [wall0, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8]

# Affiche les ennemies à l'écran
def displayEnemies():
    if len(bullets_right) == 0:
        for every_single_enemy in enemies: 
            enemy_instance = every_single_enemy.draw(surface)

# Affiche le joueur à l'écran
def displayPlayer():
    pygame.draw.rect(surface, rect_color.BLUE, (player_position_x, player_position_y, 50, 50))

# Check les entrées clavier
def checkKeyboardInput():

    global player_position_x
    global player_position_y
    global player_speed
    global bullet_speed
    global direction_index

    if pygame.key.get_pressed()[K_LEFT]:
        player_position_x -= player_speed                     
    elif pygame.key.get_pressed()[K_RIGHT]:
        player_position_x += player_speed 
    elif pygame.key.get_pressed()[K_UP]:
        player_position_y -= player_speed 
    elif pygame.key.get_pressed()[K_DOWN]:
        player_position_y += player_speed 

    # Position du canon
    if pygame.key.get_pressed()[K_z]:
        direction_index = 0
        pygame.draw.rect(surface, rect_color.BLACK, (player_position_x+20, player_position_y-15, 10, 25))
    elif pygame.key.get_pressed()[K_d]:
        direction_index = 1
        pygame.draw.rect(surface, rect_color.BLACK, (player_position_x + 40, player_position_y + 20, 25, 10))
    elif pygame.key.get_pressed()[K_s]:
        direction_index = 2
        pygame.draw.rect(surface, rect_color.BLACK, (player_position_x + 20, player_position_y + 40, 10, 25))
    elif pygame.key.get_pressed()[K_q]:
        direction_index = 3
        pygame.draw.rect(surface, rect_color.BLACK, (player_position_x-15, player_position_y+20, 25, 10))
    else:
        direction_index = 1
        pygame.draw.rect(surface, rect_color.BLACK, (player_position_x + 40, player_position_y + 20, 25, 10))

# Gère le déplacement des projectiles et check les collisions de ces derniers    
def bulletsCollisions(bullet_direction, bullet_x, bullet_y):

    for bullet in bullet_direction:         
        bullet.x += bullet_x
        bullet.y += bullet_y
        bullet_instance = bullet.draw(surface)
        if bullet_instance.collidelist(walls) != -1:# Si le projectile touche un mur, il est supprimé
            bullet_direction.pop(bullet_direction.index(bullet)) 
        for every_single_enemy in enemies:
            enemy_instance = every_single_enemy.draw(surface)
            if bullet_instance.colliderect(enemy_instance): # Si le projectile touche un ennemi, il est supprimé et l'ennemi également
                bullet_direction.pop(bullet_direction.index(bullet))
                enemies.pop(enemies.index(every_single_enemy)) 
                
# Vérifie les collisions
def checkCollisions():  
     
    global player_position_x
    global player_position_y

    check_collision_rect = pygame.Rect(player_position_x-1, player_position_y-1, 52, 52) # On crée un rectangle fictif légèrement plus grand que le joueur
    
    if check_collision_rect.collidelist(walls) != -1 or (player_position_x < 0) or (player_position_x > 650) or (player_position_y < 0) or (player_position_y > 650):
       # Si le rectangle fictif touche un mur ou un des bords de l'écran, le joueur revient à sa position précédente
        player_position_x = last_position_x
        player_position_y = last_position_y     

    bulletsCollisions(bullets_left, -bullet_speed, 0)
    bulletsCollisions(bullets_right, bullet_speed, 0)
    bulletsCollisions(bullets_up, 0, -bullet_speed)
    bulletsCollisions(bullets_down, 0, bullet_speed)

# Sauvegarde la dernière position du joueur
def saveLastPosition():

    global last_position_x
    global last_position_y

    last_position_x = player_position_x
    last_position_y = player_position_y


surface = pygame.display.set_mode((window_width, window_height)) # Affiche la fenêtre
pygame.display.set_caption("Tanks War") # Affiche le nom du jeu dans la barre de la fenêtre 
background_image = "background.jpg" # On stocke l'image d'arrière plan dans la variable background_image
background = pygame.image.load(background_image).convert() # Télécharge l'image depuis le disque dur et la convertit au même format que l'affichage

while True:

    clock.tick(60)
    surface.fill((0, 0, 0)) # Permet d'effacer le carré précédent représentant le joueur  à chaque frame pour éviter de dessiner une ligne continue      
    surface.blit(background, (0,0)) # Affiche le background avec ses coordonnées initales   
     
    displayWalls() 
    displayPlayer()
    displayEnemies()
    checkCollisions()   
    saveLastPosition()
    checkKeyboardInput()
    pygame.display.update() 
       
    for event in pygame.event.get():
            
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            if direction_index == 0:
                bullets_up.append(projectile.Projectile(player_position_x + 20, player_position_y + 20))
            elif direction_index == 1:
                bullets_right.append(projectile.Projectile(player_position_x + 20, player_position_y + 20))
            elif direction_index == 2:
                bullets_down.append(projectile.Projectile(player_position_x + 20, player_position_y + 20))
            elif direction_index == 3:
                bullets_left.append(projectile.Projectile(player_position_x + 20, player_position_y + 20))
        elif event.type == KEYDOWN and event.key == K_a:
            while enemy_is_valide == False:
                random_x =  random.randint(10,640)
                random_y = random.randint(10,640)         
                enemy_list = pygame.draw.rect(surface, rect_color.RED,(random_x, random_y, 50, 50))
                if enemy_list.collidelist(walls) == -1: # Si l'ennemi n'est pas en collision avec un mur
                    enemy_list = enemies.append(enemy.Enemy(random_x, random_y)) # On l'ajoute à la liste d'ennemies
                    enemy_is_valide = True
        enemy_is_valide = False


        
               
          
           


            
        

    

    


    
    
    
    
