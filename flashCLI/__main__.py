import click
from typing import Union, Tuple, Dict
from flashCLI import (
    __app_name__, __version__, SUCC_CODE_0, FILE_ERR_CODE_2, cli, config, db_API
)


@click.group()
@click.version_option(__version__)
def main():
    '''----------[ COMMAND INSTRUCTIONS ]----------\n
    >>> python3 -m flashCLI <CMD_ARG> <flashcard set name>
    \n\n\twhere CMD_ARG is the command name.\n
    [Example]: to create chemistry flashcards: \n
    >>> python3 -m flashCLI init chemistry\n
    To see full documentation of any command\n
    >>> python3 -m flashCLI <CMD_ARG> --help
    \n\n---------------[ INSTR END ]---------------
    '''


@main.command()
@click.argument('db_name')
def list(db_name:str) -> None:
    ''' display flashcards from database's dataset '''
    flashcards_dataset:Union[int, Dict[int, Tuple[str]]] = cli.get_flashcards_from(db_name)
    if flashcards_dataset == FILE_ERR_CODE_2:
        return click.echo(cli.err_msg(db_name))
    elif len(flashcards_dataset) == 0:
        return click.echo(cli.warning_msg(db_name))
    cli.show_flashcard_table_format(db_name, flashcards_dataset)


@main.command()
def showdb() -> None:
    ''' shows flashcard stacks saved into the database '''
    cli.show_all_db()


@main.command()
@click.argument('db_name')
def study(db_name) -> None:
    ''' initiates study session for a specific flashcard set '''
    flashcards_dataset:Union[int, Dict[int, Tuple[str]]] = cli.get_flashcards_from(db_name)
    if flashcards_dataset == FILE_ERR_CODE_2:
        return click.echo(cli.err_msg(db_name))
    elif len(flashcards_dataset) == 0:
        return click.echo(cli.warning_msg(db_name))
    cli.begin_study_session(db_name, flashcards_dataset)
    click.echo(click.style('\n[SUCCESS]:: ', fg='bright_white') + 'Study session over\n') 


@main.command()
@click.argument('db_name')
def addto(db_name:str) -> None:
    ''' adds flashcard(s) to a pre-existing database\n
    User can input "\\n" or "\\t" to format display output
    '''
    session = ''
    while session != 'N':
        backend_resp:Union[str, int] = cli.add_to(db_name)
        if backend_resp == FILE_ERR_CODE_2:
            return click.echo(f'\nDatabase not found. \nPlease run, "python3 -m flashCLI init {db_name}"\n')
        else:
            click.echo(backend_resp)
        session = input('\nDo you wish to add another flashcard?\nAdd More?::[y/N]: ').upper()
    click.echo(f'\nThank you, your {db_name} flashcard set has been successfully updated\n')


@main.command()
@click.argument('db_name')
def edit(db_name) -> None:
    ''' edits a flashcard from a dataset '''
    cli.edit(db_name)


@main.command()
@click.argument('db_name')
def deletefrom(db_name) -> None:
    ''' deletes flashcard from a dataset '''
    cli.deletefrom(db_name)

@main.command()
@click.argument('db_name')
def delete(db_name) -> None:
    ''' deletes database file from database '''
    cli.delete(db_name)


@main.command() 
@click.argument('db_name')
def init(db_name) -> None:
    ''' Used to initialize a database for a specific flashcard set'''
    code_res = config.init_app(db_name)
    if code_res == SUCC_CODE_0:
        db_API.init_database(db_name)
        click.echo(click.style("\n[Success]:", fg="bright_green") + ': Database created\n')
    elif code_res == 2:
        click.echo(click.style("\n[Error]", fg="red") + f': Database for {db_name} already created\n')

if __name__ == '__main__':
    main()