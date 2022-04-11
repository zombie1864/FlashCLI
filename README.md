# FlashCLI 
----------
A CLI (_command line application_) that allows users to create virtual flashcards. CLI's are applications that act like a more robust script intended with the use of flexibility and scalability. To acheive both desired factors this application follows MVC design architecture patterns to solve a bigger problem by dissolving it into smaller and module parts. 

## MVC Design Pattern 
---------------------
An MVC pattern is designed to handle the storing and retrieving of data, manipluation of data, packaging data, and deliverance of said data to the correct route. The database is directly read and written into memory to allow a serverless application to operate locally on user machine without required network access. Many web frameworks rely on MVC design pattern to handle data requests between user and a database. For this CLI app the "View" layer is the terminal, the "Controller" layer falls under 'utils.FlashcardController', and "Models" layer is 'db_API.py' script. The "physical" database is held in the _flashcards-db/_ dir which stores each flashcard dataset as json file. 

## Click Over argparse
----------------------
The choice of using _Click_ rather than argparse is for the purpose of using intuitive decorator based API that runs argparse under the hood. The use of decorators, in this context, provides further functionality to an existing object without modifying its structure. This is a design choice to allow top-level _main_ file to act as an entry point in which all other functionalities of FlashCLI commands are extended from the main function rather than having a script for every single command in the application. 
```python
import click

@click.group()
def main():
    '''  docstring will get printed here when we call "python3 -m flashCLI --help"
    '''
    pass 

@main.command()
@click.argument('cmd_arg')
def cli_cmd_1(cmd_arg):
    '''  '''
    pass 

@main.command()
@click.argument('cmd_arg')
def cli_cmd_2(cmd_arg):
    '''  '''
    pass 
```