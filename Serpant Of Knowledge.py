import pygame
import random
import sys
import json
import os 

pygame.init()
correct_sound = pygame.mixer.Sound('apple ate.wav')
wrong_sound = pygame.mixer.Sound('MISSED.wav')
game_over_sound = pygame.mixer.Sound('GAME OVER.wav')
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  # Trigger when song ends
playlist = [
    "Motocross Game.mp3",
    "upbeat.mp3",
    "gameboy.mp3",
    "techy.mp3",
    "funky.mp3"
]
current_song_index = 0


# Constants
WINDOWWIDTH = 1920
WINDOWHEIGHT = 1080
CELLSIZE = 20
FPS = 10

GRID_X = 650
GRID_Y = (WINDOWHEIGHT - 640) // 2
GRID_WIDTH = 1080
GRID_HEIGHT = 640
GRID_COLS = GRID_WIDTH // CELLSIZE
GRID_ROWS = GRID_HEIGHT // CELLSIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
PURPLE = (75, 0 , 130)
PINK = (250 , 0 , 150 )

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

glow_timer = 0
score = 0
previous_score = 0
question_bank = {
    "Science": [
        {"question": "What is the chemical symbol for water?", "answers": ["H2O", "O2", "CO2"], "correct": "H2O"},
        {"question": "Which organ pumps blood throughout the body?", "answers": ["Liver", "Brain", "Heart"], "correct": "Heart"},
        {"question": "What is the function of red blood cells?", "answers": ["Clot blood", "Transport oxygen", "Fight infection"], "correct": "Transport oxygen"},
        {"question": "What does DNA stand for?", "answers": ["Deoxyribonucleic Acid", "Dynamic Nuclear Atom", "Dioxide Nitric Acid"], "correct": "Deoxyribonucleic Acid"},
        {"question": "Which gas is essential for human respiration?", "answers": ["Oxygen", "Carbon Dioxide", "Nitrogen"], "correct": "Oxygen"},
        {"question": "What is the pH of a neutral substance?", "answers": ["0", "7", "14"], "correct": "7"},
        {"question": "Which subatomic particle has a positive charge?", "answers": ["Electron", "Proton", "Neutron"], "correct": "Proton"},
        {"question": "What is the unit of electrical current?", "answers": ["Ampere", "Volt", "Ohm"], "correct": "Ampere"},
        {"question": "Which planet is closest to the Sun?", "answers": ["Venus", "Earth", "Mercury"], "correct": "Mercury"},
        {"question": "What is the main function of chlorophyll?", "answers": ["Absorb water", "Absorb sunlight", "Release oxygen"], "correct": "Absorb sunlight"},
        {"question": "Which organ is responsible for pumping blood around the body?", "answers": ["Heart", "Lungs", "Kidney"], "correct": "Heart"},
        {"question": "What is the chemical formula for water?", "answers": ["H2O", "CO2", "O2"], "correct": "H2O"},
        {"question": "Which of these is a metal?", "answers": ["Iron", "Sulfur", "Oxygen"], "correct": "Iron"},
        {"question": "What is the unit of electrical current?", "answers": ["Ampere", "Volt", "Watt"], "correct": "Ampere"},
        {"question": "Where does photosynthesis occur in plants?", "answers": ["Leaves", "Roots", "Stems"], "correct": "Leaves"},
        {"question": "Which gas is essential for combustion?", "answers": ["Oxygen", "Carbon Dioxide", "Nitrogen"], "correct": "Oxygen"},
        {"question": "Which particle has a negative charge?", "answers": ["Electron", "Proton", "Neutron"], "correct": "Electron"},
        {"question": "What type of energy is stored in food?", "answers": ["Chemical", "Kinetic", "Thermal"], "correct": "Chemical"},
        {"question": "What does a voltmeter measure?", "answers": ["Voltage", "Current", "Resistance"], "correct": "Voltage"},
        {"question": "What happens to particles when a solid melts?", "answers": ["They move more freely", "They stop moving", "They become smaller"], "correct": "They move more freely"},
        {"question": "What is the function of the mitochondria?", "answers": ["Produce energy", "Store DNA", "Control movement"], "correct": "Produce energy"},
        {"question": "What happens to enzymes at high temperatures?", "answers": ["They denature", "They replicate", "They freeze"], "correct": "They denature"},
        {"question": "What is the chemical formula for methane?", "answers": ["CH4", "CO2", "C2H6"], "correct": "CH4"},
        {"question": "What is the main role of white blood cells?", "answers": ["Fight infection", "Carry oxygen", "Digest food"], "correct": "Fight infection"},
        {"question": "Which process causes water to rise in plant stems?", "answers": ["Capillary action", "Evaporation", "Osmosis"], "correct": "Capillary action"},
        {"question": "Which force resists motion between two surfaces?", "answers": ["Friction", "Gravity", "Magnetism"], "correct": "Friction"},
        {"question": "Which part of the eye controls the amount of light entering?", "answers": ["Iris", "Lens", "Retina"], "correct": "Iris"},
        {"question": "What is the role of the pancreas?", "answers": ["Produce insulin", "Store bile", "Filter blood"], "correct": "Produce insulin"},
        {"question": "Which metal is liquid at room temperature?", "answers": ["Mercury", "Aluminum", "Iron"], "correct": "Mercury"},
        {"question": "Which type of energy is stored in a stretched rubber band?", "answers": ["Elastic potential", "Kinetic", "Thermal"], "correct": "Elastic potential"},
        {"question": "What is the name of the green pigment in plants?", "answers": ["Chlorophyll", "Cellulose", "Starch"], "correct": "Chlorophyll"},
        {"question": "Which part of a plant anchors it to the ground?", "answers": ["Roots", "Stems", "Leaves"], "correct": "Roots"},
        {"question": "Which type of electromagnetic wave has the shortest wavelength?", "answers": ["Gamma rays", "Ultraviolet", "Microwaves"], "correct": "Gamma rays"},
        {"question": "What is the function of ribosomes?", "answers": ["Make proteins", "Store energy", "Transport materials"], "correct": "Make proteins"},
        {"question": "What happens to the pressure of a gas if volume decreases?", "answers": ["It increases", "It decreases", "It stays the same"], "correct": "It increases"},
        {"question": "Which structure in a leaf allows gas exchange?", "answers": ["Stomata", "Xylem", "Cuticle"], "correct": "Stomata"},
        {"question": "What is an element?", "answers": ["A substance made of one type of atom", "A mix of metals", "A compound with hydrogen"], "correct": "A substance made of one type of atom"},
        {"question": "What is the function of the large intestine?", "answers": ["Absorb water", "Digest protein", "Store glucose"], "correct": "Absorb water"},
        {"question": "Which method separates a soluble solid from a liquid?", "answers": ["Evaporation", "Filtration", "Chromatography"], "correct": "Evaporation"},
        {"question": "Which blood vessel carries blood away from the heart?", "answers": ["Artery", "Vein", "Capillary"], "correct": "Artery"}
    

    ] * 5,  
    "Geography": [
        {"question": "What is the longest river in the world?", "answers": ["Amazon", "Nile", "Yangtze"], "correct": "Nile"},
        {"question": "Which layer of the Earth is liquid?", "answers": ["Mantle", "Outer Core", "Crust"], "correct": "Outer Core"},
        {"question": "What is a tsunami caused by?", "answers": ["Rainfall", "Tectonic activity", "Wind"], "correct": "Tectonic activity"},
        {"question": "Which is the largest desert on Earth?", "answers": ["Sahara", "Gobi", "Antarctica"], "correct": "Antarctica"},
        {"question": "What type of rock is formed from magma?", "answers": ["Sedimentary", "Igneous", "Metamorphic"], "correct": "Igneous"},
        {"question": "Which scale measures earthquakes?", "answers": ["Richter", "Beaufort", "Mercalli"], "correct": "Richter"},
        {"question": "What is the process by which rocks are broken down?", "answers": ["Erosion", "Weathering", "Deposition"], "correct": "Weathering"},
        {"question": "Which line divides the Earth into Northern and Southern Hemispheres?", "answers": ["Equator", "Prime Meridian", "Tropic of Cancer"], "correct": "Equator"},
        {"question": "What is the capital city of Zimbabwe?", "answers": ["Lusaka", "Harare", "Maputo"], "correct": "Harare"},
        {"question": "What type of farming is done for the farmer’s own use?", "answers": ["Commercial", "Subsistence", "Organic"], "correct": "Subsistence"},
        {"question": "Which continent is the Sahara Desert located in?", "answers": ["Africa", "Asia", "Australia"], "correct": "Africa"},
        {"question": "What is the term for rain that falls due to mountains?", "answers": ["Relief rainfall", "Convectional rainfall", "Frontal rainfall"], "correct": "Relief rainfall"},
        {"question": "What do contour lines on a map show?", "answers": ["Height", "Temperature", "Rainfall"], "correct": "Height"},
        {"question": "Which country has the largest population?", "answers": ["China", "India", "USA"], "correct": "China"},
        {"question": "Which natural hazard involves ground shaking?", "answers": ["Earthquake", "Tornado", "Flood"], "correct": "Earthquake"},
        {"question": "What type of rock is granite?", "answers": ["Igneous", "Sedimentary", "Metamorphic"], "correct": "Igneous"},
        {"question": "What is the process of wearing away rocks?", "answers": ["Erosion", "Condensation", "Evaporation"], "correct": "Erosion"},
        {"question": "Which ocean is west of Africa?", "answers": ["Atlantic", "Pacific", "Indian"], "correct": "Atlantic"},
        {"question": "What is urbanization?", "answers": ["Growth of cities", "Deforestation", "Volcano eruption"], "correct": "Growth of cities"},
        {"question": "Which of these is a non-renewable energy source?", "answers": ["Coal", "Solar", "Wind"], "correct": "Coal"},
        {"question": "What is the biggest waterfall in Africa?", "answers": ["Victoria Falls","Niagara Falls","Tugela Falls"], "correct": "Victoria Falls"},
        {"question": "What is the term for a river's bend, often found in its middle or lower course?", "answers": ["Gorge", "Meander", "Waterfall"], "correct": "Meander"},
        {"question": "Which type of energy source is replenished naturally on a human timescale?", "answers": ["Coal", "Natural gas", "Solar power"], "correct": "Solar power"},
        {"question": "What is the name for the imaginary line that runs through Greenwich, England, marking 0 degrees longitude?", "answers": ["Equator", "Tropic of Cancer", "Prime Meridian"], "correct": "Prime Meridian"},
        {"question": "Which of the following describes a 'pull factor' for migration?", "answers": ["War", "Unemployment", "Better healthcare"], "correct": "Better healthcare"},
        {"question": "What is the process by which fertile land becomes desert, typically as a result of drought, deforestation, or inappropriate agriculture?", "answers": ["Deforestation", "Desertification", "Urbanization"], "correct": "Desertification"},
        {"question": "Which type of rainfall occurs when warm, moist air is forced to rise over mountains?", "answers": ["Convectional rainfall", "Frontal rainfall", "Relief rainfall"], "correct": "Relief rainfall"},
        {"question": "What is the name given to the sudden violent shaking of the ground, caused by the movement of plates within the Earth's crust?", "answers": ["Volcanic eruption", "Tsunami", "Earthquake"], "correct": "Earthquake"},
        {"question": "Which economic sector involves the provision of services, such as healthcare and education?", "answers": ["Primary sector", "Secondary sector", "Tertiary sector"], "correct": "Tertiary sector"},
        {"question": "What is a natural hazard that occurs when a large volume of water suddenly overflows its banks and submerges land?", "answers": ["Drought", "Tornado", "Flood"], "correct": "Flood"},
        {"question": "Which term refers to the increase in the proportion of people living in towns and cities?", "answers": ["Rural depopulation", "Suburbanization", "Urbanization"], "correct": "Urbanization"},
        {"question": "What is the name for the long-term average weather conditions in an area?", "answers": ["Weather", "Climate", "Atmosphere"], "correct": "Climate"},
        {"question": "Which of the following is an example of an extensive farming system?", "answers": ["Market gardening", "Rice paddies", "Ranching"], "correct": "Ranching"},
        {"question": "What is the breaking down of rocks by chemical reactions, such as carbonation or oxidation?", "answers": ["Freeze-thaw weathering", "Chemical weathering", "Exfoliation"], "correct": "Chemical weathering"},
        {"question": "What is the term for a map that shows physical features like mountains, rivers, and elevation?", "answers": ["Political map", "Thematic map", "Topographic map"], "correct": "Topographic map"},
        {"question": "Which major global wind belt is found between 30 and 60 degrees latitude?", "answers": ["Trade winds", "Westerlies", "Polar easterlies"], "correct": "Westerlies"}

    ] * 5  
}

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
FPSCLOCK = pygame.time.Clock()
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

