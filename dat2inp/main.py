#!/usr/bin/python3
# coding=utf8
#
# Copyright (c) 2016 - Luís Moreira de Sousa
#
# Simple script converting assorted dat files into .INP (SWMM input format)
#
# Author: Luís Moreira de Sousa (luis.de.sousa[@]protonmail.ch)
# Date: 31-03-2016 

conduits = []
coordinates = []
subcatchments = []

headerFile = "../data/header.inp"

condsFile = '../data/conduits.dat'
coordsFile = '../data/coordinates.dat'
catchFile = '../data/subcatchments.dat'

for line in open(condsFile, 'r'):
    conduits.append(line.rstrip())
    
for line in open(coordsFile, 'r'):
    coordinates.append(line.rstrip())
    
for line in open(catchFile, 'r'):
    subcatchments.append(line.rstrip())
    
fh = open("out.inp","w")

for line in open(headerFile, 'r'):
    print(line.rstrip(), file=fh)
    

print("\n[RAINGAGES]", file=fh)
print(";;Name           Format    Interval SCF      Source ", file=fh)   
print(";;-------------- --------- ------ ------ ----------", file=fh)
ind = 1
for catch in subcatchments:
    sub = catch.split(" ") 
    print(str(ind) + "           0        0         0    ", file=fh)
    ind = ind + 1

# Assuming subcatchments are ordered by outlet node
print("\n[SUBCATCHMENTS]", file=fh)
print(";;Name           Rain Gage        Outlet           Area     %Imperv  Width    %Slope   CurbLen  SnowPack ", file=fh)       
print(";;-------------- ---------------- ---------------- -------- -------- -------- -------- -------- ----------------", file=fh)
ind = 1
for catch in subcatchments:
    sub = catch.split(" ") 
    print(str(ind) + " 0 " + str(ind) + " " + str(float(sub[1])) + " 100 " + str(float(sub[2])) + " " + str(float(sub[3])) + " 0 0", file=fh)
    ind = ind + 1
    
    
print("\n[SUBAREAS]", file=fh)
print(";;Subcatchment   N-Imperv   N-Perv     S-Imperv   S-Perv     PctZero    RouteTo    PctRouted ", file=fh)
print(";;-------------- ---------- ---------- ---------- ---------- ---------- ---------- ----------", file=fh)
ind = 1
for catch in subcatchments:
    sub = catch.split(" ") 
    print(str(ind) + "    0.016      0.25       1.778      5.08       25         OUTLET   ", file=fh)
    ind = ind + 1


print("\n[INFILTRATION]", file=fh)
print(";;Subcatchment   MaxRate    MinRate    Decay      DryTime    MaxInfil  ", file=fh)
print(";;-------------- ---------- ---------- ---------- ---------- ----------  ", file=fh) 
ind = 1
for catch in subcatchments:
    sub = catch.split(" ") 
    print(str(ind) + "           75         1.5        5          7          0    ", file=fh)
    ind = ind + 1
    
    
print("\n[JUNCTIONS]", file=fh)
print(";;Name           Elevation  MaxDepth   InitDepth  SurDepth   Aponded   ", file=fh)
print(";;-------------- ---------- ---------- ---------- ---------- ----------", file=fh)
# Dummy data for now
z = 100
for coord in coordinates:
    junc = coord.split(" ") 
    print(str(int(float(junc[1]))) + " " + str(z) + "    1.5     0     0     0", file=fh)
    z = z - 1

    
print("\n[CONDUITS]", file=fh)
print(";;Name           From Node        To Node          Length     Roughness  InOffset   OutOffset  InitFlow   MaxFlow", file=fh)   
print(";;-------------- ---------------- ---------------- ---------- ---------- ---------- ---------- ---------- ----------", file=fh)
for cond in conduits:
    pipe = cond.split(" ") 
    print(str(int(float(pipe[1]))) + " " + str(int(float(pipe[2]))) + " " + str(int(float(pipe[3]))) + " 0 0.013 0 0 0 0", file=fh)
    
    
print("\n[XSECTIONS]", file=fh)
print(";;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels    Culvert ", file=fh)  
print(";;-------------- ------------ ---------------- ---------- ---------- ---------- ---------- ----------", file=fh)
for cond in conduits:
    pipe = cond.split(" ")
    print(str(int(float(pipe[1]))) + "             CIRCULAR     0.5              0          0          0          1", file=fh)  
    
    
print("\n[COORDINATES]                                       ", file=fh)
print(";;Node           X-Coord            Y-Coord           ", file=fh)
print(";;-------------- ------------------ ------------------", file=fh)
# Note that coordinates are given in km
for coord in coordinates:
    junc = coord.split(" ") 
    print(str(int(float(junc[1]))) + " " + str(float(junc[2]) * 1000) + " " + str(float(junc[3]) * 1000), file=fh)
    

print("\n[REPORT]", file=fh)
print(";;Reporting Options", file=fh)
print("INPUT      NO", file=fh)
print("CONTROLS   NO", file=fh)
print("SUBCATCHMENTS ALL", file=fh)
print("NODES ALL", file=fh)
print("LINKS ALL", file=fh)

fh.close()