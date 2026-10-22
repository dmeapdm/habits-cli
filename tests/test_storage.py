from datetime import date
from pathlib import Path

import pytest

from habits import core, storage

TODAY = date(2026, 10, 21)


def make_habit(name="Estudiar Python", completions=(), goal=None):
    return core.Habit(
        name=name,
        created_at=TODAY,
        completions=[date.fromisoformat(day) for day in completions],
        goal=goal,
    )


def test_load_returns_empty_list_when_file_does_not_exist(tmp_path):
    path = tmp_path / "habits.json"

    assert storage.load(path) == []


def test_save_writes_readable_json_with_version_and_habits(tmp_path):
    path = tmp_path / "habits.json"

    storage.save(path, [make_habit()])

    content = path.read_text(encoding="utf-8")
    assert '"version": 1' in content
    assert '"name": "Estudiar Python"' in content
    assert content.endswith("\n")


def test_save_creates_missing_parent_directory(tmp_path):
    path = tmp_path / "nested" / "folder" / "habits.json"

    storage.save(path, [make_habit()])

    assert path.exists()


def test_load_reads_back_the_habits_that_were_saved(tmp_path):
    path = tmp_path / "habits.json"
    habit = make_habit(completions=["2026-10-20", "2026-10-21"])

    storage.save(path, [habit])

    assert storage.load(path) == [habit]


def test_save_writes_the_goal_when_the_habit_has_one(tmp_path):
    path = tmp_path / "habits.json"

    storage.save(path, [make_habit(goal=3)])

    assert '"goal": 3' in path.read_text(encoding="utf-8")


def test_save_omits_the_goal_key_when_the_habit_has_none(tmp_path):
    path = tmp_path / "habits.json"

    storage.save(path, [make_habit()])

    assert '"goal"' not in path.read_text(encoding="utf-8")


def test_load_reads_back_the_goal_that_was_saved(tmp_path):
    path = tmp_path / "habits.json"
    habit = make_habit(completions=["2026-10-20"], goal=4)

    storage.save(path, [habit])

    assert storage.load(path) == [habit]


def test_load_reads_a_legacy_habit_as_having_no_goal(tmp_path):
    path = tmp_path / "habits.json"
    path.write_text(
        '{"version": 1, "habits": ['
        '{"name": "Leer", "created_at": "2026-10-01", '
        '"completions": ["2026-10-05"]}]}',
        encoding="utf-8",
    )

    habits = storage.load(path)

    assert habits[0].goal is None


@pytest.mark.parametrize("goal", ["0", "8", '"tres"', "true", "null", "3.5"])
def test_load_raises_error_for_invalid_goal_in_file(tmp_path, goal):
    path = tmp_path / "habits.json"
    path.write_text(
        '{"version": 1, "habits": ['
        '{"name": "Leer", "created_at": "2026-10-01", "completions": [], '
        f'"goal": {goal}]}}',
        encoding="utf-8",
    )

    with pytest.raises(storage.DataCorruptedError):
        storage.load(path)


def test_update_keeps_the_goal_of_a_habit(tmp_path):
    path = tmp_path / "habits.json"
    storage.save(path, [make_habit(goal=4)])

    result = storage.update(
        path, lambda habits: core.mark_done(habits, "Estudiar Python", TODAY)
    )

    assert result[0].goal == 4
    assert storage.load(path)[0].goal == 4


def test_load_raises_error_for_invalid_json(tmp_path):
    path = tmp_path / "habits.json"
    path.write_text("{esto no es json", encoding="utf-8")

    with pytest.raises(storage.DataCorruptedError):
        storage.load(path)


def test_load_raises_error_for_empty_file(tmp_path):
    path = tmp_path / "habits.json"
    path.write_text("", encoding="utf-8")

    with pytest.raises(storage.DataCorruptedError):
        storage.load(path)


def test_load_raises_error_for_unexpected_structure(tmp_path):
    path = tmp_path / "habits.json"
    path.write_text('{"habits": "texto"}', encoding="utf-8")

    with pytest.raises(storage.DataCorruptedError):
        storage.load(path)


def test_load_raises_error_for_habit_with_unexpected_shape(tmp_path):
    path = tmp_path / "habits.json"
    path.write_text('{"version": 1, "habits": [{"name": "Estudiar"}]}', encoding="utf-8")

    with pytest.raises(storage.DataCorruptedError):
        storage.load(path)


def test_update_does_not_overwrite_a_corrupted_file(tmp_path):
    path = tmp_path / "habits.json"
    original = "{esto no es json"
    path.write_text(original, encoding="utf-8")

    with pytest.raises(storage.DataCorruptedError):
        storage.update(path, lambda habits: habits + [make_habit()])

    assert path.read_text(encoding="utf-8") == original


def test_update_saves_the_result_of_the_change(tmp_path):
    path = tmp_path / "habits.json"

    result = storage.update(path, lambda habits: habits + [make_habit()])

    assert len(result) == 1
    assert storage.load(path) == result


def test_default_data_path_lives_in_the_user_home():
    path = storage.default_data_path()

    assert path.parent.name == ".habits-cli"
    assert path.name == "habits.json"
    assert path.parent.parent == Path.home()
