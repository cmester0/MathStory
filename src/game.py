import os
import png


player = {"x": 0, "y": 0, "oldx": 0, "oldy": 0}
level = [
    {"description": "Use 'move <left,right,up,down>' to get to (3,0)", "goal": {"x": 3, "y": 0}, "walls": []},
    {"description": "Use 'display [width] [height] [name]' to get an image of the map, and then move to the goal", "goal": {"x": -4, "y": 4}, "walls": []},
    {"description": "You can use 'run [filename]' to run files, avoid walls", "goal": {"x": 9, "y": -15}, "walls": [(0,-1),(0,-2),(0,-3)]},
]
current_level = 0

def EditPrograms():
    while True:
        print ("Edit program (Y/n): ", end='')
        edit = input()
    
        if edit.lower() == "n":
            if not os.path.isfile("../GameFiles/Program.txt"):
                print ("'program' file still needs editing")
                continue
            break
    
        print ("Program name: ", end='')

        program = input()

        if program == "":
            continue
    
        if ("/" in program):
            program = program[program.rlast("/"):]

        with open("../GameFiles/" + program.lower() + ".txt", 'w') as f:
            while True:
                print (">> ", end='')
                instruction = input()
            
                if (instruction.lower() == "quit"):
                    break
        
                f.write(instruction.lower() + "\n")

def CheckLevelGoal():    
    global current_level
    
    if player["x"] == level[current_level]["goal"]["x"] and \
       player["y"] == level[current_level]["goal"]["y"]:
        print ("Level",current_level,"complete")
        print ()
        
        current_level += 1
        player["x"] = 0
        player["y"] = 0
        player["oldx"] = 0
        player["oldy"] = 0
        
        if current_level >= len(level):
            return True

        print ("Starting", current_level)
        print (level[current_level]["description"])
        
    return False
        

def RunFile(filename):
    with open("../GameFiles/" + filename + ".txt", 'r') as f:
        while True:
            instruction = f.readline()[:-1]
            if not instruction:
                return False
            
            print ("STEP " + instruction)

            if instruction[:4] == "move":
                direction = instruction[5:]

                player["oldx"] = player["x"]
                player["oldy"] = player["y"]
                
                if direction == "left":
                    player["x"] -= 1
                elif direction == "right":
                    player["x"] += 1
                elif direction == "up":
                    player["y"] -= 1
                elif direction == "down":
                    player["y"] += 1

                if (player["x"], player["y"]) in level[current_level]["walls"]:
                    player["x"] = player["oldx"]
                    player["y"] = player["oldy"]
                    
            elif instruction[:7] == "display":
                dims = instruction[8:]
            
                if not (" " in dims and dims.find(" ") != dims.rfind(" ")):
                    continue                
            
                x = int(dims[:dims.find(" ")])
                y = int(dims[dims.find(" ")+1:dims.rfind(" ")])
                name = dims[dims.rfind(" ")+1:]

                displ = open("../" + name + ".png", 'wb')
                w = png.Writer(x, y, greyscale=False)

                displ_img = [[[100 if i % 2 == 0 else 50 + \
                               100 if j % 2 == 0 else 50] * 3 for i in range(x)] for j in range(y)]

                if (0 <= level[current_level]["goal"]["y"] - player["y"] + y // 2 and
                    level[current_level]["goal"]["y"] - player["y"] + y // 2 <= y and
                    0 <= level[current_level]["goal"]["x"] - player["x"] + x // 2 and
                    level[current_level]["goal"]["x"] - player["x"] + x // 2 <= x):
                    displ_img\
                        [level[current_level]["goal"]["y"] - player["y"] + y // 2]\
                        [level[current_level]["goal"]["x"] - player["x"] + x // 2]\
                        = [255, 0, 0]

                for i in range(x):
                    for j in range(y):
                        if (i + player["x"] - y // 2,
                            j + player["y"] - x // 2) in level[current_level]["walls"]:
                            displ_img[j][i] = [0, 255, 0]
                        
                    
                displ_img\
                    [y // 2]\
                    [x // 2]\
                    = [0, 0, 255]
            
                displ_img = [sum(x, []) for x in displ_img]
            
                w.write(displ, displ_img)
                displ.close()

            elif instruction[:3] == "run":
                path = instruction[4:]
                if RunFile(path):
                    return True
                

            if CheckLevelGoal():
                return True
        CheckLevelGoal()

if __name__ == "__main__":
    EditPrograms()
    
    print ("Running program")

    print ("Starting",current_level)
    print (level[current_level]["description"])
                
    RunFile("program")
