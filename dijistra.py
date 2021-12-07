import time
start=time.time()
import numpy as nu;
import cv2;
import math;
import random;
# clear cell marked with O
# waitingList cells marked with -

class cell:
    def __init__(self,r,c):
        self.i=r
        self.j=c
        self.ngbList=[]
        self.f=0
        self.g=0
        self.h=0
        self.parent=None
        self.block=False

    
    
    #to fill matrix with appropriate symbols

    # if(random.random()<0.1):
    #     self.block=True

    def fillValue(self):
        value[self.i,self.j]='O'

        if self in waitingList:
            #print("found this object in waiting list")
            value[self.i,self.j]='-'
            Result[self.i,self.j]=255, 120, 0
        elif self in visited:
            #print("found this object in visited list {} {}".format(self.i,self.j))
            value[self.i,self.j]='*'
            Result[self.i,self.j]=0, 127, 255
            #print(value)
        
        if self in path:
            value[self.i,self.j]='P'
            Result[self.i,self.j]= 127, 0, 0
        if self.block == True:
            value[self.i,self.j]='X'

    

    #function to calculate neighbours
    def Ngb(self):
        #print("Calculating neighbours")
        #print(self)
        if(self.i < row-1):
            #print("bottom")
            self.ngbList.append(grid[self.i+1,self.j])
        if(self.j < col-1):
            #print("left")
            self.ngbList.append(grid[self.i,self.j+1])
        if(self.i > 0):
            #print("top")
            self.ngbList.append(grid[self.i-1,self.j])
        if(self.j>0):
            #print("right")
            self.ngbList.append(grid[self.i,self.j-1])

def heuristic(a,b):
    hueV=0
    return hueV
#generating matrix from Img

img=cv2.imread('Task_1_Low.png')

a,b,c=nu.shape(img)

imgU=nu.zeros((10*a,10*b,c), nu.uint8)
Result=nu.copy(img)
ResultU=nu.copy(imgU)
# for i in range(10*a):
#     for j in range(10*b):
#         I=int(i/10)
#         J=int(j/10)
#         imgU[i,j]=img[I,J]

# Result=nu.copy(imgU)


row=a
col=b
grid=nu.empty((row,col),dtype=cell)
value=nu.empty((row,col),dtype='U')
f_value=nu.empty((row,col))
waitingList=[]
visited=[]
path=[]
path_found=False
for i in range(row):
    for j in range(col):
        grid[i,j]=cell(i,j)
        #grid[i,j].fillValue()

        #assigning the beginnning node and end node
beginning=grid[0,0]
destination=grid[row-1,col-1]
#print(img[10,10])
for p in range(row):
    for q in range(col):
        if img[p,q,0] == 113 and img[p,q,1] == 204 and img[p,q,2] == 45:
            beginning=grid[p,q]
            #img[p,q] = 255, 0, 0 

        if img[p,q,0] == 60 and img[p,q,1] == 76 and img[p,q,2] == 231:
            destination=grid[p,q]
            #img[p,q] = 3, 190, 252

        if img[p,q,0] == 255 and img[p,q,1] == 255 and img[p,q,2] == 255:
            grid[p,q].block=True
            #img[p,q] = 252, 3, 252






#added starting point to the waiting list

waitingList.append(beginning)

#Computing neighbours
for i in range(row):
    for j in range(col):
        grid[i,j].Ngb()
        grid[i,j].fillValue()

#print("First fill value executed")
# loop to find path and explore nodes

# grid[4,3].block=True
# grid[3,3].block=True
# grid[3,4].block=True

while(len(waitingList)>0):

    #finding the optimal neighbour

    current=waitingList[0]
    for x in waitingList:
        if x.f<current.f:
            current=x


    if(current==destination):
        #path is found
        path_found=True
    #     print("Path found -- Reached End successfully")
    #     print("The cost of Path was {}".format(destination.g))

    #     #deducing the path
    #     prev=current
    #     path.append(prev)
    #     while(prev.parent!=None):
    #         path.append(prev.parent)
    #         prev=prev.parent
    #     break

    
    
    #removing items from waiting list and adding it to visited list
    waitingList.remove(current)
    visited.append(current)

    current.fillValue()


    #print(value)

    #print("I passed {} {}".format(current.i,current.j))
    # current=waitingList[0]
    # visited.append(waitingList[0])
    # waitingList.pop(0)
    # cNgb=current.ngbList

    Cngb=current.ngbList
    
    for x in Cngb:
        tG=0
        if x not in visited and x.block == False :
            tG = current.g + 1

            #if node has been explored but not closed
            if x in waitingList:
                if tG < x.g:
                    x.g=tG        
            else:
                #if node is still unexplored
                x.g=tG
                waitingList.append(x)
        
            x.h=heuristic(x,destination)
            x.f=x.g+x.h
            x.parent=current
#print("While loop fill value executed")


if path_found==False:
    print("We couldn't find a path")
else:
    print("Minimum distance = {}".format(destination.g))
for i in range(row):
    for j in range(col):
        grid[i,j].fillValue()
#print("last and final fill value executed")


#Upscaling Image
for i in range(10*a):
    for j in range(10*b):
        I=int(i/10)
        J=int(j/10)
        ResultU[i,j]=Result[I,J]

end=time.time()
print("Time = {}".format((end-start)))
cv2.imshow('Identified things ',ResultU)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('Result.jpg',ResultU)


# grid[0,0].Ngb()
# grid[1,1].Ngb()

#Highlighting neighbours of cell 1
#lst=grid[1,1].ngbList
# lst1=grid[0,0].ngbList
# for x in lst:
#     value[x.i,x.j]='*'
# grid[0,0].f=2

# print(grid)
# print(waitingList)
#print(value)
#print(len(lst1))
#print(len(lst))
# print(grid[0,0].f)
# print(grid[1,1].f)
# a,b=grid.shape
# print(a)
# print(b)

# img=cv2.imread('Task_1_Low.png')


# a,b,c=nu.shape(img)

# imgU=nu.zeros((10*a,10*b,c), nu.uint8)
# for i in range(10*a):
#     for j in range(10*b):
#         I=int(i/10)
#         J=int(j/10)
#         imgU[i,j]=img[I,J]
# print("The dimensions of upscaled image is")
# print(nu.shape(imgU))
# cv2.imshow('Image', img)
# cv2.imshow('Upscaled Image',imgU)
# cv2.imwrite('Result.jpg',imgU)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# while(len(waitingList)>0):
#     break