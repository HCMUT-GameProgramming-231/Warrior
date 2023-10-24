import pygame
from .warrior import WarriorAnimation
from .background import Ground, Flame, VillageObjects, VillageObject, Clouds, Cloud
from .Chest import Chests, Chest
from .camera import Camera
from .slime import Slimes, Slime
from .menu import MainMenu
import random

#tomorrow task: add small delay when jump from slipping
class Processor:
    
    def __init__(self, screen, warrior : WarriorAnimation, ground : Ground, cam : Camera, menu : MainMenu) -> None:
        self.warrior = warrior
        self.ground = ground
        self.cam = cam
        self.slimes = Slimes(screen)
        self.menu = menu
        self.state = 'menu'
        #self.score = 0
        #self.score_rect = pygame.Rect((10, 10, 200, 40))
        self.font= pygame.font.SysFont('Comic Sans MS', 50)
        self.font_rect = pygame.Rect((0, 0, 300, 100))
        self.font_rect.center = (menu.width / 2, menu.height / 2)
        self.text_game_over = self.font.render('Game Over', False, (255, 255, 255))
        self.text_the_end = self.font.render('The end !', False, (255, 255, 255))
        self.end_time = 0
        
        #slime
        slime_pos = []
        slime_map = open('./Map/slime.txt','r')
        for i,line in enumerate(slime_map):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            slime_pos.append([int(ele) for ele in elements if ele != ''])
        slime_map.close()
        
        for pos in slime_pos:
            self.slimes.Generate(pos)
        
        boss_pos = [[6400, 300]]
        for pos in boss_pos:
            self.slimes.GenerateBos(pos)
        
        #flame
        self.flame = []
        flame_pos = open('./Map/flame.txt','r')
        for i,line in enumerate(flame_pos):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            self.flame.append(Flame(screen, [int(ele) for ele in elements if ele != '']))
        flame_pos.close()

        #chest
        self.chests = Chests()
        self.chests_list = []
        chest_pos = open('./Map/chest.txt', 'r')
        for i, line in enumerate(chest_pos):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            pos = [int(ele) for ele in elements if ele!= '']
            self.chests_list.append(self.chests.Generate(screen, [pos[0], pos[1]], pos[2]))
        
        #village object
        vil = VillageObjects()
        self.vil_obj = []
        self.well = None
        
        obj_pos = open('./Map/villageobject.txt', 'r')
        for i, line in enumerate(obj_pos):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            pos = [int(ele) for ele in elements]
            
            if pos[2] == 11:
                self.well = vil.Generate((pos[0], pos[1]), pos[2], screen)
                self.vil_obj += [self.well]
            else:
                self.vil_obj += [vil.Generate((pos[0], pos[1]), pos[2], screen)]
        
        self.interactable = self.chests_list + [self.well]
        
        #cloud
        clo = Clouds()
        self.clouds = []
        
        cloud_pos = open('./Map/cloud.txt', 'r')
        for i, line in enumerate(cloud_pos):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            pos = [int(ele) for ele in elements]
            self.clouds.append(clo.Generate(pos, screen))
        
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        
        self.timeFromBeginning = 0
        self.currentTime = 0
        self.DELTA = 0.01
        #self.currentFrameTime = 0
        self.accumulator = 0
        self.screen = screen
        
    def Update(self, fps, SCREEN):
        ev = pygame.event.get()
        newTime = pygame.time.get_ticks()
        frameTime = (newTime - self.currentTime) / 1000
        if frameTime  > 1 / fps:
            frameTime = 1 / fps
        
        if self.state == 'game':
            pygame.mouse.set_visible(False)
            self.warrior.GetEvent(ev)
            
                
            self.currentTime = newTime
            self.accumulator += frameTime
            
            while self.accumulator >= self.DELTA:
                #self.lastState = copy.copy(self)
                self.Intergrate(self.DELTA)
                self.timeFromBeginning += self.DELTA
                #self.currentFrameTime += self.DELTA
                self.accumulator -= self.DELTA
            
            for f in self.flame:
                    f.Update()
            
            for obj in self.vil_obj:
                obj.Update()
                
            for cloud in self.clouds:
                cloud.Update()
            
            
            
            self.ground.Update()
            for c in self.chests_list:
                c.Update()
                
            self.slimes.Update(self.timeFromBeginning)
                
            self.warrior.Update(fps)

        
        elif self.state == 'menu':
            pygame.mouse.set_visible(True)
            if not self.menu.playing_music:
                self.menu.playing_music = True
                pygame.mixer.music.load('./sound/BG_Music.mp3')
                pygame.mixer.music.play(-1)
            self.state = self.menu.Update(ev, self.timeFromBeginning)

            
                
        elif self.state == 'credits':
            self.menu.RenderBackground(self.timeFromBeginning)
            self.state = self.menu.Credits.display(ev)
            pygame.mouse.set_visible(True)

        elif self.state == 'setting':
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.menu.RenderBackground(self.timeFromBeginning)
            self.state, name = self.menu.setting.display(ev)
            self.warrior.name = name
            pygame.mouse.set_visible(True)
            
        elif self.state == 'end' or self.state == 'gameover':
            self.Intergrate(self.DELTA)
            self.ground.Update()
            self.warrior.Update(fps)
            
            for f in self.flame:
                    f.Update()
            
            for obj in self.vil_obj:
                obj.Update()
                
            for cloud in self.clouds:
                cloud.Update()
            
            for c in self.chests_list:
                c.Update()
                
            for obj in self.vil_obj:
                obj.Update()
            
            self.slimes.Update(self.timeFromBeginning)
            
            self.screen.blit(self.text_the_end, self.font_rect) if self.state == 'end' else self.screen.blit(self.text_game_over, self.font_rect)
            if pygame.time.get_ticks() / 1000 - self.end_time >= 7:
                self.state = 'menu'
                self.reset()
        
            
    def Intergrate(self, deltaTime):
        
        falling = True
        self.warrior.collide_left = False
        self.warrior.collide_right = False
        
        for slime in self.slimes.slimes:
            slime.DetectWarrior(self.warrior.rect)
            if not slime.temp_dead and not self.warrior.fainting and not self.warrior.stand_up and self.warrior.IsCollidingWithSlime(slime):
                if self.warrior.unbeatable:
                    slime.curHP = 0
                else:
                    if self.warrior.falling or self.warrior.jumping or self.warrior.dashing: continue
                    self.warrior.faint_time = self.timeFromBeginning * 1000
                    self.warrior.ChangeStatus('faint')
                    self.warrior.curHP -= slime.damage
                    self.warrior.attacked_by = 'slime'
                    break
            
            if not slime.jumping:
                slime.falling = True
            else:
                slime.falling = False
        
        
        for gr in self.ground.map:
            
            if  gr[-1] == False:  
                
                ret, pos = self.warrior.IsColliding(gr)
                if ret:
                    falling = False
                    if pos == 'On':
                        if not gr[-2] == 10 or gr[-2] == 9:
                            self.warrior.rect.bottom = gr[1].top
                            self.warrior.rect.y += 2
                            self.warrior.falling = False
                            if self.warrior.slipping:
                                self.warrior.slipping = False
                                if self.warrior.direction == 'right':
                                    self.warrior.rect.x += 2
                                else: 
                                    self.warrior.rect.x -= 2
                        
                    elif pos == 'Left':
                        if not self.warrior.slipping:
                            self.warrior.collide_right = True
                            self.warrior.rect.right = gr[1].left + 1


                            
                    elif pos == 'Right':
                        if not self.warrior.slipping :
                            self.warrior.collide_left = True
                            self.warrior.rect.left = gr[1].right - 1
                        


                        
                    elif pos == 'Down':
                        if not self.warrior.slipping: 
                            self.warrior.jumping = False
                            self.warrior.ChangeStatus('fall')
                            
                    elif pos == 'TopLeft' or pos == 'TopRight':
                        if not gr[-2] == 10 or gr[-2] == 9:
                        

                            if pos == 'TopLeft':
                                self.warrior.rect.right = gr[1].left
                            else:
                                
                                self.warrior.rect.left = gr[1].right
                                
                            self.warrior.rect.top = gr[1].top
                            self.warrior.rect.y += 5
                            self.warrior.ChangeStatus('hanging')


                    elif pos == 'SlipLeft' or pos == 'SlipRight':
                        if self.warrior.standing and not self.warrior.slipping: 
                            if pos == 'SlipLeft':
                                self.warrior.rect.right = gr[1].left - 1
                            else:
                                self.warrior.rect.left = gr[1].right + 1
                        else:
                            if pos == 'SlipLeft':
                                self.warrior.rect.right = gr[1].left + 1
                                self.warrior.collide_right = True
                            else:
                                self.warrior.collide_left = True
                                self.warrior.rect.left = gr[1].right - 1
                            self.warrior.falling = False
                            self.warrior.ChangeStatus('slip')
            
            
            for slime in self.slimes.slimes:
                slime.collide_left = False
                slime.collide_right = False
                ret, pos = slime.IsCollidingWithBlock(gr)
                if ret:
                    if pos == 'On':
                        slime.falling = False
                        slime.playsound = False
                        #slime.jumping = True
                        
                    elif pos == 'Left':
                        slime.detectWarrior = False
                        slime.collide_left = True
                        slime.direction = 'right'
                        slime.pos[0] += 150
                        slime.back_speed = 0
                        slime.UpdatePos()
                    
                    elif pos == 'Right': 
                        slime.detectWarrior = False
                        slime.collide_right = True
                        slime.direction = 'left'
                        slime.pos[0] -= 150   
                        slime.back_speed = 0
                        slime.UpdatePos()
                
                if slime.dead:
                    self.warrior.coin += 1
                    self.slimes.slimes.remove(slime)
                    continue
                
                if self.warrior.attacking or self.warrior.attacking_2 or self.warrior.dashing:
                    if self.warrior.attacking or self.warrior.attacking_2:      
                        if pygame.time.get_ticks() - self.warrior.attack_time > 30:  
                            attack_range = self.warrior.attack_range
                            type = 'attack' if self.warrior.attacking else 'attack_2' 
                            if slime.IsBeingAttacked(attack_range, self.timeFromBeginning, type):
                                slime.damage_taken = self.warrior.attack_damage if type == 'attack' else self.warrior.attack_2_damage
                                slime.curHP -= slime.damage_taken
                    else:
                        attack_range = self.warrior.rect
                        type = 'dash'
                        if slime.IsBeingAttacked(attack_range, self.timeFromBeginning, type):
                            slime.damage_taken = self.warrior.dash_damage
                            slime.curHP -= slime.damage_taken
        
        self.warrior.marking = False
        for obj in self.interactable:
            if obj.rect.colliderect(self.warrior.rect):
                    self.warrior.marking = True
                    if(isinstance(obj, Chest)):
                        if obj.close == False:
                            self.interactable.remove(obj)
                            continue
                        self.warrior.marking = True
                        if self.warrior.interact:
                            if obj.UnHidden(self.warrior.rect):
                                if obj.item_name == 'potion':
                                    self.warrior.curHP += 500
                                    if self.warrior.curHP > self.warrior.maxHP: self.warrior.curHP = self.warrior.maxHP
                                elif obj.item_name == 'coin':
                                    self.warrior.coin += 1
                                elif obj.item_name == 'star':
                                    self.warrior.unbeatable = True
                                    self.warrior.begin_unbeatable_time = self.timeFromBeginning
                                else:
                                    self.warrior.dash_damage *= 4
                                    self.warrior.attack_damage *= 4
                                    self.warrior.attack_2_damage *= 4
                            self.warrior.interact = False
                    else:
                        if self.warrior.interact:
                            if self.warrior.coin > 0:
                                i = random.randint(0, len(self.ground.hidden) - 1)
                                self.ground.hidden[i][-1] = False
                                self.ground.hidden.remove(self.ground.hidden[i])
                                self.warrior.coin -= 1
                                self.warrior.interact = False
                    
                
                    

        if falling:
            self.warrior.dashing = False
            self.warrior.quick_moving = False
            self.warrior.ChangeStatus('fall')

        self.warrior.Intergrate(deltaTime)
        self.slimes.Intergrate(deltaTime, self.timeFromBeginning)
        
        if self.warrior.rect.centerx > self.cam.begin_pos_x and self.warrior.rect.x < self.cam.end_pos_x:
                speed = 200
                if self.warrior.dashing or self.warrior.quick_moving:
                    speed = 300
                self.warrior.move_speed = 0
                self.warrior.dash_speed = 0
                offset_x = int(speed * deltaTime)
                if (self.warrior.isHoldingRight or ( (self.warrior.dashing or self.warrior.quick_moving) and self.warrior.direction == 'right') ) and not self.warrior.collide_right:
                    self.ground.Move(-offset_x, 0)
                    self.slimes.Move(-offset_x, 0)
                    for c in self.chests_list:
                        c.Move(-offset_x, 0)
                    for obj in self.vil_obj:
                        obj.Move(-offset_x, 0)
                    for f in self.flame:
                        f.Move(-offset_x, 0)
                    for cloud in self.clouds:
                        cloud.Move(-offset_x, 0)
                    self.cam.begin_pos_x -= offset_x
                    self.cam.end_pos_x -= offset_x
                    self.cam.pos_x = self.warrior.rect.centerx
                if (self.warrior.isHoldingLeft or ( (self.warrior.dashing or self.warrior.quick_moving) and self.warrior.direction == 'left')) and not self.warrior.collide_left:
                    #print(self.warrior.rect.centerx, self.cam.begin_pos_x)
                    self.ground.Move(offset_x, 0)
                    self.slimes.Move(offset_x, 0)
                    for c in self.chests_list:
                        c.Move(offset_x, 0)
                    for obj in self.vil_obj:
                        obj.Move(offset_x, 0)
                    for f in self.flame:
                        f.Move(offset_x, 0)
                    for cloud in self.clouds:
                        cloud.Move(offset_x, 0)
                    self.cam.begin_pos_x += offset_x
                    self.cam.end_pos_x += offset_x
                    self.cam.pos_x = self.warrior.rect.centerx
        else:
            self.warrior.move_speed = 200
            self.warrior.dash_speed = 300
            self.cam.pos_x = self.cam.begin_pos_x
    
        if self.warrior.curHP <= 0:
            self.state = 'gameover'
            self.warrior.dead = True
            self.end_time = self.timeFromBeginning
            
        if not self.slimes.slimes:
            self.state = 'end'
            self.end_time = self.timeFromBeginning
            
    def reset(self):
        self.warrior.reset()
        
            
        


            
            