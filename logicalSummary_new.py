from re import M
import angr
import sys
import claripy
import time
import pickle
class MyConcretizationStrategy(angr.concretization_strategies.SimConcretizationStrategy):
    def __init__(self, **kwargs): #pylint:disable=redefined-builtin
        super(MyConcretizationStrategy, self).__init__(**kwargs)

    def _concretize(self, memory, addr, **kwargs):
        mn,mx = self._range(memory, addr, **kwargs)
        print("min ",mn," max ", mx)
        return [mn, mx]
def runAndfind(binaryFile):
    c = angr.Project(binaryFile, auto_load_libs = False)
    #state = c.factory.call_state(0x401289)
    cmd = claripy.BVS('cmd', c.arch.bits, explicit_name=True)
    ps = claripy.BVS('ps', c.arch.bits, explicit_name=True) 
    #state = c.factory.call_state(0x415424, cmd, ps)
    state = c.factory.call_state(0x4006aa)
    # state.regs.edi = claripy.BVS('edi', c.arch.bits, explicit_name=True)
    # state.regs.rsi = claripy.BVS('rsi', c.arch.bits, explicit_name=True)
    # state.regs.rdi = claripy.BVS('rdi', c.arch.bits, explicit_name=True)
    # state.add_constraints(cmd == 0x12340000)
    # state.add_constraints(ps == 0x23450000)
    #state.add_constraints(state.regs.edi ==0x2)
    x = claripy.BVS('x', 32, explicit_name=True)
    state.memory.read_strategies = [MyConcretizationStrategy()]
    state.memory.write_strategies = [MyConcretizationStrategy()]
    #state = c.factory.call_state(0x40066a)
    #state = c.factory.entry_state()  
    #state.add_constraints( state.regs.edi * state.regs.edi  == 0x9)
    #state.add_constraints(state.regs.esi * state.regs.edx == 0x63)
    #state.add_constraints(state.regs.edi ==0x7)
    #state.add_constraints(state.regs.esi ==0x5)
    #state.add_constraints(claripy.Or(state.regs.edx ==0x3, state.regs.edx ==0x2))
    #state.add_constraints(state.regs.esi ==0x63)
    #state.add_constraints(state.regs.edx ==0x3)
    #state.add_constraints(state.regs.edx <=0x64)
    #state.options.add(angr.options.CALLLESS)
    sm = c.factory.simulation_manager(state)
    sm.explore()
    print(len(sm.found))
   # print(sm.found[0], " ", sm.found[1])
    print(len(sm.active))
    print(len(sm.deadended))
    list_list_1 = []
    constraint_summary = claripy.Or(False)
    if(len(sm.deadended)>0):
        for i in range(len(sm.deadended)):
            path = sm.deadended[i]
            print(path)
            print(len(path.solver.constraints))
            list_ = path.solver.constraints
            try:
                m_1 = path.regs.eax
            except:
                m_1 = path.regs.r0
            list_.append(m_1)
            
            #print(path.solver.constraints[0].args[0].args[0])
            #print(path.solver.constraints[0].args[1].args)
            #print(path.solver.constraints[1].args[0])
            #print(path.solver.constraints[1].args[1])
            #print(path.solver.constraints[2].args[0])
            #print(path.solver.constraints[2].args[1])
            print(path.solver.constraints)
            print(type(path.solver.constraints[0]))
            print(m_1)
            print(constraint_summary)
            constraint_and = claripy.And(True)
            print(constraint_and)
            for j in range(len(path.solver.constraints)-1):
                print(path.solver.constraints[j])
                constraint_and = claripy.And(path.solver.constraints[j], constraint_and)
                print(constraint_and)
            print(x==m_1)
            constraint_and = claripy.And(constraint_and, x==m_1)
            list_list_1.append(list_)
            print("--------------------")
            print(constraint_and)
            constraint_summary=claripy.Or(constraint_and, constraint_summary)
    return constraint_summary    


def writeFile(list_list):
    list_1 = ""
    for i in range(len(list_list)):
        if len(list_list[i])==0:
            continue
        sublist = ""
        for j in range(len(list_list[i])):     
            sublist = sublist + "#"+ str(list_list[i][j])
        list_1 = list_1 + ","+ sublist 
    return list_1
    
start_time = time.time()
print(str(sys.argv))
listName_ = sys.argv
fileName = listName_[1]
fileName2 = listName_[2]

list_list_1 = runAndfind(str(fileName))
list_list_2 = runAndfind(str(fileName2))
#list_list = writeFile(list_list_1)
#list_list2 = writeFile(list_list_2)
print("==================")
print(list_list_1)
print(type(list_list_1))
f = open("constraints_1.pkl", "ab")
pickle.dump(list_list_1, f)
f.close()
print("==================")
print(list_list_2)
print(type(list_list_2))
f = open("constraints_2.pkl", "ab")
pickle.dump(list_list_2, f)
f.close()
s = claripy.Solver()
s.add(claripy.Not(claripy.Or(claripy.And(list_list_1, list_list_2), claripy.And(claripy.Not(list_list_1), claripy.Not(list_list_2)))))

print(s.satisfiable())
if(s.satisfiable()==False):
    print("Equivalent :)")
else:
    print("Not equivalent :(")
end_time = time.time()

print("time ", end_time - start_time)