import random
import copy
import time as t
import string
from tkinter import *
start = t.time()
high_value = []
high_fitness = 0
value = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
fixed = [[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False]]
values = []
random.seed(a=None)
#Genetic algorithm for sudoku.
#Get mutation rate. Score the population of the sudoku problem. Pick high fitnesses.
def genetic(popul,selection,mutation,max_gen):
    global values
    global value
    fitness_values = []
    gen = 0

    top = Tk()
    top.title("Sudoku_Backtracking")                # 제목
    top.resizable(True, True)        # 크기 고정
    top.configure(background='white') #배경색
    top.geometry("180x600")
    problem = Label(top, text = getMat(value))
    problemlb = Label(top, text = "초기 입력 문제")
    solving = Label(top, text = getMat(value))
    solvinglb = Label(top, text = "풀이")
    high = Label(top, text = getMat(value))
    highlb = Label(top, text = "최고 적합도")
    highsclb = Label(top, text = high_fitness)
    genlb = Label(top, text = ("세대수",(gen+1)))
    fitlb = Label(top, text = ("세대수",(gen+1)))
    problemlb.pack()
    problem.pack()
    

    #First Generation
    for i in range(popul):
        fitness_values.append(copy.deepcopy(0))
        values.append(copy.deepcopy(put_element(copy.deepcopy(value))))
    for i in range(popul):
        fitness_values[i] = copy.deepcopy(get_fitness(copy.deepcopy(values[i])))
    for i in values:
        print_value(i)
    #After first generation. Loop
    while(gen != max_gen):
        for i in range(popul):
            fitness_values[i] = copy.deepcopy(get_fitness(copy.deepcopy(values[i])))
        #print
        #select
        select(copy.deepcopy(selection),popul,fitness_values)
        
        #TKinter
        solvinglb.destroy()
        solving.destroy()
        highlb.destroy()
        highsclb.destroy()
        high.destroy()
        genlb.destroy()
        fitlb.destroy()

        fitlb = Label(top, text = ("적합도",fitness_values[0]))
        genlb = Label(top, text = ("세대수",(gen+1)))
        solvinglb = Label(top, text = "문제 풀이")
        solving = Label(top, text = getMat(values[0]))
        highlb = Label(top, text = "최대 적합도")
        highsclb = Label(top, text = high_fitness)
        high = Label(top, text = getMat(high_value))

        highlb.pack()
        highsclb.pack()
        high.pack()
        genlb.pack()
        highsclb.pack()
        fitlb.pack()
        solving.pack()
        
        top.update()

        #cross
        selected = int(popul*selection)
        insvalues = []
        cnt = 0
        while(cnt < popul):
            cross(insvalues,selected,copy.deepcopy(values[random.randrange(0,selected,1)]),copy.deepcopy(values[random.randrange(0,selected,1)]))
            cnt += 1
        values = copy.deepcopy(insvalues)
        #mutate
        for i in range(popul):
            values[i] = copy.deepcopy(mutate(values[i],mutation))
        
        #fix
        for i in range(popul):
            values[i] = copy.deepcopy(fix(values[i]))
        
        if(gen == 0):
            print("Gen\tHighest\tLowest\tAvg\tMax")
        if(gen % 10 == 9 or gen == 0):
            insfit=0
            for i in fitness_values:
                insfit += i
            insfit /= len(fitness_values)
            print(gen+1,"\t",fitness_values[0],"\t",fitness_values[len(fitness_values)-1],"\t",insfit,"\t",high_fitness)
        gen += 1
    top.mainloop()

    
def cross(insvalues,selected,valueo,valuet):
    global values
    insv = copy.deepcopy(valueo)
    inst = copy.deepcopy(values)
    same = {}
    n = 0
    while(n < 40):
        row = copy.deepcopy(random.randint(0,80))
        column = copy.deepcopy(random.randint(0,8))
        if(same.get(row%9) != column and not(fixed[row%9][column])):
            insv[row%9][column] = copy.deepcopy(valuet[row%9][column])
            same[row] = column
            n+=1
    return insvalues.append(copy.deepcopy(insv))

#Mutation Function. Change random space with random numbers between 0 to 9. 0 represents hollow space and it's also included in mutate factor.
def mutate(value,mutation):
    mut_val = int(mutation*81)
    same = {}
    while(mut_val != 0):
        row = copy.deepcopy(random.randint(0,80))
        column = copy.deepcopy(random.randint(0,8))
        if(same.get(row) != column and not(fixed[row%9][column])):
            value[row%9][column] = copy.deepcopy(random.randint(0,9))
            same[row] = column
            mut_val -= 1
    return value

