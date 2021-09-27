import claripy

x0 = claripy.BVS("x0",64)
x1 = claripy.BVS("x1",64)

p=claripy.Not(claripy.Or(claripy.And(claripy.And(x1>0x27,x1>0x31,x1<=0x3b,x0==0x3),claripy.And(x1<=0x3b,x1>0x31,x0==0x3)),claripy.And(claripy.Not(claripy.And(x1>0x27,x1>0x31,x1<=0x3b,x0==0x3)),claripy.Not(claripy.And(x1<=0x3b,x1>0x31,x0==0x3)))))
s = claripy.Solver()
s.add(p)
print(s.satisfiable())