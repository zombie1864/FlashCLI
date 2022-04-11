import pytest 
from click.testing import CliRunner
from flashCLI.__main__ import main 
import json 
from flashCLI import utils, SUCC_CODE_0

'''  to run test `>>> python -m pytest tests/` '''


def test_edit():
    runner = CliRunner()
    result = runner.invoke(main, ['edit'])
    assert result.exit_code == 0
    assert 'edit' in result.output


@pytest.fixture()
def mock_json_file(tmp_path):
    ''' creates and returns a temp json file, db_file, w a single flashcard 
    []_in this fixture you use tmp_path, which is a pathlib.Path obj that pytest uses to provide a tmp 
    dir for testing purposes 
    []_provides a tmp db to use for testing 
    '''
    flashcard = {
        0: ('what is 1 + 1', '2')
    }
    db_file = tmp_path / 'dummy_flashcard_db.json'
    with db_file.open('w') as db:
        json.dump(flashcard, db, indent=4)
    return db_file


def test_add(mock_json_file):
    '''  '''
    print('\n----------[ START ]----------\n')
    print(mock_json_file)
    print('\n----------[ END ]----------\n') 
    controller_inst = utils.FlashcardController(mock_json_file)
    controller_inst_flashcard, controller_inst_COMM_CODE = controller_inst.add(
        'what year were you born in?', '1993'
    )
    assert controller_inst_COMM_CODE == SUCC_CODE_0
    assert controller_inst_flashcard == ('what year were you born in?', '1993')
    read_res = controller_inst._db_handler.read_flashcard_set()
    assert len(read_res.flashcard_stack) == 2