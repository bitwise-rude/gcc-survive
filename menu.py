import pygame

class Menu:
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.running = True
        self.toPlay = False
        self.textFont = pygame.font.SysFont("Helvetica",60)
        self.textFont2 = pygame.font.SysFont("Helvetica",20)
        self.upperText = self.textFont.render("GCC- Survive the balls!",True,(255,0,255))
        self.lowerText = self.textFont2.render("Made by- Meyan Adhikari",True,(0,0,0))
        self.lowerText3= self.textFont2.render("Press Space to activate the shield, destroy the balls with your shield,\n Use the arrow keys or WASD to move, hold shift to move faster",True,(0,0,0))

        self.highScore = readHighScore()
        self.lowerText2 = self.textFont2.render(f"HighScore:{self.highScore}",True,(0,0,0))

        self.buttons = [Button("Play",(200,150,150,50),self.play,self.manageHover),Button("Quit",(200,210,150,50),self.quit,self.manageHover)]
    
    def manageHover(self,other):
        other.color = (255,0,0)
    
    def play(self):
        self.running = False
        self.toPlay = True
    
    def quit(self):
        self.running = False

    def mainloop(self):
        
        while self.running:
            
            self.screen.fill((255,255,255))
            for evs in pygame.event.get():
                if evs.type == pygame.QUIT:
                    self.running  = False
            
                if evs.type == pygame.MOUSEBUTTONUP:
                    for bts in self.buttons:
                        bts.manageClick()
            self.screen.blit(self.upperText,(50,50))
            self.screen.blit(self.lowerText,(25,620))
            self.screen.blit(self.lowerText2,(220,420))
            self.screen.blit(self.lowerText3,(10,320))

            for bts in self.buttons:
                bts.update()
            pygame.display.update()
        return


class Button:
    def __init__(self,text,rect,onClick,onHover,color=(255,255,0)):
        self.rect = rect
        self.originalRect= rect
        self.text = text
        self.originalText= text
        self.originalColor = color
        self.onClick = onClick
        self.onHover = onHover
        self.color = color
        self.toWrite = pygame.font.SysFont("Times",40)
        self.screen = pygame.display.get_surface()
    
    def resetSettings(self):
        self.color =self.originalColor
        self.rect = self.originalRect
        self.text = self.originalText 
    
    def manageHover(self):
        if self.onHover:
            x,y = pygame.mouse.get_pos()
            if x > self.rect[0] and x < self.rect[0]+self.rect[2] and y>self.rect[1] and y<self.rect[1]+self.rect[3]:
                self.onHover(self)

    def manageClick(self):
        if self.onClick:
            x,y = pygame.mouse.get_pos()
            if x > self.rect[0] and x < self.rect[0]+self.rect[2] and y>self.rect[1] and y<self.rect[1]+self.rect[3]:
                self.onClick()
    
    def update(self):
        self.resetSettings()
        self.manageHover()
        pygame.draw.rect(self.screen,self.color,self.rect,0,10)
        self.screen.blit(self.toWrite.render(self.text,False,(0,0,0)),(self.rect[0]+5,self.rect[1]+10))


def readHighScore():
    try:
        f = open("Assets\\highScore.txt",'r')
        data = int(f.read())
        f.close()
        return data
    except Exception as e:
        return 0
def writeHighScore(score):
    try:
        f = open("Assets\\highScore.txt",'w')
        f.write(str(score))
        f.close()
    except Exception as e:
        print(e)
