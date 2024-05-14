# n1 = 3
# n2 = 2
# n3 = 1
# n4 = 3

import math
import random
import turtle
from copy import deepcopy
from turtle import *
import keyboard

turtle.speed(0)

VERTEX_AMOUNT = 11
VERTEX_RADIUS = 15
FONT_SIZE = 12
FONT = ("Arial", FONT_SIZE, "normal")
SQUARE_SIZE = 300
BREAK_GAP = 10
EXTRA_GAP = 50
K = 1.0 - 1 * 0.01 - 3 * 0.005 - 0.15
ACTIVE_VERTEX = "#347ff7"
OPENED_VERTEX = "#3e557a"
CLOSED_VERTEX = "#38393b"


def drawVertex(x, y, text, color=None, obj=turtle):
    obj.up()
    obj.goto(x, y - VERTEX_RADIUS)
    obj.down()
    if (color is None):
        obj.circle(VERTEX_RADIUS)
    else:
        obj.fillcolor(color)
        obj.begin_fill()
        obj.circle(VERTEX_RADIUS)
        obj.end_fill()

    obj.up()
    obj.goto(x, y - VERTEX_RADIUS + FONT_SIZE / 2)
    obj.write(text, align="center", font=FONT)
    obj.down()

def getVertexCoords(vertexAmount, squareSize):
    vertexCoords = []

    squareStartX = -squareSize / 2
    squareStartY = squareSize / 2

    xPos = squareStartX
    yPos = squareStartY

    isXMove = 1
    isYMove = 0

    xDirection = 1
    yDirection = -1

    vertexModulus = vertexAmount % 4
    vertexStep = vertexAmount // 4

    for i in range(4):

        vertexPerSide = vertexStep

        if (vertexModulus > 0):
            vertexPerSide += 1
            vertexModulus -= 1

        if (vertexPerSide > 0): vertexGap = squareSize / vertexPerSide
        else: vertexGap = 0

        for j in range(vertexPerSide):
            vertexCoords.append({"x": round(xPos), "y": round(yPos)})
            xPos += isXMove * xDirection * vertexGap
            yPos += isYMove * yDirection * vertexGap

        xPos = round(xPos)
        yPos = round(yPos)

        if (isXMove):
            isXMove = 0
            isYMove = 1
            xDirection *= -1
        elif (isYMove):
            isYMove = 0
            isXMove = 1
            yDirection *= -1

    return vertexCoords

def generateDirMatrix(vertexAmount, k):
    random.seed(3213)

    dirMatrix = []

    for i in range(vertexAmount):
        row = []

        for j in range(vertexAmount):
            randomNumber = random.uniform(0, 2.0)
            row.append(math.floor(randomNumber * k))

        dirMatrix.append(row)

    return dirMatrix

def dirIntoUndirMatrix(dirMatrix):
    undirMatrix = deepcopy(dirMatrix)

    for i in range(len(undirMatrix)):
        for j in range(len(undirMatrix)):
            if (undirMatrix[i][j] == 1):
                undirMatrix[j][i] = 1

    return undirMatrix

def getFi(vector):
    cosFi = vector[0] / math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    fi = math.degrees(math.acos(cosFi))
    if (vector[1] < 0): fi = 360 - fi
    return fi

def arrow(startX, startY, endX, endY, fi=None, obj=turtle):
    vector = [endX - startX, endY - startY]
    if (fi == None):
        fi = 180 + getFi(vector)
    fi = math.pi * fi / 180
    lx = endX + 15 * math.cos(fi + 0.3)
    rx = endX + 15 * math.cos(fi - 0.3)
    ly = endY + 15 * math.sin(fi + 0.3)
    ry = endY + 15 * math.sin(fi - 0.3)

    drawLine(endX, endY, lx, ly, False, obj)
    drawLine(endX, endY, rx, ry, False, obj)

def drawLine(startX, startY, endX, endY, withArrow=False, obj=turtle):
    obj.up()
    obj.goto(startX, startY)
    obj.down()
    obj.goto(endX, endY)

    if (withArrow == True):
        arrow(startX, startY, endX, endY, obj=obj)

