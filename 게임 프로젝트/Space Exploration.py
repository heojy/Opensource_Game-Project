import pygame
import time
import random

pygame.init()

screen_width = 320
screen_height = 500

black = (0, 0, 0) 
white = (255, 255, 255)
blue = (0, 0, 255)

scor = 100 # 게임상 생명력 (life 점수)

displayscreen = pygame.display.set_mode([screen_width, screen_height])

font = pygame.font.Font("NanumSquareB.ttf",30) #결과 화면 폰트
play_font = pygame.font.Font("NanumSquareB.ttf",20) #게임 화면 폰트
collision_sound = pygame.mixer.Sound("collision.sound.wav") #충돌시 효과음
ending_sound = pygame.mixer.Sound("ending sound.wav") #게임 종료시 효과음

score_display = play_font.render("Life :", True, (255,255,255))
jumsu_dsplay = play_font.render("점수 :", True, (255,255,255))
game_result = font.render("Game over", True, (255,255,255))
ju = font.render("점수 :", True, (255,255,255)) #점수 밑 결과 처리시 필요한 글자 표시

enemy_list = [pygame.image.load('e1.PNG'), 
              pygame.image.load('e2.PNG'), 
              pygame.image.load('e3.PNG'), 
              pygame.image.load('e4.PNG'),
              pygame.image.load('e5.PNG'),
              pygame.image.load('e6.PNG'),
              pygame.image.load('e7.PNG'),
              pygame.image.load('e8.PNG'),
              pygame.image.load('e9.PNG'),
              pygame.image.load('e10.PNG'),
              pygame.image.load('e11.PNG'),
              pygame.image.load('e12.PNG')]

pygame.display.set_caption('Space Exploration')

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player.PNG')
        self.dx = 5
        self.dy = 5
        self.rect = self.image.get_bounding_rect()
        self.rect.x = 145 # 세팅되는 위치
        self.rect.y = 400
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 290:
            self.rect.x = 290
        
        if self.rect.y < 50:
            self.rect.y = 50
        elif self.rect.y > 464:
            self.rect.y = 464

class EnemyShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_list)
        self.dx = random.randint(-3,3)
        self.dy = random.randint(3,5)
        self.rect = self.image.get_bounding_rect()
        self.rect.x = 160
        self.rect.y = 0
        
    def move(self):
        self.rect.x += self.dx
        if self.rect.x <0:
            self.dx = random.randint(0,3)
        elif self.rect.x > 285:
            self.dx = random.randint(-3,0)
        self.rect.y += self.dy
        if self.rect.y > 460 : 
            self.rect.y = 0
            self.image = random.choice(enemy_list)
            self.rect.x = random.randint(0,280)
            self.dx = random.randint(-3,3)
            self.dy = random.randint(4,6)

object_list = pygame.sprite.Group()

ship = PlayerShip()
object_list.add(ship)

enemy = EnemyShip()
object_list.add(enemy) 

play_game = True

frame_count = 0
jum = 0 # 점수 표시

while play_game == True:
    time.sleep(0.01)
    frame_count +=1
    jum += 0.1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_game = False
       
    key = pygame.key.get_pressed() #조작하는 키의 입력을 받아 처리
    if key[pygame.K_UP]:
        ship.move(0, -3)
    if key[pygame.K_DOWN]:
        ship.move(0, +3)
    if key[pygame.K_LEFT]:
        ship.move(-3, 0)
    if key[pygame.K_RIGHT]:
        ship.move(+3, 0)
        
    if (frame_count % 1) == 0:
        enemy.move()
    
    displayscreen.fill(black)
    
    if pygame.sprite.spritecollideany(ship, [enemy]): #충돌시
            scor -= 1 # 생명을 깎고
            collision_sound.play() # 충돌 효과음 재생
            
    for obj in object_list:
        displayscreen.blit(obj.image, (obj.rect.x, obj.rect.y))
    
    displayscreen.blit(score_display,(10,430))
    displayscreen.blit(jumsu_dsplay,(10,460)) #점수 밑 결과 처리시 필요한 글자 표시
    
    li = str(scor) # LIFE 남은걸 문자형으로 
    score_displayy = play_font.render(li,True,(255,255,255)) #게임 내 life 표시
    displayscreen.blit(score_displayy,(63,430))
    
    jumsu = int(jum) # 점수를 정수형으로
    jums = str(jumsu) # 정수형으로 바꾼 점수를 문자형으로
    jumsu_display = play_font.render(jums,True,(255,255,255)) # 점수 게임 내 표시
    result_jumsu_display = font.render(jums,True,(255,255,255))
    displayscreen.blit(jumsu_display,(60,460)) #점수 밑 결과 처리시 필요한 글자 표시
        
    if scor == -1: # 생명력이 0으로 되었을경우
        time.sleep(1) # 잠시 멈춘다음
        ship.kill() # 플레이어 사망 
        play_game = False # 게임 종료
    pygame.display.update() 
        
    
displayscreen.blit(game_result, (90,200))
displayscreen.blit(result_jumsu_display,(int(screen_width/2+20),int(screen_height/2)))
displayscreen.blit(ju,(100,250)) #점수 밑 결과 처리시 필요한 글자 표시
pygame.display.update()

ending_sound.play() 
pygame.time.delay(2000) # 게임 종료시 종료 효과음 재생 및 딜레이

pygame.quit() #화면 꺼짐.