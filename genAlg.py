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
    #currscoretext = SCORE_FONT.render("Current best score: "+str(population.snakes[population.currentBestSnake].score), 1, WHITE)
    genbestscore = GEN_FONT.render("Current minimal value: "+str(best.fitness), 1, WHITE)
    matched = GEN_FONT.render("Number of matched riders: "+str(len(best.riders) - len(best.unmatched)), 1, WHITE)
    #globalscoretext = SCORE_FONT.render("All time best score: "+str(global_best_score), 1, WHITE)
    pygame.draw.rect(win, WHITE, (0,0, GAME_WIDTH, GAME_HEIGHT), 2)
    win.blit(gentext, (5,GAME_WIDTH+50))
    win.blit(genbestscore, (5, GAME_WIDTH+150))
    win.blit(matched, (5, GAME_WIDTH+100))
    pygame.display.update()


def genAlg(riderData, driverData, distMatrix, timeMatrix, vals, coords):
    population = Population(riderData, driverData, distMatrix, timeMatrix, vals)
    #print("imamo populaciju")
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
    while numOfIt < vals[9]: # or while |oldFunc-newFunc| > EPSILON
        #print(numOfIt)
        print(numOfIt)
        newRoutes = []
        #print("best value prije eval " + str(population.bestValue))
        population.evaluate(vals[0:4])
        #print("evaluated")
        #print("best value nakon eval " + str(population.bestValue))
        best1, best2 = population.findBestSolutions2()
        #print("sol found")
        #print("best value nakon findBestSol " + str(population.bestValue))
        valueOfFunc.append(population.bestValue)
        bestSolutions.append(best1)
        numOfMatched.append(len(riderData)-len(best1.unmatched))
        distance.append(best1.distance)
        time.append(best1.time)
        riderTime.append(best1.riderTime)
        newRoutes.append(best1)
        newRoutes.append(best2)
        worst = population.findWorstSolution()
       
        i = 0
        while len(newRoutes) < vals[8]:   
            #print("pokusaj broj " + str(i))
            parent1 = population.selection()
            #parent1 = population.rouletteWheelSelection()
            parent2 = population.selection()
            #parent2 = population.rouletteWheelSelection()
            child1, child2 = parent1.crossover(parent2, vals[10])
            #child = parent1.crossover2(parent2)
            #child.mutate()
            #newRoutes.append(child)
            child1.mutate(vals[10])
            #f1 = child1.returnFitness(vals[0:4])
            child2.mutate(vals[10])
            #f2 = child2.returnFitness(vals[0:4])
            #if f1 < worst and len(newRoutes) < vals[8] and i < vals[8]*3/4: newRoutes.append(child1)
            #elif i>= vals[8]*3/4: newRoutes.append(child1)
            #if f2 < worst and len(newRoutes) < vals[8] and i < vals[8]*3/4: newRoutes.append(child2)
            #elif i>= vals[8]*3/4: newRoutes.append(child2)
            draw_window(win, numOfIt+1, best1, coords, toShow)
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: #speed up the game
                        FPS+=5
                    if event.key == pygame.K_DOWN and FPS>=10: #slow down the game
                        FPS-=5
                    if event.key == pygame.K_SPACE: #show all snakes/only the best snake
                        toShow = not toShow
            i+=1
            newRoutes.append(child1)
            newRoutes.append(child2)
        population.solutions = newRoutes
        #for i in range(2, len(population.solutions)): population.solutions[i].insertUnmatched()
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
    #quit()
    return valueOfFunc, bestSolutions, numOfMatched, distance, time, riderTime
        
