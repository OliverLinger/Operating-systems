# Oliver Linger 120444372
from processes import Processes
from random import randint
import time


class MLFQ(Processes):
    # Initialise the class
    def __init__(self, listOfProcesses):
        # List of queues to be sorted
        self._listOfProcesses = listOfProcesses
        self._blocked_IO = []

        # This is our list of queus starting at position 0 with the highest
# priority, The last one being the idle process
        self._listOfQueues = [[], [], [], [], [], [], [], []]
        self._process_count = 0
        self._time_finished = 0
        self._freq_l_flag = False
    # This is the last thing that occurs and it is the idle process

    def idle_process(self):
        print("Idle process is executed")
        exit()

    def addingToQueues(self):
        # This adds processes from the process list into the ready queues or the
# blocked list
        for index in range(len(self._listOfProcesses)):
            # Check if it is I/O bound
            # iterate over every process and check if it io bound
            if self._listOfProcesses[index][4] == 1:

                print("process", self._listOfProcesses[index][0], "Is IO bound and is sent to blocked list" )
                # Add it to the blocked queue
                self._blocked_IO.append(self._listOfProcesses[index])
            else:
                # Now lets check index and insert it into the appropriate queue
                # append it to the apporopriate queu
                print("process", self._listOfProcesses[index][0], "Is added to the ready queue. Into queue", self._listOfProcesses[index][5])
                self._process_count += 1
                self._listOfQueues[self._listOfProcesses[index][5] -1].append(self._listOfProcesses[index])
    def blockedProcesses(self):
        # this gives a time to the blocked processes in which they will execute for
        for i in range(len(self._blocked_IO)):
            self._blocked_IO[i][6]=randint(5, 100)
    def roundRobinExecution(self, i, time_quantum):
        # This is an execution of round robin as it is in the last queue
        # We remove the item and place onto the back of the 8th queue.
        while self._listOfQueues[i] != []:
            temp_process=self._listOfQueues[i][0]
            self._listOfQueues[i].remove(self._listOfQueues[i][0])
            # append it onto the back of the 8th queue
            self._listOfQueues[i].append(temp_process)
            if self._listOfQueues[i][0][2] <= 0:
                # Change count of procceses
                self._process_count -= 1
                TAT=(self._listOfQueues[i][0][3] - self._listOfQueues[i][0][1])
                WT=TAT - self._listOfQueues[i][0][7]
                print("Process ID:", self._listOfQueues[i][0][0], "is completed.","Arrival Time: ", self._listOfQueues[i][0][1],"Completion time:", self._listOfQueues[i][0][3], "Turnaround time: ",TAT, "Waiting Time: ", WT, "In queue:", self._listOfQueues[i][0][5])
                self._listOfQueues[i][0][2]=0
                self._listOfQueues[i].remove(self._listOfQueues[i][0])
                # print timeCompleted, arrival time etc
                # subtract all appropriate values from the blocked list
                self.subtractingBlockedProcessTime(time_quantum)
            for j in range(len(self._blocked_IO)):
                temp_t=self._blocked_IO[j][6]
                self._blocked_IO[j][6]=temp_t - time_quantum
        self.executingProcesses()


    def subtractingBlockedProcessTime(self, time_quantum):
        # Each time this is called it subtracts the time quantum from the blocked process time.
        for i in range(len(self._blocked_IO)):
            temp_time=self._blocked_IO[i][6]
            self._blocked_IO[i][6]=temp_time - time_quantum
        self.executingProcesses()

    def executingProcesses(self):
        # This will execute the main body of the MLFQ
        # Check if IO processes are empty
        b_empty=False
        if self._blocked_IO == []:
            b_empty=True
        else:
            # Check if any operations have completed There wait and if so call the adding to main processes queue
            for b_queue in self._blocked_IO:
                if b_queue[6] <= 0:
                    self._process_count += 1
                    print("Process", b_queue[0],
                          "Is added back into ready queue.")
                    # set arrival time, in this case it is the time_finished of the previous time process.
                    b_queue[1]=self._time_finished
                    # check if its already in queue 1 ie 0
                    if b_queue[5] == 1:
                        b_queue[6]=0
                        self._listOfQueues[b_queue[5]-1].append(b_queue)
                        print("It is added to queue:", b_queue[5])
                        self._blocked_IO.remove(b_queue)
                    else:
                        # Add it back to the queue
                        temp_priority=b_queue[5]
                        b_queue[5]=temp_priority - 1
                        # reset the value of the blocked completed time
                        b_queue[6]=0
                        self._listOfQueues[b_queue[5]-1].append(b_queue)
                        print("It is added to queue:", b_queue[5])
                        self._blocked_IO.remove(b_queue)
        # look through main queues and check if all processes have been executed
        q_empty=True
        for queue in self._listOfQueues:
            if queue != []:
                q_empty=False
                break
        # now check if both MLFQ and blocked list are empty
        if q_empty == True and b_empty == True:
            self.idle_process()
        else:
            for i in range(len(self._listOfQueues)):
                if self._listOfQueues[i] != []:
                    # Check if is IO bound, ie needs info to be fetched fromhardware
                    self._listOfQueues[i][0][4]=randint(0, 5)  # A one in five chance of being sent to the blocked list
                    if self._listOfQueues[i][0][4] == 1:
                        self._process_count -= 1
                        print("process", self._listOfQueues[i][0][0], "Is IO bound and is sent to blocked list")
                        # Add it to the blocked queue
                        self._blocked_IO.append(self._listOfQueues[i][0])
                        self._listOfQueues[i].remove(self._listOfQueues[i][0])
                        # Give it a completion value
                        self._blocked_IO[-1][6]=randint(5, 100)
                        self.executingProcesses()
                    else:
                        time_quantum=5*(2**i)
                        # Check if there are only two operations
                        if self._process_count > 2:
                            if self._freq_l_flag == True:
                                print("Number of processes is above 2 again. Increase frequency and voltage, To 1GHz time quantum=",
                                time_quantum, "milliseconds")
                            self._freq_l_flag=False
                        # Make sure that there are less than 2 processes and thatthey are in the lowest priority queue.
                        elif self._process_count <= 2 and i == 7:
                            time_quantum=time_quantum * 1.20
                            if self._freq_l_flag == False:
                                print("-------------------------------------------------------")
                                print("There are 2 or less processes within the ready queues in the lowest possible queue ie queue 8.")
                                print("Frequency, voltage configuration is changed to a lower one. From 1GHz to 0.8Ghz, ",
                                "This results in the time taken=time quantum * 1.20, in the case",
                                time_quantum, "milliseconds.")

                                print("-------------------------------------------------------")
                                self._freq_l_flag=True

                                print("-------------------------------------------------------")
                        print("process:", self._listOfQueues[i][0][0], "is executing, for", time_quantum,"milliseconds in queue", i+1)

                        print("-------------------------------------------------------")
                        # stall the program for x number of milliseconds
                        time.sleep(time_quantum / 1000)
                        # Subtract the time quantum from the burst time.
                        t_complete=self._listOfQueues[i][0][2]
                        self._listOfQueues[i][0][2]=t_complete - time_quantum
                        # add the suitable time to the counter
                        self._time_finished += time_quantum
                        # set the value of the completed time
                        self._listOfQueues[i][0][3]=self._time_finished
                        if self._listOfQueues[i][0][5] == 8:
                                print("round robin execution for final Readyqueue")
                                self.roundRobinExecution(i, time_quantum)
                        # check if it was completed within the time quantum
                        if self._listOfQueues[i][0][2] <= 0:
                            self._process_count -= 1

                            TAT=(self._listOfQueues[i][0][3] - self._listOfQueues[i][0][1])
                            WT=TAT - self._listOfQueues[i][0][7]
                            print("Process ID:", self._listOfQueues[i][0][0], "iscompleted.","Arrival Time: ",
                            self._listOfQueues[i][0][1], "Completion time: ",self._listOfQueues[i][0][3], "Turnaround time: ",
                            TAT, "Waiting Time:", WT, "In queue:", self._listOfQueues[i][0][5])
                            self._listOfQueues[i][0][2]=0
                            self._listOfQueues[i].remove(
                                self._listOfQueues[i][0])
                            # subtract all appropriate values from the blocked list
                            self.subtractingBlockedProcessTime(time_quantum)

                        else:
                            # Change its priority To one of lower importance
                            self._listOfQueues[i][0][5]=self._listOfQueues[i][0][5] + 1
                            # place it into a queue of decreased importance
                            self._listOfQueues[i+1].append(self._listOfQueues[i][0])
                            # Remove the queue from the queue of higher importance
                            self._listOfQueues[i].remove(
                                self._listOfQueues[i][0])
                            # Subtract apppropriate values from blocked queus
                            self.subtractingBlockedProcessTime(time_quantum)
