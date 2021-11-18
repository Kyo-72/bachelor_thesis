from z3 import *

x1,x2,x3 = Bools(["x1","x2","x3"])

x_vec = BitVec(("x_vec"),10)
x_vec = 10
y_vec = BitVec(("y_vec"),10)

print(y_vec)

s = Solver()

x_vec = x_vec^y_vec
print(type(x_vec))
P = x_vec == 3
s.add(P)

c = s.check()
if c == sat:
    m = s.model()

print(m[y_vec].as_long())




