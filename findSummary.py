#from copyreg import pickle
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

def runAndfind(binaryFile, resultName):
    c = angr.Project(binaryFile, auto_load_libs = False)
    state = c.factory.entry_state()
    #state = c.factory.call_state(0x400671)
    x = claripy.BVS('x', 32, explicit_name=True)
    state.memory.read_strategies = [MyConcretizationStrategy()]
    state.memory.write_strategies = [MyConcretizationStrategy()]
    sm = c.factory.simulation_manager(state)
    sm.explore()
    print(len(sm.deadended))
 
    if(len(sm.deadended)>0):
        #fileName = resultName+".txt"
        f = open(resultName+".txt", "w")
        f.write(str(len(sm.deadended)))
        f.close()
        for i in range(len(sm.deadended)):
            path = sm.deadended[i]
            print(len(path.solver.constraints))
 
            try:
                m_1 = path.regs.eax
            except:
                m_1 = path.regs.r0

            constraint_and = claripy.And(True)
            for j in range(len(path.solver.constraints)):
                constraint_and = claripy.And(path.solver.constraints[j], constraint_and)
                
            constraint_and = claripy.And(constraint_and, x==m_1)
            print(constraint_and)
            fileName = resultName + str(i)+".pkl"
            f = open(fileName, "wb")
            pickle.dump(constraint_and, f)
            f.close()   

    

print(str(sys.argv))
listName_ = sys.argv
fileName = listName_[1]
resultName = str(listName_[2])
print(fileName," ",resultName)
runAndfind(str(fileName), resultName)

