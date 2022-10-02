import claripy

x0 = claripy.BVS("x0",64)
x1 = claripy.BVS("x1",64)
a = claripy.BVS("a",64)
b = claripy.BVS("b",64)

p=claripy.Not(claripy.Or(claripy.And(claripy.Or(claripy.And(x1==0x3,x1!=0x1,x1!=0x2,x0==a*b)),claripy.Or(claripy.And(x1==0x3,x1!=0x1,x1!=0x2,x0==a*b))),claripy.And(claripy.Not(claripy.Or(claripy.And(x1==0x3,x1!=0x1,x1!=0x2,x0==a*b))),claripy.Not(claripy.Or(claripy.And(x1==0x3,x1!=0x1,x1!=0x2,x0==a*b))))))
s = claripy.Solver()
s.add(p)
if(s.satisfiable()==False):print("Equivalent")
else:print("Not equivalent")
