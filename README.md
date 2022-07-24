# Year2
This is an example of a process managment system in Python. It contians a mehtod for adding proceesses to the priority queues. Each process then executes in order according to their 
priority. Some processes will be added to blocked queue if resources need to be fetched from memory. 
These have a timer on them and will be added back to the priority queues with increased priority.
Once each process completes it is removed form the priority queue and a messgae is displayed that it has completed and how long it took. 
Once level 8 priority has been reached it executes in a "Round Robin" fasion.
When all processes have executed the idle process is executed and the progrem completes.
Thenprogram is recursive and you can set the number of processes to be executed.
