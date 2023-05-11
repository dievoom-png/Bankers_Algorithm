# Banker's Algorithm Simulation

This is a Python program that simulates the Banker's Algorithm, which is a deadlock avoidance algorithm used by operating systems to manage resources.

The program takes the following inputs:

- The number of the total resources
- The number of available resources of each type
- The maximum number of resources of each type that can be allocated to each process
- The current allocation of resources to each process
- A request for resources made by a process

The program then simulates the allocation of resources to the processes and determines whether or not the system is in a safe state (i.e., there is no deadlock).

The program was implemented using the PySimpleGUI library to create a simple graphical user interface (GUI) that allows the user to enter the necessary inputs and view the program's output.

## Requirments

`pip install PySimpleGUI`
`pip install numpy`

## Usage

To use this program, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt` in the command line.
3. Run the program by running `python banker_algorithm.py` in the command line.
4. Enter the necessary inputs in the GUI and click the "Submit" button to run the simulation.
5. View the program's output in the "Logs" section of the GUI.

