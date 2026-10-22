from datetime import date, timedelta

import pytest

from habits import core

TODAY = date(2026, 10, 21)


def test_add_habit_creates_habit_with_creation_date():
    habits = core.add_habit([], "Estudiar Python", TODAY)

    assert len(habits) == 1
    assert habits[0].name == "Estudiar Python"
    assert habits[0].created_at == TODAY
    assert habits[0].completions == []


def test_add_habit_trims_surrounding_whitespace():
    habits = core.add_habit([], "  Estudiar Python  ", TODAY)

    assert habits[0].name == "Estudiar Python"


def test_add_habit_rejects_duplicate_ignoring_case_and_spaces():
    habits = core.add_habit([], "Estudiar Python", TODAY)

    with pytest.raises(core.DuplicateHabitError):
        core.add_habit(habits, "  estudiar python ", TODAY)


def test_add_habit_rejects_empty_name():
    with pytest.raises(core.InvalidNameError):
        core.add_habit([], "", TODAY)


def test_add_habit_rejects_whitespace_only_name():
    with pytest.raises(core.InvalidNameError):
        core.add_habit([], "   ", TODAY)


def test_add_habit_does_not_mutate_the_given_list():
    habits = [core.Habit(name="Leer", created_at=TODAY)]

    result = core.add_habit(habits, "Estudiar Python", TODAY)

    assert habits == [core.Habit(name="Leer", created_at=TODAY)]
    assert result is not habits


def test_add_habit_uses_the_default_goal_when_no_goal_is_given():
    habits = core.add_habit([], "Estudiar Python", TODAY)

    assert habits[0].goal == core.DEFAULT_WEEKLY_GOAL


def test_add_habit_uses_the_default_goal_when_the_goal_is_none():
    habits = core.add_habit([], "Estudiar Python", TODAY, goal=None)

    assert habits[0].goal == core.DEFAULT_WEEKLY_GOAL


def test_add_habit_accepts_an_explicit_goal():
    habits = core.add_habit([], "Estudiar Python", TODAY, goal=3)

    assert habits[0].goal == 3


def test_add_habit_accepts_a_goal_given_as_text():
    habits = core.add_habit([], "Estudiar Python", TODAY, goal="3")

    assert habits[0].goal == 3


@pytest.mark.parametrize("goal", [0, 8, -1])
def test_add_habit_rejects_a_goal_out_of_range(goal):
    with pytest.raises(core.InvalidGoalError):
        core.add_habit([], "Estudiar Python", TODAY, goal=goal)


@pytest.mark.parametrize("goal", ["abc", "", "3.5"])
def test_add_habit_rejects_a_non_numeric_goal(goal):
    with pytest.raises(core.InvalidGoalError):
        core.add_habit([], "Estudiar Python", TODAY, goal=goal)


def test_habit_round_trips_through_dict():
    habit = core.Habit(
        name="Estudiar Python",
        created_at=TODAY,
        completions=[date(2026, 10, 20), date(2026, 10, 21)],
    )

    assert core.Habit.from_dict(habit.to_dict()) == habit


def test_habit_from_dict_rejects_malformed_data():
    with pytest.raises(ValueError):
        core.Habit.from_dict({"name": "Estudiar Python", "created_at": "ayer"})


def test_mark_done_adds_today_to_completions():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY)

    result = core.mark_done([habit], "Estudiar Python", TODAY)

    assert result[0].completions == [TODAY]


def test_mark_done_keeps_previous_completions():
    habit = core.Habit(
        name="Estudiar Python",
        created_at=TODAY,
        completions=[date(2026, 10, 19)],
    )

    result = core.mark_done([habit], "Estudiar Python", TODAY)

    assert result[0].completions == [date(2026, 10, 19), TODAY]


def test_mark_done_is_idempotent():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY, completions=[TODAY])

    result = core.mark_done([habit], "Estudiar Python", TODAY)

    assert result[0].completions == [TODAY]


def test_mark_done_finds_habit_ignoring_case_and_spaces():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY)

    result = core.mark_done([habit], "  estudiar python ", TODAY)

    assert result[0].completions == [TODAY]


def test_mark_done_raises_not_found_for_unknown_habit():
    with pytest.raises(core.HabitNotFoundError):
        core.mark_done([], "Estudiar Python", TODAY)


def test_mark_done_does_not_mutate_the_given_habit():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY)

    core.mark_done([habit], "Estudiar Python", TODAY)

    assert habit.completions == []


def test_remove_habit_deletes_the_habit_with_its_history():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY, completions=[TODAY])

    result = core.remove_habit([habit], "Estudiar Python")

    assert result == []


def test_remove_habit_keeps_the_other_habits():
    keep = core.Habit(name="Leer", created_at=TODAY)
    drop = core.Habit(name="Estudiar Python", created_at=TODAY)

    result = core.remove_habit([keep, drop], "Estudiar Python")

    assert result == [keep]


