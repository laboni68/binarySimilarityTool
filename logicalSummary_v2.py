import angr
import sys
import pickle
import claripy

def runAndfind(binaryFile, file1):
    symbolic_integer1 = claripy.BVS("z_intle:32", 32)
    symbolic_integer_le1 = claripy.Concat(
        claripy.Extract(7,0,symbolic_integer1),
        claripy.Extract(15,8,symbolic_integer1),
        claripy.Extract(23,16,symbolic_integer1),
        claripy.Extract(31,24,symbolic_integer1))
    
    c = angr.Project(binaryFile, auto_load_libs = False)
    state = c.factory.entry_state()
    sm = c.factory.simulation_manager(state)
    sm.explore()
    print(len(sm.deadended))
    #list_list_1 = claripy.Or(1==0,1==0)
    if(len(sm.deadended)>0):
        for i in range(len(sm.deadended)):
            path = sm.deadended[i]
            print(len(path.solver.constraints))
            #list_ = path.solver.constraints
            try:
                m_1 = path.regs.eax
            except:
                m_1 = path.regs.r0
            #list_=claripy.And(path.solver.constraints)
            #list_= claripy.And(list_, symbolic_integer_le1=m_1)
            pickle.dump(path.solver.constraints, file1)
           # pickle.dump(m_1, file1)
            print(path.solver.constraints)
        #print(path.regs.eax)
       


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
#resultName = str(listName_[2])+".txt"
resultName = str(listName_[2])+".pkl"
print(fileName," ",resultName)
f = open(resultName, "ab")
runAndfind(str(fileName),f)
#list_list = writeFile(list_list_1)

#pickle.dump(list_list_1, f)
#f.write(str(list_list))
f.close()