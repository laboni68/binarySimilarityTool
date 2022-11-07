#!/bin/bash
#!/usr/bin/python
import os
import sys
import time
import pickle
import claripy

def initialization():
    print(str(sys.argv))
    list_ = sys.argv
    files_ = []
    text_file_flag =0
    for i in range(len(sys.argv)):
        if i==0:
            continue
        if(len(list_[i].split("."))==2):
            text_file_flag = 1
        files_.append(list_[i])
    print(len(files_))
    if(text_file_flag==1):
        return
    for i in range(len(files_)):
        #print("file ",i+1," : ",files_[i])
        print("file ", files_[i])
        result = "constraints_"+str(i+1)
        command2 = "python3.8 logicalSummary.py " +files_[i]+" "+result
        print(command2)
        os.system(command2)

start = time.time()
initialization()
print("===========================")
infile = open('constraints_1.pkl','rb')
constraint_1 = pickle.load(infile)
infile.close()
infile = open('constraints_2.pkl','rb')
constraint_2 = pickle.load(infile)
infile.close()
print(constraint_1)
print("===========================")
print(constraint_2)
solver = claripy.Solver()
solver.add(claripy.Not(claripy.Or(claripy.And(constraint_1, constraint_2), claripy.And(claripy.Not(constraint_1), claripy.Not(constraint_2)))))
print(solver.satisfiable())

if(solver.satisfiable()==False):
    print("Equivalent :)")
else:
    print("Not equivalent :(")
end_time = time.time()
end = time.time()
print("time : \n", end-start)