#Fix Function to make each generation be feasible
def fix(value):
    for i in range(9):
        for j in range(9):
            if(len(getposElement(value,i,j)) > 0 ):
                value[i][j] = copy.deepcopy(getposElement(value,i,j)[copy.deepcopy(random.randrange(0,len(getposElement(value,i,j)),1))])
            else:
                value[i][j] = 0
    return value
    
    

#Selection
def select(selection,popul,fitness_values):
    global values
    global high_fitness
    global high_value
    selected=int(popul*selection)
    insf = 0
    insv = values[0]
    for i in range(popul):
        for j in range(popul):
            if(fitness_values[i] > fitness_values[j]):
                insf = copy.deepcopy(fitness_values[j])
                fitness_values[j] = copy.deepcopy(fitness_values[i])
                fitness_values[i] = copy.deepcopy(insf)
                insv = copy.deepcopy(values[j])
                values[j] = copy.deepcopy(values[i])
                values[i] = copy.deepcopy(insv)
    if(high_fitness < fitness_values[0]):
        high_value = copy.deepcopy(values[0])
        high_fitness = copy.deepcopy(fitness_values[0])
        if(fitness_values[0] == 243):
            global start
            print(t.time()-start,"\t")
            print_highest()
    
    
    


#ready for problem to put fixed values.
def ready():
    global value
    global fixed
    for i in range (9):
        for j in range (9):
            if(value[i][j] != 0):
                fixed[i][j] = True
            else:
                fixed[i][j] = False

def get_fitness(value):
    fitness = 0
    for i in range(9):
        for j in range(9):
             fitness += copy.deepcopy(checkElementScore(value,i,j))
    return fitness

def checkElementFlag(value,i,j): 
    rowDif = i%3
    colDif = j%3
    flag = True
    #Check column element
    for column in range (9):
        if(value[i][j]==value[i][column]):
            if(column != j):
                flag = False
    #Check row element
    for row in range (9):
        if(value[i][j]==value[row][j]):
            if(row != i):
                flag = False
    #Check square element
    for row in range (3):
        for column in range(3):
            if(value[i][j]==value[i-rowDif+row][j-colDif+column]):
                if(i-rowDif+row != i and j-colDif+column != j):
                    flag = False
    return flag

def checkElementScore(value,i,j):
    if(value[i][j] == 0):
        return 0
    rowDif = i%3
    colDif = j%3
    score = 0
    flag = True
    #Check column element
    for column in range (9):
        if(value[i][j]==value[i][column]):
            if(column != j):
                flag = False
    if(flag):
        score += 1
    flag = True
    #Check row element
    for row in range (9):
        if(value[i][j]==value[row][j]):
            if(row != i):
                flag = False
    if(flag):
        score += 1
    flag = True
    #Check square element
    for row in range (3):
        for column in range(3):
            if(value[i][j]==value[i-rowDif+row][j-colDif+column]):
                if(i-rowDif+row != i and j-colDif+column != j):
                    flag = False
    if(flag):
        score += 1
    flag = True
    return score

def getposElement(value,i,j):
    posv = []
    for k in range(1,10,1):
        value[i][j] = k 
        if(checkElementFlag(value,i,j)):
            posv.append(k)
        value[i][j] = 0
    return posv

def put_element(value):
    global fixed
    for i in range(9):
        for j in range(9):
            if(not fixed[i][j]):
                value[i][j] = random.randint(1,9)
    return value
 
def print_gen(popul,gen):
    global values
    print(gen+1,"gen : ")

    for i in range(popul):
        print_value(values[i])

               
def print_value(value):
    print("\n")
    for i in range(9):
        for j in range(9):
            print(value[i][j]," ",end="")
        print()
    print()
                
def getMat(value):
    v = ""
    for i in value:
        v = v + str(i) + "\n"
    return v

def print_highest() :
    global high_value
    global high_fitness
    print("\n")
    print("Fitness : ",high_fitness)
    for i in range(9):
        for j in range(9):
            print(high_value[i][j]," ",end="")
        print()
    print()

if __name__ == "__main__":

    popul = 10
    selection = 0.2
    mutation = 0.05
    max_gen = 300000
    
    ready()
    genetic(popul,selection,mutation,max_gen)
    print_highest()
