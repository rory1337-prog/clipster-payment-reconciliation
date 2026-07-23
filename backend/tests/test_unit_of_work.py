from unittest.mock import Mock

from backend.app.db.unit_of_work import UnitOfWork


def test_unit_of_work_commits_on_success() -> None:
    session = Mock()

    with UnitOfWork(session):
        pass

    session.commit.assert_called_once()
    session.rollback.assert_not_called()
    session.close.assert_called_once()


def test_unit_of_work_rolls_back_on_error() -> None:
    session = Mock()

    try:
        with UnitOfWork(session):
            raise ValueError("boom")
    except ValueError:
        pass

    session.rollback.assert_called_once()
    session.commit.assert_not_called()
    session.close.assert_called_once()
