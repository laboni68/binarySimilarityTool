from termios import CR1
import angr
import sys
import claripy
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
    #state = c.factory.call_state(0x400671) #This is for add and add_processed
    # ptr1 = claripy.BVS('address_ps', c.arch.bits)
    # ptr2 = claripy.BVS("address_cmd", c.arch.bits)
    #state = c.factory.call_state(0x402370, ptr1, ptr2) #for SampleShip game
    cmd = claripy.BVS('cmd', c.arch.bits, explicit_name=True)
    ps = claripy.BVS('ps', c.arch.bits, explicit_name=True)
    #state = c.factory.call_state(0x4012c0, ps, cmd)#Sample_ShipGame cgc_ProcessPlace
    #state = c.factory.entry_state()
    #state = c.factory.call_state(0x4006aa)#for test_9 and test_10
    state = c.factory.call_state(0x401189)#for calculator and its essences 
    #state = c.factory.call_state(0x401289)#for calc2 and its essences 
    # state = c.factory.call_state(0x415424, cmd, ps)
    state.regs.rbp = claripy.BVS('rbp', c.arch.bits, explicit_name=True)
    state.regs.rsi = claripy.BVS('rsi', c.arch.bits, explicit_name=True)
    state.regs.rdx = claripy.BVS('rdx', c.arch.bits, explicit_name=True)
    state.regs.rdi = claripy.BVS('rdi', c.arch.bits, explicit_name=True)
    state.regs.xmm0lq = claripy.BVS('xmm0lq', c.arch.bits, explicit_name=True)
    # state.add_constraints(cmd == 0x12340000)
    # state.add_constraints(ps == 0x23450000)
    #state.add_constraints(ptr1 == 0x12340000)
    #state.add_constraints(ptr2 == 0x23450000)
    x = claripy.BVS('x', 32, explicit_name=True)
    state.memory.read_strategies = [MyConcretizationStrategy()]
    state.memory.write_strategies = [MyConcretizationStrategy()]
    #state.stack_push(ps)
    #state.add_constraints(ps == 0x23450000)
    #state.add_constraints(cmd == 0x12340000)
    # symbolic_row = claripy.BVS('row', 8)
    # symbolic_col = claripy.BVS('col', 8)
    # state.memory.store(ptr2+1, symbolic_row)
    # state.memory.store(ptr2+2, symbolic_col)
    #state = c.factory.call_state(0x4011da) #for AreaCalc
    #state = c.factory.entry_state()
    #state.add_constraints( state.regs.edi * state.regs.edi  == 0x9)
    #state.add_constraints(state.regs.esi * state.regs.edx == 0x63)
    #state.add_constraints(state.regs.edi ==0x2)
    
    #state.add_constraints(state.regs.esi ==0x19)
    #state.add_constraints(state.regs.rdx ==0x3) #added for calculator case 1
    state.add_constraints(claripy.Or(state.regs.rdx ==0x3, state.regs.rdx ==0x2)) #added for calculator case 2
    #state.add_constraints(state.regs.rdi ==115) #added for calc2 case 1
    #state.add_constraints(claripy.Or(state.regs.rdi ==115, state.regs.rdi == 94)) #added for calc2 case 2
    #state.add_constraints(claripy.Or(state.regs.rdi ==115, state.regs.rdi == 94, state.regs.rdi == 47)) #added for calc2 case 3
    #state.add_constraints(claripy.Not(state.regs.rdi==0x0))
    #state.add_constraints(state.regs.rdi == 0x115)#added for calc2 case1
    #state.add_constraints(claripy.Or(state.regs.rdi ==0x115, state.regs.rdi ==0x5e))
    #state.add_constraints(claripy.Or(state.regs.edx ==0x3, state.regs.edx ==0x2))
    #state.add_constraints(claripy.Or(state.regs.rdi ==0x73, state.regs.rdi ==0x5e, state.regs.rdi ==0x2f))
    #state.add_constraints(state.regs.esi ==0x63)
    #state.add_constraints(state.regs.edx ==0x63)
    #state.add_constraints(state.regs.edx <=0x64)
    #state.options.add(angr.options.CALLLESS) #for sampleShip Game
    sm = c.factory.simulation_manager(state)
    #sm.explore(find=0x401363) #find = 0x402766 #for sampleShip Game
    sm.explore()
    print(len(sm.deadended))
    #import ipdb; ipdb.set_trace()
    constraint_summary = claripy.Or(False)
    if(len(sm.deadended)>0):
        for i in range(len(sm.deadended)):
            path = sm.deadended[i]
            print(path)
            print(len(path.solver.constraints))
            try:
                m_1 = path.regs.eax
            except:
                m_1 = path.regs.r0
            print(path.solver.constraints)
            print(type(path.solver.constraints[0]))
            print(m_1)
            print(constraint_summary)
            constraint_and = claripy.And(True)
            print(constraint_and)
            for j in range(len(path.solver.constraints)):
                print(path.solver.constraints[j])
                constraint_and = claripy.And(path.solver.constraints[j], constraint_and)
                print(constraint_and)
            print(x==m_1)
            constraint_and = claripy.And(constraint_and, x==m_1)
            print("--------------------")
            print(constraint_and)
            constraint_summary=claripy.Or(constraint_and, constraint_summary)
    return constraint_summary    

    
print(str(sys.argv))
listName_ = sys.argv
fileName = listName_[1]
resultName = str(listName_[2])+".pkl"
print(fileName," ",resultName)
list_list_1 = runAndfind(str(fileName))
print(list_list_1)
f = open(resultName, "wb")
pickle.dump(list_list_1, f)
f.close()
