# binarySimilarityTool
**Branch PartialSE:** Runs on nano editor and the processed version of the nano_editor
**Command:**
1. python runLogicalSummary.py nano nano_processed <technique_name>
<br />
**Technique Names:**
1. dfs
2. memWatch
3. loopSeer

<br />
Partially checked equivalence with 10000 steps for both the programs. The step size in angr means the number of blocks checked for collecting the path constraints using symbolic execution. Another thing to note that, we do not consider the return value in this partial symbolic execution equivalence checking. Only on the basis of input constraints, they are shown as equivalent using method summary. 
Moreover, different techniques are used for collecting the path constraints from the programs partially. Depth First Search (dfs) , Memory Watcher (memWatch), loopSeering (loopSeer) are the names of the different techniques we can use for doing the partial symbolic execution and all the techniques confirmed the equivalence in the input constraint upto 10000 blocks.
