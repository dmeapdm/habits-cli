from datetime import date

import pytest

from habits import cli

TODAY = date(2026, 10, 21)


@pytest.fixture
def data_path(tmp_path):
    return tmp_path / "habits.json"


def run(argv, data_path, capsys, today=TODAY):
    code = cli.main(argv, path=data_path, today=today)
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_add_creates_the_habit_and_confirms_it(data_path, capsys):
    code, out, err = run(["add", "Estudiar Python"], data_path, capsys)

    assert code == 0
    assert "Estudiar Python" in out
    assert err == ""


def test_add_rejects_a_duplicate(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["add", "estudiar python"], data_path, capsys)

    assert code == 1
    assert "ya existe" in err
    assert out == ""


def test_add_rejects_an_empty_name(data_path, capsys):
    code, out, err = run(["add", "   "], data_path, capsys)

    assert code == 1
    assert "vacío" in err


def test_add_without_name_is_a_usage_error(data_path, capsys):
    code, out, err = run(["add"], data_path, capsys)

    assert code == 2
    assert "falta el nombre" in err


def test_add_with_goal_uses_it(data_path, capsys):
    code, out, err = run(["add", "Estudiar Python", "--goal", "3"], data_path, capsys)

    assert code == 0
    assert err == ""
    _, out, _ = run(["list"], data_path, capsys)
    assert "esta semana 0/3" in out


def test_add_without_goal_uses_the_default_goal(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)

    _, out, _ = run(["list"], data_path, capsys)

    assert "esta semana 0/5" in out


def test_goal_does_not_depend_on_the_week(data_path, capsys):
    run(
        ["add", "Estudiar Python", "--goal", "3"],
        data_path,
        capsys,
        today=date(2026, 10, 25),
    )

    _, out, _ = run(["list"], data_path, capsys, today=date(2026, 10, 26))

    assert "esta semana 0/3" in out


@pytest.mark.parametrize("goal", ["abc", "0", "8", "-1"])
def test_add_with_an_invalid_goal_is_a_business_error(data_path, capsys, goal):
    code, out, err = run(
        ["add", "Estudiar Python", "--goal", goal], data_path, capsys
    )

    assert code == 1
    assert "objetivo" in err
    assert out == ""


def test_edit_changes_the_goal(data_path, capsys):
    run(["add", "Estudiar Python", "--goal", "3"], data_path, capsys)

    code, out, err = run(["edit", "Estudiar Python", "--goal", "2"], data_path, capsys)

    assert code == 0
    assert "actualizado" in out
    _, out, _ = run(["list"], data_path, capsys)
    assert "esta semana 0/2" in out


def test_edit_keeps_the_history_and_recalculates_the_progress(data_path, capsys):
    run(["add", "Estudiar Python", "--goal", "5"], data_path, capsys)
    run(["done", "Estudiar Python"], data_path, capsys)

    run(["edit", "Estudiar Python", "--goal", "2"], data_path, capsys)

    _, out, _ = run(["list"], data_path, capsys)

    assert "racha 1 día" in out
    assert "esta semana 1/2" in out


def test_edit_with_an_invalid_goal_is_a_business_error(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["edit", "Estudiar Python", "--goal", "9"], data_path, capsys)

    assert code == 1
    assert "objetivo" in err
    assert out == ""


def test_edit_of_an_unknown_habit_is_an_error(data_path, capsys):
    code, out, err = run(["edit", "Estudiar Python", "--goal", "3"], data_path, capsys)

    assert code == 1
    assert "no existe" in err


def test_edit_without_goal_is_a_usage_error(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["edit", "Estudiar Python"], data_path, capsys)

    assert code == 2
    assert "falta el objetivo" in err


def test_edit_without_name_is_a_usage_error(data_path, capsys):
    code, out, err = run(["edit", "--goal", "3"], data_path, capsys)

    assert code == 2
    assert "falta el nombre" in err


def test_unknown_command_is_a_usage_error(data_path, capsys):
    code, out, err = run(["borrar", "Estudiar Python"], data_path, capsys)

    assert code == 2
    assert "orden desconocida" in err
    assert "edit" in err


def test_without_command_is_a_usage_error(data_path, capsys):
    code, out, err = run([], data_path, capsys)

    assert code == 2
    assert "falta la orden" in err


