import pygame, sys, random, asyncio

def drawFloor():
    screen.blit(floorSurface,(floorX, 670))
    screen.blit(floorSurface,(floorX+576, 670))

def createPipe():
    randomPipePos = random.choice(pipeHeight)
    bottomPipe = pipeSurface.get_rect(midtop = (600,randomPipePos))
    topPipe = pipeSurface.get_rect(midbottom = (600,randomPipePos - 300))
    return bottomPipe,topPipe

def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 750:
            screen.blit(pipeSurface, pipe)
        else:
            flipPipe = pygame.transform.flip(pipeSurface,False,True)
            screen.blit(flipPipe, pipe)

def checkCollisions(pipes):
    for pipe in pipes:
        if birdRect.colliderect(pipe):
            deathSound.play()
            return False
    if birdRect.top <= -100 or birdRect.bottom >= 670:
        return False
    return True

def rotateBird(bird):
    newBird = pygame.transform.rotozoom(bird,-birdMovement*2,1)
    return newBird

def birdAnimation():
    newBird = birdFrames[birdIndex]
    newBirdRect = newBird.get_rect(center = (100,birdRect.centery))
    return newBird,newBirdRect 

def scoreDisplay(gameState):
    if gameState == 'mainGame':
        scoreSurface = gameFont.render(str(int(score)), True, (255,255,255))
        scoreRect = scoreSurface.get_rect(center = (288,50))
        screen.blit(scoreSurface, scoreRect)
    if gameState == 'gameOver':
        scoreSurface = gameFont.render(f'Score: {int(score)}', True, (129, 255, 157))
        scoreRect = scoreSurface.get_rect(center = (288,50))
        screen.blit(scoreSurface, scoreRect)
    
        highScoreSurface = largeGameFont.render(f'High Score: {int(highScore)}', True, (129, 255, 157))
        highScoreRect = highScoreSurface.get_rect(center = (288,250))
        screen.blit(highScoreSurface, highScoreRect)

    # Brand Name
    brandSurface = smallGameFont.render(("Credits : Kuchinpotta"), True, (145,0,200))
    brandRect = brandSurface.get_rect(center = (288,15))
    screen.blit(brandSurface, brandRect)

def updateScore(score, highScore):
    if score > highScore:
        highScore = score
    return highScore

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576,750))
clock = pygame.time.Clock()
gameFont = pygame.font.Font('04b_19.ttf',40)
largeGameFont = pygame.font.Font('04b_19.ttf',60)
smallGameFont = pygame.font.Font('04b_19.ttf',20)

# Game Variables
gravity = 0.20
birdMovement = 0
gameActive = True
score = 0
highScore = 0

bgSurface = pygame.image.load('assets/background-day.png').convert()
bgSurface = pygame.transform.scale(bgSurface,(576, 750))

floorSurface = pygame.image.load('assets/base.png').convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floorX = 0

birdDownflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
birdMidflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
birdUpflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
birdFrames = [birdDownflap,birdMidflap,birdUpflap]
birdIndex = 0
birdSurface = birdFrames[birdIndex]
birdRect = birdSurface.get_rect(center = (100, 270))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipeSurface = pygame.image.load('assets/pipe-green.png').convert()
pipeSurface = pygame.transform.scale2x(pipeSurface)
pipeList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipeHeight = [450,500,600]

gameOverSurface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
gameOverRect = gameOverSurface.get_rect(center = (288,375))

flapSound = pygame.mixer.Sound('sound/sfx_wing.wav')
deathSound = pygame.mixer.Sound('sound/sfx_hit.wav')
scoreScound = pygame.mixer.Sound('sound/sfx_point.wav')
scoreSoundCountdown = 100

async def main():
    global birdMovement, gameActive, score, highScore, birdIndex, birdSurface, birdRect, pipeList, floorX, scoreSoundCountdown
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and gameActive:
                    birdMovement = 0
                    birdMovement -= 8
                    flapSound.play()
                if event.key == pygame.K_SPACE and gameActive == False:
                    gameActive = True
                    pipeList.clear()
                    birdRect.center = (100,270)
                    birdMovement = 0 
                    score = 0
                    
            if event.type == SPAWNPIPE:
                pipeList.extend(createPipe()) 
                # print(pipeList)

            if event.type == BIRDFLAP:
                if birdIndex < 2:    
                    birdIndex += 1
                else:
                    birdIndex = 0
                
                birdSurface, birdRect = birdAnimation()
        
        screen.blit(bgSurface, (0,0))

        
        if gameActive:
            # Bird
            birdMovement += gravity
            rotatedBird = rotateBird(birdSurface)
            birdRect.centery += birdMovement
            screen.blit(rotatedBird, birdRect)
            gameActive = checkCollisions(pipeList)

            # Pipes
            pipeList = movePipes(pipeList)
            drawPipes(pipeList)
            score += 0.01 
            scoreDisplay('mainGame')
            if scoreSoundCountdown <= 0:
                scoreScound.play()
                scoreSoundCountdown = 100
        else:
            screen.blit(gameOverSurface, gameOverRect)
            highScore = updateScore(score, highScore)
            scoreDisplay('gameOver')

        floorX -= 1
        drawFloor()
        if floorX <= -576:
            floorX = 0

        pygame.display.update()
        clock.tick(120)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())