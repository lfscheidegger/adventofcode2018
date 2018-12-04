#!/usr/bin/python

"""
--- Part Two ---
Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)
"""

from collections import defaultdict

import re

TIME_GROUP = r"\[(\d\d\d\d-\d\d-\d\d) (23|00):(\d\d)\]"

BEGIN_SHIFT_REGEX = re.compile(TIME_GROUP + r" Guard #(\d+) begins shift")
FALLS_ASLEEP_REGEX = re.compile(TIME_GROUP + r" falls asleep")
WAKES_UP_REGEX = re.compile(TIME_GROUP + r" wakes up")


class Guard:
    def __init__(self, guard_id, shifts):
        self.guard_id = guard_id
        self.shifts = shifts

        asleep_count_by_minute = defaultdict(int)
        for shift in shifts:
            for idx in range(len(shift)):
                if shift[idx] == 'S': asleep_count_by_minute[idx] += 1

        most_asleep_count = -1
        most_asleep_idx = -1
        for minute_idx in asleep_count_by_minute:
            if asleep_count_by_minute[minute_idx] > most_asleep_count:
                most_asleep_count = asleep_count_by_minute[minute_idx]
                most_asleep_idx = minute_idx

        self.most_asleep_minute = (most_asleep_idx, most_asleep_count)

    def guard_score(self):
        return self.most_asleep_minute[0] * int(self.guard_id)

    def count_asleep(self):
        return len(filter(lambda x: x == "S", "".join(self.shifts)))

    def __repr__(self):
        return "Guard(guard_id=%s, shifts=[%s])" % (self.guard_id, "\n".join(self.shifts))


def parse_single_night(lines):
    begin_shift_match = BEGIN_SHIFT_REGEX.match(lines[0])
    assert begin_shift_match is not None

    guard_id = begin_shift_match.groups()[3]
    date = begin_shift_match.groups()[0]

    minute_last_woke_up = 0 if begin_shift_match.groups()[1] != "00" \
                          else int(begin_shift_match.groups()[2])
    minute_last_fell_asleep = None

    minutes = '.' * minute_last_woke_up
    
    for l in lines[1:]:
        falls_asleep_match = FALLS_ASLEEP_REGEX.match(l)
        wakes_up_match = WAKES_UP_REGEX.match(l)
        if falls_asleep_match is not None:
            assert minute_last_fell_asleep is None
            assert minute_last_woke_up is not None
            assert falls_asleep_match.groups()[1] == "00"

            minute_last_fell_asleep = int(falls_asleep_match.groups()[2])
            minutes += 'A' * (minute_last_fell_asleep - minute_last_woke_up)
            minute_last_woke_up = None
        elif wakes_up_match is not None:
            assert minute_last_fell_asleep is not None
            assert minute_last_woke_up is None
            
            minute_last_woke_up = int(wakes_up_match.groups()[2])
            minutes += 'S' * (minute_last_woke_up - minute_last_fell_asleep)
            minute_last_fell_asleep = None
        else:
            raise Error("Can't parse " + l)
    
    if minute_last_fell_asleep is None:
        # Guard ends their shift awake
        assert minute_last_woke_up is not None
        minutes += 'A' * (60 - minute_last_woke_up)
    else:
        # Guard ends their shift awake
        assert minute_last_woke_up is None
        minutes += 'S' * (60 - minute_last_fell_asleep)

    assert len(minutes) == 60, len(minutes)
    return (guard_id, minutes)
        
def get_input():
    lines = []
    try:
        while True:
            lines.append(raw_input())
    except EOFError:
        pass
    lines = sorted(lines)
    
    shifts_by_guard_id = defaultdict(list)

    lines_in_single_night = None
    for l in lines:
        if BEGIN_SHIFT_REGEX.match(l) is not None:
            if lines_in_single_night is None:
                # First guard of the data
                lines_in_single_night = [l]
            else:
                # Switching to a new guard
                single_night = parse_single_night(lines_in_single_night)
                shifts_by_guard_id[single_night[0]].append(single_night[1])
                lines_in_single_night = [l]
        else:
            lines_in_single_night.append(l)

    # Last guard
    single_night = parse_single_night(lines_in_single_night)
    shifts_by_guard_id[single_night[0]].append(single_night[1])

    return list(map(lambda guard_id: Guard(guard_id, shifts_by_guard_id[guard_id]), shifts_by_guard_id))    

def main():
    guards = get_input()
    the_guard = max(guards, key=lambda x: x.most_asleep_minute[1])
    print the_guard.guard_score()
    
if __name__ == "__main__":
    main()
