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
        command2 = "python findSummary.py " +files_[i]+" "+result
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
    #print(separated_)
    for i in range(1, length):
        separated_[i] = separated_[i]. rstrip("\n")
        if(separated_[i].endswith("s")):
            separated_[i]=separated_[i].replace("s","")
        elif(separated_[i].endswith(">")):
            separated_[i]=separated_[i].replace(">","")
        constraint =  constraint + separated_[i]
        symbols_.add(separated_[1])
        if(separated_[i].startswith("mem")):
            symbols_.add(separated_[i])
    #print(constraint)
    return constraint
        



def preprocessList(final_list_1):
    for i in range(len(final_list_1)):
        for j in range(len(final_list_1[i])):
            final_list_1[i][j] = final_list_1[i][j].replace("(z_intle:32_10_32[7:0] .. z_intle:32_10_32[15:8] .. z_intle:32_10_32[23:16] .. z_intle:32_10_32[31:24])","z")
            final_list_1[i][j] = final_list_1[i][j].replace("BV64 0x0 .. ","Bool z == ")
            final_list_1[i][j] = final_list_1[i][j].replace("BV32 ","Bool z == ")
            separated_= final_list_1[i][j].split(" ")
            #symbols_.add(separated_[1])
            final_list_1[i][j] = processConstraint(separated_)
    return final_list_1


def makeInitialAnd(c1):
    innerS = "claripy.And("
    innerS = innerS + c1[0]
    for j in range(1,len(c1)):
        innerS = innerS + "," + c1[j]
    innerS = innerS +")"
    return innerS


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
    #print(d)
    return d   
def makeFileAndRun(c1,c2):
    declaration = declareSymbol(symbols_)
    finalS_ = makeConstraintWithNot(
            makeConstraintWithOr(
                makeConstraintWithAnd(
                    c1
                    ,
                    c2
                ), 
                makeConstraintWithAnd(
                makeConstraintWithNot(c1)
                ,
                makeConstraintWithNot(c2)
                )
                )
                )
    f = open("finalRun.py","w")
    f.write("import claripy\n")
    f.write(declaration)
    f.write("\n\np=")
    f.write(finalS_)
    f.write("\ns = claripy.Solver()")
    f.write("\ns.add(p)")
    f.write("\nprint(s.satisfiable())")
    f.close()
    os.system("python finalRun.py>>l.txt")
    f1=open("l.txt","r")
    l=f1.read()
    os.system("rm l.txt")
    return l
 
start = time.time()   
initialization()
symbols_ = set()

list_1_f = open("constraints_1.txt", "r")
list_2_f = open("constraints_2.txt", "r")

final_list_1 = makeList(list_1_f)
final_list_2 = makeList(list_2_f)


final_list_1 = preprocessList(final_list_1)
final_list_2 = preprocessList(final_list_2)

f1=open("matched.txt","w")
f2=open("unmatched.txt","w")
f3=open("nomatched.txt","w")
hash_table = {}
k = 0
for val in symbols_:
    symbol = "x"+str(k)
    k=k+1
    hash_table[val]=symbol
k=0
for con1 in final_list_1:
    c1 = makeInitialAnd(con1)
    for val in symbols_:
        c1=c1.replace(val,hash_table[val])
    final_list_1[k]=c1
    k=k+1
k=0
for con2 in final_list_2:
    c2 = makeInitialAnd(con2)
    for val in symbols_:
        c2=c2.replace(val,hash_table[val])
    final_list_2[k]=c2
    k=k+1

for c1 in final_list_1:
    for c2 in final_list_2:
        check=makeFileAndRun(c1,c2).strip("\n").strip(" ")
        if(check =="False"):
            f1.write(str(c1))
            f1.write("\n")
            f1.write(str(c2))
            f1.write("\n")
            f1.write("=====================\n")
            final_list_2.remove(c2)
            break 
        else:
            f2.write(str(c1))
            f2.write("\n")
            f2.write(str(c2))
            f2.write("\n")
            f2.write("=====================\n")
    if(check=="False"):
        continue
    f3.write(str(c1))
    f3.write("\n")

f3.write("===================\n")
for con2 in final_list_2:
    f3.write(str(con2))
    f3.write("\n")
       
f1.close()
f2.close()
f3.close()
end = time.time() 
print("time : ", end-start)
