import pygame, sys, time
global menu, game_done

#INITIALIZING PYGAME
pygame.init()
pygame.mixer.init()

# Music
game_music_file="assets/tvari-tokyo-cafe-159065.mp3"
music_file = "assets\win_sound.mp3"
select_sound_file = "assets/select_sound.mp3"
float_up_file="assets\click-button-140881.mp3"
float_down_file="assets\disc_place.mp3"
float_aside_file="assets\drop_sound.mp3"

def menu_music():
    if menu:
          # Assuming correct path
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  # Play music on a loop

def game_music():
    pygame.mixer.music.stop()

    pygame.mixer.music.load(game_music_file)
    pygame.mixer.music.play(-1)


def play_select_sound(): 
    select_sound = pygame.mixer.Sound(select_sound_file)
    select_sound.play()

def float_up_sound():
    float_sound=pygame.mixer.Sound(float_up_file)
    float_sound.play()
    
def float_down_sound():
    float_down=pygame.mixer.Sound(float_down_file)
    float_down.play()
    
def float_aside_sound():
    float_aside=pygame.mixer.Sound(float_aside_file)
    float_aside.play()
    
#SETTING UP DISPLAY
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
menu=True



# game vars:
game_done = False
framerate = 60
steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0

# DEFINING COLOURS:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78,162,196) 
grey = (170, 170, 170)
green = (77, 206, 145)

 #DEFINING FUNCTIONS 
def blit_text(screen, text, midtop, aa=True, font=None, font_name = None, size = None, color=(255,0,0)):
    if font is None:                                    # font option is provided to save memory if font is
        font = pygame.font.SysFont(font_name, size)     # already loaded and needs to be reused many times
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)
    
def menu_screen():  # to be called before starting actual game loop
    global screen, n_disks, game_done
    menu_done = False
    menu=True
    menu_music()
    while not menu_done:  # every screen/scene/level has its own loop
        screen.fill(green)
        blit_text(screen, 'Towers of Hanoi', (323,122), font_name='sans serif', size=90, color=grey)
        blit_text(screen, 'Towers of Hanoi', (320,120), font_name='sans serif', size=90, color=gold)
        blit_text(screen, 'Use arrow keys to select difficulty:', (320, 220), font_name='sans serif', size=30, color=black)
        blit_text(screen, str(n_disks), (320, 260), font_name='sans serif', size=40, color=red)
        blit_text(screen, 'Press ENTER to continue', (320, 320), font_name='sans_serif', size=30, color=black)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    game_done = True
                    menu=False
                if event.key == pygame.K_RETURN:
                    menu_done = True
                    menu=False
                    game_music()
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    play_select_sound()
                    if n_disks > 6:
                        n_disks = 6
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    play_select_sound()
                    if n_disks < 1:
                        n_disks = 1
            if event.type == pygame.QUIT:
                menu_done = True
                menu=False
                game_done = True
        pygame.display.flip()
        clock.tick(60)

def game_over(): # game over screen
    global screen, steps, game_done 
    # screen.fill(blue)
    min_steps = 2**n_disks - 1
    # Display game over messages
    if min_steps == steps:
        screen.fill(blue)
        blit_text(screen, 'You finished in minimum steps!', (320, 300), font_name='mono', size=26, color=red)
        blit_text(screen, 'You finished in minimum steps!', (321, 301), font_name='mono', size=26, color=red)
        blit_text(screen, 'Congrats, You Won!', (320, 200), font_name='sans serif', size=72, color=gold)
        blit_text(screen, 'Congrats, You Won!', (321, 201), font_name='sans serif', size=72, color=gold)
        blit_text(screen, 'Your Steps: ' + str(steps), (320, 360), font_name='mono', size=30, color=red)
        blit_text(screen, 'Your Steps: ' + str(steps), (321, 361), font_name='mono', size=30, color=red)
        blit_text(screen, 'Minimum Steps: ' + str(min_steps), (320, 390), font_name='mono', size=30, color=black)
        blit_text(screen, 'Minimum Steps: ' + str(min_steps), (321, 391), font_name='mono', size=30, color=black)
        blit_text(screen, 'Press R to Restart', (320, 430), font_name='sans_serif', size=30, color=black)

    else:
        screen.fill(grey)
        blit_text(screen, "You didn't finish in minimum steps!", (320, 300), font_name='mono', size=26, color=red)
        blit_text(screen, "You didn't finish in minimum steps!", (321, 301), font_name='mono', size=26, color=red)
        blit_text(screen, 'Better Luck Next Time!', (320, 200), font_name='sans serif', size=72, color=gold)
        blit_text(screen, 'Better Luck Next Time!', (321, 201), font_name='sans serif', size=72, color=gold)
        blit_text(screen, 'Your Steps: ' + str(steps), (320, 360), font_name='mono', size=30, color=red)
        blit_text(screen, 'Your Steps: ' + str(steps), (321, 361), font_name='mono', size=30, color=red)
        blit_text(screen, 'Minimum Steps: ' + str(min_steps), (320, 390), font_name='mono', size=30, color=black)
        blit_text(screen, 'Minimum Steps: ' + str(min_steps), (321, 391), font_name='mono', size=30, color=black)
        blit_text(screen, 'Press R to Restart', (320, 430), font_name='sans_serif', size=30, color=black)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Check if left mouse button is clicked
                    game_done = False  # Reset the game_done flag
                    reset()  # Call the reset function to restart the game
                    return  # Exit the game_over function
    
        clock.tick(framerate)


    
def draw_towers():
    global screen
    for xpos in range(40, 460+1, 200):
        pygame.draw.rect(screen, blue, pygame.Rect(xpos, 400, 160 , 20))
        pygame.draw.rect(screen, black, pygame.Rect(xpos+75, 200, 10, 200))
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    blit_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=black)


def make_disks():
    global n_disks, disks
    disks = []
    height = 20
    ypos = 397 - height
    width = n_disks * 23
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (120, ypos)
        disk['val'] = n_disks-i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height+3
        width -= 23


def draw_disks():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(screen, green, disk['rect'])
    return

def draw_ptr():
    ptr_points = [(towers_midx[pointing_at]-7 ,440), (towers_midx[pointing_at]+7, 440), (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(screen, red, ptr_points)
    return

def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(1)
        game_over()

def reset():
    global steps,pointing_at,floating,floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    make_disks()



#CALLING IMPORTANT FUNCTIONS
menu_screen()
make_disks()

# MAIN GAME LOOP
while not game_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                reset()
            if event.key == pygame.K_q:
                game_done = True
            if event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at+1)%3
                if floating:
                    float_aside_sound()
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_LEFT:
                pointing_at = (pointing_at-1)%3
                if floating:
                    float_aside_sound()
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_UP and not floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        float_up_sound()
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        break
            if event.key == pygame.K_DOWN and floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk)!=floater:
                        if disk['val']>disks[floater]['val']:
                            floating = False
                            float_down_sound()
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                            steps += 1
                        break
                else: 
                    floating = False
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                    steps += 1
    screen.fill(gold)
    draw_towers()
    draw_disks()
    draw_ptr()
    min_steps = 2**n_disks-1
    blit_text(screen, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=black)
    blit_text(screen, 'Best Steps: '+str(min_steps), (320, 50), font_name='mono', size=30, color=black)
    pygame.display.flip()
    if not floating:
        check_won()
    clock.tick(framerate)