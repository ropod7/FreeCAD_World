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
import inspect

import domeFCMacro
importlib.reload(domeFCMacro)

from domeFCMacro import ThorusPoints, FrameDome, FrameCorner, FrameDisc, \
        FrameThorus, FrameRoot, Materials, MonoWireFrame, ModelRoot,      \
        MonoDome, MonoCorner, Frame, MonoModelLayer, MonoRoot,             \
        Root, MonoExtend, MonoDisc, MonoThorus, Compound,                   \
        compoundModel, MonoCompound, FrameExtend, FrameCompound

# BEGIN: House Frame root creation system

class HouseFrameRoot(FrameRoot):
    _mtrl_ = FrameRoot._mtl_

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class HouseFrameDome(FrameDome, HouseFrameRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class HouseFrameCorner(FrameCorner, HouseFrameRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class HouseFrameDisc(FrameDisc, HouseFrameRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class HouseFrameThorus(FrameThorus, HouseFrameRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class HouseFrame(Root):
    _roots_ = {
        Root._dome_ : HouseFrameDome,
        Root._corn_ : HouseFrameCorner,
        Root._disc_ : HouseFrameDisc,
        Root._thor_ : HouseFrameThorus
    }

    def __new__(cls, *args, root=None, OUTSCRIBE=False, **kwargs):
        assert root in __class__._roots_.keys(), "TypeError: unknown type of building"
        clss = __class__._roots_.get(root)
        return super().__new__(cls, clss, *args, **kwargs)

# END: House Frame root creation system

# BEGIN: Insulant root creation system

class InsulantWireFrame(MonoWireFrame):
    _mtl_ = str('insulant')

    def _createMonoWireFrame(self, *args, **kwargs):
        mtl = __class__._mtl_
        super()._createMonoWireFrame(*args, mtl=mtl, **kwargs)

class InsulantModelLayer(MonoModelLayer, InsulantWireFrame):
    _tool_ = str('tools')
    _fram_ = str('frame_') + _tool_

    def _cutPolyH1ByFrame(self, block):
        frame = self.house_frame
        h1b = self.copy( frame.getRoot(FrameRoot._h1ba_) )
        h1b = self._moveBtmHorBarTool(h1b, frame.MTL, mono=True)
        return self._cutHPolysByTool(block, h1b)

    def _cutPolyPolys(self, e):
        blocks = super()._cutPolyPolys(e)
        return self.__cutPolyPolysByFrame(blocks)

    def __cutPolyPolysByFrame(self, blocks):
        pTool = self.house_frame.polygon_tool
        b = self._cutHPolysByTool(blocks, pTool)
        tools = self.__getPolyPolyTools()
        obj, blocks = list(), list()
        if not self.less_rows and self.quatro and self.dome:
            blocks.extend(self.cut( [b[0]], [tools[0]] ))
            b = b[1:]
        for i in range(len(tools)-1):
            obj.append(   self.cut( [b[i]], [tools[i]]   ))
            blocks.extend(self.cut( obj[i], [tools[i+1]] ))
        return blocks

    def __getPolyPolyTools(self):
        frame = self.house_frame
        allb = frame.getRoot(FrameRoot._hplb_)
        l = int(len(allb)/2)
        corn_and_thor = self.corn and frame.thor
        corn_less_rows = corn_and_thor and self.less_rows
        corn_not_quatro = corn_and_thor and not self.quatro
        thor_and_thor = self.thor and frame.thor
        abs_quatro = not self.less_rows and self.quatro
        if corn_not_quatro or corn_less_rows:
            bars = allb[:l]
        elif corn_and_thor:
            bars = allb[:l+1]
        elif thor_and_thor and abs_quatro:
            bars = [ allb[0] ]
            bars.extend(allb[l+1:])
        elif thor_and_thor:
            bars = allb[l:]
        else: bars = allb
        return self.copy(bars.copy())

    def _cutExtPoly(self, block):
        frame = self.house_frame
        tools = self.copy( frame.getRoot(FrameRoot._shte_) )
        dir_y = -1 if self.disc else 1
        tools.extend(self.pArrayYB(tools, dir_y))
        for t in tools:
            block = self.cut(block, [t])
        return block

    def _cutOnTopH1(self, block, tool):
        frame = self.house_frame
        times = self.house_frame.insH1N-1
        dim = self.house_frame.insH1L
        dim *= times
        b = self.h1Lift(block, dim)
        b = self.cut(b, tool)
        b = self.h1Lift(b, dim/times)
        b = self.cut(b, tool)
        return self.h1Drop(b, dim+dim/times)

    def _getExtrudeReduce(self):
        frame = self.house_frame
        fWidth = self.frame[0]
        return (self.insLongL-frame.insLongL+fWidth), fWidth

class InsulantRoot(MonoRoot, InsulantModelLayer):
    _mtrl_ = InsulantWireFrame._mtl_
    _hpl_  = MonoRoot._hpl_

    def __init__(self, *args, **kwargs):
        super().__init__(*args, RGB=(1.0,1.0,1.0), **kwargs)

    def wireFrame(self, *args, **kwargs):
        super().wireFrame(*args, **kwargs)

    def _build(self, **kwargs):
        super()._build(**kwargs)

    def _buildPolyH1(self):
        w = self.insH1L-self.frame[0]
        try: b, tp = super()._buildPolyH1(cls=__class__, w=w)
        except TypeError: return
        block = self._cutPolyH1ByFrame(b)
        block = self.h1Lift(block, self.frame[0]/2)
        return self.extendRoot(tp, block)

    def _buildExtH1(self):
        reduc, fWidth = self._getExtrudeReduce()
        try: b, tp  = super()._buildExtH1(cls=__class__, reduc=reduc)
        except TypeError: return
        frame  = self.house_frame
        b  = self.move(b, 0,-fWidth/2,0, 1, vis=True, cp=False)
        tool = self.copy( frame.getRoot(FrameRoot._shte_) )
        expr = self.insH1N > 1
        cut = self._cutOnTopH1 if expr else self.cut
        block = cut(b, tool)
        return self.extendRoot(tp, block)

    def _buildPolyPoly(self):
        blocks = super()._buildPolyPoly(cls=__class__)

    def _buildExtPoly(self):
        reduc, fWidth = self._getExtrudeReduce()
        try: b, tp = super()._buildExtPoly(cls=__class__, reduc=reduc)
        except TypeError: return
        b = self.move(b, 0,-fWidth/2,0, 1, vis=True, cp=False)
        block = self._cutExtPoly(b)
        return self.extendRoot(tp, block)

    @property
    def house_frame(self):
        try: return self.__house_frame_
        except AttributeError:
            self.__house_frame_ = None
        return self.__house_frame_

    @house_frame.setter
    def house_frame(self, house_frame):
        assert isinstance(house_frame, FrameRoot), "TypeError: unknown type of frame"
        self.__house_frame_ = house_frame
        return self.__house_frame_

    @house_frame.deleter
    def house_frame(self):                          # calling in Compound options
        del self.__house_frame_

class InsulantDome(MonoDome, InsulantRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class InsulantCorner(MonoCorner, InsulantRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class InsulantDisc(MonoDisc, InsulantRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class InsulantThorus(MonoThorus, InsulantRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Insulant(Root):
    _roots_ = {
        Root._dome_ : InsulantDome,
        Root._corn_ : InsulantCorner,
        Root._disc_ : InsulantDisc,
        Root._thor_ : InsulantThorus
    }

    def __new__(cls, frame, insulant, lng, h1, Or, dets, root=None, OUTSCRIBE=False, **kwargs):
        assert root in __class__._roots_.keys(), "TypeError: unknown type of building"
        clss = __class__._roots_.get(root)
        obj = super().__new__(cls, clss, insulant, lng, h1, Or, dets, **kwargs)
        cls.setOR(obj, Or, frame[0], root, OUTSCRIBE)
        obj.frame = frame
        return obj

    @classmethod
    def setOR(cls, obj, Or, matW, root, OUTSCRIBE):
        if root == Root._dome_ or root == Root._disc_: return
        obj.X_ORreduced = -obj.rightSideB_ByA(matW/1.5, obj.DETAIL_A)

    @property
    def frame(self):
        try: return self.__frame_
        except AttributeError:
            self.__frame_ = tuple()
        return self.__frame_

    @frame.setter
    def frame(self, frame):
        self.__frame_ = frame
        return self.__frame_

# END: Insulant root creation system

# BEGIN: Cover root creation system

class CoverRoot(MonoRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CoverDome(MonoDome, CoverRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CoverCorner(MonoCorner, CoverRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CoverDisc(MonoDisc, CoverRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CoverThorus(MonoThorus, CoverRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Cover(Root):
    _min_contour_ = int(3)  # if CONTOUR is 0 and COVER > 0 add 3 mm between layers
    _roots_ = {
        Root._dome_ : CoverDome,
        Root._corn_ : CoverCorner,
        Root._disc_ : CoverDisc,
        Root._thor_ : CoverThorus
    }

    def __new__(cls, cover, contour, lng, h1, Or, dets, root=None, OUTSCRIBE=False, **kwargs):
        assert root in __class__._roots_.keys(), "TypeError: unknown type of building"
        clss = __class__._roots_.get(root)
        obj = super().__new__(cls, clss, cover, lng, h1, Or, dets, **kwargs)
        cls.setOR(obj, Or, cover, contour, root)
        return obj

    @classmethod
    def setOR(cls, obj, Or, cover, contour, root):
        contour = __class__._min_contour_ if not contour else contour
        contour = obj.rightHypothenuseByA(contour, obj.DETAIL_A)
        produce = contour + obj.rightHypothenuseByA(cover, obj.DETAIL_A)
        if root == Root._dome_:
            obj.X_ORreduced = produce
        elif root == Root._corn_:
            reduc = produce
            obj.X_ORreduced = reduc
        elif root == Root._disc_ or root == Root._thor_:
            reduc = produce
            obj.X_ORreduced = reduc

# END: Cover root creation system

# BEGIN: House root creation system

class House(object):

    def __init__(self, *args, FRAME=None, INSULANT=None, CONTOUR=None, COVER=None, **kwargs):
        assert isinstance(FRAME, tuple), "TypeError: FRAME must be tuple"
        assert len(FRAME) == 2,     "Wrong tuple length. Must be 2 as (width, height)"
        assert FRAME[0] < FRAME[1], "FRAME width must be lower than FRAME height"
        assert INSULANT < FRAME[1], "INSULANT must be lower than FRAME height"
        assert CONTOUR >= 0,        "CONTOUR must be higher than 0 or 0"
        self.house_frame = HouseFrame(*(*FRAME, *args), **kwargs)
        self.insulant = Insulant(FRAME, INSULANT, *args, **kwargs)
        self.cover = Cover(COVER, CONTOUR, *args, **kwargs) if COVER else None
        self.insulant.house_frame = self.house_frame                     #
        del self.house_frame                                             # reduce amount of objects

    def wireFrame(self, *args, **kwargs):
        self.__run(*args, **kwargs)

    def root(self, *args, **kwargs):
        self.__run(*args, **kwargs)
        return [ self.insulant, self.cover ]

    def cprint(self, *args):
        try: return self.insulant.cprint(*args)
        except AttributeError: return

    def __run(self, *args, **kwargs):
        mn = inspect.stack()[1][3]
        objs = [ self.insulant.house_frame, self.insulant, self.cover ]
        [ getattr(o, mn)(*args, **kwargs) for o in objs if o is not None ]

# END: House root creation system

# BEGIN: Basic flexible extends and compounds oh House

class HouseExtend(FrameExtend, MonoExtend):

    def __init__(self, objs, **kwargs):
        insulant, cover = objs
        tmp = FrameExtend(insulant.house_frame, **kwargs)
        self.__hfr_ = tmp.obj
        tmp = MonoExtend(insulant, **kwargs)
        self.__ins_ = tmp.obj
        tmp = MonoExtend(cover, **kwargs) if cover else None
        self.__cvr_ = tmp.obj if cover else None
        del tmp

    @property
    def obj(self):          # HouseFrame object as Root object of Compound
        return self.__hfr_

    @property               # HouseFrame object
    def hfr(self):
        return self.__hfr_

    @property               # Insulant object
    def ins(self):
        return self.__ins_

    @property                # Cover object
    def cvr(self):
        return self.__cvr_

class HouseCompound(HouseExtend):
    _totl_ = Compound._totl_
    _abs_totl_ = str('absolute_') + _totl_

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._collectTotal(self.hfr)
        self._collectTotal(self.ins)
        if self.cvr:
            self._collectTotal(self.cvr)

    def compound(self):
        abs_total = __class__._abs_totl_
        hfr_total = super().compound(obj=self.hfr)
        ins_total = super().compound(obj=self.ins)
        cvr_total = super().compound(obj=self.cvr) if self.cvr else None
        totals = [ hfr_total, ins_total, cvr_total ]
        [ self.obj.extend(abs_total, t) for t in totals if t is not None ]

    def rotate(self, *args):
        objs = self.obj.get(__class__._abs_totl_)
        return super()._rotate(objs, *args)

    def move(self, vector, *args):
        objs = self.obj.get(__class__._abs_totl_)
        x,y,z = vector
        return super()._move(objs, x,y,z, *args)

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

    args = (LONG, H1, OR, DETAILS)

    if       THORUS.get('CORNER') and not THORUS.get('DISC'):
        root = Root._corn_
        obj = House(*args, root=root, cleanup=CLEANUP, **HOUSE)

    elif not THORUS.get('CORNER') and     THORUS.get('DISC'):
        root = Root._disc_
        obj = House(*args, root=root, cleanup=CLEANUP, **HOUSE)

    elif     THORUS.get('CORNER') and     THORUS.get('DISC'):
        root = Root._thor_
        obj = House(*args, root=root, cleanup=CLEANUP, **HOUSE)

    else:
        root = Root._dome_
        obj = House(*args, root=root, cleanup=CLEANUP, **HOUSE)

    OBJ = HouseCompound

    obj.wireFrame(ROWS, COLS, vis=WIREFRAME)
    if not ROOT: exit(0)

    objs = obj.root(solid=SOLID)

    for o in [ Root._dome_, Root._corn_, Root._disc_, Root._thor_ ]:
        compoundModel( root, objs, o, OBJ, EXTEND, COMPOUND, ROTATE, MOVE )

    t = time.time() - t
    m = int(t/60)
    s = t - m*60
    obj.cprint('Executed in: {0} minutes, {1:.1f} seconds'.format(m, s))

elif main and not CONFIG:
    "Start coding here disabling CONFIG and TEST"
    # As example created "heart system":
    pass