SCORES_FILE = 'scores.json'                
LEADERBOARD_FILE = "leaderboard.json"

def scale_x(x):
    return int(x * SCREEN_WIDTH / BASE_WIDTH)

def scale_y(y):
    return int(y * SCREEN_HEIGHT / BASE_HEIGHT)

def loadScores():
    if not os.path.exists(SCORES_FILE):
        data = {
            "high_score": 0,
            "previous_score": 0,
            "leaderboard": []
        }
        with open(SCORES_FILE, 'w') as f:
            json.dump(data, f)
        return data
    with open(SCORES_FILE, 'r') as f:
        return json.load(f)

def saveScores(data):
    with open(SCORES_FILE, 'w') as f:
        json.dump(data, f)

def updateScores(new_score):
    # Loading existing data or start fresh
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as file:
            scores = json.load(file)
    else:
        scores = {"high_score": 0, "previous_score": 0}

    scores["previous_score"] = new_score

    if new_score > scores.get("high_score", 0):
        scores["high_score"] = new_score

    # Saving the updated data
    saveScores(scores)

def showMenuScreen():
    scores_data = loadScores()

    # Load custom fonts
    try:
        title_font = pygame.font.Font('Steelar.otf', 45)
        label_font = pygame.font.Font('OMNIBLACK_demo.otf', 35)
        small_font = pygame.font.Font('Simple Subject.otf', 35)
    except:
        print("Falling back to default font.")
        title_font = pygame.font.Font(None, 72)
        label_font = pygame.font.Font(None, 1)
        small_font = pygame.font.Font(None, 28)

    # Load background
    try:
        background = pygame.image.load('aurora.jpg')
        background = pygame.transform.scale(background, (WINDOWWIDTH, WINDOWHEIGHT))
    except:
        background = None

    # Load and play music
    try:
        pygame.mixer.music.load('Simulacra.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except:
        print("Menu music not found or failed to load.")

    # Create text surfaces
    title_surf = title_font.render("SERPENT OF KNOWLEDGE ", True, (0, 255, 0))
    subject_prompt = label_font.render("Press 1 for SCIENCE", True, (200, 0, 0))
    subject_prompt2 = label_font.render("Press 2 for GEOGRAPHY", True, (200, 0, 0))
    high_score_surf = small_font.render(f"High Score: {scores_data['high_score']}", True, (255, 255, 0))
    prev_score_surf = small_font.render(f"Previous Score: {scores_data['previous_score']}", True, (255, 255, 255))

    # Updated logic: Level increases every 10 points
    estimated_level = scores_data['previous_score'] // 10 + 1
    level_surf = small_font.render(f"Level Reached: {estimated_level}", True, (255, 255, 255))

    # Rewards/Upgrades display
    rewards_title = label_font.render("LEVEL REWARDS", True, (255, 180, 180))
    reward1 = small_font.render("Level 2: Neon Snake", True, (255, 255, 255))
    reward2 = small_font.render("Level 3: Shadow Serpent", True, (255, 255, 255))
    reward3 = small_font.render("Level 5: Cosmic Dragon", True, (255, 255, 255))
    reward4 = small_font.render("Level 5: GOLDEN PYTHON", True, (255, 255, 255))

    while True:
        # Background
        if background:
            DISPLAYSURF.blit(background, (0, 0))
        else:
            DISPLAYSURF.fill((10, 10, 10)) # fallback color

        # Title
        title_rect = title_surf.get_rect(center=(WINDOWWIDTH // 2, 150))
        pygame.draw.rect(DISPLAYSURF, (50, 50, 100), title_rect, border_radius=15)
        DISPLAYSURF.blit(title_surf, title_rect)

        # Stats
        pygame.draw.rect(DISPLAYSURF, BLUE, (200, 400, 500, 300), border_radius=15)
        DISPLAYSURF.blit(high_score_surf, (250, 450))
        DISPLAYSURF.blit(prev_score_surf, (250, 550))
        DISPLAYSURF.blit(level_surf, (250, 650))

        # Prompt
        pygame.draw.rect(DISPLAYSURF, PURPLE, pygame.Rect(192, 899, 556, 339), border_radius=5)
        prompt_rect = subject_prompt.get_rect(center=(415, WINDOWHEIGHT - 160))
        prompt_rect2 = subject_prompt2.get_rect(center=(450, WINDOWHEIGHT - 125))
        DISPLAYSURF.blit(subject_prompt, prompt_rect)
        DISPLAYSURF.blit(subject_prompt2, prompt_rect2)
        # Rewards panel
        pygame.draw.rect(DISPLAYSURF, BLUE, (1230, 400, 500, 300), border_radius=15)
        DISPLAYSURF.blit(rewards_title, (WINDOWWIDTH - 650, 420))
        DISPLAYSURF.blit(reward1, (WINDOWWIDTH - 550, 470))
        DISPLAYSURF.blit(reward2, (WINDOWWIDTH - 550, 510))
        DISPLAYSURF.blit(reward3, (WINDOWWIDTH - 550, 550))
        DISPLAYSURF.blit(reward4, (WINDOWWIDTH - 550, 600))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pygame.mixer.music.stop()
                    return "Science"
                elif event.key == pygame.K_2:
                    pygame.mixer.music.stop()
                    return "Geography"



def terminate():
    pygame.quit()
    sys.exit()

def getRandomQuestion(topic):
    topic_key = topic.capitalize()  
    
    # Get the question list or empty list if topic not found
    questions = question_bank.get(topic_key, [])
    
    if not questions:
        raise ValueError(f"No questions found for topic '{topic_key}'")
    
    q = random.choice(questions)
    
    # Defensive check - 'correct' must be in 'answers' list
    if q["correct"] not in q["answers"]:
        raise ValueError(f"Correct answer '{q['correct']}' not in answers list for question: {q['question']}")
    
    correct_index = q["answers"].index(q["correct"])
    return q["question"], q["answers"], correct_index


def getRandomApples(answer_list, correct_index):
    apples = []
    labels = ['A', 'B', 'C']
    for i, ans in enumerate(answer_list):
        while True:
            x = random.randint(0, GRID_COLS - 1)
            y = random.randint(0, GRID_ROWS - 1)
            if all(a['x'] != x or a['y'] != y for a in apples):
                apples.append({
                    'x': x, 'y': y,
                    'label': labels[i],
                    'value': ans,
                    'is_correct': i == correct_index
                })
                break
    return apples

def showTopicSelectionScreen():
    title_font = pygame.font.Font('freesansbold.ttf', 60)
    option_font = pygame.font.Font('freesansbold.ttf', 36)
    prompt_font = pygame.font.Font('freesansbold.ttf', 28)

    title_surf = title_font.render("Select a Quiz Topic", True, (100, 200, 255))  # soft blue
    option1_surf = option_font.render("1 - Science", True, (255, 255, 255))        # white
    option2_surf = option_font.render("2 - Geography", True, (255, 255, 255))      # white
    prompt_surf = prompt_font.render("Press 1 or 2 to choose", True, (200, 200, 200))  # light gray

    while True:
        DISPLAYSURF.fill((0, 0, 20))  # dark blue-black background

        # Center and draw texts vertically spaced
        DISPLAYSURF.blit(title_surf, title_surf.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 3)))
        DISPLAYSURF.blit(option1_surf, option1_surf.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2)))
        DISPLAYSURF.blit(option2_surf, option2_surf.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 50)))
        DISPLAYSURF.blit(prompt_surf, prompt_surf.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 120)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "science"
                elif event.key == pygame.K_2:
                    return "geography"
        
