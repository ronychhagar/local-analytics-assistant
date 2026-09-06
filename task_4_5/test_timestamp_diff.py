from task_4_5.timestamp_diff import business_hours_difference, hours_difference


def test_hours_difference_rounds_to_full_hours():
    assert hours_difference('2022/02/15 00:05', '2022/02/15 01:00') == 1
    assert hours_difference('2022/02/15 12:00', '2022/02/15 14:30') == 3


def test_business_hours_difference_only_counts_weekdays_and_9_17_window():
    assert business_hours_difference('2022/02/15 08:30', '2022/02/15 17:30') == 8
    assert business_hours_difference('2022/02/18 09:00', '2022/02/21 10:00') == 9
