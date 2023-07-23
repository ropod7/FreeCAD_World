#!/usr/bin/env python
# -*- coding: utf-8 -*-

__Name__ = 'FreeCAD World'
__Comment__ = 'Flexible parametric design of domical objects'
__Author__ = 'ropod7'
__Version__ = '0.4.2'
__Status__ = 'alpha'
__Date__ = '23.07.2023'
__License__ = 'GNU General Public License v3.0'
__Web__ = 'https://github.com/ropod7/FreeCAD_World'
__Wiki__ = 'https://github.com/ropod7/FreeCAD_World/tree/master/docs'
__Icon__ = ''
__Help__ = 'Inscribed Polygon System'
__Requires__ = '>=FreeCAD-0.20.2 + python3 build'
__Contact__ = 'https://forum.freecad.org/viewtopic.php?f=22&t=53551'
__Communication__ = 'https://forum.freecad.org/viewtopic.php?f=29&t=53554'
__Files__ = 'https://github.com/ropod7/FreeCAD_World'

"""

       In front of you a machine tool for the production of any FreeCAD
      Macros of any complexity with increased accuracy of calculation of
            target objects of polygonal and orthogonal geometry.
     At current stage it works as calc for practical designs of buildings
  and for overall development of kids, students, individuals and households.

"""

###############################################################################
#         ____   _____  __   _______ __  _____    _
#        /  __\ /  _  \|  \_| |  ___|  |/ ____\  |_|
#       |  |___|  |_|  |  _   |  |_ |  |  \_,-,   _
#        \____/ \_____/|_| \__|__|-'|__|\___  |  |_|
#                                           '-'
###############################################################################

# Root object params (mm):
DETAILS  = int(10)  # Detalization of polygon [should be divisible by 4 and min is 4 (otherwise experimental)]
OR     = float(4027.1) # Outscribed R of polygon (or inscribed polygon) & carriage on X axis
H1     = float(2684.1) # Height of 1st 'floor' & carriage on Z (or 0)
LONG   = float(2054.7) # Extension & carriage on Y axis (or 0)
THORUS = dict( # Proportionally expanded (OR becomes IR or both False is DOME)
    CORNER = bool(False), # Inner side of thorus. Outside R of dome becomes inside R
    DISC   = bool(True)  # Outer side of thorus. OR = OR*3
) # template of SpreadSheet system of object:
ROWS    = int(2)#DETAILS/4) # Number of rows revolving around Y axis (min: 0; max: DETAILS/4)
COLS    = int(DETAILS)   # Number of cols revolving around Z axis (min: 0; max: DETAILS)

# Materials (mm)    [ (!!!) it works just with domeFCMacro.py module (!!!) ]:
MONO   = float(200)        # Sheet mtl/Stone/concrete system (wall thickness). if MONO > 0: not FRAME
FRAME = tuple((50, 200)) # (Width, Height) of wooden bar/pipe/sheet mtl. etc: == [Width < Height]

# Construction (mm) [ (!!!) it works just with houseFCMacro.py module (!!!) ]:
HOUSE = dict( # THORUS still experimental:
    FRAME    = tuple((339.7, 1138.9)),# (Width, Height) of wooden bar/pipe/sheet mtl. etc: == [Width < Height]
    INSULANT  = float(692),# Insulant thickness. (!!!) Must be lower than FRAME BAR height (!!!).
    CONTOUR   = float(134.8), # Ventilated contour (if 0 Gives + 1-3 mm). (!!!) Make sure differences between H1, LONG layers (!!!).
    COVER     = float(786.9), # Sheet material thickness (or 0). (!!!) floating CONTOUR space accuracy +\- 2 mm. (!!!)
    # OUTSCRIBE = bool(True) # in case of needs to outscribe THORUS into DOME building according COVER and CONTOUR. (!!!) NOT YET IMPLEMENTED (!!!).
)

# 2 + 2 [ (!!!) it works just with _2plus2FCMacro.py module (!!!) ]:
NICETY = int(100) # Nicety of circle. Precision or decimal digits of modern π. min is 3 (returns 3.14); max 10**4.

