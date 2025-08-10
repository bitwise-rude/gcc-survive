import pygame,random,time


class Sound:
    def __init__(self,path):
        self.sound = pygame.mixer.Sound("Assets\\"+path)
        self.playing = False
    
    def play(self):
        self.sound.play()
    
    def stop(self):
        self.sound.stop()

class Container:
    def collidedLeft(self,other):
        return other.x <= self.colliderRect[0]

    def collidedRight(self,other):
        return other.x >= (self.colliderRect[0] + self.colliderRect[2]-other.widht)

    def collidedTop(self,other):
        return other.y <= self.colliderRect[1]
    
    def collidedBottom(self,other):
        return other.y >= (self.colliderRect[1] + self.colliderRect[3]-other.height)
 
    def __init__(self,rect,colliderRect=None) -> None:
        self.x = rect[0]
        self.y = rect[1]
        self.image = pygame.image.load("Assets\\board.png").convert()
        self.image.set_colorkey((255,255,255))

        self.width = rect[2]
        self.height = rect[3]
        self.screen = pygame.display.get_surface()

        colliderRect= (self.x+24,self.y+23,496,455)
        if not colliderRect:
            self.colliderRect = rect
        else:
            self.colliderRect = colliderRect

        # manage actual game sprite here  and their size handeling
        ##
    
    def update(self):

        # manage acutal game printing here
        # pygame.draw.rect(self.screen,(255,2,2),(self.x,self.y,self.width,self.height),1,10)
        self.screen.blit(self.image,(self.x,self.y))
    


class Player:
    def __init__(self,x=100,y=100,conatiner= None):
        self.x =x
        self.playerSpeed = 200
        self.y = y
        self.screen = pygame.display.get_surface()
        self.widht = 20
        self.height = 35
        self.lives = 3
        self.container = conatiner
        
        self.sheidActivated = False
        self.shieldTimer = 8

        self.shieldCooldown = 5
        self.lastActivated = 0
        self.isOnCoolDown = False

     


        self.power = Sound('power.mp3')
        self.wrong = Sound('wrong.mp3')
        self.off  = Sound('off.mp3')
        self.on = Sound('on.mp3')



    
    def activateShield(self):
        if not self.sheidActivated and not self.isOnCoolDown:
            self.sheidActivated = time.time()
            self.power.play()
        else:
            self.wrong.play()
            
    
    def update(self):
        if self.sheidActivated:
            pygame.draw.circle(self.screen,(255,255,0),(self.x+self.widht/2,self.y+self.height/2),20,0)
            if time.time() - self.sheidActivated > self.shieldTimer:
                self.off.play()
                self.sheidActivated = False
                self.lastActivated = time.time()
                self.isOnCoolDown = True

        if self.isOnCoolDown and  (time.time()-self.lastActivated) >self.shieldCooldown:
            self.isOnCoolDown = False
            self.on.play()
      
        if self.sheidActivated:
            pygame.draw.line(self.screen,(0,255,0),(self.x,self.y-10),(self.x + (self.widht-(self.widht * ((time.time()-self.sheidActivated)/self.shieldTimer))),self.y-10),10)   

        if self.isOnCoolDown:
            pygame.draw.line(self.screen,(255,0,0),(self.x,self.y-10),(self.x + (self.widht-(self.widht * ((time.time()-self.lastActivated)/self.shieldCooldown))),self.y-10),10)   
        
        pygame.draw.rect(self.screen,(255,0,255),(self.x,self.y,self.widht,self.height),0,10)
        pygame.draw.circle(self.screen,(255,255,255),(self.x+10,self.y+10),2,0)
        pygame.draw.circle(self.screen,(255,255,255),(self.x+self.widht-10,self.height+self.y-10),2,0)

    def collided(self,other):
        x_overlap = (other.x > self.x and (other.x )< (self.x+self.widht))
        y_overlap = (other.y > self.y and (other.y )< (self.y+self.height))

        return x_overlap and y_overlap


