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
junctions = []
polygons = []
outfalls = []
subcatchments = []

headerFile = "../data/header.inp"

condsFile = '../data/conduits.dat'
coordsFile = '../data/coordinates.dat'
juncsFile = '../data/junctions.dat'
mapFile = '../data/map.dat'
fallsFile = '../data/outfalls.dat'
polysFile = '../data/polygons.dat'
catchFile = '../data/subcatchments.dat'


outputFile = "/home/desouslu/EAWAG/out.inp"

for line in open(condsFile, 'r'):
    conduits.append(line.rstrip())
    
for line in open(coordsFile, 'r'):
    coordinates.append(line.rstrip())
      
for line in open(juncsFile, 'r'):
    junctions.append(line.rstrip())
 
for line in open(fallsFile, 'r'):
    outfalls.append(line.rstrip()) 
       
for line in open(polysFile, 'r'):
    polygons.append(line.rstrip())
         
for line in open(catchFile, 'r'):
    subcatchments.append(line.rstrip())
    
fh = open(outputFile,"w")

for line in open(headerFile, 'r'):
    print(line.rstrip(), file=fh)
    

# Get rid of headers
conduits.pop(0)
coordinates.pop(0)
junctions.pop(0)
outfalls.pop(0)
polygons.pop(0)
subcatchments.pop(0)
    

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
    print(str(ind) + " " + str(ind) + " " + sub[0] + " " + sub[1] + " 100 " + sub[2] + " " + sub[3] + " 0 0", file=fh)
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
# The first junction is an outfall
junctions.pop(0)
ind = 2
for junc in junctions:
    print(str(ind) + " " + junc.split(" ")[0] + "    1.5     0     0     0", file=fh)
    ind = ind + 1


print("\n[OUTFALLS]", file=fh)
print(";;Name           Elevation  Type       Stage Data       Gated    Route To ", file=fh)       
print(";;-------------- ---------- ---------- ---------------- -------- ----------------", file=fh)
for out in outfalls:
    fall = out.split(" ")
    print(fall[0] + " " + fall[1] + "    FREE                        NO            ", file=fh)

    
print("\n[CONDUITS]", file=fh)
print(";;Name           From Node        To Node          Length     Roughness  InOffset   OutOffset  InitFlow   MaxFlow", file=fh)   
print(";;-------------- ---------------- ---------------- ---------- ---------- ---------- ---------- ---------- ----------", file=fh)
ind = 1
for cond in conduits:
    pipe = cond.split(" ") 
    print(str(ind) + " " + pipe[0] + " " + pipe[1] + " " + pipe[2] + " 0.013 0 0 0 0", file=fh)
    ind = ind + 1
    
    
print("\n[XSECTIONS]", file=fh)
print(";;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels    Culvert ", file=fh)  
print(";;-------------- ------------ ---------------- ---------- ---------- ---------- ---------- ----------", file=fh)
for ind in range(len(conduits)):
    print(str(ind+1) + "             CIRCULAR     0.5              0          0          0          1", file=fh)  
    
    
print("\n[COORDINATES]                                       ", file=fh)
print(";;Node           X-Coord            Y-Coord           ", file=fh)
print(";;-------------- ------------------ ------------------", file=fh)
ind = 1
for coord in coordinates:
    junc = coord.split(" ") 
    print(str(ind) + " " + junc[0] + " " + junc[1], file=fh)
    ind = ind + 1
    
    
print("\n[Polygons]                                      ", file=fh)
print(";;Subcatchment   X-Coord            Y-Coord           ", file=fh)
print(";;-------------- ------------------ ------------------", file=fh)
for poly in polygons:
    pol = poly.split(" ") 
    print(pol[0] + " " + pol[1] + " " + pol[2], file=fh)
    

print("\n[REPORT]", file=fh)
print(";;Reporting Options", file=fh)
print("INPUT      NO", file=fh)
print("CONTROLS   NO", file=fh)
print("SUBCATCHMENTS ALL", file=fh)
print("NODES ALL", file=fh)
print("LINKS ALL", file=fh)

fh.close()