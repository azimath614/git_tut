import sys
import pygame
import os.path
import random

main_dir = os.path.split(os.path.abspath(__file__))[0]
GROUND_Y = 700 - 120
WALK_X = 100
WALK_Y = GROUND_Y - 200
GROUND_ERASE_Y = 1000


def load_image(file):
    file = os.path.join(main_dir,'data', file)
    try:
        screen = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return screen.convert_alpha()

class dummysound:
  def play(self): pass

def load_sound(file):
  if not pygame.mixer: return dummysound()
  file = os.path.join(main_dir, 'data', file)
  try:
    sound = pygame.mixer.Sound(file)
    return sound
  except pygame.error:
    print ('Warning, unable to load, %s' % file)
  return dummysound()

class Player():
    images = []
    rect = pygame.Rect(0,0,110,200)
    animation = 0
    animation_delta = 1
    jump_delta = 0.0
    fall = False
    def __init__(self):
        self.images.append(load_image("Girl0.png"))
        self.images.append(load_image("Girl1.png"))
        self.images.append(load_image("Girl2.png"))
        self.images.append(load_image("Girl3.png"))
        self.images.append(load_image("Girl4.png"))
        self.rect = self.images[0].get_rect()
        self.rect.left = WALK_X
        self.rect.top = WALK_Y
        
    def move(self, screen):
        if self.animation < 0 or self.animation >= 24:
            self.animation_delta *= -1
        self.animation += self.animation_delta

        if self.fall == False:
            self.rect.top -= int(self.jump_delta)
            if self.rect.top < WALK_Y:
                self.jump_delta -= 1
            else:
                self.rect.top = WALK_Y
                self.jump_delta = 0
        else:
            self.rect.top += 8
        screen.blit(self.images[int(self.animation/5)], self.rect)



class Ground():
    image = None
    rects = []
    speed = 4.0
    mouse_down = False

    def __init__(self):
        self.image = load_image("Ground.png")
        for i in range(14):
            self.rects.append(self.image.get_rect())
            self.rects[i].left = i * 80
            self.rects[i].top = GROUND_Y
    def move(self, screen, fall):
        if self.mouse_down:
            if self.speed <= 29:
                self.speed += 0.1
        elif self.speed >= 1.4:
            self.speed -= 0.2
        for rect in self.rects:
            if fall == False:
                rect.left -= int(self.speed)
            if rect.left <= -80:
                rect.left += 80 * 14
                if random.randint(0,3) == 0:
                    rect.top = GROUND_ERASE_Y
                else:
                    rect.top = GROUND_Y
            if rect.top == GROUND_Y:
                screen.blit(self.image, rect)
    def fall(self,y):
        for rect in self.rects:
            if rect.top == GROUND_ERASE_Y and y >=WALK_Y and rect.left >= WALK_X-20 and rect.left <= WALK_X+60:
                return True
            return False

class ScoreFont():
    score = 0
    hi_score = 500
    font = None
    def __init__(self):
        self.font = pygame.font.SysFont("Arial",50)
    def draw(self,screen):
        self.score += 1
        text = self.font.render("Score "+str(self.score),True,(0,0,255))
        screen.blit(text,(10,10))
        if self.score >= self.hi_score:
            self.hi_score = self.score
            text = self.font.render("HiScore "+str(self.hi_score),True,(0,0,255))
            screen.blit(text,(480,10))



def main():
    pygame.init()
    screen = pygame.display.set_mode((960,700))
    pygame.display.set_caption("ジャンプゲーム")

    ground = Ground()
    player = Player()
    score_font = ScoreFont()

    bgm_sound = load_sound('BGM.wav')
    over_sound = load_sound('GameOver.wav')
    bgm_sound.play(-1)

    while(True):
        screen.fill((128,192,255))
        score_font.draw(screen)
        ground.move(screen,player.fall)
        if ground.fall(player.rect.top) and player.fall == False:
            player.fall = True
            over_sound.play()
        player.move(screen)
        pygame.time.wait(30)
        pygame.display.update()

        if player.rect.top >= 800:
            player.rect.top = WALK_Y
            player.fall = False
            player.jump_delta = 0
            score_font.score = 0
            for rect in ground.rects:
                rect.top = GROUND_Y
            ground.speed = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                ground.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                ground.mouse_down = False
                if player.rect.top == WALK_Y:
                    player.jump_delta = ground.speed
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            

if __name__ == "__main__":
    main()