def getOrtVector(startX, startY, endX, endY):
    vector = [endX - startX, endY - startY]
    vectorLenght = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    ortVector = [vector[0] / vectorLenght, vector[1] / vectorLenght]
    return ortVector

def normVector(ortVector):
    nVector = [-ortVector[1], ortVector[0]]
    return nVector

def isOnSameSide(Ax, Ay, Bx, By):
    if((Ax == Bx) and (abs(Ax) == SQUARE_SIZE/2)): return True
    elif((Ay == By) and (abs(Ay) == SQUARE_SIZE/2)): return True
    else: return False

def vertexBetween(vertexA, vertexB):
    distance = min(abs(vertexB - vertexA), VERTEX_AMOUNT - abs(vertexB - vertexA))
    return distance

def drawEdge(vertexA, vertexB, graphType, isDoubleWay, obj = turtle):
    if (graphType == "dir"): withArrow = True
    elif (graphType == "undir"): withArrow = False
    vertexCoords = getVertexCoords(VERTEX_AMOUNT, SQUARE_SIZE)
    startX = vertexCoords[vertexA]["x"]
    startY = vertexCoords[vertexA]["y"]
    if (vertexA == vertexB):
        fi = round(getFi([startX, startY]))
        if (((0 < fi) and (fi < 45)) or ((315 < fi) and (fi < 360))):
            fi = 0
            obj.setheading(270)
        elif (((45 < fi) and (fi < 135))):
            fi = 90
            obj.setheading(0)
        elif (((135 < fi) and (fi < 225))):
            fi = 180
            obj.setheading(90)
        elif (((225 < fi) and (fi < 315))):
            fi = 270
            obj.setheading(180)
        elif (fi == 45):
            obj.setheading(315)
        elif (fi == 135):
            obj.setheading(45)
        elif (fi == 225):
            obj.setheading(135)
        else:
            obj.setheading(225)

        obj.up()
        obj.goto(startX + math.cos(math.radians(fi)) * VERTEX_RADIUS, startY + math.sin(math.radians(fi)) * VERTEX_RADIUS)
        obj.down()
        obj.circle(10)
        if (graphType == "dir"):
            arrow(turtle.pos()[0], turtle.pos()[1], turtle.pos()[0], turtle.pos()[1],
                  150 + turtle.heading(), obj)

    else:
        extraGapVector = [0, 0]
        endX = vertexCoords[vertexB]["x"]
        endY = vertexCoords[vertexB]["y"]
        midX = (startX + endX) / 2
        midY = (startY + endY) / 2
        ortVector = getOrtVector(startX, startY, endX, endY)

        if (isOnSameSide(startX, startY, endX, endY)):
            k = vertexBetween(vertexA, vertexB) - 1
            extraGapOrtVector = getOrtVector(0, 0, midX, midY)
            extraGapVector = [extraGapOrtVector[0] * EXTRA_GAP * k, extraGapOrtVector[1] * EXTRA_GAP * k]

        if (isDoubleWay == True and graphType == "dir"):
            nVector = normVector(ortVector)
            nVector[0] = nVector[0] * BREAK_GAP
            nVector[1] = nVector[1] * BREAK_GAP
            drawLine(startX + ortVector[0] * 15, startY + ortVector[1] * 15,
                     midX + nVector[0] + extraGapVector[0],
                     midY + nVector[1] + extraGapVector[1], False, obj)
            drawLine(midX + nVector[0] + extraGapVector[0], midY + nVector[1] + extraGapVector[1],
                     endX - ortVector[0] * 15,
                     endY - ortVector[1] * 15, True, obj)

        else:
            drawLine(startX + ortVector[0] * 15, startY + ortVector[1] * 15,
                     midX + extraGapVector[0],
                     midY + extraGapVector[1], False, obj)
            drawLine(midX + extraGapVector[0], midY + extraGapVector[1],
                     endX - ortVector[0] * 15,
                     endY - ortVector[1] * 15, withArrow, obj)

