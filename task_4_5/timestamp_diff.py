from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP


def _parse_timestamp(value: str) -> datetime:
    return datetime.strptime(value, '%Y/%m/%d %H:%M')


def _round_half_up_hours(total_hours: float) -> int:
    return int(Decimal(str(total_hours)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def hours_difference(start: str, end: str) -> int:
    """Return the rounded full-hour difference between two timestamps."""
    start_dt = _parse_timestamp(start)
    end_dt = _parse_timestamp(end)
    if end_dt < start_dt:
        start_dt, end_dt = end_dt, start_dt
    delta_hours = (end_dt - start_dt).total_seconds() / 3600
    return _round_half_up_hours(delta_hours)


def business_hours_difference(start: str, end: str) -> int:
    """Compute the full-hour difference only within weekdays and 09:00-17:00."""
    start_dt = _parse_timestamp(start)
    end_dt = _parse_timestamp(end)

    if end_dt < start_dt:
        start_dt, end_dt = end_dt, start_dt

    total_seconds = 0.0
    current_day = start_dt.date()
    while current_day <= end_dt.date():
        if current_day.weekday() < 5:
            business_start = datetime.combine(current_day, datetime.min.time()).replace(hour=9, minute=0)
            business_end = datetime.combine(current_day, datetime.min.time()).replace(hour=17, minute=0)
            overlap_start = max(start_dt, business_start)
            overlap_end = min(end_dt, business_end)
            if overlap_end > overlap_start:
                total_seconds += (overlap_end - overlap_start).total_seconds()

        current_day += timedelta(days=1)

    return _round_half_up_hours(total_seconds / 3600)


if __name__ == '__main__':
    print(hours_difference('2022/02/15 00:05', '2022/02/15 01:00'))
    print(business_hours_difference('2022/02/15 08:30', '2022/02/15 17:30'))
