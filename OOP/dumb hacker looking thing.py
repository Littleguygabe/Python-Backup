import pygame,sys
import random
import string
pygame.init()

GREEN = (61, 224, 2)
BLACK = (0,0,0)

def getjapan():
    japanese_letters = ['あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ', 'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と', 'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ', 'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん']
    print(japanese_letters)
    return random.choice(japanese_letters)

class text():
    def __init__(self,screen,x,y,font):
        self.screen = screen
        self.x = x
        self.y = y
    
        self.font = font

    def draw(self):
        #text_surface = self.font.render(random.choice(string.ascii_letters), False, GREEN)
        #text_surface = self.font.render(str(random.randint(0,1)), False, GREEN)
        text_surface = self.font.render(getjapan(), False, GREEN)
        self.screen.blit(text_surface, (self.x,self.y))

def startprogram():
    sw=2000
    sh=1000

    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()

    textList = []
    letterGap = 20
    my_font = pygame.font.SysFont('Yu Mincho UI', letterGap)
    for y in range(0,sh,letterGap):
        temparr = []
        for x in range(0,sw,letterGap):
            textVar = text(screen,x,y,my_font)
            temparr.append(textVar)
        textList.append(temparr)


    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            screen.fill(BLACK)

            for y in range(len(textList)):
                for x in range(len(textList[y])):
                    textList[y][x].draw()

            pygame.display.flip()
            clock.tick(30)
            
if __name__ == '__main__':
    startprogram()