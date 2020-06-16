import random
import copy
import time as t
import string

start = t.time()
sudoku_problem = []
sudoku_solve = []
high_value = []
high_fitness = 0
prob = [[9,0,0,8,1,2,0,0,6],[0,1,2,0,0,0,8,7,0],[6,0,0,7,9,5,0,1,0],[0,5,7,3,6,0,0,0,0],[0,0,1,0,2,0,3,0,0],[0,0,0,0,4,7,9,2,0],[0,4,0,2,5,1,0,0,3],[0,8,6,0,0,0,2,5,0],[1,0,0,6,8,3,0,0,4]]
value = []
fixed = [[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False]]
values = []
element = [1,2,3,4,5,6,7,8,9]
random.seed(a=None)
times = 0.0
gens = 0
n = 0
#Genetic algorithm for sudoku.
#Get mutation rate. Score the population of the sudoku problem. Pick high fitnesses.
def genetic(popul,selection,mutation,max_gen):
    global values
    global value
    global high_fitness
    global times
    global gens
    global n
    global start
    fitness_values = []
    start = t.time()
    gen = 0
    #First Generation
    for i in range(popul):
        fitness_values.append(copy.deepcopy(0))
        values.append(copy.deepcopy(put_element(copy.deepcopy(value))))
    for i in range(popul):
        fitness_values[i] = copy.deepcopy(get_fitness(copy.deepcopy(values[i])))
    #After first generation. Loop
    while(gen != max_gen):
        #answerFound
        if(high_fitness==243):
            
            time = t.time()-start
            print(time)
            times += time
            print(gen+1," Generation")
            print("Complete!")
            gens += gen
            n += 1
            return
        #getFitness
        for i in range(popul):
            fitness_values[i] = copy.deepcopy(get_fitness(copy.deepcopy(values[i])))
        #select
        select(copy.deepcopy(selection),popul,copy.deepcopy(fitness_values))
        #cross
        cross(popul,selection)
        #mutate
        for i in range(popul):
            values[i] = copy.deepcopy(mutate(values[i],mutation))
        
        gen+= 1
    if(high_fitness!=243):
        print("Cannot find the answer.")
    
    

    
def cross(popul,selection):
    global values
    selected = int(popul*selection)
    inst = []
    while(len(inst) != popul):
        valueo = copy.deepcopy(values[random.randint(0,selected-1)])
        valuet = copy.deepcopy(values[random.randint(0,selected-1)])
        for i in range(9):
            for j in range(9):
                ins = copy.deepcopy(valueo[i][j])
                valueo[i][j] = copy.deepcopy(valuet[i][j])
                if(not checkElementFlag(valueo,i,j)):
                    valueo[i][j] = copy.deepcopy(ins)
        inst.append(copy.deepcopy(valueo))
    values = copy.deepcopy(inst)

def mutate(value,mutation):
    mut_val = int(mutation*81)
    blank = 0
    same = {}
    while(mut_val != 0):
        row = copy.deepcopy(random.randint(0,80))
        column = copy.deepcopy(random.randint(0,8))
        if(same.get(row) != column and not(fixed[row%9][column])):
            if(len(getposElement(value,row%9,column)) > 1 ):
                value[row%9][column] = copy.deepcopy(getposElement(value,row%9,column)[copy.deepcopy(random.randrange(0,len(getposElement(value,row%9,column)),1))])
                same[row] = column
                mut_val -= 1
            else:
                value[row%9][column] = copy.deepcopy(0)
                same[row] = column
                mut_val -= 1
                blank += 1
    for i in range(9):
        for j in range(9):
            if(value[i][j]==0):
                if(len(getposElement(value,i,j)) > 0 ):
                    value[i][j] = copy.deepcopy(getposElement(value,i,j)[copy.deepcopy(random.randrange(0,len(getposElement(value,i,j)),1))])
                    blank -= 1
            if(blank == 0):
                return value
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
        for j in  range(popul):
            if(fitness_values[i] < fitness_values[j]):
                insf = copy.deepcopy(fitness_values[j])
                fitness_values[j] = copy.deepcopy(fitness_values[i])
                fitness_values[j] = copy.deepcopy(insf)
                insv = copy.deepcopy(values[j])
                values[j] = copy.deepcopy(values[i])
                values[j] = copy.deepcopy(insv)
    for i in range(selected):
        values.pop()
    if(high_fitness < fitness_values[0]):
        high_value = copy.deepcopy(values[0])
        high_fitness = copy.deepcopy(fitness_values[0])
    
    
    


#ready for problem to put fixed values.
def ready():
    global value
    global fixed
    global prob
    global high_fitness
    global high_value
    global values
    values = []
    high_fitness = 0
    high_value = []
    value = copy.deepcopy(prob)
    
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
    cnt = 81
    same = {}
    
    while(cnt != 0):
        row = copy.deepcopy(random.randint(0,8))
        column = copy.deepcopy(random.randint(0,8))
        if(same.get(row) != column and not(fixed[row][column])):
            ins = copy.deepcopy(value[row][column])
            value[row][column] = copy.deepcopy(random.randint(1,9))
            if(not checkElementFlag(value,row,column)):
                value[row][column] = copy.deepcopy(ins)
                same[row] = column
            else:
                same[row] = column
                cnt -= 1
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
    selection = 0.5
    mutation = 0.05
    max_gen = 300000
    
    for i in range(100):
        ready()
        genetic(popul,selection,mutation,max_gen)
        print_highest()
    
    print("Average Time : ",times/n)
    print("Average Generation : ",gens/n)
