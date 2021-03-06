# SimpleGraphNoSQL
Python library implementing a simple NoSql database(+ curses interface) based on a graph model, using excel files as source. 

The program takes a folder containing excel tables as source and generates a queryable, NoSQL graph database. The database
can be accesed by a curses frontend, and uses modified B+ and Trie trees to index and order data. 

So far i have implemented a very limited proof-of-concept subset of queries, and the code needs 
to be heavily refactored and optimized. This project originaly started as a final project for my "Data search and classification" 
class, but its scope ended up being heavily expanded so i could experiment with graph dbs and managing states in memory.

There is plenty of room for optimization, even if some data structures are (almost) optimal. The original lab report (in portugeuse) can be find in the relatorio.pdf file and includes some information about how the program works.


Includes:curses, dill, easygui, xlrd, regex

Files:



![File structure](https://raw.githubusercontent.com/mlcruz/SimpleGraphNoSQL/master/folders.png)

Curses Interface:

![Main screen](https://raw.githubusercontent.com/mlcruz/SimpleGraphNoSQL/master/prog.png)

