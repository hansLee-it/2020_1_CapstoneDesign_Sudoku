import random
import copy
import time as t
import string

sudoku_problem = []
sudoku_solve = []
high_value = []
high_fitness = 0
value = [[9,0,0,8,1,2,0,0,6],[0,1,2,0,0,0,8,7,0],[6,0,0,7,9,5,0,1,0],[0,5,7,3,6,0,0,0,0],[0,0,1,0,2,0,3,0,0],[0,0,0,0,4,7,9,2,0],[0,4,0,2,5,1,0,0,3],[0,8,6,0,0,0,2,5,0],[1,0,0,6,8,3,0,0,4]]
marking = [[[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False]]]
order = [[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]]
fixed = [[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False]]
values = []
turn = 1
used = 0
element = [1,2,3,4,5,6,7,8,9]
random.seed(a=None)
posRowElements = [0,0,0,0,0,0,0,0,0]
posColElements = [0,0,0,0,0,0,0,0,0]
posSquareElements = [[0,0,0],[0,0,0],[0,0,0]]
#Genetic algorithm for sudoku.
#Get mutation rate. Score the population of the sudoku problem. Pick high fitnesses.
def genetic(popul,selection,mutation,max_gen):
    global values
    global value
    fitness_values = []
    
    gen = 0
    #First Generation
    for i in range(popul):
        fitness_values.append(0)
        values.append(put_element(copy.deepcopy(value)))
    for i in range(popul):
        fitness_values[i] = get_fitness(values[i])
    #After first generation. Loop
    while(gen != max_gen):
        for i in range(popul):
            fitness_values[i] = get_fitness(values[i])
        #print
        
        print_gen(popul,gen)
        
        #select
        select(selection,popul,fitness_values)
        #cross
        selected = int(popul*selection)
        cross(popul,selection,copy.deepcopy(values[random.randrange(0,selected,1)]),copy.deepcopy(values[random.randrange(0,selected,1)]))
        #mutate
        for i in range(popul):
            values[i] = mutate(values[i],mutation)
        if(gen % 100 == 99):
            print(gen+1,"Gen")
            print_highest()
            t.sleep(0.5)
            

        gen += 1
    

    
def cross(popul,selection,valueo,valuet):
    global values
    insv = copy.deepcopy(valueo)
    inst = copy.deepcopy(values)
    cnt = 0
    while(cnt != popul):
        for i in range(9):
            for j in range(9):
                if(checkElementFlag(valuet,i,j)):
                    insv[i][j] = valuet[i][j]
        inst[cnt] = copy.deepcopy(insv) 
        cnt += 1
    values = copy.deepcopy(inst)





def mutate(value,mutation):
    mut_val = int(mutation*81)
    same = {}
    
    while(mut_val != 0):
        row = copy.deepcopy(random.randint(0,8))
        column = copy.deepcopy(random.randint(0,8))
        if(same.get(row) != column and not(fixed[row][column])):
            value[row][column] = copy.deepcopy(random.randint(1,9))
            same[row] = column
            mut_val -= 1
    return value


#Selection
def select(selection,popul,fitness_values):
    global values
    global high_fitness
    global high_value
    high_loc = []
    high_loc.clear()
    selected=int(popul*selection)
    for i in range(popul):
        high_loc.append(i)

    insf = 0
    insl = 0
    insv = values[0]
    for i in range(popul):
        for j in  range(popul):
            if(fitness_values[i] < fitness_values[j]):
                insf = copy.deepcopy(fitness_values[j])
                fitness_values[j] = copy.deepcopy(fitness_values[i])
                fitness_values[j] = copy.deepcopy(insf)
                insl = copy.deepcopy(high_loc[j])
                high_loc[j] = copy.deepcopy(high_loc[i])
                high_loc[j] = copy.deepcopy(insl)
                insv = copy.deepcopy(values[j])
                values[j] = copy.deepcopy(values[i])
                values[j] = copy.deepcopy(insv)
    if(high_fitness < fitness_values[0]):
        high_value = copy.deepcopy(values[0])
        high_fitness = copy.deepcopy(fitness_values[0])
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
             fitness += checkElement(value,i,j)
    return fitness

def checkElementFlag(value,i,j):
    rowDif = i%3
    colDif = j%3
    score = 0
    flag = True
    #Check column element
    for column in range (9):
        if(value[i][j]==value[i][column]):
            if(column != j):
                flag = False
        
    if(not flag):
        score += 1
        flag = True
    #Check row element
    for row in range (9):
        if(value[i][j]==value[row][j]):
            if(row != i):
                flag = False
    if(not flag):
        score += 1
        flag = True
    #Check square element
    for row in range (3):
        for column in range(3):
            if(value[i][j]==value[i-rowDif+row][j-colDif+column]):
                if(i-rowDif+row != i and j-colDif+column != j):
                    flag = False
    if(not flag):
        score += 1
        flag = True
    if(score == 3):
        return True
    else:
        return False

def checkElement(value,i,j):
    rowDif = i%3
    colDif = j%3
    score = 0
    flag = True
    #Check column element
    for column in range (9):
        if(value[i][j]==value[i][column]):
            if(column != j):
                flag = False
        
    if(not flag):
        score += 1
        flag = True
    #Check row element
    for row in range (9):
        if(value[i][j]==value[row][j]):
            if(row != i):
                flag = False
    if(not flag):
        score += 1
        flag = True
    #Check square element
    for row in range (3):
        for column in range(3):
            if(value[i][j]==value[i-rowDif+row][j-colDif+column]):
                if(i-rowDif+row != i and j-colDif+column != j):
                    flag = False
    if(not flag):
        score += 1
        flag = True
    return score

def put_element(value):
    global fixed
    for i in range(9):
        for j in range(9):
            if(not fixed[i][j]):
                random.seed(random.randint(0,10))
                value[i][j] = copy.deepcopy(random.randint(1,9))
    return value

def print_gen(popul,gen):
    global values
    print(gen+1,"Gen : ")

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

    popul = 50
    selection = 0.5
    mutation = 0.3
    max_gen = 300000

    ready()
    genetic(popul,selection,mutation,max_gen)
    print_highest()
