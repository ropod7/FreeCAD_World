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

from domeFCMacro import Blocks, Materials, ModelRoot, MonoGraduatedArc

from domeFCMacro import Root, FrameRoot, FrameDome, FrameCorner, \
        FrameDisc, FrameThorus, MonoWireFrame, MonoModelLayer,    \
        MonoRoot, MonoDome, MonoCorner, MonoDisc, MonoThorus,      \
        Compound, FrameCompound, MonoCompound, compoundModel

# BEGIN: House Frame root creation system

class HouseFrameRoot(FrameRoot):

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

class InsulantMaterials(Materials):

    def __init__(self, *args, frame_w=None,  **kwargs):
        super().__init__(*args, **kwargs)
        self.__insulant = True
        self.__frame_w = frame_w

    @property
    def INSULANT(self):
        return self.__insulant

    @property
    def FRAME_W(self):
        return self.__frame_w

class InsulantModelRoot(ModelRoot):

    def _setMaterial(self, **kwargs):
        self.MTL = InsulantMaterials(self, **kwargs)

class InsulantWireFrame(MonoWireFrame, InsulantModelRoot):
    _mtl_ = str('insulant')

    def _createMonoWireFrame(self, *args, **kwargs):
        mtl = __class__._mtl_
        super()._createMonoWireFrame(*args, mtl=mtl, **kwargs)

class InsulantModelLayer(MonoModelLayer, InsulantWireFrame):

    def _cutPolyH1ByFrame(self, block):
        frame = self.house_frame
        h1b = self.copy( frame.getRoot(FrameRoot._h1ba_) )
        h1b = self._moveBtmHorBarTool(h1b, frame.MTL, mono=True)
        return self._cutHPolysByTool(block, h1b)

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
        times = frame.insH1N-1
        dim = frame.insH1L
        dim *= times
        b = self.h1Lift(block, dim)
        b = self.cut(b, tool)
        b = self.h1Lift(b, dim/times)
        b = self.cut(b, tool)
        return self.h1Drop(b, dim+dim/times)

class InsulantRoot(MonoRoot, InsulantModelLayer):
    _mtrl_ = InsulantWireFrame._mtl_

    def __init__(self, tp, thickn, *args,                                # absolute self __init__
            frame_w=None, RGB=(1.0,1.0,1.0),
            **kwargs):
        assert thickn,  "No Insulant thickness defined"
        assert frame_w, "No Frame width defined"
        self._setMaterial(thickn=thickn, RGB=RGB, frame_w=frame_w, **kwargs)
        MonoGraduatedArc.__init__(self, tp, *args, **kwargs)

    def wireFrame(self, *args, **kwargs):
        mnp = -(self.MTL.FRAME_W/(self.DETAILS/2)) if self.corn else 0   # additional move just for corner
        super().wireFrame(*args, marking=True, manipulator=mnp, **kwargs)

    def _build(self, **kwargs):
        super()._build(**kwargs)

    def _buildPolyH1(self):
        w = self.insH1L-self.MTL.FRAME_W
        try: b, tp = super()._buildPolyH1(cls=__class__, w=w)
        except TypeError: return
        block = self._cutPolyH1ByFrame(b)
        block = self.h1Lift(block, self.MTL.FRAME_W/2)
        self.updateGui(True, fitV=True)
        return self.extendRoot(tp, block)

    def _buildExtH1(self):
        fWidth = self.MTL.FRAME_W
        try: b, tp = super()._buildExtH1(cls=__class__, reduc=fWidth)
        except TypeError: return
        block = self.move(b, 0,-fWidth/2,0, 1, vis=True, cp=False)
        if not self.thor:
            frame = self.house_frame
            tool = self.copy( frame.getRoot(FrameRoot._shte_) )
            expr = self.insH1N > 1
            cut = self._cutOnTopH1 if expr else self.cut
            block = cut(block, tool)
        self.updateGui(True, fitV=True)
        return self.extendRoot(tp, block)

    def _buildPolyPoly(self):
        rev = self.MTL.FRAME_W/2
        blocks = super()._buildPolyPoly(cls=__class__, rev=rev)

    def _buildExtPoly(self):
        fWidth = self.MTL.FRAME_W
        try: b, tp = super()._buildExtPoly(cls=__class__, reduc=fWidth)
        except TypeError: return
        b = self.move(b, 0,-fWidth/2,0, 1, vis=True, cp=False)
        block = self._cutExtPoly(b)
        self.updateGui(True, fitV=True)
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
    def house_frame(self):
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

    def wireFrame(self, *args, **kwargs):
        self.__cornWireFrame(*args, **kwargs)
        self.__thorWireFrame(*args, **kwargs)
        return self.get(Blocks._wfr_)

    def __cornWireFrame(self, *args, **kwargs):
        self.pointSystem = Root._corn_
        return self.__wireFrame(*args, **kwargs)

    def __thorWireFrame(self, *args, **kwargs):
        self.pointSystem = Root._thor_
        return self.__wireFrame(*args, **kwargs)

    def __wireFrame(self, *args, **kwargs):
        return InsulantRoot.wireFrame(self, *args, **kwargs)

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
        obj = super().__new__(cls, clss, insulant, lng, h1, Or, dets, frame_w=frame[0], **kwargs)
        return obj

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

    def __init__(self, *args,
            FRAME=None, INSULANT=None, CONTOUR=None, COVER=None,
            cleanup=None, **kwargs):
        assert isinstance(FRAME, tuple), "TypeError: FRAME must be type of tuple"
        assert len(FRAME) == 2,     "Wrong tuple length. Must be 2 as (width, height)"
        assert FRAME[0] < FRAME[1], "FRAME width must be lower than FRAME height"
        assert INSULANT < FRAME[1], "INSULANT must be lower than FRAME height"
        assert CONTOUR >= 0,        "CONTOUR must be higher than 0 or 0"
        self.house_frame = HouseFrame(*(*FRAME, *args), cleanup=cleanup, **kwargs)
        self.insulant = Insulant(FRAME, INSULANT, *args, cleanup=False, **kwargs)
        self.cover = Cover(COVER, CONTOUR, *args, cleanup=False, **kwargs) if COVER else None
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

