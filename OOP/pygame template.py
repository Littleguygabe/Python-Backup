import pygame,sys
pygame.init()

def startprogram():
    sw=2400
    sh=1200
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
            pygame.display.flip()
            clock.tick(30)
            
if __name__ == '__main__':
    startprogram()