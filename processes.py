from random import randint


class Processes:
    def __init__(self):
        # Loop to generate the processes
        self._listOfProcesses = []
        self._id = 0
        for i in range(0, 6):
            # Create a list to encapsulate our attributes for each process.
            listOfAttributes = []
            # These are each processes attributes
            self._arrivalTime = 0
            self._burstTime = randint(10, 100)
            self._completionTime = None
            self._ioBound = randint(0, 2)
            self._priority = randint(1, 8)
            self._blockedExecutionTime = 0
            self._savedBurstTime = self._burstTime
            # Now add this to a list of attributes
            listOfAttributes.extend([self._id, self._arrivalTime, self._burstTime,
                                     self._completionTime,
                                     self._ioBound, self._priority, self._blockedExecutionTime,
                                     self._savedBurstTime])
            self._listOfProcesses.append(listOfAttributes)