def test_remove_habit_finds_habit_ignoring_case_and_spaces():
    drop = core.Habit(name="Estudiar Python", created_at=TODAY)
    keep = core.Habit(name="Leer", created_at=TODAY)

    result = core.remove_habit([keep, drop], "  ESTUDIAR PYTHON ")

    assert result == [keep]


def test_remove_habit_raises_not_found_for_unknown_habit():
    with pytest.raises(core.HabitNotFoundError):
        core.remove_habit([], "Estudiar Python")


def test_calculate_streak_is_zero_without_completions():
    assert core.calculate_streak([], TODAY) == 0


def test_calculate_streak_counts_a_single_day():
    assert core.calculate_streak([TODAY], TODAY) == 1


def test_calculate_streak_is_alive_when_the_last_day_is_yesterday():
    yesterday = date(2026, 10, 20)

    assert core.calculate_streak([yesterday], TODAY) == 1


def test_calculate_streak_is_zero_when_the_last_day_is_older_than_yesterday():
    assert core.calculate_streak([date(2026, 10, 19)], TODAY) == 0


def test_calculate_streak_counts_consecutive_days():
    days = [date(2026, 10, 19), date(2026, 10, 20), TODAY]

    assert core.calculate_streak(days, TODAY) == 3


def test_calculate_streak_stops_at_the_gap():
    days = [date(2026, 10, 18), date(2026, 10, 20), TODAY]

    assert core.calculate_streak(days, TODAY) == 2


def test_calculate_streak_ignores_future_dates():
    days = [date(2026, 10, 20), TODAY, date(2026, 10, 22)]

    assert core.calculate_streak(days, TODAY) == 2


def test_calculate_streak_is_zero_with_only_future_dates():
    assert core.calculate_streak([date(2026, 10, 22)], TODAY) == 0


def test_calculate_streak_ignores_duplicated_dates():
    assert core.calculate_streak([TODAY, TODAY], TODAY) == 1


def test_list_habits_returns_empty_list_without_habits():
    assert core.list_habits([], TODAY) == []


def test_list_habits_sorts_by_streak_descending():
    low = core.Habit(name="Leer", created_at=TODAY)
    high = core.Habit(
        name="Estudiar Python",
        created_at=TODAY,
        completions=[date(2026, 10, 20), TODAY],
    )

    result = core.list_habits([low, high], TODAY)

    assert [summary.name for summary in result] == ["Estudiar Python", "Leer"]


def test_list_habits_sorts_by_name_when_streak_is_equal():
    first = core.Habit(name="Leer", created_at=TODAY)
    second = core.Habit(name="Estudiar Python", created_at=TODAY)

    result = core.list_habits([first, second], TODAY)

    assert [summary.name for summary in result] == ["Estudiar Python", "Leer"]


def test_list_habits_reports_the_streak():
    habit = core.Habit(
        name="Estudiar Python",
        created_at=TODAY,
        completions=[date(2026, 10, 20), TODAY],
    )

    result = core.list_habits([habit], TODAY)

    assert result[0].streak == 2


def test_list_habits_reports_the_last_completion():
    habit = core.Habit(
        name="Estudiar Python",
        created_at=TODAY,
        completions=[date(2026, 10, 19), date(2026, 10, 20)],
    )

    result = core.list_habits([habit], TODAY)

    assert result[0].last_completion == date(2026, 10, 20)


def test_list_habits_reports_no_last_completion_without_completions():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY)

    result = core.list_habits([habit], TODAY)

    assert result[0].last_completion is None


def test_list_habits_ignores_future_dates_in_the_last_completion():
    habit = core.Habit(
        name="Estudiar Python",
        created_at=TODAY,
        completions=[date(2026, 10, 20), date(2026, 10, 22)],
    )

    result = core.list_habits([habit], TODAY)

    assert result[0].last_completion == date(2026, 10, 20)


def test_default_weekly_goal_is_five():
    assert core.DEFAULT_WEEKLY_GOAL == 5


def test_habit_to_dict_includes_the_goal():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY, goal=3)

    assert habit.to_dict()["goal"] == 3


def test_habit_to_dict_omits_the_goal_when_the_habit_has_none():
    habit = core.Habit(name="Leer", created_at=TODAY)

    assert "goal" not in habit.to_dict()


def test_habit_from_dict_reads_the_goal():
    habit = core.Habit.from_dict(
        {
            "name": "Estudiar Python",
            "created_at": "2026-10-21",
            "completions": [],
            "goal": 3,
        }
    )

    assert habit.goal == 3


def test_habit_from_dict_without_goal_key_reads_no_goal():
    habit = core.Habit.from_dict(
        {"name": "Leer", "created_at": "2026-10-01", "completions": []}
    )

    assert habit.goal is None


def test_habit_round_trips_with_goal():
    habit = core.Habit(
        name="Estudiar Python",
        created_at=TODAY,
        completions=[date(2026, 10, 20)],
        goal=4,
    )

    assert core.Habit.from_dict(habit.to_dict()) == habit


@pytest.mark.parametrize("goal", [0, 8, -1])
def test_habit_from_dict_rejects_goal_out_of_range(goal):
    data = {"name": "Estudiar Python", "created_at": "2026-10-21", "completions": []}

    with pytest.raises(ValueError):
        core.Habit.from_dict({**data, "goal": goal})


