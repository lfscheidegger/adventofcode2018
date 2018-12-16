#!/usr/bin/python

"""
--- Part Two ---
Using the samples you collected, work out the number of each opcode and execute the test program (the second section of your puzzle input).

What value is contained in register 0 after executing the test program?
"""

from collections import defaultdict

import multiprocessing
import re
import sys
import time

BEFORE_REGEX = re.compile(r"Before: \[(\d+), (\d+), (\d+), (\d+)\]")
AFTER_REGEX = re.compile(r"After:  \[(\d+), (\d+), (\d+), (\d+)\]")

PROGRAM = \
"""2 0 1 1
2 2 2 3
2 0 0 2
3 2 3 1
8 1 2 1
13 1 0 0
12 0 1 1
2 3 1 3
2 2 0 0
2 3 3 2
9 0 2 2
8 2 3 2
13 2 1 1
12 1 3 3
2 2 3 1
2 3 3 0
2 1 2 2
7 0 1 1
8 1 2 1
8 1 1 1
13 3 1 3
12 3 1 1
8 0 0 2
15 2 0 2
2 1 2 0
2 2 3 3
8 0 2 0
8 0 1 0
13 1 0 1
2 1 0 0
2 0 2 3
2 2 0 2
6 2 3 2
8 2 3 2
13 2 1 1
12 1 2 3
8 1 0 2
15 2 2 2
2 2 3 1
12 0 2 1
8 1 2 1
13 1 3 3
12 3 3 2
8 0 0 0
15 0 2 0
2 0 1 1
2 2 0 3
4 0 3 3
8 3 3 3
13 2 3 2
12 2 3 3
2 1 1 1
2 2 2 2
10 1 0 0
8 0 1 0
13 0 3 3
12 3 0 2
2 2 0 0
2 1 3 3
11 0 3 0
8 0 2 0
13 2 0 2
12 2 3 3
2 1 0 0
2 1 1 2
13 1 0 2
8 2 2 2
13 2 3 3
2 0 0 1
2 3 0 2
15 0 1 2
8 2 3 2
8 2 2 2
13 2 3 3
12 3 0 1
2 2 3 0
2 0 0 3
2 3 3 2
5 0 2 0
8 0 2 0
13 1 0 1
12 1 2 3
2 1 0 0
2 1 3 2
8 0 0 1
15 1 0 1
15 0 1 1
8 1 1 1
13 1 3 3
12 3 0 1
8 1 0 2
15 2 3 2
2 2 0 3
8 3 0 0
15 0 2 0
4 0 3 2
8 2 2 2
13 2 1 1
12 1 0 2
8 1 0 1
15 1 1 1
2 1 3 0
10 1 3 3
8 3 1 3
13 2 3 2
12 2 2 0
2 0 1 2
2 2 2 3
2 2 1 1
3 2 3 1
8 1 3 1
13 0 1 0
12 0 1 1
2 3 2 0
2 0 2 3
9 2 0 0
8 0 2 0
8 0 3 0
13 1 0 1
12 1 0 2
2 0 1 0
2 0 2 1
8 3 0 3
15 3 2 3
2 3 0 0
8 0 1 0
8 0 1 0
13 0 2 2
12 2 0 3
2 0 0 2
2 3 0 0
9 2 0 2
8 2 2 2
8 2 2 2
13 2 3 3
12 3 3 1
8 2 0 3
15 3 2 3
2 1 2 0
2 1 3 2
13 0 0 2
8 2 3 2
13 2 1 1
2 2 2 2
2 2 2 0
4 0 3 3
8 3 2 3
13 3 1 1
12 1 3 0
2 1 0 2
8 3 0 1
15 1 3 1
8 1 0 3
15 3 1 3
15 3 1 2
8 2 1 2
8 2 3 2
13 2 0 0
12 0 1 1
2 3 2 2
2 1 1 0
2 0 3 3
8 0 2 0
8 0 3 0
13 0 1 1
12 1 3 0
2 2 0 3
2 1 1 1
8 1 0 2
15 2 0 2
3 2 3 1
8 1 1 1
13 0 1 0
12 0 0 1
8 1 0 3
15 3 1 3
2 2 0 0
2 2 3 2
11 0 3 3
8 3 2 3
8 3 3 3
13 3 1 1
12 1 1 2
2 2 0 1
2 2 0 3
2 1 2 0
13 0 0 1
8 1 1 1
13 2 1 2
12 2 3 0
2 2 2 1
2 0 1 2
2 1 0 3
8 3 2 1
8 1 2 1
13 0 1 0
12 0 1 2
2 2 3 0
2 0 0 1
2 2 0 3
4 0 3 0
8 0 1 0
13 0 2 2
12 2 3 3
2 2 0 2
2 1 0 0
12 0 2 0
8 0 1 0
8 0 2 0
13 3 0 3
12 3 3 2
2 2 0 0
2 1 3 3
2 1 1 1
11 0 3 3
8 3 3 3
8 3 3 3
13 2 3 2
12 2 0 0
2 0 3 3
2 2 2 2
14 3 2 3
8 3 2 3
13 0 3 0
12 0 0 1
2 2 2 0
2 2 2 3
2 3 1 2
9 0 2 0
8 0 3 0
13 0 1 1
8 2 0 0
15 0 2 0
2 0 2 2
3 2 3 3
8 3 3 3
13 3 1 1
2 1 0 2
2 0 2 3
2 3 0 0
0 0 2 0
8 0 3 0
8 0 3 0
13 0 1 1
2 1 0 0
2 3 1 3
8 3 0 2
15 2 2 2
12 0 2 2
8 2 2 2
13 2 1 1
12 1 3 3
2 2 3 0
2 1 3 1
2 1 1 2
10 1 0 2
8 2 1 2
13 3 2 3
12 3 0 2
8 1 0 3
15 3 3 3
7 3 0 0
8 0 2 0
13 2 0 2
12 2 2 0
2 2 1 2
2 0 2 1
8 1 0 3
15 3 1 3
13 3 3 1
8 1 3 1
13 1 0 0
12 0 1 2
2 2 2 1
2 0 0 3
2 3 0 0
5 1 0 3
8 3 2 3
8 3 2 3
13 3 2 2
12 2 1 0
2 1 1 3
2 3 2 1
2 2 0 2
1 2 1 2
8 2 2 2
8 2 3 2
13 2 0 0
12 0 1 2
8 2 0 3
15 3 2 3
8 2 0 0
15 0 2 0
2 2 3 1
4 0 3 1
8 1 3 1
8 1 1 1
13 2 1 2
2 2 1 1
8 0 0 0
15 0 3 0
2 1 0 3
5 1 0 1
8 1 2 1
13 2 1 2
2 0 0 3
2 2 1 1
6 1 3 3
8 3 3 3
13 2 3 2
12 2 2 1
2 1 1 3
2 2 1 0
8 1 0 2
15 2 3 2
8 3 2 0
8 0 1 0
13 0 1 1
12 1 1 0
2 0 2 1
2 0 3 3
2 1 2 1
8 1 2 1
13 0 1 0
12 0 3 1
8 0 0 2
15 2 1 2
8 0 0 3
15 3 1 3
2 3 3 0
13 3 3 3
8 3 2 3
13 1 3 1
2 2 0 3
2 2 3 0
4 0 3 3
8 3 1 3
13 3 1 1
12 1 3 3
2 1 1 1
10 1 0 0
8 0 2 0
13 3 0 3
12 3 0 2
2 1 2 3
2 2 0 0
2 0 3 1
15 3 1 3
8 3 2 3
8 3 2 3
13 3 2 2
12 2 3 1
2 1 1 3
2 2 0 2
2 1 2 0
12 0 2 2
8 2 1 2
8 2 3 2
13 1 2 1
12 1 3 3
2 0 0 2
8 0 0 1
15 1 1 1
13 0 0 0
8 0 1 0
13 3 0 3
12 3 2 2
8 3 0 3
15 3 3 3
2 3 3 0
2 2 1 1
2 1 3 1
8 1 1 1
13 1 2 2
12 2 0 3
8 3 0 0
15 0 1 0
2 1 3 1
2 0 1 2
8 0 2 2
8 2 2 2
13 3 2 3
12 3 1 0
2 1 3 2
2 3 0 1
2 2 3 3
7 1 3 1
8 1 1 1
13 1 0 0
12 0 1 3
2 2 2 1
2 2 2 2
2 1 0 0
12 0 2 0
8 0 3 0
13 3 0 3
12 3 0 1
2 2 3 0
8 1 0 2
15 2 3 2
2 3 0 3
7 3 0 0
8 0 2 0
13 1 0 1
12 1 1 2
2 3 1 1
2 2 2 0
2 1 3 3
7 1 0 3
8 3 1 3
13 3 2 2
8 2 0 1
15 1 2 1
8 2 0 3
15 3 0 3
2 3 0 0
8 0 2 0
13 0 2 2
12 2 1 0
2 2 2 3
2 0 3 2
2 0 0 1
3 2 3 3
8 3 1 3
13 0 3 0
8 3 0 1
15 1 3 1
2 3 1 3
2 3 3 2
0 3 2 1
8 1 1 1
13 1 0 0
2 1 3 3
2 2 1 1
5 1 2 3
8 3 1 3
13 3 0 0
12 0 1 1
2 3 2 0
8 1 0 3
15 3 2 3
8 1 0 2
15 2 1 2
0 0 2 3
8 3 3 3
13 3 1 1
12 1 1 0
2 2 1 2
2 0 2 3
2 2 1 1
14 3 2 1
8 1 2 1
13 1 0 0
12 0 3 1
2 1 0 0
8 2 0 3
15 3 2 3
2 1 1 2
10 0 3 0
8 0 3 0
13 1 0 1
2 0 0 0
2 2 3 2
6 2 3 3
8 3 2 3
13 1 3 1
2 0 1 2
2 1 3 3
2 1 2 0
13 0 0 2
8 2 2 2
13 1 2 1
12 1 1 2
8 0 0 1
15 1 3 1
2 2 0 0
11 0 3 1
8 1 3 1
13 2 1 2
12 2 1 1
2 1 1 2
2 2 0 3
4 0 3 2
8 2 2 2
8 2 3 2
13 1 2 1
2 3 3 0
2 2 0 2
1 2 0 0
8 0 1 0
8 0 1 0
13 1 0 1
12 1 2 0
2 1 3 1
2 0 2 3
8 0 0 2
15 2 3 2
2 2 3 2
8 2 3 2
8 2 3 2
13 0 2 0
2 0 0 2
2 2 3 3
2 2 1 1
6 1 3 1
8 1 1 1
13 1 0 0
12 0 3 2
2 2 1 0
2 3 2 1
4 0 3 1
8 1 1 1
13 1 2 2
12 2 0 3
2 0 3 1
2 3 0 2
5 0 2 0
8 0 3 0
8 0 1 0
13 0 3 3
12 3 1 2
8 0 0 3
15 3 2 3
2 1 0 1
2 0 0 0
10 1 3 0
8 0 2 0
13 2 0 2
12 2 3 0
8 1 0 1
15 1 3 1
2 0 0 3
2 0 1 2
0 1 2 3
8 3 1 3
13 0 3 0
12 0 3 2
2 0 1 1
8 0 0 0
15 0 1 0
2 0 0 3
13 0 0 3
8 3 1 3
13 3 2 2
12 2 0 1
8 3 0 3
15 3 2 3
2 2 1 0
2 3 1 2
4 0 3 0
8 0 1 0
13 0 1 1
8 3 0 3
15 3 0 3
2 3 0 0
0 0 2 2
8 2 1 2
13 2 1 1
12 1 2 3
8 1 0 1
15 1 3 1
2 0 0 2
9 2 0 2
8 2 2 2
8 2 3 2
13 3 2 3
12 3 0 2
2 2 3 0
8 3 0 3
15 3 2 3
7 1 0 3
8 3 2 3
13 2 3 2
12 2 2 3
2 2 2 1
2 1 1 0
2 0 1 2
8 0 2 2
8 2 2 2
13 3 2 3
12 3 3 0
2 1 2 3
8 0 0 1
15 1 0 1
2 0 3 2
8 3 2 1
8 1 2 1
13 1 0 0
12 0 1 3
2 0 1 1
2 2 3 0
2 3 0 2
5 0 2 1
8 1 2 1
13 1 3 3
12 3 3 0
2 1 1 3
2 0 3 2
2 3 1 1
8 3 2 2
8 2 2 2
13 2 0 0
12 0 1 1
2 3 3 3
2 3 3 0
2 1 1 2
0 3 2 0
8 0 3 0
13 1 0 1
12 1 3 2
2 1 1 0
2 2 2 3
2 0 3 1
13 0 0 3
8 3 2 3
13 2 3 2
12 2 3 1
2 3 1 3
2 3 1 0
2 3 0 2
0 3 2 3
8 3 2 3
8 3 1 3
13 1 3 1
2 1 2 3
8 3 0 0
15 0 2 0
11 0 3 3
8 3 2 3
13 1 3 1
12 1 1 0
2 2 2 2
8 3 0 3
15 3 0 3
2 2 1 1
2 3 2 1
8 1 3 1
13 1 0 0
2 3 1 2
2 1 0 3
8 2 0 1
15 1 3 1
15 3 1 1
8 1 2 1
13 0 1 0
12 0 3 1
8 2 0 0
15 0 1 0
8 3 2 3
8 3 1 3
13 3 1 1
12 1 1 3
2 2 1 2
2 3 3 0
2 2 0 1
7 0 1 2
8 2 3 2
8 2 1 2
13 3 2 3
12 3 2 1
2 0 0 2
2 1 2 3
0 0 2 2
8 2 1 2
13 2 1 1
2 0 0 3
2 1 0 0
2 2 1 2
12 0 2 3
8 3 1 3
8 3 1 3
13 3 1 1
12 1 1 3
8 2 0 1
15 1 0 1
12 0 2 1
8 1 1 1
13 3 1 3
12 3 1 1
2 3 1 3
2 3 1 0
2 0 2 2
9 2 0 0
8 0 3 0
13 1 0 1
12 1 0 3
2 3 1 2
8 2 0 0
15 0 2 0
2 3 1 1
2 2 1 2
8 2 1 2
13 3 2 3
2 0 0 2
2 3 1 0
9 2 0 0
8 0 2 0
13 3 0 3
12 3 3 2
2 3 0 3
2 0 3 1
2 1 1 0
13 0 0 0
8 0 1 0
8 0 1 0
13 0 2 2
12 2 2 1
2 1 2 3
2 0 3 2
8 3 0 0
15 0 2 0
11 0 3 0
8 0 1 0
13 1 0 1
2 2 2 3
2 1 3 0
2 3 2 2
8 0 2 0
8 0 3 0
8 0 3 0
13 1 0 1
12 1 3 0
2 0 3 3
2 2 3 2
2 0 2 1
14 3 2 2
8 2 1 2
8 2 3 2
13 0 2 0
12 0 2 1
8 1 0 3
15 3 1 3
2 1 0 2
2 3 0 0
0 0 2 2
8 2 3 2
13 1 2 1
12 1 0 3
2 0 2 1
2 1 3 2
2 0 2 0
2 2 0 0
8 0 2 0
13 3 0 3
12 3 2 1
2 2 1 2
2 2 2 3
2 3 0 0
1 2 0 2
8 2 1 2
8 2 2 2
13 1 2 1
12 1 2 3
2 3 2 2
2 2 2 0
2 3 1 1
5 0 2 1
8 1 3 1
8 1 2 1
13 1 3 3
12 3 3 2
2 3 3 1
2 0 2 3
1 0 1 1
8 1 1 1
13 2 1 2
12 2 1 1
2 0 2 2
2 1 2 0
2 1 3 3
13 3 0 3
8 3 2 3
8 3 1 3
13 1 3 1
12 1 3 0
8 3 0 1
15 1 0 1
2 2 3 3
2 2 3 2
2 3 2 1
8 1 2 1
13 0 1 0
12 0 3 1
2 1 1 3
2 2 2 0
11 0 3 0
8 0 2 0
13 0 1 1
12 1 2 0
2 2 2 3
2 2 1 1
6 1 3 3
8 3 3 3
13 3 0 0
12 0 0 3
8 3 0 0
15 0 2 0
2 3 0 1
1 0 1 0
8 0 1 0
13 0 3 3
12 3 2 2
2 2 0 3
8 0 0 0
15 0 2 0
4 0 3 0
8 0 3 0
13 0 2 2
12 2 1 0
8 3 0 3
15 3 1 3
8 2 0 2
15 2 0 2
15 3 1 1
8 1 1 1
13 0 1 0
2 3 3 1
8 3 2 1
8 1 1 1
13 1 0 0
12 0 1 2
8 2 0 0
15 0 2 0
2 0 2 1
11 0 3 3
8 3 1 3
13 2 3 2
12 2 3 1
8 0 0 3
15 3 0 3
2 3 1 2
5 0 2 3
8 3 2 3
8 3 3 3
13 1 3 1
12 1 1 2
8 3 0 3
15 3 3 3
2 2 0 1
2 3 3 0
5 1 0 3
8 3 3 3
13 3 2 2
12 2 3 3
2 1 1 0
2 1 2 1
2 2 1 2
12 0 2 2
8 2 3 2
13 2 3 3
12 3 1 2
2 0 3 3
8 0 0 0
15 0 2 0
6 0 3 1
8 1 3 1
13 2 1 2
2 3 3 0
2 2 0 3
8 1 0 1
15 1 3 1
7 1 3 3
8 3 3 3
13 3 2 2
2 1 2 0
2 2 1 3
2 2 2 1
6 1 3 1
8 1 2 1
13 1 2 2
12 2 0 1
2 0 1 2
2 1 2 3
2 2 3 0
11 0 3 2
8 2 3 2
8 2 1 2
13 1 2 1
2 1 0 0
2 2 3 2
12 0 2 0
8 0 3 0
8 0 1 0
13 1 0 1
12 1 1 0
2 3 0 1
8 0 0 2
15 2 0 2
0 1 2 3
8 3 3 3
13 0 3 0
12 0 1 3
2 2 0 2
2 1 1 0
12 0 2 1
8 1 2 1
13 1 3 3
2 0 0 1
2 3 1 0
2 1 2 2
0 0 2 1
8 1 2 1
8 1 2 1
13 3 1 3
12 3 3 2
2 2 0 3
2 2 3 0
2 1 0 1
4 0 3 3
8 3 3 3
13 2 3 2
8 0 0 3
15 3 3 3
2 3 1 1
1 0 1 1
8 1 3 1
13 1 2 2
12 2 0 1
2 2 2 2
2 1 0 0
2 0 3 3
14 3 2 3
8 3 3 3
8 3 1 3
13 3 1 1
12 1 2 3
2 3 0 0
8 2 0 1
15 1 2 1
5 1 0 1
8 1 1 1
13 1 3 3
12 3 2 1
8 1 0 3
15 3 0 3
14 3 2 2
8 2 1 2
13 1 2 1
12 1 2 3
2 3 1 1
2 1 3 0
2 2 0 2
12 0 2 0
8 0 1 0
13 0 3 3
12 3 1 0
2 1 0 3
15 3 1 1
8 1 3 1
13 1 0 0
12 0 1 2
2 2 3 0
8 3 0 3
15 3 2 3
2 3 3 1
4 0 3 3
8 3 2 3
13 2 3 2
2 1 2 1
2 1 0 0
2 2 2 3
10 1 3 1
8 1 2 1
13 1 2 2
12 2 3 1
2 2 0 2
2 0 0 3
12 0 2 2
8 2 3 2
13 2 1 1
12 1 3 3
2 2 3 2
2 0 0 1
2 3 1 0
1 2 0 2
8 2 1 2
13 2 3 3
12 3 3 1
2 1 0 0
2 1 0 3
2 0 1 2
8 0 2 2
8 2 1 2
8 2 3 2
13 2 1 1
12 1 1 2
2 3 1 3
2 2 2 1
2 2 1 0
7 3 0 3
8 3 3 3
13 3 2 2
12 2 2 1
2 3 3 3
2 0 1 2
0 3 2 2
8 2 2 2
13 2 1 1
12 1 0 2
2 3 2 1
2 1 0 0
2 2 0 3
15 0 1 1
8 1 3 1
8 1 1 1
13 2 1 2
2 2 3 0
2 2 0 1
8 0 0 3
15 3 0 3
6 0 3 1
8 1 2 1
13 1 2 2
2 0 1 1
2 1 0 3
11 0 3 0
8 0 3 0
8 0 2 0
13 0 2 2
12 2 0 0"""


