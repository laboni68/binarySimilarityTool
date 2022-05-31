import angr
import sys

def runAndfind(binaryFile):
    c = angr.Project(binaryFile, auto_load_libs = False)
    #state = c.factory.call_state(0x400671) #This is for add and add_processed
    #state = c.factory.call_state(0x40066a)
    state = c.factory.entry_state()
    #state.add_constraints( state.regs.edi ==0x9)
    #state.add_constraints(state.regs.esi ==0x04)
    #state.add_constraints(state.regs.edx ==0x03)
    #state.add_constraints(state.regs.esi <=0x64)
    #state.add_constraints(state.regs.edx <=0x64)
    #state.options.add(angr.options.CALLLESS)
    sm = c.factory.simulation_manager(state)
    sm.explore()
    print(len(sm.deadended))
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
