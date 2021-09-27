import claripy

x0 = claripy.BVS("x0",64)
x1 = claripy.BVS("x1",64)
x2 = claripy.BVS("x2",64)

p=claripy.Not(claripy.Or(claripy.And(claripy.And(x2>0x63,x0>0x18,x0>0x32,x1==0x3),claripy.And(x2>0x63,x0>0x18,x0>0x32,x1==0x3)),claripy.And(claripy.Not(claripy.And(x2>0x63,x0>0x18,x0>0x32,x1==0x3)),claripy.Not(claripy.And(x2>0x63,x0>0x18,x0>0x32,x1==0x3)))))
s = claripy.Solver()
s.add(p)
print(s.satisfiable())