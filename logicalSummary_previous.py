from termios import CR1
import angr
import sys
import os
import claripy

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
    state = c.factory.call_state(0x4006aa)
    # state = c.factory.call_state(0x415424, cmd, ps)
    # state.regs.rbp = claripy.BVS('rbp', c.arch.bits, explicit_name=True)
    # state.add_constraints(cmd == 0x12340000)
    # state.add_constraints(ps == 0x23450000)
    #state.add_constraints(ptr1 == 0x12340000)
    #state.add_constraints(ptr2 == 0x23450000)
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
    #state.add_constraints(state.regs.edx ==0x3)
    #state.add_constraints(claripy.Not(state.regs.rdi==0x0))
    #state.add_constraints(state.regs.rsi == 0x0)
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
    list_list_1 = []
    if(len(sm.deadended)>0):
        for i in range(len(sm.deadended)):
            path = sm.deadended[i]
            print(len(path.solver.constraints))
            list_ = path.solver.constraints
            try:
                m_1 = path.regs.eax
            except:
                m_1 = path.regs.r0
            
            # with open(f"state_{os.getpid()}_{i}.txt", 'w') as f:
            #     f.write("\n".join(path.history.descriptions) + "\n\n\n")
            #     f.write("\n".join(map(repr, path.solver.constraints)) + "\n\n\n")
            #     f.write(repr(m_1))

            list_.append(m_1)
            print(path.solver.constraints)
            #print(path.regs.eax)
            list_list_1.append(list_)
    return list_list_1    


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
    

print(str(sys.argv))
listName_ = sys.argv
fileName = listName_[1]
resultName = str(listName_[2])+".txt"
print(fileName," ",resultName)
list_list_1 = runAndfind(str(fileName))
list_list = writeFile(list_list_1)
f = open(resultName, "w")
f.write(str(list_list))
f.close()
