import pygame
from .background import Ground, Clouds, VillageObjects, Flame
from .slime import Slimes

class MainMenu(pygame.sprite.Sprite):
    def __init__(self, screen, WINDOW_WIDTH, WINDOW_HEIGHT):
     
        self.playing_music = False
        self.SCREEN = screen
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        
        self.bg = Ground(screen, './map/menu.txt')
        
        clo = Clouds()
        self.clouds = []
        cloud_pos = open('./Map/menu_cloud.txt', 'r')
        for i, line in enumerate(cloud_pos):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            pos = [int(ele) for ele in elements]
            self.clouds.append(clo.Generate(pos, screen))
            
        vil = VillageObjects()
        self.vil_obj = []

        obj_pos = open('./Map/villageobjects_menu.txt', 'r')
        for i, line in enumerate(obj_pos):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            pos = [int(ele) for ele in elements]
            self.vil_obj += [vil.Generate((pos[0], pos[1]), pos[2], screen)]
        
        #flame
        self.flame = []
        flame_pos = open('./Map/flame_menu.txt','r')
        for i,line in enumerate(flame_pos):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            self.flame.append(Flame(screen, [int(ele) for ele in elements if ele != '']))
        flame_pos.close()
        
        #slimes
        self.slimes = Slimes(screen)
        slime_pos = []
        slime_map = open('./Map/slime_menu.txt','r')
        for i,line in enumerate(slime_map):
            if line[0] == '#' or line[0] == '' or line[0] == '\n': continue
            line = line.replace('\n', '')
            elements = line.split(' ')
            slime_pos.append([int(ele) for ele in elements if ele != ''])
        slime_map.close()
        
        for pos in slime_pos:
            self.slimes.Generate(pos)
        
		#buttons
        self.buttons = []
        button_size = (120, 50)
        self.playButton = Button("game", pygame.Rect((0, 0), (120, 50)), button_size, "./Assets/Button/play.png")
        self.creditsButton = Button("credits", pygame.Rect((0, 0), (120, 50)), button_size, "./Assets/Button/credits.png")
        self.exitButton = Button("exit", pygame.Rect((0, 0), (120, 50)), button_size, "./Assets/Button/exit.png")
        self.settingButton = Button("setting", pygame.Rect((0, 0), (120, 50)), button_size, "./Assets/Button/setting.png")

        self.buttons += [self.playButton, self.creditsButton, self.settingButton,self.exitButton]
		
        i = 0
        while i < 4:
            self.buttons[i].rect.center = (self.width / 2, self.height / 2)
            self.buttons[i].rect.y += 60*i
            i += 1

        self.clickSound = pygame.mixer.Sound("./sound/sword-sound-1.mp3")
        self.Credits = Credits(screen, WINDOW_WIDTH, WINDOW_HEIGHT)

    """Hien thi main menu"""
    def Update(self, event, time):
        pos = pygame.mouse.get_pos()
        status = "menu"
        if(self.check_hover(pos)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)	
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)	
		
        for ev in event:
            if ev.type == pygame.QUIT:
                pygame.quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:		
                clicked_button = self.check_clicked(pos)		
                if clicked_button:
                    if clicked_button.name == "exit":
                        pygame.quit()
                    else:
                        pygame.mixer.find_channel(True).play(self.clickSound)
                        status = clicked_button.name

        self.RenderBackground(time)
        for button in self.buttons:
            self.SCREEN.blit(button.img,  button.rect)
		
        return status
    
    def RenderBackground(self, time):
        self.slimes.Intergrate(0.01, time)
        
        for f in self.flame:
            f.Update()
        for cloud in self.clouds:
            cloud.Update()
        for obj in self.vil_obj:
            obj.Update()
        self.slimes.Update(time)
        self.bg.Update()
 
    """Check xem mouse co de tren button nao k"""
    def check_hover(self, pos):
        for button in self.buttons:
            if pos[0] > button.rect.x and pos[0] < button.rect.x + button.rect.width:
                if pos[1] > button.rect.y and pos[1] < button.rect.y + button.rect.height:
                    return True
        return False

    """check xem mouse co click vao button nao k"""
    def check_clicked(self, pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                return button
        return None

class Button(pygame.sprite.Sprite):
	def __init__(self, name, rect, size, img_path):
		self.name = name
		self.rect = rect
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, size)
  
class Credits:
	def __init__(self, screen, WINDOW_WIDTH, WINDOW_HEIGHT):
		self.screen = screen
		self.width = WINDOW_WIDTH
		self.height = WINDOW_HEIGHT
		# Background image
		self.screen_rect = self.screen.get_rect()
		
		font = pygame.font.SysFont("monospace", 40)
		credit_list = ["CREDITS - ZombieHitHead"," ","Hoa Phuong Tung - 2012385","Nguyen Hoang Tri Vien - 2015043", "Nguyen Phu Vinh Toan - 2014775"]
		self.texts = []
		
		for i, line in enumerate(credit_list):
			s = font.render(line, 1, (60, 255, 100))
			
			r = s.get_rect(centerx=self.screen_rect.centerx, y=self.screen_rect.bottom + i * 60)
			self.texts.append((r, s))
	
	def display(self, ev):
		status = "credits"

		for event in ev:
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				status = "menu"
				for i in range(len(self.texts)):
					self.texts[i][0].centerx = self.screen_rect.centerx
					self.texts[i][0].y = self.screen_rect.bottom + i * 60
     
		# Draw texts
		for r, s in self.texts:
			r.move_ip(0, -1)
			self.screen.blit(s, r)
		# Check end of texts
		if not self.screen_rect.collidelistall([r for (r, _) in self.texts]):
			status = "menu"
			for i in range(len(self.texts)):
				self.texts[i][0].centerx = self.screen_rect.centerx
				self.texts[i][0].y = self.screen_rect.bottom + i * 60

		return status