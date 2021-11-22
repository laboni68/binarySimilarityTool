import pickle
#!/bin/bash
#!/usr/bin/python
import os
import sys
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
        command2 = "python logicalSummary_v2.py " +files_[i]+" "+result
        print(command2)
        os.system(command2)

initialization()
constraint_1 = []
k = 0
with open('constraints_1.pkl', 'rb') as fr:
    try:
        while True:
            constraint_1.append(pickle.load(fr))
            k=k+1
    except EOFError:
        pass
print("====================")
print(constraint_1)
# with open('constraints_1.pkl', 'rb') as f:
#     constraints_1 = pickle.load(f)
# with open('constraints_2.pkl', 'rb') as f1:
#     constraints_2 = pickle.load(f1)
# print(constraints_2)
print("====================")
constraint_2 = []
k2 = 0
with open('constraints_2.pkl', 'rb') as fr:
    try:
        while True:
            constraint_2.append(pickle.load(fr))
            k2=k2+1
    except EOFError:
        pass
print("====================")
print(constraint_2)
print("====================")
constraint_1_or = claripy.Or(False)
for i in range(len(constraint_1)):
    constraint_1_and = claripy.And(constraint_1[i][0],True)
    for j in range(1,len(constraint_1[i])-1):
        constraint_1_and = claripy.And(constraint_1_and,constraint_1[i][j])
    constraint_1_or = claripy.Or(constraint_1_and, constraint_1_or)
print(constraint_1_or)
print("====================")
constraint_2_or = claripy.Or(False)
for i in range(len(constraint_2)):
    constraint_2_and = claripy.And(constraint_2[i][0],True)
    for j in range(1,len(constraint_2[i])-1):
        constraint_2_and = claripy.And(constraint_2_and,constraint_2[i][j])
    constraint_2_or = claripy.Or(constraint_2_and, constraint_2_or)
print(constraint_2_or)




final_constraint = claripy.Not(claripy.Or(claripy.And(constraint_1_or,constraint_2_or), claripy.And(claripy.Not(constraint_1_or),claripy.Not(constraint_2_or))))
print(final_constraint)
solver = claripy.Solver()
print(final_constraint)
solver.add(final_constraint)
print(solver.satisfiable())