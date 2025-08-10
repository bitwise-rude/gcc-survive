import pygame
from characters import *
from menu import *
import sys

pygame.init()
pygame.display.init()
pygame.font.init()


font = pygame.font.SysFont('Times',20)
pygame.mixer.music.load("Assets\\bg.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

count = Sound('count.mp3')


class MainGame():
    def __init__(self):
        self.screen = pygame.display.set_mode((600,650))
        icon = pygame.image.load('Assets\\icon.png').convert()
        pygame.display.set_icon(icon)
        pygame.display.set_caption("GCC- Survive the balls")
        self.running = True
        self.clock = pygame.time.Clock()
        self.score = 0
        # menu
        menu = Menu()
        menu.mainloop()

        if not menu.toPlay:
            pygame.quit()
            sys.exit()        
        self.highScore = menu.highScore

        # container
        self.container = Container((25,50,550,500))

        # main character

        # first enemy
        self.player = Player()
        self.enemy = Monster(self.container.x+self.container.width//2-75,self.container.y+self.container.height//2-75,self.container,self.player)
        self.fillColor = (255,20,20,200)
        self.background = pygame.image.load('Assets\\back.png').convert()
        self.mainloop()


    def manageDeadScreen(self):
        run = True
        loose = pygame.font.SysFont("Times",35)
        toWrite = loose.render(f"You Are Dead. Score = {self.score}\n {"New High Score" if self.score>self.highScore else ""}",True,(0,0,0))
        if self.score > self.highScore:
                            writeHighScore(self.score)
        self.screen.blit(toWrite,(150,100))
        pygame.display.update()

        while run:
            for evs in pygame.event.get():
                if evs.type == pygame.QUIT:
                    run = False
                    sys.exit()
                
                if evs.type == pygame.KEYDOWN:
                     run = False
        

    

    def mainloop(self):
        playing = True
        while self.running:
            self.screen.fill(self.fillColor)
            for evs in pygame.event.get():
                if evs.type == pygame.QUIT:
                    self.running = False

                if evs.type == pygame.KEYDOWN:
                    if evs.key == pygame.K_SPACE:
                        self.player.activateShield()
                    
                    if evs.key == pygame.K_LSHIFT:
                        self.player.playerSpeed *=1.5
                
                if evs.type == pygame.KEYUP:
                    if evs.key == pygame.K_LSHIFT:
                        self.player.playerSpeed /= 1.5
            
            dt = self.clock.tick(60)/1000

            # checking for keypresses
            pressd_key = pygame.key.get_pressed()

            if (pressd_key[pygame.K_LEFT] or pressd_key [pygame.K_a]) and not self.container.collidedLeft(self.player):
                self.player.x -= self.player.playerSpeed * dt
            if (pressd_key[pygame.K_UP] or pressd_key [pygame.K_w])and not self.container.collidedTop(self.player):
                self.player.y -= self.player.playerSpeed * dt
            if (pressd_key[pygame.K_RIGHT] or pressd_key [pygame.K_d]) and not self.container.collidedRight(self.player):
                self.player.x += self.player.playerSpeed * dt
            if (pressd_key[pygame.K_DOWN] or pressd_key [pygame.K_s]) and not self.container.collidedBottom(self.player):
                self.player.y += self.player.playerSpeed * dt
            
            self.screen.blit(self.background,(0,0))

            self.container.update()
            self.player.update()
            if self.enemy.update():
                self.player.lives -=1
                if(self.player.lives <= 0):
                        self.running = False
                        self.manageDeadScreen()

            score = font.render(f"Score:{self.score}",True,(0,0,255))
            self.screen.blit(score,(250,550))

            lives = font.render(f"Lives:{self.player.lives}",True,(0,0,255))
            self.screen.blit(lives,(50,550))

            timeRemaining = int(abs((time.time()-self.enemy.previousGeneration) - self.enemy.timeAfterEachProjectile))
            if timeRemaining == 3 and not playing:
                count.play()
                playing = True
            else:
                playing = False

            timer = font.render(f'Next Wave in:{timeRemaining}',True,(0,0,255))
            self.screen.blit(timer,(400,550))

            for particles in self.enemy.projectiles:
                do = particles.update(dt,self.container,self.player)
                if do=='DONE':
                    self.enemy.projectiles.remove(particles)
                    self.score +=1
                elif do =='DEAD':
                    self.player.isOnCoolDown = False
                    self.player.sheidActivated = time.time()
                    self.player.activateShield()
                    self.enemy.projectiles.remove(particles)
                    self.player.lives -= 1

                    if(self.player.lives <= 0):
                        self.running = False
                        self.manageDeadScreen()

            pygame.display.update()
        
        

while True:
    MainGame()
sys.exit()