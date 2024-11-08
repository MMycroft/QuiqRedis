# Quiq Redis

This project contains a simple Redis CLI clone with the commands SET, GET, MGET, DEL, LPUSH, LPOP, LRANGE, HSET, and HGET.

## Assumptions

The project assumes it will be run locally, with only one user. Data is stored in memory and does not persist 
after the program is terminated. Data that is given a lifetime is cleaned immediately prior to a user action,
which may be well after it expires. This works since only one user is ever using the database, but would not be
sufficient for a multiuser database. Additionally, since the database will not grow very large, it is sufficient
to simply iterate over a list of keys with lifetimes to check if any have expired. For a larger, multi-user, persistent
system, a data structure like a tree would be much better suited, since the search time is O(log n) rather than O(n).

## Set Up
Ensure that you have Python installed on your system. Open a terminal and navigate to the folder you have saved
>Redis.py

and run
>python Redis.py

Read the menu options carefully. The program is not case sensitive, so commands may be entered in any format the user 
prefers. Enter
>HELP

to learn about the available commands. Enter
>HELP \<command name\>

to learn about a specific command. Enter
>END

to terminate the program.

