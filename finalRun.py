import claripy

x0 = claripy.BVS("x0",64)
x1 = claripy.BVS("x1",64)
x2 = claripy.BVS("x2",64)

p=claripy.Not(claripy.Or(claripy.And(claripy.Or(claripy.And(claripy.Not(x1<=0xfffffffffffff000),x2==1),claripy.And(x1<=0xfffffffffffff000)),claripy.Or(claripy.And(claripy.Not(x1<=0xfffffffffffff000),x2==1),claripy.And(x1<=0xfffffffffffff000))),claripy.And(claripy.Not(claripy.Or(claripy.And(claripy.Not(x1<=0xfffffffffffff000),x2==1),claripy.And(x1<=0xfffffffffffff000))),claripy.Not(claripy.Or(claripy.And(claripy.Not(x1<=0xfffffffffffff000),x2==1),claripy.And(x1<=0xfffffffffffff000))))))
s = claripy.Solver()
s.add(p)
print(s.satisfiable())
if(s.satisfiable()==False):print("Equivalent")
else:print("Not equivalent")