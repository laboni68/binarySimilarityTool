#!/bin/bash
#!/usr/bin/python
import os
import sys

for i in range(2):
    command = "python runLogicalSummary.py nano nano_processed dfs 20000"
    os.system(command)
for i in range(2):
    command = "python runLogicalSummary.py nano nano_processed memWatch 20000"
    os.system(command) 
for i in range(2):
    command = "python runLogicalSummary.py nano nano_processed loopSeer 20000"
    os.system(command) 
