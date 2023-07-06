#!/usr/bin/env python
# -*- coding: utf-8 -*-

__Name__ = 'FreeCAD World'
__Comment__ = 'Flexible parametric design of domical objects'
__Author__ = 'ropod7'
__Version__ = '0.3.1'
__Status__ = 'alpha'
__Date__ = '06.07.2023'
__License__ = 'GNU General Public License v3.0'
__Web__ = 'https://github.com/ropod7/FreeCAD_World'
__Wiki__ = 'https://github.com/ropod7/FreeCAD_World/tree/master/docs'
__Icon__ = ''
__Help__ = 'Inscribed Polygon System'
__Requires__ = 'python3'
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
DETAILS  = int(4)  # Detalization of polygon [should be divisible by 4 and min is 4 (otherwise experimental)]
OR     = float(4300) # Outscribed R of polygon (or inscribed polygon) & carriage on X axis
H1     = float(6210/2) # Height of 1st 'floor' & carriage on Z (or 0)
LONG   = float(6210) # Extension & carriage on Y axis (or 0)
THORUS = dict( # Proportionally expanded (OR becomes IR or both False is DOME)
    CORNER = bool(False), # Inner side of thorus. Outside R of dome becomes inside R
    DISC   = bool(False)  # Outer side of thorus. OR = OR*3
) # template of SpreadSheet system of object:
ROWS    = int(DETAILS/4) # Number of rows revolving around Y axis (min: 0; max: DETAILS/4)
COLS    = int(DETAILS/4)   # Number of cols revolving around Z axis (min: 0; max: DETAILS)

# Materials (mm)    [ (!!!) it works just with domeFCMacro.py module (!!!) ]:
MONO   = float(50)        # Sheet mtl/Stone/concrete system (wall thickness). if MONO > 0: not FRAME
FRAME = tuple((50, 200)) # (Width, Height) of wooden bar/pipe/sheet mtl. etc: == [Width < Height]

# Construction (mm) [ (!!!) it works just with houseFCMacro.py module (!!!) ]:
HOUSE = dict( # THORUS still experimental:
    FRAME    = tuple((50, 200)),# (Width, Height) of wooden bar/pipe/sheet mtl. etc: == [Width < Height]
    INSULANT  = float(100),# Insulant thickness. (!!!) Must be lower than FRAME BAR height (!!!).
    CONTOUR   = float(50), # Ventilated contour (or 0). Gives + 3-5 mm. (!!!) Make sure differences between H1, LONG layers (!!!).
    COVER     = float(15), # Sheet material thickness (or 0). (!!!) floating CONTOUR space accuracy +\- 2 mm. (!!!)
    # OUTSCRIBE = bool(True) # in case of needs to outscribe THORUS into DOME building according COVER and CONTOUR. (!!!) NOT YET IMPLEMENTED (!!!).
)

# Compound options:
EXTEND   = bool(True)   # Root as open contour system (fill up long, cols etc.)
COMPOUND = bool(True)   # Simple compounded object (if LONG: COLS <= DETAILS/2)

# Movement (mm):
ROTATE = dict( # Rotate compounded or extended object
    DO       = bool(False),     # Do rotate or not
    ANGLE  =  float(180),     # Angle to rotate object
    CENTER = tuple((0, 0, 0)), # Center of axis to rotate object (x, y, z)
    AXIS   = tuple((0, 1, 0)),  # Rotation axis (around x, around y, around z)
    COPY     = bool(True),     # Copy object to rotate
    TIMES     = int(1)          # How many pcs to COPY. eg. if COPY: polar array.
)
MOVE = dict(     # Move compounded or extended object
    DO       = bool(False),    # Do move or not
    VECTOR = tuple((1500, -0, 0)), # Vector to move object (x, y, z)
    COPY     = bool(False),     # Copy object to move
    TIMES     = int(1)          # How many pcs to COPY. eg. if COPY: ortho array.
)

# Extra options:
WIREFRAME  = bool(False)   # To reproduce or hide wireframe
ROOT       = bool(True)    # To show just wireframe if reproduced
SOLID      = bool(True)    # Experimental attempt to speedup compound presentation in case of [False]
# PRODUCTION = bool(False) # Produce Root for production (in case of STL or DXF needs)
PRINT3D   = tuple((0, 0))  # Scale MONO or FRAME (not HOUSE) to 3D printer bed. if > 0 and COMPOUND: do
CLEANUP    = bool(True)    # Clean up document before build
CONFIG     = bool(True)    # Switch off CONFIG to extend macros by python3 code

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

assert OR,                            "Empty Radius definition"
assert FRAME[0] and FRAME[1] or MONO, "Empty cell[/s] in FRAME or MONO definition"
assert FRAME[0] < FRAME[1],           "FRAME width must be lower than FRAME height"
DETAILS = 4 if DETAILS < 4 else DETAILS
h = FRAME[1] + FRAME[0]/2 if not MONO else MONO
MONO = OR if MONO > OR else MONO
H1 = h if H1 < h and H1 else H1
maxrows = int(DETAILS/4)
ROWS = maxrows if ROWS > maxrows else ROWS
COLS = DETAILS if COLS > DETAILS else COLS

h = HOUSE
assert h['FRAME'][1] > h['INSULANT'], "INSULANT thickness must be lover than FRAME bar height"
