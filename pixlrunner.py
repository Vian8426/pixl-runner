import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('asset/graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('asset/graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2 ]
        self.player_index = 0
        self.player_jump = pygame.image.load('asset/graphics/Player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300,))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('asset/audio/jump.mp3')
        self.jump_sound.set_volume(0.4)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20 
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y  += self.gravity
        if self.rect.bottom >=300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300 :
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacal (pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('asset/graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('asset/graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 250
        else:
            snail_1 = pygame.image.load('asset/graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('asset/graphics/snail/snail2.png').convert_alpha()
            self.frames= [snail_1,snail_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()    
    
    def update (self,x):
        self.animation_state()
        self.rect.x -= 8 + speed_increase
        self.destroy()

def display_score():
    s_time = int( pygame.time.get_ticks() /1000)  - n_time
    scr = tfont.render(f'Score:{s_time}' , False, (64,64,64))
    scr_hitbox = scr.get_rect(center = (400,50) )
    screen.blit(scr,scr_hitbox)
    return s_time

def high_score(n1,highscr):
    if n1 >= highscr:
        highscr = n1
    return highscr


def collision_sprite():
     if pygame.sprite.spritecollide(player.sprite,obstacal_group,False):
        bg_music.stop()
        game_over.play()
        
        obstacal_group.empty()
        return False
     return True
     

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Pixl runner")
clock = pygame.time.Clock()
game_active = False
n_time = 0
no_of_games = 0
score = 0
highscr = 0
speed_increase= 0
last_speed_increase = 0
difficulty_increase = 0
obstcal_timer_interval = 1500
fly_spawn = False
bg_change = 1

# Load sounds
bg_music = pygame.mixer.Sound('asset/audio/music.wav')
bg_music.set_volume(0.2)
menu_music = pygame.mixer.Sound('asset/audio/menu music.wav')
menu_music.set_volume(0.2)
game_over = pygame.mixer.Sound('asset/audio/game_over.wav')
game_over.set_volume(0.3)

#Sprite groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacal_group = pygame.sprite.Group()



#Background
jungle= pygame.image.load('asset/graphics/Sky.png').convert_alpha()
cave = pygame.image.load('asset/graphics/Cave.png').convert_alpha()
ground = pygame.image.load('asset/graphics/ground.png').convert_alpha()
stone = pygame.image.load('asset/graphics/stone.png').convert_alpha()


#Text dislpay
tfont = pygame.font.Font('asset/font/Pixeltype.ttf',100)
tfont_small = pygame.font.Font('asset/font/Pixeltype.ttf',50)
End_message = tfont.render("GAME OVER",False, "RED")
End_messagehit = End_message.get_rect(center = (400,60))
intro = tfont.render("Pixl Runner", True, (111,196,169))
intro_hit = intro.get_rect(center = (400,60)) 
start = tfont_small.render("Press SPACE to Start", True, (111,196,169))
start_hit = start.get_rect(center = (400,290)) 


#Introscreen 
player_stand = pygame.image.load('asset/graphics/Player/player_stand.png').convert_alpha()
player_stand_scaled = pygame.transform.scale2x(player_stand)
player_stand_hit = player_stand_scaled.get_rect(center = (400,170))

#timers
obstcal_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstcal_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2 
pygame.time.set_timer(snail_animation_timer,300)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,100)

if no_of_games == 0 and game_active == False:
    menu_music.play(1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstcal_timer and fly_spawn:
                obstacal_group.add(Obstacal(choice(['fly','snail','snail','snail'])))
            elif event.type == obstcal_timer :
                obstacal_group.add(Obstacal('snail'))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active =True
                no_of_games += 1
                menu_music.stop()
                bg_music.play(-1)


    
    if game_active:  
        #bckground  
        if bg_change % 2 == 0:
            screen.blit(cave,(0,000))
            screen.blit(stone,(0,300))

        else:
            screen.blit(jungle,(0,000))
            screen.blit(ground,(0,300))
        
        #score system
        score = display_score()
        highscr = high_score(score,highscr)
        
        #enemy speed and difficulty increase
        if score > 0 and score % 10 == 0 and score != last_speed_increase :
            speed_increase += 2
            fly_spawn = True     
            last_speed_increase = score
            bg_change += 1
             
        if score > 0 and score % 10 == 0 and score != difficulty_increase:
            if obstcal_timer_interval > 300: 
                obstcal_timer_interval -= 100
                pygame.time.set_timer(obstcal_timer, obstcal_timer_interval)
                difficulty_increase = score
       
        #class instances
        player.draw(screen)
        player.update()
        obstacal_group.draw(screen)
        obstacal_group.update(speed_increase)
        game_active = collision_sprite()
        
    #game over screen and menu
    else :
        screen.fill((94,129,162))  
        n_time = int(pygame.time.get_ticks() / 1000 )

        #menu screen
        if no_of_games == 0:
            screen.blit(intro,intro_hit)
            screen.blit(start,start_hit)
            screen.blit(player_stand_scaled,player_stand_hit)
            menu_music.play(1)

        #game over screen
        else:
            screen.blit(start,start_hit)
            screen.blit(End_message,End_messagehit)
            screen.blit(player_stand_scaled,player_stand_hit)
            
            score_txt = tfont_small.render(f'Current Score: {score}', False, (111,196,169))
            score_txt_hit = score_txt.get_rect(center = (400,330))
            screen.blit (score_txt,score_txt_hit)

            highscore_txt = tfont_small.render(f'High Score: {highscr}', False, (111,196,180))
            highscore_txt_hit = highscore_txt.get_rect(center = (400,370))
            screen.blit (highscore_txt,highscore_txt_hit)
            speed_increase = 0
            last_speed_increase = 0
            bg_change = 1
            fly_spawn = False
            obstcal_timer_interval = 1500
            pygame.time.set_timer(obstcal_timer,obstcal_timer_interval)

    pygame.display.update()
    clock.tick(60)
