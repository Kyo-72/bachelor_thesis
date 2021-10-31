from z3 import *

x1,x2,x3 = Bools(["x1","x2","x3"])

s = Solver()


P1 = Or(x1,Not(x2))
P2 = x3
P3 = Or(Not(x1),Not(x2))

s.add(P1,P2,P3)

c = s.check()
if c == sat:
    m = s.model()

list = [x1,x2,x3]

for i in list:
    print(i)
    print(' = ')
    print(is_true(m[i]))
