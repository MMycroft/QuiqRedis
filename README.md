# Quiq Redis

This project contains a simple Redis CLI clone with the commands SET, GET, MGET, DEL, LPUSH, LPOP, LRANGE, HSET, and HGET.

## Assumptions

The project assumes it will be run locally, with only one user. Data is stored in memory and does not persist 
after the program is terminated. Data that is given a lifetime is cleaned immediately prior to a user action,
which may be well after it expires. This works since only one user is ever using the database, but would not be
sufficient for a multiuser database. Additionally, since the database will not grow very large, it is sufficient
to simply iterate over a list of keys with lifetimes to check if any have expired. For a larger, multi-user, persistent
system, a data structure like a tree would be much better suited, since the search time is O(log n) rather than O(n).

## Versions

The project contains two versions of the program. Version one of the program,
> Redis_v1.py

functions similar to the Redis CLI, but uses print statements for errors, and is not formatted exactly the same as Redis CLI.
Version two of the program,
>Redis_v2.py

improves on version one with error handling. The format of the printed statements is the same as the Redis CLI. Additionally,
version 2 fixes some logical errors in the options of the SET command of version one.

## Implementation & Design
The program uses a simple map (dictionary) to map command strings to functions. This allows more general code for command execution,
as opposed to a switch/match statement, or long chain of if/else statements. Extending the program to include a new command simply involves
adding the new command to the map, and implementing a function. This approach has the addition benefit of using the function doc string
for the help function, so that the command is only listed in the help function if the command exists in the map and the function has been
implemented to include a doc string. Options are not implemented in this way, but are contained within the relevant function. Help information
must be included in the doc string of the relevant function.

## Set Up
Ensure that you have Python installed on your system. Open a terminal and navigate to the folder you have saved
>Redis_v2.py

and run
>python Redis_v2.py

Read the menu options carefully. The program is not case-sensitive, so commands may be entered in any format the user 
prefers. Enter
>HELP

to learn about the available commands. Enter
>HELP \<command name\>

to learn about a specific command. Enter
>QUIT

to terminate the program.

