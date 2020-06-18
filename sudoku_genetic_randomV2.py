import random
import copy
import time as t
import string
from tkinter import *
start = t.time()
sudoku_problem = []
sudoku_solve = []
high_value = []
high_fitness = 0
value = [[9,0,0,8,1,2,0,0,6],[0,1,2,0,0,0,8,7,0],[6,0,0,7,9,5,0,1,0],[0,5,7,3,6,0,0,0,0],[0,0,1,0,2,0,3,0,0],[0,0,0,0,4,7,9,2,0],[0,4,0,2,5,1,0,0,3],[0,8,6,0,0,0,2,5,0],[1,0,0,6,8,3,0,0,4]]
marking = [[[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False]]]
order = [[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]]
fixed = [[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False]]
values = []
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
        select(copy.deepcopy(selection),popul,copy.deepcopy(fitness_values))
        
        #TKinter
        solvinglb.destroy()
        solving.destroy()
        highlb.destroy()
        highsclb.destroy()
        high.destroy()
        genlb.destroy()

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
        solvinglb.pack()
        solving.pack()
        
        top.update()

        #cross
        selected = int(popul*selection)
        cross(popul,selection,copy.deepcopy(values[random.randrange(0,selected,1)]),copy.deepcopy(values[random.randrange(0,selected,1)]))
        #mutate
        for i in range(popul):
            values[i] = copy.deepcopy(mutate(values[i],mutation))
        
        

        if(gen % 100 == 99):
            print(gen+1,"Gen")
            print_highest()
        gen += 1
    top.mainloop()

    
def cross(popul,selection,valueo,valuet):
    global values
    insv = copy.deepcopy(valueo)
    inst = copy.deepcopy(values)
    cnt = 0

    same = {}
    while(cnt != popul):
        n = 0
        while(n != 40):
            row = copy.deepcopy(random.randint(0,80))
            column = copy.deepcopy(random.randint(0,8))
            if(same.get(row%9) != column and not(fixed[row%9][column])):
                insv[row%9][column] = copy.deepcopy(valuet[row%9][column])
                same[row] = column
                n+=1
        inst[cnt] = copy.deepcopy(insv)
        cnt += 1
    values = copy.deepcopy(inst)

'''
def mutate(value,mutation):
    mut_val = int(mutation*81)
    same = {}
    
    while(mut_val != 0):
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
                mut_val -= 1
    return value
'''
'''
def mutate(value,mutation):
    mut_val = int(mutation*81)
    same = {}
    for i in range(9):
        for j in range(9):
            if(value[i][j]==0):
                value[i][j] = copy.deepcopy(random.randint(1,9))
                if(not checkElementFlag(value,i,j)):
                    value[i][j] = copy.deepcopy(0)
                else:
                    mut_val -= 1  
                if(mut_val == 0):
                    return value
    while(mut_val != 0):
        row = copy.deepcopy(random.randint(0,8))
        column = copy.deepcopy(random.randint(0,8))
        if(same.get(row) != column and not(fixed[row][column])):
            ins = copy.deepcopy(value[row][column])
            value[row][column] = copy.deepcopy(random.randint(1,9))
            if(not checkElementFlag(value,row,column)):
                value[row][column] = copy.deepcopy(0)
                same[row] = column
            else:
                same[row] = column
                mut_val -= 1
    return value
'''
def mutate(value,mutation):
    mut_val = int(mutation*81)
    same = {}
    while(mut_val != 0):
        row = copy.deepcopy(random.randint(0,8))
        column = copy.deepcopy(random.randint(0,8))
        if(same.get(row) != column and not(fixed[row][column])):
            value[row][column] = copy.deepcopy(random.randint(1,9))
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
        if(high_fitness == 243):
            global start
            print(t.time()-start)
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

'''
def put_element(value):
    global fixed
    for i in range(9):
        for j in range(9):
            if(not fixed[i][j]):
                posv=getposElement(value,i,j)
                try:
                    value[i][j] = copy.deepcopy(posv[random.randint(0,len(posv)-1)])
                except:
                    pass
    return value
'''
def put_element(value):
    global fixed
    for i in range(9):
        for j in range(9):
            if(not fixed[i][j]):
                value[i][j] = random.randint(1,9)
    return value
        
'''
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
        else:
            same[row] = column
    return value
'''

'''
def put_element(value):
    global fixed
    cnt = 81
    while(cnt == 0):
        element = [1,2,3,4,5,6,7,8,9]
        min = [0,0,0,0]
        mini = [999,999,999]
        for i in range(9):
            for j in range(9):
                posRowElements[i] = 0
                posColElements[j] = 0
                posSquareElements[i//3][j//3] = 0
        for i in range(9):
            for j in range(9):
                if(value[i][j] == 0):
                    posRowElements[i] += 1
                    posColElements[j] += 1
                    posSquareElements[i//3][j//3] += 1
        
        for l in range(9):
            if(posRowElements[l] < mini[0] and posRowElements[l] != 0):
                mini[0] = posRowElements[l]
                min[0] = l
        for k in range(9):
            if(posColElements[k] < mini[1] and posColElements[k] != 0):
                mini[1] = posColElements[k]
                min[1] = k
        for m in range(3):
            for n in range(3):
                if(posSquareElements[m][n] < mini[2] and posSquareElements[m][n] != 0):
                    mini[2] = posSquareElements[m][n]
                    min[2] = m
                    min[3] = n
        if(mini[2] <= mini[0] and mini[2] <= mini[1] and mini[2] != 0):
            for l in range(min[2]*3,(min[2]*3)+3,1):
                for k in range(min[3]*3,(min[3]*3)+3,1):
                    if(not fixed[l][k] or value[l][k] == 0):
                        value[l][k] = random.randint(1,9)
                    else: 
                        break

        elif(mini[0] <= mini[1] and mini[0] != 0):
            for k in range(9):
                if(not fixed[min[0]][k]):
                    value[min[0]][k] = random.randint(1,9)
                else:
                    break
                        
        elif(mini[0] > mini[1] and mini[1] != 0):
            for k in range(9):
                if(not fixed[k][min[1]]):
                    value[k][min[1]] = random.randint(1,9)
                else:
                    break
        cnt -= 1
    for i in range(9):
        for j in range(9):
            if(not fixed[i][j]):
                pos = getposElement(value,i,j)
                if(len(pos)>0):
                    value[i][j] = copy.deepcopy(pos[random.randint(0,len(pos)-1)])
                else:
                    return value
    return value
'''
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

    popul = 50
    selection = 0.5
    mutation = 0.05
    max_gen = 10000
    
    ready()
    genetic(popul,selection,mutation,max_gen)
    print_highest()