# Compound options:
EXTEND   = bool(True)   # Root as open contour system (fill up long, h1, cols, rows)
COMPOUND = bool(False)   # Simple compounded object (if LONG: COLS <= DETAILS/2)
SLICE    = bool(True)    # if EXTEND and SLICE are True returns sliced polygonal parts of (!!!) HOUSE (!!!)

# Movement (mm):
ROTATE = dict( # Rotate COMPOUNDed object
    DO       = bool(False),     # Do rotate or not
    ANGLE  =  float(360/5),     # Angle to rotate object
    CENTER = tuple((OR*6, 0, 0)), # Center of axis to rotate object (x, y, z)
    AXIS   = tuple((0, 0, 1)),  # Rotation axis (around x, around y, around z)
    COPY     = bool(True),     # Copy object to rotate
    TIMES     = int(4)          # How many pcs to COPY. eg. if COPY: polar array.
)
MOVE = dict(     # Move COMPOUNDed object
    DO       = bool(False),    # Do move or not
    VECTOR = tuple((OR*3, -0, 0)), # Vector to move object (x, y, z)
    COPY     = bool(True),     # Copy object to move
    TIMES     = int(5)          # How many pcs to COPY. eg. if COPY: ortho array.
)

# Extra options:
WIREFRAME   = bool(False)   # To reproduce or hide wireframe
ROOT        = bool(True)    # To show just wireframe if reproduced
SOLID       = bool(True)    # Experimental attempt to speedup compound presentation in case of [False]
# PRODUCTION = bool(False)  # Produce Root for production (in case of STL or DXF needs)
PRINT3D     = tuple((0, 0)) # Scale MONO or FRAME (not HOUSE) to 3D printer bed. if > 0 and COMPOUND: do
CLEANUP     = bool(True)    # Clean up document before build
GUI_CLEANUP = bool(False)   # if CLEANUP: to do update screen during clean up
# NEW_DOC     = bool(False)    # Build in new document (except CLEANUP)
CONFIG      = bool(True)    # Switch off CONFIG to extend macros by python3 code

###################################################################################
#######################################################################клинопись###
## top view                                   _ /                                ##
##                                  ^     _ /                                    ##
##                DOME              | _ /             CORNER                     ##             DISC
##     <-                        _  |                                  <- ->     ##
##  y torsion     -----------,      | y axis                         y torsion   ##
##  |                 B   _ /*| B/2 |                                |           ##
##  |                 _ /******|    |                                |           ##
##  |        OR   _ /****** A **| <---[ base of isosceles triangle ] |           ##
##  |         _ /****************|  | [  and base of construction  ] |           ##
##  |     _ /*********************| |                                |           ##
##  |  _/***** B ******************|| 90°        OR*2 on x axis      |           ##
## 0|------------------------------>|------------------------------->|           ##
##  z [ left ] torsion for DOME and THORUS at x,y: [ 0 mm ]                      ##
## _____________________________________________________________________________ ##
##                                                                               ##
##       B = 360°/DETAILS          A + B/2 = 90°        A = (180° - B)/2         ##
###################################################################################
###################################################################################

assert OR,                            "Empty or ZERO Radius definition"
assert FRAME[0] and FRAME[1] or MONO, "Empty cell[/s] in FRAME or MONO definition"
assert FRAME[0] < FRAME[1],           "FRAME width must be lower than FRAME height"
DETAILS = 4 if DETAILS < 4 else DETAILS
h = FRAME[1] + FRAME[0]/2 if not MONO else MONO
MONO = OR if MONO > OR else MONO
H1 = h if H1 < h and H1 else H1
maxrows = int(DETAILS/4)
ROWS = maxrows if ROWS > maxrows else ROWS
ROWS = 0 if ROWS < 0 else ROWS
COLS = DETAILS if COLS > DETAILS else COLS
COLS = 0 if COLS < 0 else COLS
if NICETY < 3: NICETY = 3
elif NICETY > 10**4: NICETY = 10**4

h = HOUSE
assert h['FRAME'][1] > h['INSULANT'], "INSULANT thickness must be lover than FRAME bar height"