def createGraph(VERTEX_AMOUNT, VERTEX_RADIUS, SQUARE_SIZE, BREAK_GAP, EXTRA_GAP, dirMatrix, graphType):
    vertexCoords = getVertexCoords(VERTEX_AMOUNT, SQUARE_SIZE)

    matrix = dirMatrix

    if (graphType == "undir"):
        undirMatrix = dirIntoUndirMatrix(dirMatrix)

        for row in undirMatrix:
            print(row)

        matrix = undirMatrix
    else:
        for row in dirMatrix:
            print(row)

    for i in range(len(vertexCoords)):
        x = vertexCoords[i]["x"]
        y = vertexCoords[i]["y"]
        drawVertex(x, y, str(i + 1))

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if (matrix[i][j] == 1):
                if (matrix[j][i] == 1 and graphType == "dir"):
                    drawEdge(i, j, graphType, True)
                else:
                    drawEdge(i, j, graphType, False)

        if (graphType == "undir" and i == j):
            break

    turtle.setheading(0)

dirMatrix = generateDirMatrix(VERTEX_AMOUNT, K)
graphType = "dir"
createGraph(VERTEX_AMOUNT, VERTEX_RADIUS, SQUARE_SIZE, BREAK_GAP, EXTRA_GAP, dirMatrix, graphType)

def matrixMultiply(A, B):
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])

    result = [[0 for col in range(colsB)] for row in range(rowsA)]

    for i in range(rowsA):
        for j in range(colsB):
            for k in range(colsA):
                result[i][j] += A[i][k] * B[k][j]

    return result

def matrixPower(matrix, power):
    if (power == 1):
        return matrix

    return matrixMultiply(matrix, matrixPower(matrix, power - 1))

def matrixSum(A, B):
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])

    result = [[0 for col in range(colsB)] for row in range(rowsA)]

    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = A[i][j] + B[i][j]

    return result

def binaryDisplay(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (matrix[i][j] != 0): matrix[i][j] = 1

    return matrix

def matrixReachability(matrix):

    I = [[0] * len(matrix) for i in range(len(matrix))]

    for i in range(len(matrix)):
        I[i][i] = 1

    answerMatrix = I

    for i in range(len(matrix)):
        answerMatrix = matrixSum(answerMatrix, matrixPower(matrix, i + 1))

    return binaryDisplay(answerMatrix)

def transposeMatrix(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix))]

def multiplyMatrixByElements(A, B):
    result = []
    for i in range(len(A)):
        resultRow = []
        for j in range(len(A[0])):
            resultRow.append(A[i][j] * B[i][j])
        result.append(resultRow)
    return result

def strongConnectivityMartix(matrix):
    return multiplyMatrixByElements(matrix, transposeMatrix(matrix))

def strongConnectivityComponents(matrix):
    indeces = []
    uniqueRows = []

    for index, row in enumerate(matrix):
        if (row not in uniqueRows):
            uniqueRows.append(row)

    for uniqueRow in uniqueRows:
        groupIndeces = []
        for index, row in enumerate(matrix):
            if (row == uniqueRow):
                groupIndeces.append(index)
        indeces.append(groupIndeces)

    return indeces

def redrawVertex(vertex, status, obj):
    vertexCoords = getVertexCoords(VERTEX_AMOUNT, SQUARE_SIZE)
    x = vertexCoords[vertex]["x"]
    y = vertexCoords[vertex]["y"]
    if (status == "active"):
        drawVertex(x, y, str(vertex + 1), ACTIVE_VERTEX, obj)
    elif (status == "open"):
        drawVertex(x, y, str(vertex + 1), OPENED_VERTEX, obj)
    elif (status == "close"):
        drawVertex(x, y, str(vertex + 1), CLOSED_VERTEX, obj)