def fadeOut(duration=1000):
    """Fade out the screen to black over `duration` milliseconds."""
    fade_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    fade_surface.fill((0, 0, 0))
    clock = pygame.time.Clock()

    alpha = 0
    fade_speed = 255 / (duration / 30)  # increment alpha per frame (assuming ~30 FPS)

    while alpha < 255:
        fade_surface.set_alpha(int(alpha))
        DISPLAYSURF.blit(fade_surface, (0, 0))
        pygame.display.update()
        alpha += fade_speed
        clock.tick(30)


def showStartScreen():
    try:
        title_font = pygame.font.Font('Steelar.otf', 70)
        prompt_font = pygame.font.Font('Summerfavourite.ttf', 36)
    except:
        title_font = pygame.font.Font(None, 72)
        prompt_font = pygame.font.Font(None, 36)

    # Load background
    try:
        background = pygame.image.load('welcomebg.jpg')
        background = pygame.transform.scale(background, (WINDOWWIDTH, WINDOWHEIGHT))
    except:
        background = None

    # Load and scale small logo/image
    try:
        logo = pygame.image.load('logo.png')
        logo = pygame.transform.scale(logo, (250, 155))
        logo_rect = logo.get_rect(center=(WINDOWWIDTH // 2, 350))
    except:
        logo = None

    # Load and play music
    try:
        pygame.mixer.music.load('rescue_me.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except:
        print("Music file not found or failed to load.")

    title_surf = title_font.render("SERPANT OF KNOWLEDGE", True, ( 0, 0, 255))
    prompt_surf = prompt_font.render("Press ENTER to continue", True, (180, 0, 0))

    while True:
        if background:
            DISPLAYSURF.blit(background, (0, 0))
        else:
            DISPLAYSURF.fill((0, 0, 0))

        if logo:
            DISPLAYSURF.blit(logo, logo_rect)

        DISPLAYSURF.blit(title_surf, title_surf.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 50)))
        DISPLAYSURF.blit(prompt_surf, prompt_surf.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 50)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.mixer.music.stop()  # Stop music on transition
                return

def drawGrid():
    for x in range(0, GRID_WIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (GRID_X + x, GRID_Y), (GRID_X + x, GRID_Y + GRID_HEIGHT))
    for y in range(0, GRID_HEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (GRID_X, GRID_Y + y), (GRID_X + GRID_WIDTH, GRID_Y + y))
    pygame.draw.rect(DISPLAYSURF, (255, 255, 0), pygame.Rect(GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT), 3)

def draw_text_wrapped(surface, text, x, y, font, color, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    for i, line in enumerate(lines):
        line_surf = font.render(line.strip(), True, color)
        surface.blit(line_surf, (x, y + i * font.get_linesize()))


def showGameOverScreen(final_score=0, final_level=1):
    DISPLAYSURF.fill(BLACK)

    # Fonts
    bigFont = pygame.font.Font('freesansbold.ttf', 120)
    medFont = pygame.font.Font('freesansbold.ttf', 48)
    smallFont = pygame.font.Font('freesansbold.ttf', 32)

    # Text surfaces
    gameOverText = bigFont.render("GAME OVER", True, RED)
    scoreText = medFont.render(f"Final Score: {final_score}", True, WHITE)
    levelText = medFont.render(f"Level Reached: {final_level}", True, WHITE)
    promptText = smallFont.render("Press any key to return to main menu", True, LIGHTGRAY)

    # Center positions
    gameOverRect = gameOverText.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 100))
    scoreRect = scoreText.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
    levelRect = levelText.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 60))
    promptRect = promptText.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 150))

    # Draw all elements
    DISPLAYSURF.blit(gameOverText, gameOverRect)
    DISPLAYSURF.blit(scoreText, scoreRect)
    DISPLAYSURF.blit(levelText, levelRect)
    DISPLAYSURF.blit(promptText, promptRect)

    pygame.display.update()

    updateScores(final_score)  # Update scores after game over

    # Wait for 1 second while processing events (non-blocking)
    wait_start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - wait_start < 1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        FPSCLOCK.tick(30)  # keep it responsive

    # Now wait for a key press to return to main menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                waiting = False  # exit loop and return

        FPSCLOCK.tick(30)


