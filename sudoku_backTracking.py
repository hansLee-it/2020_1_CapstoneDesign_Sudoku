import random
import string
import copy
from tkinter import *
import time as t
prob = [[0,0,0,8,1,2,0,0,6],[0,1,2,0,0,0,8,7,0],[6,0,0,7,9,5,0,1,0],[0,5,7,3,6,0,0,0,0],[0,0,1,0,2,0,3,0,0],[0,0,0,0,4,7,9,2,0],[0,4,0,2,5,1,0,0,3],[0,8,6,0,0,0,2,5,0],[1,0,0,6,8,3,0,0,4]]
value = []
fixed = [[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False]]
element_mark = []
#Backtracking algorithm for sudoku.
#ready for problem to put fixed values.

        

def solve():
    global prob
    global value
    global fixed
    top = Tk()
    top.title("Sudoku_Backtracking")                # 제목
    top.resizable(True, True)        # 크기 고정
    top.configure(background='white') #배경색
    top.geometry("180x400")
    problem = Label(top, text = getMat(prob))
    problemlb = Label(top, text = "초기 입력 문제")
    solving = Label(top, text = getMat(value))
    solvinglb = Label(top, text = "풀이")
    problemlb.pack()
    problem.pack()
    solvinglb.pack()
    ready()
    posElement=[]
    i=0
    j=0
    while(i<9):
        try:
            try:
                if(len(posElement[(i*9)+j])>=0):
                    pass
            except:
                posElement.append(getposElement(value,i,j))
            if(len(posElement[(i*9)+j])>0):
                if(not fixed[i][j]):
                    value[i][j] = copy.deepcopy(posElement[(i*9)+j].pop())
                    solving.destroy()
                    solving = Label(top, text = getMat(value))
                    solving.pack()
                    t.sleep(0.05)
                    top.update()
        except:
            while(True):
                if(i == 0 and j == 0) :
                    print("Unsolvable")
                    return
                elif(j == 0 and i > 0):
                    posElement.pop()
                    if(not fixed[i][j]):
                        value[i][j] = 0
                    i -= 1
                    j = 8
                elif(j>0):
                    posElement.pop()
                    if(not fixed[i][j]):
                        value[i][j] = 0
                    j -= 1
                if(j == -1):
                    j = 1
                if(not fixed[i][j]):
                    value[i][j] = 0
                    j -= 1
                    break
                solving.destroy()
                solving = Label(top, text = getMat(value))
                solving.pack()
                t.sleep(0.05)
                top.update()
        j += 1
        if(j==9):
            i += 1
            j = 0
    top.mainloop()
        

def ready():
    global prob
    global value
    global fixed
    value = copy.deepcopy(prob)
    for i in range (9):
        for j in range (9):
            if(value[i][j] != 0):
                fixed[i][j] = True
            else:
                fixed[i][j] = False

def getposElement(value,i,j):
    posv = []
    ins = value[i][j]
    for k in range(1,10,1):
        value[i][j] = k 
        if(checkElement(i,j)):
            posv.append(k)
    value[i][j] = ins
    return posv

def checkElement(i,j):
    global value
    checkFlag = True
    rowDif = i%3
    colDif = j%3
    #Check column element
    for column in range (9):
        if(value[i][j]==value[i][column]):
            if(column != j):
                checkFlag = False
    #Check row element
    for row in range (9):
        if(value[i][j]==value[row][j]):
            if(row != i):
                checkFlag = False

    #Check square element
    for row in range (3):
        for column in range(3):
            if(value[i][j]==value[i-rowDif+row][j-colDif+column]):
                if(i-rowDif+row != i and j-colDif+column != j):
                    checkFlag = False
    return checkFlag

def print_value():
    global value
    cnt = 0
    for i in value:
        print(str(i)+" ")
        cnt += 1
        if(cnt%9 == 0):
            print("\n")

def getMat(value):
    v = ""
    for i in value:
        v = v + str(i) + "\n"
    return v

if __name__ == "__main__":
    start = t.time()
    ready()
    solve()
    print(t.time()-start )






