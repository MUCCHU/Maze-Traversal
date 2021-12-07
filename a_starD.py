import time
start=time.time()
import numpy as nu;
import cv2;
import math;
import random;

class cell:
    def __init__(self,r,c):
        self.i=r
        self.j=c
        self.ngbList=[]
        self.f=0.0
        self.g=0.0
        self.h=0.0
        self.parent=None
        self.block=False


    def fillValue(self):

        if self in waitingList:
            Result[self.i,self.j]=255, 120, 0
        elif self in visited:
            Result[self.i,self.j]=0, 127, 255
        
        if self in path:
            Result[self.i,self.j]= 127, 0, 0
        if self.block == True:
            Result[self.i,self.j]=255,255,255

    

    #function to calculate neighbours
    def Ngb(self):
        if(self.i < row-1):
            self.ngbList.append(grid[self.i+1,self.j])
        if(self.j < col-1):
            self.ngbList.append(grid[self.i,self.j+1])
        if(self.i > 0):
            self.ngbList.append(grid[self.i-1,self.j])
        if(self.j>0):
            self.ngbList.append(grid[self.i,self.j-1])
        if(self.i>0 and self.j>0):
            self.ngbList.append(grid[self.i-1,self.j-1])
        if(self.i<row-1 and self.j>0):
            self.ngbList.append(grid[self.i+1,self.j-1])
        if(self.i<row-1 and self.j<col-1):
            self.ngbList.append(grid[self.i+1,self.j+1])
        if(self.i>0 and self.j<col-1):
            self.ngbList.append(grid[self.i-1,self.j+1])

def heuristic(a,b):
    hueV=math.sqrt((a.i-b.i)*(a.i-b.i)+(a.j-b.j)*(a.j-b.j))
    return hueV


#generating matrix from Img

img=cv2.imread('inputImg.png')

a,b,c=nu.shape(img)

imgU=nu.zeros((10*a,10*b,c), nu.uint8)
Result=nu.copy(img)
ResultU=nu.copy(imgU)


row=a
col=b
grid=nu.empty((row,col),dtype=cell)
waitingList=[]
visited=[]
path=[]
path_found=False
for i in range(row):
    for j in range(col):
        grid[i,j]=cell(i,j)

        #assigning the beginnning node and end node
beginning=grid[0,0]
destination=grid[row-1,col-1]
for p in range(row):
    for q in range(col):
        if img[p,q,0] == 113 and img[p,q,1] == 204 and img[p,q,2] == 45:
            beginning=grid[p,q] 

        if img[p,q,0] == 60 and img[p,q,1] == 76 and img[p,q,2] == 231:
            destination=grid[p,q]

        if img[p,q,0] == 255 and img[p,q,1] == 255 and img[p,q,2] == 255:
            grid[p,q].block=True






#added starting point to the waiting list

waitingList.append(beginning)

#Computing neighbours
for i in range(row):
    for j in range(col):
        grid[i,j].Ngb()
        grid[i,j].fillValue()


# loop to find path and explore nodes

while(len(waitingList)>0):

    #finding the optimal neighbour

    current=waitingList[0]
    for x in waitingList:
        if x.f<current.f:
            current=x


    if(current==destination):
        #path is found
        path_found=True
        print("Path found -- Reached End successfully")
        print("Cost of the path was {}".format(destination.parent.f))

        #deducing the path
        prev=current
        path.append(prev)
        while(prev.parent!=None):
            path.append(prev.parent)
            #print("On cell {}, {} cost= ".format(prev.i, prev.j, prev.g))
            prev=prev.parent
        break

    
    
    #removing items from waiting list and adding it to visited list
    waitingList.remove(current)
    visited.append(current)

    current.fillValue()

    Cngb=current.ngbList
    for x in Cngb:
        tG=0
        if x not in visited and x.block == False :
            if(abs(current.i-x.i)==1 and abs(current.j-x.j)==1):
                tG = current.g + 1.4
            else:
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


if path_found==False:
    print("We couldn't find a path")


for i in range(row):
    for j in range(col):
        grid[i,j].fillValue()


#Upscaling Image
for i in range(10*a):
    for j in range(10*b):
        I=int(i/10)
        J=int(j/10)
        ResultU[i,j]=Result[I,J]

end=time.time()
print("Time = {}".format((end-start)))
cv2.imshow('Identified things-Diagonal ',ResultU)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('ResultD.jpg',ResultU)