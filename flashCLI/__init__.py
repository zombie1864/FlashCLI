from pathlib import Path 

__app_name__ = 'FlashCLI'
__version__ = '0.1.0'

(
    SUCC_CODE_0, 
    DIR_ERR_CODE_1, 
    FILE_ERR_CODE_2, 
    DB_READ_ERR_CODE_3, 
    DB_WRITE_ERR_CODE_4,
    JSON_ERR_CODE_5
) = range(6)

DB_DIR_PATH:Path = Path(__file__).cwd() / 'flashcards_db'