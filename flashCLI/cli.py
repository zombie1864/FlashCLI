''' this file will contain only the business logic that is req to perform op for CLI '''
import click
import os
import random
from pathlib import Path 
from typing import Dict, Tuple, Union
from flashCLI import __app_name__, __version__, DB_DIR_PATH, SUCC_CODE_0, FILE_ERR_CODE_2, utils


def get_flashcard_controller_API(db_name:str) -> Union[utils.FlashcardController, int]:
    ''' checks if db file exist, if not returns ERR_CODE else returns inst:FlashcardController'''
    file_path:Path = DB_DIR_PATH / f"{db_name}_flashcards_db.json"
    if not file_path.exists():
        return FILE_ERR_CODE_2
    return utils.FlashcardController(file_path)


def show_all_db():
    '''  '''
    print(os.listdir(DB_DIR_PATH))


def add_to(db_name:str) -> Union[str, int]:
    '''  '''
    controller_API:Union[utils.FlashcardController, int] = get_flashcard_controller_API(db_name)
    if controller_API == FILE_ERR_CODE_2:
        return FILE_ERR_CODE_2
    qstn_input = input('\nPlease input flashcard question: ')
    ans_input = input('\nPlease input the answer to your question: ')
    flashcard, COMM_CODE = controller_API.add(qstn_input, ans_input)
    if COMM_CODE == SUCC_CODE_0:
        return f'\nFlashcard: {flashcard} \nWas added to {db_name} set'


def get_flashcards_from(db_name) -> Union[int, Dict[int, Tuple[str]]]:
    '''  '''
    controller_API:Union[utils.FlashcardController, int] = get_flashcard_controller_API(db_name)
    if controller_API == FILE_ERR_CODE_2:
        return FILE_ERR_CODE_2
    else: 
        return controller_API.retrieve_dataset()


def format(txt):
    ''' An algo that continously, via while loop, reads double_esc chars from input 
    and injects single_esc char until the format is complete. This is a M.P.O. 
    '''
    formated_complete = False 
    while not formated_complete:
        if "\\n" in txt:
            esc_char_idx = txt.index("\\n")
            txt = txt[:esc_char_idx] + "\n" + txt[esc_char_idx + 2:]
            continue
        if "\\t" in txt:
            esc_char_idx = txt.index("\\t")
            txt = txt[:esc_char_idx] + "\t" + txt[esc_char_idx + 2:]
            continue
        formated_complete = True 
    return txt


def flashcard_list_format(idx, qstn, ans) -> click:
    '''  '''
    formated_ans = click.style("\n\tAns::>> ", fg="cyan") + f'{format(ans)}\n'
    formated_idx = f'\n[{idx}]_'
    formated_qstn = click.style("Qstn::", fg='magenta') + f'{format(qstn)}'
    return formated_idx + formated_qstn + formated_ans


def err_msg(db_name:str) -> click:
    '''  '''
    first_line_msg = click.style("\n[Error]:", fg="red", bold=True)
    second_line_msg = f'\n\t[]_Database not found. \n\t[]_Please run, "python3 -m flashCLI init {db_name}"\n\t' 
    third_line_msg = f'[]_To create a database to store flashcards for {db_name}\n'
    return first_line_msg + second_line_msg + third_line_msg


def warning_msg(db_name):
    '''  '''
    return click.style("\n[Warning]:", fg="yellow", bold=True) + f' {db_name} is empty. Please add to {db_name}\n'


def show_flashcard_table_format(db_name:str, flashcards_dataset:Dict[int, Tuple[str]]) -> None:
    '''  '''
    click.echo(click.style(f"\n[{db_name.upper()}]:\n", fg="bright_white"))
    columns = ("[ID]_  ", f"|| QUESTION  ||  ", "|| >> ANSWER  ||  ")
    headers = "".join(columns)
    click.echo(headers)
    for idx, flashcard in enumerate(flashcards_dataset.values()):
        click.echo(click.style("-" * len(headers) + "\n"))
        click.echo(flashcard_list_format(idx, flashcard[0], flashcard[1]))
    click.echo(click.style("-" * len(headers) + "\n"))


def random_select_from(flashcards_dataset) -> Tuple[int,Tuple[str]]:
    '''  '''
    selected_key:int = random.choice(list(flashcards_dataset))
    return (selected_key, flashcards_dataset[selected_key])