class Sample:
    def __init__(self, before_registers, instruction, after_registers):
        self.before_registers = before_registers
        self.opcode = instruction[0]
        self.A = instruction[1]
        self.B = instruction[2]
        self.C = instruction[3]
        self.after_registers = after_registers

    def __repr__(self):
        return "Sample(before=%s, after=%s, opcode=%s, A=%s, B=%s, C=%s)" % (self.before_registers, self.after_registers, self.opcode, self.A, self.B, self.C)


    def addr(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] + self.before_registers[self.B]
        return result

    def addi(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] + self.B
        return result

    def mulr(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] * self.before_registers[self.B]
        return result

    def muli(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] * self.B
        return result

    def banr(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] & self.before_registers[self.B]
        return result        

    def bani(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] & self.B
        return result

    def borr(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] | self.before_registers[self.B]
        return result

    def bori(self):
        result = list(self.before_registers)
        result[self.C] = self.before_registers[self.A] | self.B
        return result

    def setr(self):
        result = list(self.before_registers)
        result[self.C] = result[self.A]
        return result

    def seti(self):
        result = list(self.before_registers)
        result[self.C] = self.A
        return result

    def gtir(self):
        result = list(self.before_registers)
        if self.A > self.before_registers[self.B]:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def gtri(self):
        result = list(self.before_registers)
        if self.before_registers[self.A] > self.B:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def gtrr(self):
        result = list(self.before_registers)
        result = list(self.before_registers)
        if self.before_registers[self.A] > self.before_registers[self.B]:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def eqir(self):
        result = list(self.before_registers)
        if self.A == self.before_registers[self.B]:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def eqri(self):
        result = list(self.before_registers)
        if self.before_registers[self.A] == self.B:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def eqrr(self):
        result = list(self.before_registers)
        result = list(self.before_registers)
        if self.before_registers[self.A] == self.before_registers[self.B]:
            result[self.C] = 1
        else:
            result[self.C] = 0
        return result

    def count_compatible(self):
        result = 0
        instructions = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']
        for instruction in instructions:
            to_call = getattr(Sample, instruction)
            after_registers = to_call(self)
            if after_registers == self.after_registers:
                result += 1

        return result

    def find_compatible(self, to_exclude):
        result = None
        instructions = set(['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']) - to_exclude
        for instruction in instructions:
            to_call = getattr(Sample, instruction)
            after_registers = to_call(self)
            if after_registers == self.after_registers:
                if result is not None:
                    # found a duplicate. Whoops
                    return None
                result = instruction

        if result is not None:
            return (self.opcode, result)
        else:
            return None


