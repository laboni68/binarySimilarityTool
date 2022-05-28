import claripy

x0 = claripy.BVS("x0",64)
x1 = claripy.BVS("x1",64)
x2 = claripy.BVS("x2",64)

p=claripy.Not(claripy.Or(claripy.And(claripy.And(x0>0x63,x2>0x19,x1==0x2),claripy.And(x0>0x63,x2<=0x18,x1==0x2)),claripy.And(claripy.Not(claripy.And(x0>0x63,x2>0x19,x1==0x2)),claripy.Not(claripy.And(x0>0x63,x2<=0x18,x1==0x2)))))
s = claripy.Solver()
s.add(p)
print(s.satisfiable())