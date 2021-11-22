import angr
import claripy
import sys

def runAndfind(binaryFile):
    c = angr.Project(binaryFile, auto_load_libs = False)
    state = c.factory.entry_state()
    sm = c.factory.simulation_manager(state)
    sm.explore()
    print(len(sm.deadended))
    list_list_1 = []
    if(len(sm.deadended)>0):
        for i in range(len(sm.deadended)):
            path = sm.deadended[i]
            #for step in path.state.history.jump_guards:
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

def runAndfindNew(binaryFile, technique, steps):
    #print(technique)
    c = angr.Project(binaryFile, auto_load_libs = False)
    state = c.factory.entry_state()
    sm = c.factory.simulation_manager(state)
    if(technique=="dfs"):
        print("dfs")
        sm.use_technique(angr.exploration_techniques.DFS())
    elif(technique=="memWatch"):
        print("memWatch")
        sm.use_technique(angr.exploration_techniques.MemoryWatcher())
    elif(technique=="loopSeer"):
        print("loopSeer")
        sm.use_technique(angr.exploration_techniques.LoopSeer())
    sm.run(n=int(steps))
    print("deadended : ",len(sm.deadended))
    print("active : ",len(sm.active))
    print("pruned : ",len(sm.pruned))
    print("unconstrained : ",len(sm.unconstrained))
    print("unsat : ",len(sm.unsat))
    list_list_1 = []
    if(len(sm.deadended)>0):
        for i in range(len(sm.deadended)):
            path = sm.deadended[i]
            list_ = path.solver.constraints
            #list_.append(path.regs.eax)
            print(path.solver.constraints)
            print(path.regs.eax)
            list_list_1.append(list_)
    if(len(sm.active)>0):
        for i in range(0,len(sm.active)):
            path = sm.active[i]
            list_ = path.solver.constraints
            #list_.append(path.regs.eax)
            print(path.solver.constraints)
            print(path.regs.eax)
            list_list_1.append(list_)
    if(technique=="dfs"and len(sm.deferred)>0):
        print("deferred : ",len(sm.deferred))
        for i in range(len(sm.deferred)):
            path = sm.deferred[i]
            list_ = path.solver.constraints
            #list_.append(path.regs.eax)
            print(path.solver.constraints)
            print(path.regs.eax)
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
techniqueName = listName_[3]
steps = listName_[4]
resultName = str(listName_[2])+".txt"
print(fileName," ",resultName)
list_list_1 = runAndfindNew(str(fileName), techniqueName, steps)
list_list = writeFile(list_list_1)
f = open(resultName, "w")
f.write(str(list_list))
f.close()