def test_usage_errors_are_reported_in_spanish(data_path, capsys):
    code, out, err = run(["add"], data_path, capsys)

    assert "the following arguments are required" not in err
    assert "usage:" not in err


def test_done_marks_the_habit_as_done_today(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["done", "Estudiar Python"], data_path, capsys)

    assert code == 0
    assert "marcado" in out
    assert err == ""


def test_done_twice_is_idempotent(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)
    run(["done", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["done", "Estudiar Python"], data_path, capsys)

    assert code == 0
    assert "ya estaba" in out


def test_done_finds_the_habit_ignoring_case_and_spaces(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["done", "  ESTUDIAR PYTHON "], data_path, capsys)

    assert code == 0
    assert "marcado" in out


def test_done_of_an_unknown_habit_suggests_the_list(data_path, capsys):
    code, out, err = run(["done", "Estudiar Python"], data_path, capsys)

    assert code == 1
    assert "habits list" in err


def test_list_shows_the_habits_with_their_streak(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)
    run(["done", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["list"], data_path, capsys)

    assert code == 0
    assert "Estudiar Python" in out
    assert "— racha 1 día —" in out


def test_list_uses_the_plural_for_several_days(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)
    run(["done", "Estudiar Python"], data_path, capsys)
    run(["done", "Estudiar Python"], data_path, capsys, today=date(2026, 10, 22))

    code, out, err = run(["list"], data_path, capsys, today=date(2026, 10, 22))

    assert "racha 2 días" in out


def test_list_sorts_by_streak_and_then_by_name(data_path, capsys):
    run(["add", "Leer"], data_path, capsys)
    run(["add", "Estudiar Python"], data_path, capsys)
    run(["done", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["list"], data_path, capsys)

    assert out.index("Estudiar Python") < out.index("Leer")


def test_list_without_habits_invites_to_create_the_first(data_path, capsys):
    code, out, err = run(["list"], data_path, capsys)

    assert code == 0
    assert "habits add" in out
    assert err == ""


def test_list_shows_the_last_completion_date(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)
    run(["done", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["list"], data_path, capsys)

    assert "2026-10-21" in out


def test_list_shows_that_a_habit_has_no_completions_yet(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["list"], data_path, capsys)

    assert "sin días completados" in out


def test_list_shows_the_weekly_progress(data_path, capsys):
    run(["add", "Estudiar Python", "--goal", "5"], data_path, capsys)
    run(["done", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["list"], data_path, capsys)

    assert code == 0
    assert "esta semana 1/5" in out


def test_list_shows_the_progress_above_the_goal(data_path, capsys):
    run(["add", "Estudiar Python", "--goal", "2"], data_path, capsys)
    run(["done", "Estudiar Python"], data_path, capsys, today=date(2026, 10, 19))
    run(["done", "Estudiar Python"], data_path, capsys, today=date(2026, 10, 20))
    run(["done", "Estudiar Python"], data_path, capsys)

    code, out, err = run(["list"], data_path, capsys)

    assert "esta semana 3/2" in out


def test_list_shows_no_goal_for_a_legacy_habit(data_path, capsys):
    data_path.write_text(
        '{"version": 1, "habits": ['
        '{"name": "Leer", "created_at": "2026-10-01", "completions": []}]}',
        encoding="utf-8",
    )

    code, out, err = run(["list"], data_path, capsys)

    assert code == 0
    assert "sin objetivo" in out


def test_rm_deletes_the_habit(data_path, capsys):
    run(["add", "Estudiar Python"], data_path, capsys)
    run(["add", "Leer"], data_path, capsys)

    code, out, err = run(["rm", "Estudiar Python"], data_path, capsys)

    assert code == 0
    assert "eliminado" in out
    _, out, _ = run(["list"], data_path, capsys)
    assert "Estudiar Python" not in out
    assert "Leer" in out


def test_rm_of_an_unknown_habit_is_an_error(data_path, capsys):
    code, out, err = run(["rm", "Estudiar Python"], data_path, capsys)

    assert code == 1
    assert "no existe" in err


def test_a_corrupted_file_is_not_overwritten(data_path, capsys):
    original = "{esto no es json"
    data_path.write_text(original, encoding="utf-8")

    code, out, err = run(["add", "Estudiar Python"], data_path, capsys)

    assert code == 1
    assert err != ""
    assert data_path.read_text(encoding="utf-8") == original
