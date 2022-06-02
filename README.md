# Kenken Solver
A Simple Kenken Solver with descriptive visual GUI
        
Our project is a Kenken GUI that can solve kenken with any board size using three methods:
 <br> 1- backtracking
 <br> 2- backtracking with forward checking
 <br> 3- backtracking with arc consistency.

## Representation

### GUI
When we open the GUI, we see two options. The user will specify the board size and the algorithm to solve the board with.
<div align="center">
<img src="https://github.com/Hazem-ali/KenKen-Solver/blob/main/Screenshots/Picture1.jpg" width="550">  
</div>

### Board
The Kenken board is represented by a square n-by-n grid of cells. 
The grid may contain between 1 and n boxes (cages) represented by a heavily outlined perimeter.
Each cage will contain in superscript: the target digit value for the cage followed by a mathematical operator. 
<div align="center">
<img src="https://github.com/Hazem-ali/KenKen-Solver/blob/main/Screenshots/Picture11.jpg" width="550">  
</div>

### Constraints

Each valid solution must follow the below rules:

- The only numbers you may write are 1 to N for a NxN size puzzle.
- A number cannot be repeated within the same row or column.
- In a one-cell cage, just write the target number in that cell.
- Each "cage" (region is colored a specific color) contains a "target number" and an arithmetic operation. You must fill that cage with numbers that produce the target number, using only the specified arithmetic operation. Numbers may be repeated within a cage, if necessary, as long as they do not repeat within a single row or column.

## Comparison Between Algorithms
The below table represents the time performance of each algorithm, to solve different size puzzles each 100 times.

|  Size  |  2   | 3  | 4 | 5 | 6 | 7 | 8 |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
|   Backtracking  | 2.9e-5s | 0.000143s | 0.0017s | 0.0130s | 0.0525s | 7.957s | 92.3s |    
|   Forward Checking  | 2.42e-5s | 0.000109s | 0.000229s | 0.0005s | 0.0005s |0.0009s | 0.0016s |0.00246s |    
|   Arc Consistency  | 2.96e-5s | 0.000107s | 0.00286s | 0.0006s | 0.001198s | 0.002016s | 0.00323s |    

## GUI Manual
This is an example of how to use the GUI.
1. This is the front window in which the user specifies the board size as a single number and the algorithm used to solve the board.

<div align="center">
<img src="https://github.com/Hazem-ali/KenKen-Solver/blob/main/Screenshots/Picture1.jpg" width="550">  
</div>

2. This is an example of 5x5 board generated
<div align="center">
<img src="https://github.com/Hazem-ali/KenKen-Solver/blob/main/Screenshots/Picture4.jpg" width="550">  
</div>
3. Choosing the algorithm to solve the board
<div align="center">
<img src="https://github.com/Hazem-ali/KenKen-Solver/blob/main/Screenshots/Picture6.jpg" width="550">  
</div>
4. After solving the board using forward checking.
<div align="center">
<img src="https://github.com/Hazem-ali/KenKen-Solver/blob/main/Screenshots/Picture7.jpg" width="550">  
</div>


