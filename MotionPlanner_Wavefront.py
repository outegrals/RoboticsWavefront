#!/usr/bin/env python
#Tommy Truong

import numpy as np

def main():
    with open("world3.txt") as f:
        lst = f.read().split('\n')
        #takes in the txt file and split it by the '\n' character
        #at each index, split it by ' ' character
        #convert the new list into a list of int
        
        #parsing for x,y,z
        #(lower bound, upper bound)
        x = lst[0].split(' ')
        x = [int(i) for i in x]

        y = lst[1].split(' ')
        y = [int(i) for i in y]

        z = lst[2].split(' ')
        z = [int(i) for i in z]
        
        #parsing for obstacles
        #Centerpoint position on x,y,z, length of edges
        obj1 = lst[3].split(' ')
        obj1 = [int(i) for i in obj1]

        obj2 = lst[4].split(' ')
        obj2 = [int(i) for i in obj2]

        obj3 = lst[5].split(' ')
        obj3 = [int(i) for i in obj3]

        obj4 = lst[6].split(' ')
        obj4 = [int(i) for i in obj4]

        #Parsing for start and goal position
        #x,y,z position
        start = lst[7].split(' ')
        start = [int(i) for i in start]

        end = lst[8].split(' ')
        end = [int(i) for i in end]
    #print(z)
    #initalize the configuration space, diff is use under the assumption the lower bound can be greater then 0
    diffX = x[1] - x[0] 
    diffY = y[1] - y[0] 
    diffZ = z[1] - z[0] 
    world = np.zeros((diffX,diffY,diffZ))
    print('the configuration space has been made\n')

    #putting the start and end position in the configuration space
    world[start[0],start[1],start[2]] = 1
    world[end[0],end[1],end[2]] = 2
    waveNum = 2

    #putting the obstacles into the configuration space
    cube = []
    sphere = []
    #the first position of the cube is the centerpoint - half the length of the edge - the lower bound if lower bound isn't 0
    for i in range (int(obj1[0] - obj1[3]/2 - 1), int(obj1[0] + obj1[3]/2 )):
        for j in range (int(obj1[1]  - 1  - obj1[3]/2), int(obj1[1]  + obj1[3]/2)):
                for k in range (int(obj1[2] - 1   - obj1[3]/2),int( obj1[2] + obj1[3]/2)):
                    world[i,j,k] = -1
                    #print([i,j,k], ' , ', world[i,j,k])
    print('cube 1 has been placed in the configuration space\n')
    for i in range (int(obj2[0]  - 1  - obj2[3]/2), int(obj2[0]    + obj2[3]/2 )):
        for j in range (int(obj2[1]  -1  - obj2[3]/2), int(obj2[1]    + obj2[3]/2)):
                for k in range (int(obj2[2] -1   - obj2[3]/2),int( obj2[2]    + obj2[3]/2)):
                    world[i,j,k] = -1
                   # print([i,j,k])
    #Same structure as a cube but point will only be labled if distance from that point to center is less than the radius 
    print('cube 2 has been placed in the configuration space\n')
    for i in range (int(obj3[0] - obj3[3]), int(obj3[0] + obj3[3])):
        for j in range (int(obj3[1] - obj3[3]), int(obj3[1] + obj3[3])):
                for k in range (int(obj3[2] - obj3[3]),int( obj3[2] + obj3[3])):
                    if distance(i, j, k, obj3[0], obj3[1], obj3[2], obj3[3]):
                        world[i,j,k] = -1
                       # print([i,j,k])
    print('sphere 1 has been placed in the configuration space\n')
    #print(obj4[0], ' ',diffX ,' ', obj4[3])
    for i in range (int(obj4[0] - obj4[3]), int(obj4[0] + obj4[3])):
        for j in range (int(obj4[1] - obj4[3]), int(obj4[1] + obj4[3])):
                for k in range (int(obj4[2] - obj4[3]),int( obj4[2] + obj4[3])):
                    if distance(i, j, k, obj4[0], obj4[1], obj4[2], obj4[3]):
                        world[i,j,k] = -1

                        #print([i,j,k])
    print('sphere 2 has been placed in the configuration space\n')

    sequence = []
    position = []
    #Wavefront process

    #initial process
    '''
    waveNum = waveNum + 1
    for i in range (end[0] - 1   , end[0] + 2   ):
        for j in range (end[1] - 1   , end[1] + 2   ):
            for k in range (end[2] - 1   , end[2] + 2   ):
                if (i == end[0] and j == end[1] and k == end[2]):
                    #skips if spot is at goal
                    continue
                else:
                    #places the increment value around the goal and stores the position in the list 
                    world[i,j,k] = waveNum
                    position.append([i,j,k])
    '''
    
    position.append([end[0], end[1], end[2]])
    #print(end)
    #populating the space with numbers
    while (len(position) != 0):

        #Setting up the bound for where the wavefront needs to check 
        x_lower = 1
        x_upper = 2
        y_lower = 1
        y_upper = 2
        z_lower = 1
        z_upper = 2

        #gets the current position and deletes it from the list
        pos = position[0]
        #print(pos)
        position.pop(0)
        #takes the current value of the position and increment it by one
        waveNum = world[pos[0], pos[1], pos[2]]
        waveNum = waveNum + 1
        #checks if any of the x,y,z position is at the edge and set the boundary to 0
        if isEdge(pos[0] + 1, x):
            if pos[0] == x[0]:
                x_lower = 0
            elif pos[0] + 1== x[1]:
                x_upper = 0
        if isEdge(pos[1] + 1, y):
            if pos[1] == y[0]:
                y_lower = 0
            elif pos[1] + 1 == y[1]:
                y_upper = 0
        if isEdge(pos[2] + 1, z):
            if pos[2] == z[0]:
                z_lower = 0
            elif pos[2] + 1 == z[1]:
                z_upper = 0
        #checking for cells around the selected position and adding it to the list if a value was assigned 
        for i in range (pos[0] - x_lower   , pos[0] + x_upper   ):
            for j in range (pos[1] - y_lower   , pos[1] + y_upper   ):
                for k in range (pos[2] - z_lower   , pos[2] + z_upper   ):
                    if (world[i,j,k] != 0):
                        continue
                    else:
                        world[i,j,k] = waveNum
                        position.append([i,j,k])

    print('Wavefront is finish populating array')
    position.append([start[0],start[1],start[2]])
   # print('starting position: ', start)
    #finding the path
    min = 1000000
    minSpot = []
    x_lower = 1
    x_upper = 2
    y_lower = 1
    y_upper = 2
    z_lower = 1
    z_upper = 2
    if isEdge(start[0]+ 1 , x):
        if start[0] == x[0]:
            x_lower = 0
        elif start[0] + 1 == x[1]:
            x_upper = 0
    if isEdge(start[1]+ 1 , y):
        if start[1] == y[0]:
            y_lower = 0
        elif start[1] + 1 == y[1]:
            y_upper = 0
    if isEdge(start[2]+ 1 , z):
        if start[2] == z[0]:
            z_lower = 0
        elif start[2] + 1 == z[1]:
            z_upper = 0
    for i in range (start[0] - x_lower   , start[0] + x_upper   ):
        for j in range (start[1] - y_lower   , start[1] + y_upper   ):
            for k in range (start[2] - z_lower   , start[2] + z_upper   ):
                if (i == start[0] and j == start[1] and k == start[2]) or world[i,j,k] == -1:
                    #skips if spot is at original value or obstacle
                    continue
                else:
                  #  print([i,j,k])
                    if min > world[i,j,k]:
                        min = world[i,j,k]
                        minSpot = [i,j,k]

       # print('current min value: ', min, 'at spot: ', minSpot)
    #adds the starting location and location with the neighbor with the smallest steps required
    sequence.append(start)
    sequence.append(minSpot)
    while min != 2:
        #flag is use to break out of all for loops if min is found
        flag = False
        #decrement min and set the minSpot to by the new position
        min = min - 1
        pos = minSpot
        
        #Setting up boundary within 1 unit around the point
        x_lower = 1
        x_upper = 2
        y_lower = 1
        y_upper = 2
        z_lower = 1
        z_upper = 2
        #set boundary to 0 if at an edge
        if isEdge(pos[0] + 1 , x):
            if pos[0] == x[0]:
                x_lower = 0
            elif pos[0] + 1 == x[1]:
                x_upper = 0
        if isEdge(pos[1]+ 1 , y):
            if pos[1] == y[0]:
                y_lower = 0
            elif pos[1]+ 1  == y[1]:
                y_upper = 0
        if isEdge(pos[2]+ 1 , z):
            if pos[2] == z[0]:
                z_lower = 0
            elif pos[2] + 1 == z[1]:
                z_upper = 0
        for i in range (pos[0] - x_lower   , pos[0] + x_upper   ):
            for j in range (pos[1] - y_lower   , pos[1] + y_upper   ):
                for k in range (pos[2] - z_lower   , pos[2] + z_upper   ):
                    if (i == pos[0] and j == pos[1] and k == pos[2]) or world[i,j,k] == -1 or world[i,j,k] == 1:
                        #skips if spot is at original value, obstacle, or center
                        continue
                    else:
                        #saves the location of the shortest path and break out of the loop
                        if min == world[i,j,k]:
                           # min = world[i,j,k]
                            minSpot = [i,j,k]
                            flag = True
                            break
                if flag:
                    break
            if flag:
                flag = False
                break
        #adds location to the path 
        sequence.append(minSpot)

        #print('current min value: ', min, 'at spot: ', minSpot)
   # for i in range(0, len(sequence)):
   #     print(world[(sequence[i][0], sequence[i][1], sequence[i][2])])
    
    print('The path have been found!\n')
    print('outputing the path into Wavefront_output.txt\n')
    #output path into txt file
    file = open("Wavefront_output.txt", "w")
    for i in range(0, len(sequence)):
       # file.write(sequence[i][0], ',',sequence[i][1],',',sequence[i][2])
        file.write('%d %d %d\n' %(sequence[i][0], sequence[i][1], sequence[i][2]))
       # file.write('\n')
    file.close()
    print('Finish!\n')

#checks if the number is at the end of the configuration space
def isEdge(position, bound):

    if position == bound[0] + 1 or position == bound[1]:
        return True
    else:
        return False


#compues the distance from the edge to the centerpoint 
def distance(x1,y1,z1,x0,y0,z0, r):
    x = np.square(float(x1) - x0)
    y = np.square(float(y1) - y0)
    z = np.square(float(z1) - z0)
    
    if np.sqrt(x+y+z)< r + 1:
        return True
    else:
        return False
    



main()
