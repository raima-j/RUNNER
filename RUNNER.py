import pygame
from sys import exit #to directly manipulate the runtime and exit the code
from random import randint,choice
import random 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player=pygame.image.load('For Game/Graphics/Player/Standing.png').convert_alpha() #player stand
        player_walk=pygame.image.load('For Game/Graphics/Player/Walking.png').convert_alpha() #player walk
        self.player_index=0 #to change the motion of the player
        self.player_jump=pygame.image.load('For Game/Graphics/Player/Jumping.png').convert_alpha()
        self.player_motion=[player,player_walk]

        self.image=self.player_motion[self.player_index]
        self.rect=self.image.get_rect(midtop=(45,315))
        self.gravity=0

        self.jump_sound=pygame.mixer.Sound('For Game/Music/Jumping.wav')
        self.jump_sound.set_volume(0.85)



    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom>=360: 
            self.gravity=-20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom>=360:
            self.rect.bottom=360

    def animation_state(self):
        if self.rect.bottom<=350:
            self.image=self.player_jump
        else:
            self.player_index+=0.12
            if self.player_index>=len(self.player_motion): self.player_index=0
            self.image=self.player_motion[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type=='boulder':
            boulder=pygame.image.load('For Game/Graphics/Boulder/Boulder.png').convert_alpha() #this'll be the enemy on ground
            self.frames=[boulder]
            y_pos=340
        else:
            meteor=pygame.image.load('For Game/Graphics/Meteor/Meteor1.png').convert_alpha()
            self.frames=[meteor]
            y_pos=180 

        self.animation_index=0
        self.image=self.frames[self.animation_index]
        self.rect=self.image.get_rect(midleft=(random.randint(450,500),y_pos))

    def animation_state(self):
        self.animation_index+=0.12
        if self.animation_index>=len(self.frames):self.animation_index=0
        self.image=self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x-= 6
        self.destroy()  #destroys the obsatcle itself if it goes out of the screen

    def destroy(self):
        if self.rect.x<=-150:
            self.kill() #destroys obstacle sprite

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x-=5   #so all obstacles will move backwards with a speed of 5

            if obstacle_rect.bottom>=300: screen.blit(boulder,obstacle_rect) #we're drawing the boulder surface on the rect
            else:
                screen.blit(meteor,obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -150]

        return obstacle_list
    else:
        return [] 

def collisions(player,obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if player.colliderect(obstacle_rect): return False  #this is in the local scope rn
	return True

def collision_sprite(): 
    if pygame.sprite.spritecollide(player1.sprite,obstacle_group,False):  #bool, if the sprite collides with the group, we check if its destroyed
        obstacle_group.empty()
        return False
    else: return True

#def player_animation():
#    #play walking/standing on floor, jump when not on the floor
#    global player_surf, player_index
#
#    if player_rect.bottom<=350: 
#        player_surf=player_jump
#    else:
#        player_index+=0.12 #slowly increase the number so that the frames will take time to adjust
#        if player_index>= len(player_motion):player_index=0
#        player_surf=player_motion[int(player_index)]

def display_score():
    current_time=int(pygame.time.get_ticks()/1000) - start_time 
    score_surface=test_font.render(f'Score: {current_time}',False,(100,45,255))
    score_rect=score_surface.get_rect(midtop=(200,75))
    screen.blit(score_surface,score_rect)
    return current_time

pygame.init() #initialising pygame and all its sub-programs
screen=pygame.display.set_mode((400,400)) #this creates the display surface FOR ONE FRAME
pygame.display.set_caption('RUNNER')
clock= pygame.time.Clock() #to set the max frame rate, C is caps
test_font=pygame.font.Font('For Game/Text/Pixeltype.ttf',30) #font type, font size
game_active=False
start_time=0
score=0

bgm=pygame.mixer.Sound('For Game/Music/BGM.wav')
bgm.play(loops=-1) #-1 indicates forever
bgm.set_volume(0.5)

player1=pygame.sprite.GroupSingle()  #group that contains a sprite class
player1.add(Player()) #accesses the sprite class

#groups
obstacle_group=pygame.sprite.Group()

#the sky
sky=pygame.image.load('For Game/Graphics/Sky.png').convert_alpha() #created a regular surface

#the ground
ground=pygame.image.load('For Game/Graphics/Ground.png').convert_alpha()

#obstacles
boulder=pygame.image.load('For Game/Graphics/Boulder/Boulder.png').convert_alpha() #this'll be the enemy on ground
#boulder_rect=boulder.get_rect(midleft=(400,340))
meteor=pygame.image.load('For Game/Graphics/Meteor/Meteor1.png').convert_alpha()
#meteor_rect=meteor.get_rect(midleft=(410,210))
obstacle_rect_list=[]

#the player
player=pygame.image.load('For Game/Graphics/Player/Standing.png').convert_alpha() #player stand
player_walk=pygame.image.load('For Game/Graphics/Player/Walking.png').convert_alpha() #player walk
player_index=0 #to change the motion of the player
player_jump=pygame.image.load('For Game/Graphics/Player/Jumping.png').convert_alpha()
player_motion=[player,player_walk]
player_surf = player_motion[player_index] #rn cuz its 0, it'll take the first player walk
player_rect=player.get_rect(midtop=(45,308)) #created a rectangle for the surface of the player
player_gravity=0

#the intro
player_intro=pygame.image.load('For Game/Graphics/Player/Sit.png').convert_alpha()
player_intro_rect=player_intro.get_rect(center=(200,200))
game_name=test_font.render('Purple Runner',True,(145, 95, 109))
game_name_rect=game_name.get_rect(center=(200,60))

game_message=test_font.render('Press space to run.',True,(145, 95, 109))
game_message_rect=game_message.get_rect(center=(200,320))

#timer
obstacle_timer=pygame.USEREVENT+1 #custom user event
pygame.time.set_timer(obstacle_timer,800)

#test_surface.fill('Blue') #this is black by default

while True:  
    #updates everything and draws elements

    for event in pygame.event.get():
        if event.type==pygame.QUIT:   #this checks for the event of quitting the pygame screen
            pygame.quit()     #allows us to close the display screen
            exit()
        
        if game_active:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and player_rect.bottom>=360 : #this makes sure the player jumps only when its on the ground
                    player_gravity=-20
                #else:  
                    #player_gravity=player_gravity
        else: 
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True
                #boulder_rect.left=350
                start_time=int(pygame.time.get_ticks()/1000)

        if event.type==obstacle_timer and game_active:
            obstacle_group.add(Obstacle(choice(['meteor','boulder','boulder','boulder'])))#75% chance of a boulder, 25% of a meteor
            #if randint(0,2):
            #    obstacle_rect_list.append(boulder.get_rect(midleft=(randint(450,500),340)))
            #else:
            #    obstacle_rect_list.append(meteor.get_rect(midleft=(randint(450,500),180)))

    if game_active:    
        #the sky
        screen.blit(sky,(0,-60)) #puts the reg surface on the display surface (screen)
        #block image transfer

        #the ground
        screen.blit(ground,(0,325)) #each new graphic is a new surface

        #the player
        #player_gravity+=1
        #player_rect.y+=player_gravity  #increases the gravity exponentially rather than systematically
        #if player_rect.bottom>=360:
        #    player_rect.bottom=360 

        #player_animation()
        #screen.blit(player_surf,player_rect) #used the player rectangle to define the area 
        player1.draw(screen)  #the surface to draw on
        player1.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        #obstacle movements
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        score= display_score()

        #the enemy
#        screen.blit(boulder,boulder_rect)
#       boulder_rect.x -= 3
#        if boulder_rect.right<=0: boulder_rect.left=400
#        if meteor_rect.right<=0: meteor_rect.left=405
#
        #the collision
#        if boulder_rect.colliderect(player_rect):
#           game_active=False
        game_active = collision_sprite()
    
    else: #shows the intro screen
        #score=display_score()
        screen.fill((170, 152, 169))
        screen.blit(player_intro,player_intro_rect)
        player_rect.midbottom = (80,360)
        player_gravity=0
        score_message=test_font.render(f'Your Score : {score}',True,(145, 95, 109))
        score_message_rect=score_message.get_rect(center=(200,320))

        obstacle_rect_list.clear() 

        screen.blit(game_name,game_name_rect)

        if score<=2:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

        #if score == 0: screen.blit(game_message,game_message_rect)
        #else: screen.blit(score_message,score_message_rect)


    pygame.display.update()
    clock.tick(60) #60fps, ie 60 iterations of the while loop per second