def find_opcode_mapping(samples):
    samples = list(samples)
    known_instructions = set()
    result = {}
    while len(samples) > 0:    
        determinable_samples = list(filter(lambda s: s.find_compatible(known_instructions) is not None, samples))
        determinable_sample = determinable_samples[0]
        compatible = determinable_sample.find_compatible(known_instructions)
        instruction = compatible[1]
        samples = filter(lambda s: s.opcode != determinable_sample.opcode, samples)
        result[determinable_sample.opcode] = instruction
        known_instructions.add(instruction)

    return result
            
def get_input():
    result = []
    try:
        while True:
            before_line = raw_input()
            instruction_line = raw_input()
            after_line = raw_input()
            _ = raw_input()

            before_groups = BEFORE_REGEX.match(before_line).groups()
            after_groups = AFTER_REGEX.match(after_line).groups()

            result.append(Sample(
                [int(before_groups[0]), int(before_groups[1]), int(before_groups[2]), int(before_groups[3])],
                list(int(x) for x in instruction_line.split()),
                [int(after_groups[0]), int(after_groups[1]), int(after_groups[2]), int(after_groups[3])]))

    except EOFError:
        return result

def main():
    samples = get_input()

    opcode_mapping = find_opcode_mapping(samples)
    executor_sample = Sample([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0])

    for program_line in PROGRAM.split("\n"):
        opcode, A, B, C = program_line.split()
        instruction = opcode_mapping[int(opcode)]
        
        executor_sample.A = int(A)
        executor_sample.B = int(B)
        executor_sample.C = int(C)
        executor_sample.before_registers = executor_sample.after_registers

        to_call = getattr(Sample, instruction)
        executor_sample.after_registers = to_call(executor_sample)

    print 'Done', executor_sample.after_registers[0]

if __name__ == "__main__":
    main()

