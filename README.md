# binarySimilarityTool
**testSource Folder :** Contains all the source code for tested programs.<br />
**testBinary Folder :** Contains all the binary corresponding to the source files present in the testBinary Folder.
<br />
<br />
**Pre-requisite for running :**
                <br />python
                <br />angr
                <br /><br />
**Running the script file:**
1. workon angr
2. pip install claripy (if angr can not find any module to run pip install that module will install that particular module)
3. python runLogialSummary.py <binary1> <binary2> 
<br />[2nd command is one time run only, for repeated use of the tool 1st and 3rd command will suffice]

**Output:** <br />
	constraints_1.txt <br />
  constraints_2.txt <br />
  finalRun.py <br />
  print equivalent or not equivalent on the basis of the result in the last line
<br />
We know that for checking the equivalence, the variables need to be mapped properly. If two variables in the different program are having the same functionality but they are defined by different symbolic variables they will result in non-equivalence. All the constraints are saved <constraints_1.txt> and <constraints_2.txt> files in raw form from the binary files that we want to compare. If we change the variable names manually in those text files, then the command for checking equivalence would be :
		<br />
    **python runLogialSummary.py constraints_1.txt constraints_2.txt**
    <br />
We can put your constraints in those text files and run the program “runLogialSummary.py” without giving any binary files also. But we have to keep in mind that the text files names must follow the same naming format. Otherwise, it will result in errors.

