#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################################################
#
#        _   _  ___  _   _  ___  ____
#       | |_| |/ _ \| | | |/ __\|  __|
#       |  _  | |_| | |_| |\__ \|  _|        [ logic ]:
#       |_| |_|\___/ \___/ \___/|____|
#
#
###################################################################################

import time
import importlib

import domeFCMacro
importlib.reload(domeFCMacro)

from domeFCMacro import Materials, FrameWireFrame,   \
        Root, Mono, Frame, MonoExtend, compoundModel, \
        MonoCompound, FrameExtend, FrameCompound

# BEGIN: Frame root creation system

class HouseFrameWireFrame(Frame):
    _mtl_ = FrameWireFrame._mtl_

class HouseFrame(HouseFrameWireFrame):
    _mtrl_ = HouseFrameWireFrame._mtl_

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

# END: Frame root creation system

# BEGIN: Insulant root creation system

class InsulantWireFrame(Mono):
    _mtl_ = str('insulant')

    def _createMonoWireFrame(self, *args, **kwargs):
        return super()._createMonoWireFrame(*args, **kwargs)

class InsulantModelLayer(InsulantWireFrame):
    _tool_ = str('tools')

    def __buildTools(self, tp, *args, **kwargs):
        mid = super().__buildTools(*args, **kwargs)


class Insulant(InsulantModelLayer):
    _mtrl_ = InsulantWireFrame._mtl_

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

# END: Insulant root creation system

# BEGIN: Cover root creation system

class CoverWireFrame(Mono):
    _mtl_ = str('cover')

    def _createCoverWireFrame(self, ny, MTL, **kwargs):
        mtl = __class__._mtl_

class Insulant(InsulantModelLayer):
    _mtrl_ = CoverWireFrame._mtl_

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

# END: Cover root creation system

# BEGIN: House root creation system

class House(Root):

    def __init__(self, det, Or, h1, lng, thor, rows, cols, house, tp=None, cleanup=True):
        pass

    def wireFrame(self, rows, cols, vis=False):
        pass

    def root(self, solid=True):
        pass

# END: House root creation system

# BEGIN: Basic flexible extends and compound oh House

class HouseExtend(MonoExtend, FrameExtend):
    pass

class HouseCompound(MonoCompound, FrameCompound):
    pass

# END: Basic flexible extends and compound oh House

# BEGIN: Coding

###################################################################################
#
#                               [ coding ]:
#
###################################################################################

main = __name__ == '__main__'

if main:

    import config
    importlib.reload(config)

    from config import DETAILS, OR, H1, LONG, THORUS, ROWS, \
            COLS, HOUSE, EXTEND, COMPOUND, ROTATE, MOVE,     \
            WIREFRAME, ROOT, SOLID, PRINT3D, CLEANUP, CONFIG

if main and CONFIG:

    t = time.time()

    args = (DETAILS, OR, H1, LONG, THORUS, ROWS, COLS, HOUSE)

    if       THORUS.get('CORNER') and not THORUS.get('DISC'):
        OBJ = str('CORNER')
        obj = House(*args, tp=OBJ, cleanup=CLEANUP)

    elif not THORUS.get('CORNER') and     THORUS.get('DISC'):
        OBJ = str('DISC')
        obj = House(*args, tp=OBJ, cleanup=CLEANUP)

    elif     THORUS.get('CORNER') and     THORUS.get('DISC'):
        OBJ = str('THORUS')
        obj = House(*args, tp=OBJ, cleanup=CLEANUP)

    else:
        OBJ = str('DOME')
        obj = House(*args, tp=OBJ, cleanup=CLEANUP)

    COMP = HouseCompound

    obj.wireFrame(ROWS, COLS, vis=WIREFRAME)
    if not ROOT: exit(0)

    obj.root(solid=SOLID)

    for o in ['DOME', 'CORNER', 'DISC', 'THORUS']:
        compoundModel( OBJ, obj, o, COMP, EXTEND, COMPOUND, ROTATE, MOVE )

    t = time.time() - t
    m = int(t/60)
    s = t - m*60
    # obj.cprint('Executed in: {0} minutes, {1:.1f} seconds'.format(m, s))
    obj.cprint('NOT YET IMPLEMENTED')

elif main and not CONFIG:
    "Start coding here disabling CONFIG and TEST"
    # As example created "heart system":
    pass