# BEGIN: Basic flexible extend and compound of House

class HouseExtend(FrameCompound, MonoCompound):

    def __init__(self, objs, **kwargs):
        insulant, cover = objs
        tmp = FrameCompound(insulant.house_frame, **kwargs)
        self.__hfr_ = tmp.obj
        del insulant.house_frame                                         # reduce amount of objects
        tmp = MonoCompound(insulant, **kwargs)
        self.__ins_ = tmp.obj
        tmp = MonoCompound(cover, **kwargs) if cover else None
        self.__cvr_ = tmp.obj if cover else None
        self.__cols = tmp.cols
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

    @property
    def cols(self):
        return self.__cols

class HouseCompound(HouseExtend):
    _hplb_ = FrameRoot._hplb_
    _hpl_  = MonoRoot._hpl_
    _totl_ = Compound._totl_
    _abs_totl_ = str('absolute_') + _totl_

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compound(self, obj=None, **kwargs):
        if obj is None: return
        abs_total = __class__._abs_totl_
        hfr_total = FrameCompound.compound(self, obj=self.hfr)
        ins_total = MonoCompound.compound(self, obj=self.ins)
        cvr_total = MonoCompound.compound(self, obj=self.cvr) if self.cvr else None
        totals = [ hfr_total, ins_total, cvr_total ]
        [ self.obj.extend(abs_total, t) for t in totals if t is not None ]

    def slicePolys(self, hideobj=True):
        if not self.obj.rows or not self.obj.cols: return
        obj, slc = self.obj, list()
        xOr = (obj.OR + obj.X_ORreduced*3)*2
        xOr = xOr if obj.dome or obj.corn else xOr*2
        hfr_hpl = obj.copy(self.hfr.getRoot(__class__._hplb_))
        ins_hpl = obj.copy(self.ins.getRoot(__class__._hpl_))
        cvr_hpl = obj.copy(self.cvr.getRoot(__class__._hpl_)) if self.cvr else None
        objs = [ hfr_hpl, ins_hpl, cvr_hpl ]
        objs = [ obj.pToSliceZHB(o, cp=False) for o in objs if o is not None ]
        [ slc.extend(obj.move(o, xOr,0,0, 1, cp=False, fitV=True)) for o in objs ]
        return obj.slice(slc)

    def rotate(self, *args):
        objs = self.obj.get(__class__._abs_totl_)
        return super()._rotate(objs, *args)

    def move(self, vector, *args):
        objs = self.obj.get(__class__._abs_totl_)
        x,y,z = vector
        return super()._move(objs, x,y,z, *args)

# END: Basic flexible extend and compound of House

# BEGIN: Coding

###################################################################################
#
#                               [ coding ]:
#
###################################################################################

main = __name__ == '__main__'

t = time.time()

if main:

    from domeFCMacro import inform, assertionInform

    CONFIG = None

    try:
        import config
        importlib.reload(config)

        from config import DETAILS, OR, H1, LONG, THORUS, ROWS, COLS,   \
                HOUSE, EXTEND, COMPOUND, SLICE, ROTATE, MOVE, WIREFRAME, \
                ROOT, SOLID, PRINT3D, CLEANUP, GUI_CLEANUP, CONFIG
    except (AssertionError, SyntaxError):
        import sys
        assertionInform(sys.exc_info()[2])
    finally:
        if CONFIG is None: exit(0)                                       # To repair CONFIG before coding

if main and CONFIG:

    args   = (LONG, H1, OR, DETAILS)
    kwargs = dict(cleanup=CLEANUP, gui=GUI_CLEANUP)

    if       THORUS.get('CORNER') and not THORUS.get('DISC'):
        root = Root._corn_
        obj = House(*args, root=root, **kwargs, **HOUSE)

    elif not THORUS.get('CORNER') and     THORUS.get('DISC'):
        root = Root._disc_
        obj = House(*args, root=root, **kwargs, **HOUSE)

    elif     THORUS.get('CORNER') and     THORUS.get('DISC'):
        root = Root._thor_
        obj = House(*args, root=root, **kwargs, **HOUSE)

    else:
        root = Root._dome_
        obj = House(*args, root=root, **kwargs, **HOUSE)

    OBJ = HouseCompound

    obj.wireFrame(ROWS, COLS, vis=WIREFRAME)
    if not ROOT: exit(0)

    objs = obj.root(solid=SOLID)

    comp = compoundModel( objs, OBJ, EXTEND, COMPOUND, ROTATE, MOVE )

    if EXTEND and SLICE: comp.slicePolys()

elif main and not CONFIG:
    "Start coding here disabling CONFIG and TEST"
    inform()

try:
    t = time.time() - t
    m = int(t/60)
    s = t - m*60
    obj.cprint('Executed in: {0} minutes, {1:.1f} seconds'.format(m, s))
except: pass