def draw_vertical_gradient(surface, rect, top_color, bottom_color):
    """Draw a vertical gradient inside rect on the given surface.
    
    Args:
        surface (pygame.Surface): Surface to draw on.
        rect (tuple): (x, y, width, height) of the rectangle area.
        top_color (tuple): RGB color at the top of the gradient.
        bottom_color (tuple): RGB color at the bottom of the gradient.
    """
    x, y, width, height = rect
    for i in range(height):
        # Calculate interpolation factor (0 at top, 1 at bottom)
        ratio = i / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + width, y + i))


def drawWorm(worm):
    for coord in worm:
        x = coord['x'] * CELLSIZE + GRID_X
        y = coord['y'] * CELLSIZE + GRID_Y
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, (x, y, CELLSIZE, CELLSIZE))
        pygame.draw.rect(DISPLAYSURF, GREEN, (x+4, y+4, CELLSIZE-8, CELLSIZE-8))

def drawAnswersUI(answers):
    panel_x = GRID_X - 450
    panel_y = GRID_Y + 100
    panel_width = 450
    panel_height = 280
    padding = 20
    spacing = 80  # vertical space between answers
    font_size = 25
    
    # font 
    font = pygame.font.Font('NeoSpeed.otf', font_size)

    # Drawing vertical gradient background for answer panel
    draw_vertical_gradient(DISPLAYSURF, (panel_x, panel_y, panel_width, panel_height), (0, 102, 204), (153, 0, 204))
    
    # Get mouse position for hover detection
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Draw each answer with hover effect
    for i, label in enumerate(['A', 'B', 'C']):
        text = f"{label}: {answers[i]}"
        
        # Calculate position for this answer
        text_x = panel_x + padding
        text_y = panel_y + padding + i * spacing
        
        # Creating rect for hover detection and highlight
        rect = pygame.Rect(text_x, text_y, panel_width - 2 * padding, font_size + 10)
        
        # Checking hover
        if rect.collidepoint(mouse_x, mouse_y):
            # Highlight background with semi-transparent white overlay
            highlight_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            highlight_surf.fill((255, 255, 255, 100))  # white, alpha 100
            DISPLAYSURF.blit(highlight_surf, (rect.x, rect.y))
            text_color = (255, 215, 0)  # gold/yellow
        else:
            text_color = WHITE
        
        # Render text
        text_surface = font.render(text, True, text_color)
        DISPLAYSURF.blit(text_surface, (text_x, text_y))



