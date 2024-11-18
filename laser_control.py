import nidaqmx
import string
from nidaqmx.constants import LineGrouping

def new_pos(pos, direction, increment, max_pos):
    new_pos = pos + direction*increment
    if(new_pos<max_pos[0] or new_pos>max_pos[1]):
        print("New position exceeds bounds. Changing direction\n")
        direction = -1*direction
        new_pos = pos + direction*increment
        
    return [new_pos,direction]

def move_axis(positions, directions, increments, max_pos):
    x,directions[0] = new_pos(positions[0],directions[0],increments[0],max_pos)
    y,directions[1] = new_pos(positions[1],directions[1],increments[1],max_pos)
    return [[x,y],directions]





def main():
    Increment_step = 0.05
    Positions = [-1.7-Increment_step,0]
    Directions = [1,1]
    Increments = [Increment_step,0]
    Max_pos = [-3, -1.7]
    with nidaqmx.Task() as task:
        
        DataOff = [0,0]
        task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        task.ao_channels.add_ao_voltage_chan("Dev1/ao1")
        task.start()
        command = "+x"

        while(command != "n"):
            if command == "+y":
                Increments[0] = 0
                Directions[1] = 1
                Increments[1] = Increment_step
                
            elif command == "-y":
                Increments[0] = 0
                Directions[1] = -1
                Increments[1] = Increment_step
            elif command == "+x":
                Increments[0] = Increment_step
                Directions[0] = 1
            elif command == "-x":
                Increments[0] = Increment_step
                Directions[0] = -1
            elif command == "": 
                Increments[0] = Increment_step
                Increments[1] = 0
            else:
                Increments[0] = 0
                Increments[1] = 0
                print("Not a valid command")
            Positions, Directions = move_axis(Positions, Directions, Increments,Max_pos)
            print(f"X Pos:{Positions[0]:.2f}, Y Pos:{Positions[1]:.2f}\n")
            task.write(Positions)
            command = input("Type 'n' to stop else increase step\n")

        task.write(DataOff)
        task.stop()
    
if __name__ == "__main__":
    main()