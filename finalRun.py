import claripy


p=claripy.Not(claripy.Or(claripy.And(claripy.Or(),claripy.Or()),claripy.And(claripy.Not(claripy.Or()),claripy.Not(claripy.Or()))))
s = claripy.Solver()
s.add(p)
print(s.satisfiable())
if(s.satisfiable()==False):print("Equivalent")
else:print("Not equivalent")