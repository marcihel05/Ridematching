import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
from population import *
from solution import *
from settings import *

pygame.font.init()
SCORE_FONT = pygame.font.SysFont("monospace", 25)
GEN_FONT = SCORE_FONT

def draw_window(win,num_of_gen, best, coords, toShow):
    win.fill(BLACK)
    best.draw(win, (0,0), GAME_HEIGHT, GAME_WIDTH, coords, toShow)
    gentext = GEN_FONT.render("Generation: "+ str(num_of_gen), 1, WHITE)
    genbestscore = GEN_FONT.render("Current minimal value: "+str(best.fitness), 1, WHITE)
    matched = GEN_FONT.render("Number of matched riders: "+str(len(best.riders) - len(best.unmatched)), 1, WHITE)
    pygame.draw.rect(win, WHITE, (0,0, GAME_WIDTH, GAME_HEIGHT), 2)
    win.blit(gentext, (5,GAME_WIDTH+50))
    win.blit(genbestscore, (5, GAME_WIDTH+150))
    win.blit(matched, (5, GAME_WIDTH+100))
    pygame.display.update()


def genAlg(riderData, driverData, distMatrix, timeMatrix, vals, coords):
    population = Population(riderData, driverData, distMatrix, timeMatrix, vals)
    numOfIt = 0
    valueOfFunc = [] #lista vrijednosti funkcije po iteracijama
    bestSolutions = []
    numOfMatched = []
    distance = []
    time = []
    riderTime = []
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Ridesharing')
    clock = pygame.time.Clock()
    FPS = 150 #frames per second
    toShow = False
    while numOfIt < vals[9]:
        print("Generation number " + str(numOfIt+1))
        newRoutes = []
        population.evaluate(vals[0:4])
        best1, best2 = population.findBestSolutions2()
        valueOfFunc.append(population.bestValue)
        bestSolutions.append(best1)
        numOfMatched.append(len(riderData)-len(best1.unmatched))
        distance.append(best1.distance)
        time.append(best1.time)
        riderTime.append(best1.riderTime)
        newRoutes.append(best1)
        newRoutes.append(best2)
        while len(newRoutes) < vals[8]:   
            parent1 = population.selection()
            parent2 = population.selection()
            child1, child2 = parent1.crossover(parent2, vals[10])
            child1.mutate(vals[10])
            child2.mutate(vals[10])
            draw_window(win, numOfIt+1, best1, coords, toShow)
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #show all routes/some routes
                        toShow = not toShow
            newRoutes.append(child1)
            newRoutes.append(child2)
        population.solutions = newRoutes
        numOfIt+=1
    population.evaluate(vals[0:4])
    best1, best2 = population.findBestSolutions2()
    bestSolutions.append(best1)
    numOfMatched.append(len(riderData)-len(best1.unmatched))
    distance.append(best1.distance)
    time.append(best1.time)
    riderTime.append(best1.riderTime)
    valueOfFunc.append(population.bestValue)
    pygame.quit()
    return valueOfFunc, bestSolutions, numOfMatched, distance, time, riderTime
        
