#!/bin/bash
#!/usr/bin/python
import os
import sys
import time

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
        command2 = "python logicalSummary.py " +files_[i]+" "+result
        print(command2)
        os.system(command2)

def makeList(list_f):
    list_ = list_f.read()
    #print(list_)
    final_list_1 = list_.split(",")
    final_list_1 = list(filter(None, final_list_1))
    #print(len(final_list_1))

    final_list = []
    for i in range(len(final_list_1)):
        final_sub_list = final_list_1[i].split("#")
        final_sub_list = list(filter(None, final_sub_list))
        final_list.append(final_sub_list)
    #print(final_list)
    return final_list

def processConstraint(separated_):
    constraint = ""
    length = len(separated_)
    print(separated_)
    print("length", length)
    for i in range(1, length-1):
        separated_[i] = separated_[i]. rstrip("\n")
        if(separated_[i].endswith("s")):
            separated_[i]=separated_[i].replace("s","")
        #elif(separated_[i].endswith(">")):
         #   separated_[i]=separated_[i].replace(">","")
        constraint =  constraint + separated_[i]
        symbols_.add(separated_[1])
        if(separated_[i].startswith("mem")):
            symbols_.add(separated_[i])
    separated_[length-1] = separated_[length-1]. rstrip("\n")
    separated_[length-1]=separated_[length-1].replace(">","")
    constraint =  constraint + separated_[length-1]
    if(separated_[length-1].startswith("mem")):
           symbols_.add(separated_[length-1])
    #print(constraint)
    return constraint
        

def makeConstraint(list_):
    list_ = makeList(list_)
    #print("===============++")
    #print(list_)
    outerS = "claripy.Or("
    for i in range(len(list_)):
        if(i!=0):
            outerS = outerS +","
        innerS = "claripy.And("
        list_[i][0] = list_[i][0].replace("(z_intle:32_10_32[7:0] .. z_intle:32_10_32[15:8] .. z_intle:32_10_32[23:16] .. z_intle:32_10_32[31:24])","z")
        separated = list_[i][0].split(" ")
        symbols_.add(separated[1])
        newC = processConstraint(separated)
        innerS = innerS + newC
        #print(separated)
        for j in range(1,len(list_[i])):
            list_[i][j] = list_[i][j].replace("(z_intle:32_10_32[7:0] .. z_intle:32_10_32[15:8] .. z_intle:32_10_32[23:16] .. z_intle:32_10_32[31:24])","z")
            list_[i][j] = list_[i][j].replace("BV64 0x0 .. ","Bool z == ")
            list_[i][j] = list_[i][j].replace("BV32 ","Bool z == ")
            separated = list_[i][j].split(" ")
            #symbols_.add(separated[1])
            #print(separated)
            newC = processConstraint(separated)
            innerS = innerS + "," + newC
        innerS = innerS +")"
        outerS = outerS + innerS
    outerS = outerS + ")"
    return outerS

def makeConstraintWithNot(constraint):
    outerS = "claripy.Not("+constraint+")"
    return outerS

def makeConstraintWithOr(constraint1,constraint2):
    outerS = "claripy.Or("+constraint1+","+constraint2+")"
    return outerS
def makeConstraintWithAnd(constraint1,constraint2):
    outerS = "claripy.And("+constraint1+","+constraint2+")"
    return outerS
def declareSymbol(symbols_):
    d = ""
    k = 0
    for val in symbols_:
        symbol = "x"+str(k)
        d = d + "\n" + symbol+" = claripy.BVS("+ "\""+symbol+"\""+",64)"
        k = k+1
    print(d)
    return d

start = time.time()
initialization()
print("===========================")
symbols_ = set()
list_1_f = open("constraints_1.txt", "r")
list_2_f = open("constraints_2.txt", "r")
outerS_1_and = makeConstraint(list_1_f)
print(outerS_1_and)
outerS_2_and = makeConstraint(list_2_f)
print(outerS_2_and)
print("===========================")
k = 0
for val in symbols_:
    print(val)
    symbol = "x"+str(k)
    k=k+1
    outerS_1_and = outerS_1_and.replace(val,symbol)
    outerS_2_and = outerS_2_and.replace(val,symbol)
print(outerS_1_and)
print(outerS_2_and)
declaration = declareSymbol(symbols_)
print("====================")
finalS_ = makeConstraintWithNot(
            makeConstraintWithOr(
                makeConstraintWithAnd(
                    outerS_1_and
                    ,
                    outerS_2_and
                ), 
                makeConstraintWithAnd(
                makeConstraintWithNot(outerS_1_and)
                ,
                makeConstraintWithNot(outerS_2_and)
                )
                )
                )
print(finalS_)
f = open("finalRun.py","w")
f.write("import claripy\n")
f.write(declaration)
f.write("\n\np=")
f.write(finalS_)
f.write("\ns = claripy.Solver()")
f.write("\ns.add(p)")
#f.write("\nprint(s.satisfiable())")
f.write("\nif(s.satisfiable()==False):")
f.write("print(\"Equivalent\")")
f.write("\nelse:")
f.write("print(\"Not equivalent\")")
f.close()

print("=========================================")
print("==================RESULT=================")
command = "python finalRun.py"
#print(command)
os.system(command)

end = time.time()
print("time : \n", end-start)
