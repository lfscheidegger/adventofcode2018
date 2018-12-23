#/usr/bin/python

def main():
    B = 0
    C = 0
    E = 0
    F = 0
    old_E = 0

    sequence_is_done = False

    e_values = set()
    while True:
        B = E | 65536
        E = 678134
        while True:
            F = B & 255
            E += F


            
            E &= 16777215
            E *= 65899
            E &= 16777215
            if 256 > B:
                break
            F = 0
            while True:
                C = (F + 1) * 256
                if C > B:
                    break
                F += 1                

            B = F
        if sequence_is_done:
            assert E in e_values, 'found new E after sequence was done %s' % E
        if E in e_values:
            print 'Result:', old_E, E
            sequence_is_done = True
            break
        e_values.add(E)
        old_E = E
        if len(e_values) % 1000 == 0:
            print len(e_values)

if __name__ == "__main__":
    main()

"""
10961197
104479
8359186
7795090
4071422
14714840
9163876
16406139
9005490
2773404
2137048
11205272
2599981
13239794
4371374
4277896
9266843
3572648
9930978
"""
