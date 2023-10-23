import pygame
from .warrior import WarriorAnimation
from .background import Ground, Flame, VillageObjects, VillageObject, Clouds, Cloud
from .Chest import Chests, Chest
from .camera import Camera
from .slime import Slimes, Slime
from .menu import MainMenu


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
        self.font = None
        
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
        
        boss_pos = [[5750, 300]]
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
            self.chests_list.append(self.chests.Generate(screen, [int(ele) for ele in elements if ele!= '']))
        
        #village object
        vil = VillageObjects()
        self.vil_obj = []

        obj_pos = open('./Map/villageobject.txt', 'r')
        for i, line in enumerate(obj_pos):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            pos = [int(ele) for ele in elements]
            self.vil_obj += [vil.Generate((pos[0], pos[1]), pos[2], screen)]
            
        
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
        
    def Update(self, fps, SCREEN):
        ev = pygame.event.get()
        
        
        if self.state == 'game':
            pygame.mouse.set_visible(False)
            self.warrior.GetEvent(ev)
            newTime = pygame.time.get_ticks()
            frameTime = (newTime - self.currentTime) / 1000
            if frameTime  > 1 / fps:
                frameTime = 1 / fps
                
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
            
            for c in self.chests_list:
                c.Update()
            
            self.ground.Update()
            self.slimes.Update(self.timeFromBeginning)
                
            self.warrior.Update(fps)
            text = self.font.render(self.warrior.name, False, (255, 255, 255))
        
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
            pass
        elif self.state == 'setting':
            self.state = 'menu'
            pygame.mouse.set_visible(True)
            pass
        
    def Intergrate(self, deltaTime):
        
        falling = True
        self.warrior.collide_left = False
        self.warrior.collide_right = False
        
        for slime in self.slimes.slimes:
            slime.DetectWarrior(self.warrior.rect)
            if not slime.temp_dead and self.warrior.IsCollidingWithSlime(slime):
                self.warrior.faint_time = self.timeFromBeginning * 1000
                self.warrior.ChangeStatus('faint')
                self.warrior.curHP -= slime.damage
                if self.warrior.curHP < 0: self.warrior.curHP = 0
                self.warrior.attacked_by = 'slime'
            
            if not slime.jumping:
                slime.falling = True
            else:
                slime.falling = False
        
        
        for gr in self.ground.map:
            
            if abs(gr[1].x - self.warrior.rect.x) < 100 and abs(gr[1].y - self.warrior.rect.y) < 100:  
                
                ret, pos = self.warrior.IsColliding(gr)
                if ret:
                    falling = False
                    if pos == 'On':
                        if gr[-1] == 10 or gr[-1] == 9: continue
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
                        if self.warrior.slipping : continue
                        self.warrior.collide_right = True
                        self.warrior.rect.right = gr[1].left + 1


                            
                    elif pos == 'Right':
                        if self.warrior.slipping : continue
                        self.warrior.collide_left = True
                        self.warrior.rect.left = gr[1].right - 1
                        


                        
                    elif pos == 'Down':
                        if self.warrior.slipping: continue
                        self.warrior.jumping = False
                        self.warrior.ChangeStatus('fall')
                            
                    elif pos == 'TopLeft' or pos == 'TopRight':
                        if gr[-1] == 10 or gr[-1] == 9: continue
                        

                        if pos == 'TopLeft':
                            self.warrior.rect.right = gr[1].left
                        else:
                            
                            self.warrior.rect.left = gr[1].right
                            
                        self.warrior.rect.top = gr[1].top
                        self.warrior.rect.y += 5
                        self.warrior.ChangeStatus('hanging')


                    elif pos == 'SlipLeft' or pos == 'SlipRight':
                        if self.warrior.slipping : continue
                        if self.warrior.standing : 
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
                        slime.collide_left = True
                        slime.direction = 'right'
                        slime.pos[0] += 150
                        slime.UpdatePos()
                    
                    elif pos == 'Right': 
                        slime.collide_right = True
                        slime.direction = 'left'
                        slime.pos[0] -= 150   
                        slime.UpdatePos()
                
                if slime.dead:
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
                        
                        
        if self.warrior.findHiddenChest:
            for chest in self.chests_list:
                if chest.UnHidden(self.warrior.rect):
                    if chest.item_name == 'potion':
                        self.warrior.curHP += 100
                        if self.warrior.curHP > self.warrior.maxHP: self.warrior.curHP = self.warrior.maxHP
                    

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


            
            