#!/usr/bin/python

"""
It turns out that the complicated input just computes the sum of divisors of a number.

The number is much bigger in part 2 than part 1, because setting register 0 to 1
(the difference in part 2) causes instructions 27-33 to run, and those are there
just to make the number much much bigger.

In my input, the small number is 987, and the big number is 10551387.

The code works with two nested loops. The outer loop increments the divisor 'candidate'.
The inner loop increments a temporary value step-by-step by the candidate amount, and has
two branches. The first branch is when the temporary value is equal to the INPUT. In this
case, the 'candidate' *is* a divisor of the INPUT, so its value is added to the result.

The second branch is when the temporary value is greater than INPUT. In this case,
it is *not* a divisor (because in its steps, it skipped 'past' the INPUT). In this case,
the code increments the 'candidate' by 1, and starts the inner loop over.

something like this:

def stupid_sum_of_divisors():
    candidate = 1
    result = 0
    while True:
        candidate += 1
        temp = 0
        while True:
            temp += candidate
            if temp == INPUT:
                result += candidate
            if temp > INPUT:
                break
        if candidate > INPUT:
            break
    return result
"""

INPUT = 10551387

def main():
    result = 0
    for idx in range(1, INPUT + 1):
        if INPUT % idx == 0:
            result += idx

    print result
if __name__ == "__main__":
    main()