def bfs(matrix, component, layer):
    random.seed(component[0] * 1488)

    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)

    layer.pencolor(r, g, b)
    layer.pensize(3)

    q = [component[0]]
    newVertexes = [i for i in range(len(matrix))]
    activeVertex = q[-1]
    newVertexes.remove(activeVertex)

    while len(q) != 0:
        activeVertex = q[-1]
        keyboard.wait("space")
        redrawVertex(activeVertex, "active", layer)
        for targetIndex, target in enumerate(matrix[activeVertex]):
            if (target == 1 and targetIndex in newVertexes and targetIndex not in q):
                keyboard.wait("space")
                drawEdge(activeVertex, targetIndex, "dir", (matrix[targetIndex][activeVertex] == 1), layer)
                keyboard.wait("space")
                redrawVertex(targetIndex, "open", layer)
                newVertexes.remove(targetIndex)
                q.insert(0, targetIndex)

        keyboard.wait("space")
        redrawVertex(activeVertex, "close", layer)
        q.pop()

def dfs(matrix, component, layer):
    random.seed(component[0] * 1488)

    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)

    layer.pencolor(r, g, b)
    layer.pensize(3)

    q = [component[0]]
    newVertexes = [i for i in range(len(matrix))]
    activeVertex = q[-1]
    newVertexes.remove(activeVertex)
    keyboard.wait("space")
    redrawVertex(activeVertex, "active", layer)

    while len(q) != 0:
        for targetIndex, target in enumerate(matrix[activeVertex]):
            if (target == 1 and targetIndex in newVertexes and targetIndex not in q):
                keyboard.wait("space")
                redrawVertex(activeVertex, "open", layer)
                keyboard.wait("space")
                drawEdge(activeVertex, targetIndex, "dir", (matrix[targetIndex][activeVertex] == 1), layer)
                newVertexes.remove(targetIndex)
                q.append(targetIndex)
                activeVertex = q[-1]
                keyboard.wait("space")
                redrawVertex(activeVertex, "active", layer)

        keyboard.wait("space")
        redrawVertex(activeVertex, "close", layer)
        q.pop()
        if len(q) != 0:
            activeVertex = q[-1]
            keyboard.wait("space")
            redrawVertex(activeVertex, "active", layer)

def bfsWrapper(matrix, componentsStrongConnectivity, layer):
    bfsLayer.clear()
    dfsLayer.clear()
    for component in componentsStrongConnectivity:
          bfs(dirMatrix, component, layer)

def dfsWrapper(matrix, componentsStrongConnectivity, layer):
    bfsLayer.clear()
    dfsLayer.clear()
    for component in componentsStrongConnectivity:
        dfs(dirMatrix, component, layer)

class Button:
    def __init__(self, x, y, width, height, label, function, fontSize=12, color="white"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.function = function
        self.fontSize = fontSize
        self.color = color

    def drawButton(self):
        up()
        goto(self.x - self.width / 2, self.y - self.height / 2)
        down()
        turtle.fillcolor(self.color)
        turtle.begin_fill()
        for i in range(2):
            turtle.forward(self.width)
            turtle.left(90)
            turtle.forward(self.height)
            turtle.left(90)
        turtle.end_fill()

        up()
        goto(self.x, self.y - self.fontSize/2)
        write(self.label, align="center", font=("Arial", self.fontSize, "normal"))

    def isButtonClicked(self, clickX, clickY):
        return ((self.x - self.width / 2 <= clickX <= self.x + self.width / 2) and
                (self.y - self.height / 2 <= clickY <= self.y + self.height / 2))

matrixReach = matrixReachability(dirMatrix)
matrixStrongConnectivity = strongConnectivityMartix(matrixReach)
componentsStrongConnectivity = strongConnectivityComponents(matrixStrongConnectivity)
print(componentsStrongConnectivity)

buttonsArray = []

def buttonClickHandler(x, y):
    for button in buttonsArray:
        if button.isButtonClicked(x, y):
            button.function()

bfsLayer = turtle.Turtle()
dfsLayer = turtle.Turtle()

bfsButton = Button(-250, 250, 100, 40, "BFS", lambda: bfsWrapper(dirMatrix, componentsStrongConnectivity, bfsLayer))
buttonsArray.append(bfsButton)
bfsButton.drawButton()

dfsButton = Button(-250, 200, 100, 40, "DFS", lambda: dfsWrapper(dirMatrix, componentsStrongConnectivity, dfsLayer))
buttonsArray.append(dfsButton)
dfsButton.drawButton()

turtle.onscreenclick(buttonClickHandler)

turtle.done()
