#!/usr/bin/python

"""
--- Day 4: Repose Record ---
You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab. You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this is as close as you can safely get.

As you search the closet for anything that might help, you discover that you're not the first person to want to sneak in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the one whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....
The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour. (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)
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

        self.most_asleep_minute = most_asleep_idx

    def guard_score(self):
        return self.most_asleep_minute * int(self.guard_id)

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
    the_guard = max(guards, key=Guard.count_asleep)
    print the_guard.guard_score()
    
if __name__ == "__main__":
    main()
