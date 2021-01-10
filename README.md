# FreeCAD World
Macro system of FreeCAD World

In front of you a machine tool for the production of any FreeCAD Macros of any complexity with increased accuracy of calculation of target objects of polygonal and orthogonal geometry.
In current stage it works as calc for practical designs of buildings and for overall development of kids, students, individuals and households.

```Python
###################################################################################
#######################################################################клинопись###
## top view                                   _ /                                ##
##                                  ^     _ /                                    ##
##                DOME              | _ /             CORNER                     ##             DISC
##     <-                        _  |                                    ->      ##
##  y torsion     -----------,      | y axis                         y torsion   ##
##  |                 B   _ /*| B/2 |                                |           ##
##  |                 _ /******|    |                                |           ##
##  |        OR   _ /****** A **| <---[ base of isosceles triangle ] |           ##
##  |         _ /****************|  | [  and base of construction  ] |           ##
##  |     _ /*********************| |                                |           ##
##  |  _/***** B ******************|| 90°      OR*2 on x axis        |           ##
## 0|------------------------------>|------------------------------->|           ##
##  z [ left ] torsion for DOME and THORUS at x,y: [ 0 mm ]                      ##
## _____________________________________________________________________________ ##
##                                                                               ##
##       B = 360°/DETAILS          A + B/2 = 90°        A = (180° - B)/2         ##
###################################################################################
###################################################################################
```
[![Macro Video](https://img.youtube.com/vi/GIyBWlv_GzM/0.jpg)](https://www.youtube.com/watch?v=GIyBWlv_GzM)

![dome_thorus](https://i.ibb.co/9qpVSw3/screenshot-2021-01-08-19-52-38.png)

# dependencies: FreeCAD + python3 build
