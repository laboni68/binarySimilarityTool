import claripy

x0 = claripy.BVS("x0",64)
x1 = claripy.BVS("x1",64)
x2 = claripy.BVS("x2",64)

p=claripy.Not(claripy.Or(claripy.And(claripy.Or(),claripy.Or(claripy.And(claripy.Not(x2<=0xfffffffffffff000),x0==1),claripy.And(x2<=0xfffffffffffff000))),claripy.And(claripy.Not(claripy.Or()),claripy.Not(claripy.Or(claripy.And(claripy.Not(x2<=0xfffffffffffff000),x0==1),claripy.And(x2<=0xfffffffffffff000))))))
s = claripy.Solver()
s.add(p)
print(s.satisfiable())
if(s.satisfiable()==False):print("Equivalent")
else:print("Not equivalent")