@pytest.mark.parametrize("goal", ["tres", 3.0, True, None])
def test_habit_from_dict_rejects_non_integer_goal(goal):
    data = {"name": "Estudiar Python", "created_at": "2026-10-21", "completions": []}

    with pytest.raises(ValueError):
        core.Habit.from_dict({**data, "goal": goal})


def test_parse_goal_accepts_a_valid_number():
    assert core.parse_goal("3") == 3
    assert core.parse_goal(" 7 ") == 7


@pytest.mark.parametrize("text", ["abc", "", "3.5", "-1", "ocho"])
def test_parse_goal_rejects_non_integer_text(text):
    with pytest.raises(core.InvalidGoalError):
        core.parse_goal(text)


@pytest.mark.parametrize("text", ["0", "8", "-1"])
def test_parse_goal_rejects_values_out_of_range(text):
    with pytest.raises(core.InvalidGoalError):
        core.parse_goal(text)


def test_week_start_on_monday_is_the_same_day():
    monday = date(2026, 10, 19)

    assert core.week_start(monday) == monday


def test_week_start_on_tuesday_is_the_monday():
    assert core.week_start(date(2026, 10, 20)) == date(2026, 10, 19)


def test_week_start_on_sunday_is_the_previous_monday():
    assert core.week_start(date(2026, 10, 25)) == date(2026, 10, 19)


def test_weekly_completed_is_zero_without_completions():
    assert core.weekly_completed([], TODAY) == 0


def test_weekly_completed_counts_days_inside_the_current_week():
    days = [date(2026, 10, 19), date(2026, 10, 20), TODAY]

    assert core.weekly_completed(days, TODAY) == 3


def test_weekly_completed_ignores_days_before_the_week():
    days = [date(2026, 10, 18), TODAY]

    assert core.weekly_completed(days, TODAY) == 1


def test_weekly_completed_ignores_days_after_the_week():
    days = [TODAY, date(2026, 10, 26)]

    assert core.weekly_completed(days, TODAY) == 1


def test_weekly_completed_ignores_future_days_within_the_week():
    days = [TODAY, date(2026, 10, 25)]

    assert core.weekly_completed(days, TODAY) == 1


def test_weekly_completed_ignores_duplicated_days():
    days = [TODAY, TODAY]

    assert core.weekly_completed(days, TODAY) == 1


def test_weekly_completed_counts_the_whole_week_on_sunday():
    sunday = date(2026, 10, 25)
    days = [date(2026, 10, 19) + timedelta(days=offset) for offset in range(7)]

    assert core.weekly_completed(days, sunday) == 7


def test_set_goal_changes_the_goal():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY, goal=5)

    result = core.set_goal([habit], "Estudiar Python", 3)

    assert result[0].goal == 3


def test_set_goal_accepts_a_goal_given_as_text():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY, goal=5)

    result = core.set_goal([habit], "Estudiar Python", "2")

    assert result[0].goal == 2


def test_set_goal_keeps_name_creation_date_and_history():
    habit = core.Habit(
        name="Estudiar Python",
        created_at=date(2026, 10, 1),
        completions=[date(2026, 10, 19), TODAY],
        goal=5,
    )

    result = core.set_goal([habit], "Estudiar Python", 2)

    assert result[0].name == "Estudiar Python"
    assert result[0].created_at == date(2026, 10, 1)
    assert result[0].completions == [date(2026, 10, 19), TODAY]


def test_set_goal_assigns_a_goal_to_a_habit_without_one():
    habit = core.Habit(name="Leer", created_at=TODAY)

    result = core.set_goal([habit], "Leer", 4)

    assert result[0].goal == 4


def test_set_goal_finds_habit_ignoring_case_and_spaces():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY, goal=5)

    result = core.set_goal([habit], "  estudiar python ", 3)

    assert result[0].goal == 3


def test_set_goal_keeps_the_other_habits():
    keep = core.Habit(name="Leer", created_at=TODAY, goal=4)
    change = core.Habit(name="Estudiar Python", created_at=TODAY, goal=5)

    result = core.set_goal([keep, change], "Estudiar Python", 2)

    assert result[0] == keep
    assert result[1].goal == 2


def test_set_goal_does_not_mutate_the_given_habit():
    habit = core.Habit(name="Estudiar Python", created_at=TODAY, goal=5)

    core.set_goal([habit], "Estudiar Python", 2)

    assert habit.goal == 5


def test_set_goal_raises_not_found_for_unknown_habit():
    with pytest.raises(core.HabitNotFoundError):
        core.set_goal([], "Estudiar Python", 3)


@pytest.mark.parametrize("goal", [0, 8, -1, "abc", ""])
def test_set_goal_rejects_an_invalid_goal(goal):
    habit = core.Habit(name="Estudiar Python", created_at=TODAY, goal=5)

    with pytest.raises(core.InvalidGoalError):
        core.set_goal([habit], "Estudiar Python", goal)