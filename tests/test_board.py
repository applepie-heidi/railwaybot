import pytest

from board import Board, City, Railway

BOARD_FILENAME = "data/jsons/board.json"


@pytest.fixture
def board():
    return Board(BOARD_FILENAME)


@pytest.fixture(scope="session")
def global_board(board):
    return board


def test_can_create_board(board):
    assert board is not None
    assert len(board.board) == 36