def drawApple(apple):
    x = GRID_X + apple['x'] * CELLSIZE
    y = GRID_Y + apple['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

    # Draw the letter (A/B/C)
    font = pygame.font.Font(None, 24)
    text_surface = font.render(apple['value'], True, WHITE)
    text_rect = text_surface.get_rect(center=(x + CELLSIZE // 2, y + CELLSIZE // 2))
    DISPLAYSURF.blit(text_surface, text_rect)

def drawScore(score, previous_score, glow_timer, max_score=20):
    # Panel position (to the left of the grid)
    panel_x = 200
    panel_y =  250# Adjusted vertically to align horizontally
    bar_width = 300
    bar_height = 30

    # Fonts
    label_font = pygame.font.Font(None, 32)
    value_font = pygame.font.Font(None, 28)

    # Draw label above the bar
    label_surface = label_font.render("Score :", True, WHITE)
    DISPLAYSURF.blit(label_surface, (200, GRID_Y --1))

    # Calculate fill amount
    fill_width = int((score / max_score) * bar_width)
    fill_width = max(0, min(fill_width, bar_width))  # Clamp to 0–bar_width

    # ✨ Glow effect
    if glow_timer > 0 and score > previous_score:
        glow_alpha = int(255 * (glow_timer / 20))  # Fade over time

        # Create a glowing green surface
        glow_surf = pygame.Surface((bar_width + 20, bar_height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (0, 255, 0, glow_alpha), glow_surf.get_rect(), border_radius=12)
        DISPLAYSURF.blit(glow_surf, (panel_x - 10, panel_y - 10))

    # Draw background bar
    pygame.draw.rect(DISPLAYSURF, DARKGRAY, (panel_x, panel_y, bar_width, bar_height), border_radius=10)

    # Draw filled part
    pygame.draw.rect(DISPLAYSURF, GREEN, (panel_x, panel_y, fill_width, bar_height), border_radius=10)

    # Draw numeric score centered above bar
    score_text = value_font.render(str(score), True, WHITE)
    text_rect = score_text.get_rect(center=(290, GRID_Y - -12))
    DISPLAYSURF.blit(score_text, text_rect)

    return glow_timer - 1 if glow_timer > 0 else 0



def drawUI(score, level, question, answers):
    ANSWER_PANEL_WIDTH = 250
    ANSWER_PANEL_X = GRID_X - ANSWER_PANEL_WIDTH - 10  # 10 px gap from grid
    font = pygame.font.SysFont(None, 36)

    # Draw level text
    level_surf = font.render(f"Level: {level}", True, (255, 255, 255))
    DISPLAYSURF.blit(level_surf, (200, GRID_Y - 60))

    # Determine color based on level
    if level <= 2:
        level_color = RED
    elif level <= 5:
        level_color = ORANGE
    else:
        level_color = GREEN

    # Level slider now positioned ABOVE the grid
    slider_width = 400
    slider_height = 20
    slider_x = 200
    slider_y = GRID_Y - 30  # Move it above the grid

    # Outline
    pygame.draw.rect(DISPLAYSURF, GREEN, (slider_x, slider_y, slider_width, slider_height), 2,10)

    # Fill bar based on level
    max_level = 10
    fill_width = int((level / max_level) * (slider_width - 4))
    pygame.draw.rect(DISPLAYSURF, level_color, (slider_x + 2, slider_y + 2, fill_width, slider_height - 4),0,10)

    # Add "Pause by pressing P"
    pause_font = pygame.font.SysFont(   'SimpleSubject.otf', 24)
    pause_text = pause_font.render("Pause by pressing P", True, RED)
    pause_rect = pause_text.get_rect(midtop=(300, 120))
    DISPLAYSURF.blit(pause_text, pause_rect)



def drawAnswerPanelBackground():
    ANSWER_PANEL_WIDTH = 250
    ANSWER_PANEL_X = GRID_X - ANSWER_PANEL_WIDTH - 10
    panel_rect = pygame.Rect(ANSWER_PANEL_X - 10, GRID_Y - 10, ANSWER_PANEL_WIDTH + 20, GRID_HEIGHT + 20)
    pygame.draw.rect(DISPLAYSURF, (30, 30, 30), panel_rect)
    pygame.draw.rect(DISPLAYSURF, (200, 200, 200), panel_rect, 2,15 )  # border


def drawQuestionAboveGrid(question):
    font = pygame.font.Font('Wake Snake.Otf', 28)
    color = (0, 255, 255)  # bright cyan

    question_surf = font.render("QUESTION-, " + question, True, color)
    text_rect = question_surf.get_rect()
    text_rect.midbottom = (GRID_X + GRID_WIDTH // 2, GRID_Y - 10)  # 10 px above grid

    DISPLAYSURF.blit(question_surf, text_rect)

def drawAnswers(answers):
    ANSWER_PANEL_WIDTH = 250
    ANSWER_PANEL_X = GRID_X - ANSWER_PANEL_WIDTH - 10  # 10 px gap from grid
    font = BASICFONT
    y_start = GRID_Y  # align top with grid
    for i, ans in enumerate(answers):
        label = chr(ord('A') + i)
        text = f"{label}: {ans}"
        surf = font.render(text, True, WHITE)
        DISPLAYSURF.blit(surf, (ANSWER_PANEL_X, y_start + i * 30))

def getApplesFromAnswers(answers, correct_index):
    apple_positions = []
    labels = ['A', 'B', 'C']

    while len(apple_positions) < 3:
        pos = {
            'x': random.randint(0, GRID_COLS - 1),
            'y': random.randint(0, GRID_ROWS - 1)
        }
        if pos not in apple_positions:
            apple_positions.append(pos)

    apples = []
    for i in range(3):
        apples.append({
            'x': apple_positions[i]['x'],
            'y': apple_positions[i]['y'],
            'value': labels[i],
            'answer': answers[i],
            'is_correct': (i == correct_index)
        })
    return apples


def runGame(topic):
    global GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT
    global current_song_index

    score = 10
    glow_timer = 0
    previous_score = 0

    # Music playlist
    playlist = [
        "gameplay1.mp3",
        "gameplay2.mp3",
        "gameplay3.mp3",
        "gameplay4.mp3",
        "gameplay5.mp3"
    ]
    current_song_index = 0

    # Set music end event
    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

    try:
        pygame.mixer.music.load(playlist[current_song_index])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
    except:
        print("Failed to load first music track.")

    startx = random.randint(3, GRID_COLS - 4)
    starty = random.randint(3, GRID_ROWS - 4)
    worm = [{'x': startx, 'y': starty}, {'x': startx - 1, 'y': starty}, {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    question, answers, correct_index = getRandomQuestion(topic)
    apples = getApplesFromAnswers(answers, correct_index)

    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                terminate()
            elif event.type == pygame.USEREVENT + 1:
                current_song_index = (current_song_index + 1) % len(playlist)
                try:
                    pygame.mixer.music.load(playlist[current_song_index])
                    pygame.mixer.music.play()
                except:
                    print("Failed to load next track.")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_LEFT and direction != RIGHT:
                        direction = LEFT
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        direction = RIGHT
                    elif event.key == pygame.K_UP and direction != DOWN:
                        direction = UP
                    elif event.key == pygame.K_DOWN and direction != UP:
                        direction = DOWN

        if paused:
            DISPLAYSURF.fill((30, 30, 30))
            drawGrid()
            drawWorm(worm)
            for apple in apples:
                drawApple(apple)
            drawQuestionAboveGrid(question)
            drawAnswersUI(answers)
            drawScore(score, previous_score, glow_timer)
            drawUI(score, len(worm) // 4 + 1, question, answers)

            pause_font = pygame.font.Font('OMNIBLACK_outline_demo.otf', 72)
            pause_surf = pause_font.render("PAUSED", True, (255, 255, 255))
            pause_rect = pause_surf.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
            DISPLAYSURF.blit(pause_surf, pause_rect)

            pygame.display.update()
            FPSCLOCK.tick(5)
            continue

        head = worm[0]
        newHead = {'x': head['x'], 'y': head['y']}

        if direction == UP:
            newHead['y'] -= 1
        elif direction == DOWN:
            newHead['y'] += 1
        elif direction == LEFT:
            newHead['x'] -= 1
        elif direction == RIGHT:
            newHead['x'] += 1

        worm.insert(0, newHead)

        if (newHead['x'] < 0 or newHead['x'] >= GRID_COLS or
            newHead['y'] < 0 or newHead['y'] >= GRID_ROWS):
            game_over_sound.play()
            showGameOverScreen(final_score=score, final_level=len(worm) // 4 + 1)
            return

        if newHead in worm[1:]:
            game_over_sound.play()
            showGameOverScreen(final_score=score, final_level=len(worm) // 4 + 1)
            return

        ate_apple = False
        for apple in apples:
            if newHead['x'] == apple['x'] and newHead['y'] == apple['y']:
                ate_apple = True
                if apple['is_correct']:
                    score += 1
                    correct_sound.play()
                else:
                    score -= 1
                    wrong_sound.play()
                    if score <= 0:
                        game_over_sound.play()
                        showGameOverScreen(final_score=score, final_level=len(worm) // 4 + 1)
                        return
                question, answers, correct_index = getRandomQuestion(topic)
                apples = getApplesFromAnswers(answers, correct_index)
                break

        if not ate_apple:
            worm.pop()

        DISPLAYSURF.fill(BLACK)
        drawGrid()
        drawWorm(worm)
        for apple in apples:
            drawApple(apple)
        drawQuestionAboveGrid(question)
        drawAnswersUI(answers)
        glow_timer = drawScore(score, previous_score, glow_timer)
        drawUI(score, len(worm) // 4 + 1, question, answers)

        pygame.display.update()
        FPSCLOCK.tick(FPS + len(worm) // 5)

        if score <= 0:
            game_over_sound.play()
            showGameOverScreen(final_score=score, final_level=len(worm) // 4 + 1)
            return

def main():
    pygame.init()
    global DISPLAYSURF, BASICFONT, FPSCLOCK
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Serpent of Knowledge')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    FPSCLOCK = pygame.time.Clock()

    showStartScreen()  

    while True:
        topic = showMenuScreen()  
        runGame(topic)            

if __name__ == '__main__':
    main()