class Monster:
    def collided(self,other):
        x_overlap = (other.x+other.widht > self.x and (other.x )< (self.x+self.widht))
        y_overlap = (other.y+other.height > self.y and (other.y )< (self.y+self.height+20))

        return x_overlap and y_overlap
    def __init__(self,x=50,y=50,container=None,player=None):
        self.x=x
        self.y = y 
        self.height = 75
        self.widht = 75
        self.screen = pygame.display.get_surface()
        self.projectiles = []
        self.container = container
        self.player = player

        self.images = []
        # loading all animation images
        for i in range(1,6):
            self.images.append(pygame.transform.scale(pygame.image.load(f"Assets\\enemy{i}.png").convert_alpha(),(self.widht,self.height)))
        self.working_image = self.images[0]
        self.placeChangeTime = 15
        self.lastPlaceChangeTime = time.time()

        self.spawanblePlaceX = []
        self.spawanblePlaceY = []
        self.calculatePlaces()

        self.x = random.choice(self.spawanblePlaceX)
        self.y = random.choice(self.spawanblePlaceY)

        self.timeAfterEachProjectile = 5
        self.previousGeneration = time.time()
        # self.previousGeneration = 0
        self.working = False
        self.explode = Sound("explode.mp3")

        # animationStuff
        self.animationCounter= 0
        self.animationTimeCounter = time.time()
        self.animationStep = 0.3

    
    def calculatePlaces(self):
        for i in range(self.container.x + self.widht, self.container.x+self.container.width-self.widht):
            self.spawanblePlaceX.append(i)
        
        for i in range(self.container.y, self.container.y+self.container.height-self.height):
            self.spawanblePlaceY.append(i)

    
    def generateNewParticles(self):
        self.explode.play()
        for i in range(8):
            self.projectiles.append(Particle(self.x+self.widht//2 ,self.y+self.height//2,random.randint(-200,200),random.randint(-200,200)))
            self.previousGeneration = time.time()
    
    def animate(self):
        if time.time() - self.animationTimeCounter >= self.animationStep:
            self.animationCounter+=1
            if self.animationCounter ==5:
                self.animationCounter = 0
            self.animationTimeCounter = time.time()
        
        self.working_image = self.images[self.animationCounter]


    def update(self):
        self.animate()
        if time.time() - self.lastPlaceChangeTime > self.placeChangeTime:
            self.spawanblePlaceX.sort()
            self.spawanblePlaceY.sort()
            self.x = random.choice(self.spawanblePlaceX)
            self.y = random.choice(self.spawanblePlaceY)
            self.lastPlaceChangeTime = time.time()

        if time.time() - self.previousGeneration >= self.timeAfterEachProjectile and not self.working:
            self.generateNewParticles()
            self.timeAfterEachProjectile = random.randint(5,20)
       
        # pygame.draw.rect(self.screen,(50,20,210),(self.x,self.y,self.widht,self.height),0,10)
        if self.collided(self.player):
            return True
        self.screen.blit(self.working_image,(self.x,self.y))


class Particle:
    def __init__(self,x=50,y=50,velx=50,vely=50):
        self.x = x
        self.y = y 
        self.radius = 5
        self.widht = self.radius
        self.height = self.radius
        self.image = pygame.image.load("Assets\\ball.png").convert()
        self.image.set_colorkey((255,255,255))

        self.velx = velx
        self.vely = vely
        self.screen = pygame.display.get_surface()

        self.points = Sound('points.mp3')
        self.damage = Sound('damange.mp3')
    
    def update(self,dt,container,player):
        self.x += self.velx * dt
        self.y += self.vely * dt

        if player.collided(self):
            if player.sheidActivated:
                self.points.play()
                return "DONE"
            

            else:
                self.damage.play()
                return "DEAD"

        if container.collidedLeft(self) or container.collidedRight(self):
            self.velx *= -1
        
        if container.collidedTop(self) or container.collidedBottom(self):
            self.vely *= -1
            
        # pygame.draw.circle(self.screen,(0,0,255),(self.x,self.y),self.radius,0)
        self.screen.blit(self.image,(self.x,self.y))