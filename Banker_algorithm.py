import PySimpleGUI as sg
import numpy as np

safeSeq = np.empty(0, dtype="U6")


def isSafe(current, available, need, window):
    global safeSeq
    updateLog("Checking if the current state is safe...", window)
    work = available.copy()
    finish = [False] * len(current)
    while True:
        found = False
        for i in range(len(current)):
            if not finish[i] and np.all(
                need[i] <= work
            ):  # checks if the maximum is less than the work aka available resources
                found = True
                finish[i] = True
                work += current[i]  # release the resources back to the system
                updateLog(
                    f"Process {i} can complete, releasing resources: {current[i]}",
                    window,
                )
                safeSeq = np.append(safeSeq, i)  # adds the process to the safe sequence

        if not found:
            break

    if all(finish):
        updateLog("No deadlock could detected, ACCEPTED", window)
        updateLog(f"safe seq {safeSeq}", window)
        return True
    else:
        updateLog("Deadlock may occur, REJECTED", window)
        return False


def requestRes(PID, request, available, current, need, window):
    global safeSeq

    updateLog(f"Process {PID} is requesting {request} resources", window)
    request = np.array(request, dtype=int)
    if np.all(request <= need[PID]):
        if np.all(
            request <= available
        ):  # Temporarily allocate the requested # resources to the process
            current[PID] += request
            available -= request
            need[PID] -= request
            # Check if the new state is safe
            updateLog(
                f"Allocation of {request} resources to process {PID} is safe, Temporarily allocating the "
                f"requested # resources to the process",
                window,
            )

            if isSafe(current, available, need, window):

                return True
            else:
                updateLog(
                    f"Allocation of {request} resources to process {PID} is not safe, returning the resources...",
                    window,
                )

                return False
        else:
            updateLog(
                f"Process {PID} must wait, since the resources are not available",
                window,
            )
            print(f"process {PID} must wait, since the resources are not available")

    else:
        updateLog(f"Process {PID} exceeds its max claim", window)
        return False


def updateLog(log, window):
    current_text = window["-TEXT-"].get()
    new_text = current_text + "\n" + log
    window["-TEXT-"].update(new_text)


def main():
    Logs = sg.Text("")

    sg.theme("DarkGrey")  # Add a touch of color
    # 3 processes and 3 resources m = resources n = processes
    layout = [  # [sg.Text('Total Resources'), sg.InputText()],
        [sg.Text("Available Resources"), sg.InputText()],
        [
            sg.Text(
                "Enter maximum resources that can be allocated to each process: (Please note that the process are "
                "the rows and the resources are the columns)"
            )
        ],
        [sg.InputText(size=(5, 1), key=(0, i)) for i in range(3)],
        [sg.InputText(size=(5, 1), key=(1, i)) for i in range(3)],
        [sg.InputText(size=(5, 1), key=(2, i)) for i in range(3)],
        [sg.Text("Current allocation of resources to each process:")],
        [sg.InputText(size=(5, 1), key=(3, i)) for i in range(3)],
        [sg.InputText(size=(5, 1), key=(4, i)) for i in range(3)],
        [sg.InputText(size=(5, 1), key=(5, i)) for i in range(3)],
        [sg.Text("Request Format: PID(0->2))"), sg.InputText()],
        [sg.Text("Request Format:Resources(0->2)"), sg.InputText()],
        [sg.Text("Logs", key="-TEXT-"), Logs],
        [sg.Button("Submit"), sg.Button("Cancel")],
    ]

    # Create the Window
    window = sg.Window("Banker's Algorithm", layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == "Submit":
            available_resources = values[0].split(",")
            maximum = [[values[(i, j)] for j in range(3)] for i in range(3)]
            current = [[values[(i + 3, j)] for j in range(3)] for i in range(3)]
            maximum = np.array(maximum, dtype=int)
            current = np.array(current, dtype=int)
            available_resources = np.array(available_resources, dtype=int)
            pid = values[1]
            pid = int(pid)
            request = values[2].split(",")

            need = maximum - current
            updateLog(f"Necessary resources for each process: {need}", window)
            requestRes(pid, request, available_resources, current, need, window)
        if (
            event == sg.WIN_CLOSED or event == "Cancel"
        ):  # if user closes window or clicks cancel
            break

    window.close()


if __name__ == "__main__":
    main()