def begin_study_session(db_name, flashcards_dataset) -> None:
    ''' NOTE in the future you will want to IMPL a way to "save session". 
    what ever the dataset is at the point of a save session should be saved in a tmp file 
    when user goes back to save session and completes the remainder the file should be deleted 
    '''
    click.echo(click.style(f"\n[NOW STUDYING {db_name.upper()}]:\n", fg="bright_white"))
    click.echo('You can exit at any time, simply enter `e` when prompted an input')
    while len(flashcards_dataset) != 0:
        flashcard_selected:Tuple[int,Tuple[str]] = random_select_from(flashcards_dataset)
        click.echo(
            click.style("\n[Qstn]:\n", fg='magenta', bold=True) + 
            f'\t{flashcard_selected[1][0]}\n' #NOTE use namedtuple 
        )
        ui_ans = input('[Your answer]: ')
        if ui_ans == 'e':
            return 
        click.echo(
            click.style("\n[Result]:\n", fg='bright_blue') + 
            click.style("\tYour Answer::>> ", fg='cyan') + f'{ui_ans}\n' + 
            click.style("\tCorrect Answer::>> ", fg='cyan') + f'{flashcard_selected[1][1]}\n' 
        )
        is_succ_attempt = input('Do results match?\nSuccess::[y/N]: ').lower()
        if is_succ_attempt == 'y':
            del flashcards_dataset[flashcard_selected[0]] #NOTE M.P.O
        elif is_succ_attempt == 'n':
            continue
        elif is_succ_attempt == 'e':
            return 
        else:
            click.echo(click.style("\n[Error]: ", fg="red", bold=True) + 'Invalid input please provide valid input next time\n')


def edit(db_name:str):
    '''  '''
    controller_API:Union[utils.FlashcardController, int] = get_flashcard_controller_API(db_name)
    if controller_API == FILE_ERR_CODE_2:
        return click.echo(err_msg(db_name))
    click.echo('\nWhich ID would you like to edit?')
    click.echo('To cancel type "e"')
    _id = input('>>ID to edit: ')
    if _id == 'e':
        return click.echo('\nCancel success\n')
    flashcard = controller_API.get_flashcard(_id)
    click.echo(click.style('\n\tQstn:: ', fg='bright_yellow') + f'{flashcard[0]}')
    click.echo(click.style('\tAns::>> ', fg='bright_yellow') + f'{flashcard[1]}\n')
    click.echo('What would you like to edit?')
    valid_input_resp = False 
    qstn_or_ans_resp = None
    while not valid_input_resp:
        qstn_or_ans_resp = input('Question(q)/Answer(a): ').lower()
        if qstn_or_ans_resp == 'e':
            return click.echo('\nCancel success\n')
        elif not qstn_or_ans_resp in ['a', 'q']:
            click.echo(
                click.style("\n[Error]: ", fg="red", bold=True) + 'invalid input. Please input a valid response\n'
            )
        else: 
            valid_input_resp = True 
    ui_input = input('Input your edit now: ')
    flashcard, COMM_CODE = controller_API.edit_flashcard(flashcard, qstn_or_ans_resp, ui_input, _id)
    if COMM_CODE == SUCC_CODE_0:
        click.echo('\n[SUCCESS]: your edit has been saved\n')
    else:
        click.echo('[Error]: something went wrong') #WARNING use better desc here 


def delete(db_name:str):
    '''  '''
    warning_delimiter = click.style("\n[Warning]: ", fg="yellow", bold=True)
    click.echo(warning_delimiter + f'Are you sure you wish to delete {db_name}?\n')
    ui_resp = input('Delete?::[y/N] ').lower()
    if ui_resp == 'y':
        controller_API:Union[utils.FlashcardController, int] = get_flashcard_controller_API(db_name)
        if controller_API == FILE_ERR_CODE_2:
            return click.echo(err_msg(db_name))
        controller_API.delete_dataset()
        return click.echo(f'\nSuccess:: {db_name} has been deleted\n')
    elif ui_resp == 'n':
        return click.echo('\nCancel success\n')
    else:
        return click.echo(click.style("\n[Error]: ", fg="red", bold=True) + 'Invalid input, cancelling request\n')


def deletefrom(db_name):
    '''  '''
    _id = input('Which ID would you like to delete?')
    ui_resp = input(f'\nAre you sure you wish to delete flashcard id {_id} from the {db_name} database?').lower()
    if ui_resp == 'y':
        controller_API:Union[utils.FlashcardController, int] = get_flashcard_controller_API(db_name)
        if controller_API == FILE_ERR_CODE_2:
            return click.echo(err_msg(db_name))
        controller_API.delete_from_dataset(_id)
        return click.echo(f'\nSuccess:: flashcard {_id} has been deleted from {db_name}\n')
    elif ui_resp == 'n':
        return click.echo('\nCancel success\n')
    else:
        return click.echo(click.style("\n[Error]: ", fg="red", bold=True) + 'Invalid input, cancelling request\n')