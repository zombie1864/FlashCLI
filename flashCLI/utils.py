''' this file acts like the controller in an MVC design pattern containing the business logic that COMM w CLI 
and connects COMM(CLI,DB). Here we make use of NamedTuple - a factory function which is designed to make your 
code more pythonic when working with tuples. NameTuples allow you to create immutable seq types that allow you to 
access their values using desc field names and the "dot notation" instead of using unclear integer indices 
'''
from pathlib import Path
from typing import Tuple, Dict, NamedTuple, List, Union
from flashCLI.db_API import DBResponse, DBHandler
from flashCLI import DB_READ_ERR_CODE_3


class CurrentFlashCard(NamedTuple):
    ''' data model/ data container for the curr flashcard '''
    flashcard: Tuple[str]
    COMM_CODE: int 


class FlashcardController:
    ''' This class CONN(CLI, DBHandler) and acts as a controller in MVC design pattern '''
    def __init__(self, file_path:Path) -> None:
        self._db_handler = DBHandler(file_path) #composition 

    def add(self, qstn:str, ans:str) -> CurrentFlashCard:
        ''' retrieves dataset from db, adds a single flashcard to dataset then saves updated dataset to db '''
        flashcard:Tuple[str] = (qstn, ans)
        db_resp:DBResponse = self._db_handler.read_flashcard_dataset() 
        if db_resp.COMM_CODE == DB_READ_ERR_CODE_3:
            return CurrentFlashCard(flashcard, db_resp.COMM_CODE)
        if len(db_resp.dataset) == 0: # init it will be {}
            db_resp.dataset[0] = flashcard
        else: 
            db_resp.dataset[int(list(db_resp.dataset.keys())[-1]) + 1] = flashcard
        db_req:DBResponse = self._db_handler.write_flashcard_dataset(db_resp.dataset)
        return CurrentFlashCard(flashcard, db_req.COMM_CODE)

    def retrieve_dataset(self) -> Dict[int, Tuple[str]]:
        ''' return a copy of the dataset from the correct database file '''
        db_resp = self._db_handler.read_flashcard_dataset()
        return db_resp.dataset

    def get_flashcard(self, _id:str) -> Union[List[str], CurrentFlashCard]:
        ''' Reads db and retrieves single flashcard from dataset '''
        db_resp:DBResponse = self._db_handler.read_flashcard_dataset()
        if db_resp.COMM_CODE == DB_READ_ERR_CODE_3:
            return CurrentFlashCard((), db_resp.COMM_CODE)
        flashcard = db_resp.dataset[_id]
        return flashcard

    def edit_flashcard(self, flashcard:List[str], qstn_or_ans_resp:str, ui_input:str, _id:str):
        '''  '''
        if qstn_or_ans_resp == 'a':
            flashcard[1] = ui_input
        else:
            flashcard[0] = ui_input
        dataset = self.retrieve_dataset()
        dataset[_id] = flashcard
        db_req:DBResponse = self._db_handler.write_flashcard_dataset(dataset)
        return CurrentFlashCard(flashcard, db_req.COMM_CODE)

    def delete_dataset(self):
        '''  '''
        db_resp:DBResponse = self._db_handler.delete_flashcard_dataset()
        if db_resp.COMM_CODE == DB_READ_ERR_CODE_3:
            return CurrentFlashCard((), db_resp.COMM_CODE)
        return db_resp.COMM_CODE

    def delete_from_dataset(self,_id):
        '''  '''
        dataset = self.retrieve_dataset()
        del dataset[_id]
        db_req:DBResponse = self._db_handler.write_flashcard_dataset(dataset)
        return CurrentFlashCard((), db_req.COMM_CODE)
