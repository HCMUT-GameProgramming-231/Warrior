import pygame
from .background import Ground

class MainMenu(pygame.sprite.Sprite):
    def __init__(self, screen, WINDOW_WIDTH, WINDOW_HEIGHT):
     
        self.playing_music = False
        self.SCREEN = screen
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.bg = Ground(screen, './map/menu.txt')
		#buttons
        self.buttons = []
        button_size = (120, 50)
        self.playButton = Button("game", pygame.Rect((0, 0), (120, 50)), button_size, "./Assets/Button/play.png")
        self.creditsButton = Button("setting", pygame.Rect((0, 0), (120, 50)), button_size, "./Assets/Button/credits.png")
        self.exitButton = Button("exit", pygame.Rect((0, 0), (120, 50)), button_size, "./Assets/Button/exit.png")
        self.settingButton = Button("setting", pygame.Rect((0, 0), (120, 50)), button_size, "./Assets/Button/setting.png")

        self.buttons += [self.playButton, self.creditsButton, self.settingButton,self.exitButton]
		
        i = 0
        while i < 4:
            self.buttons[i].rect.center = (self.width / 2, self.height / 2)
            self.buttons[i].rect.y += 60*i
            i += 1

        self.clickSound = pygame.mixer.Sound("./sound/sword-sound-1.mp3")

    """Hien thi main menu"""
    def Update(self, event):
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
                    elif clicked_button.name == "setting":
                        status = clicked_button.name
                    else:
                        pygame.mixer.find_channel(True).play(self.clickSound)
                        status = 'game'
                        self.playing_music = False


        self.RenderBackground()
        for button in self.buttons:
            self.SCREEN.blit(button.img,  button.rect)
		
        return status
    
    def RenderBackground(self):
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