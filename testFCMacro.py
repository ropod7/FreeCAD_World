#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################################################
#
#        ______ _____  ____  ______
#       |__  __|  ___|/ ___\|random|
#         |  | |  __| \___ \  |  |         [ logic ]:
#         |__| |_____|\____/  |__|
#
#
###################################################################################

import time
import importlib

from random import randint

import domeFCMacro
importlib.reload(domeFCMacro)

from domeFCMacro import Root, FrameRoot, MonoRoot, compoundModel
from domeFCMacro import MacroRoot, ExtensionPoints

import houseFCMacro
importlib.reload(houseFCMacro)

from houseFCMacro import House, HouseCompound

# BEGIN: Randomized test of House

class TestHouse(House):

    def wireFrame(self, rows, cols, **kwargs):
        super().wireFrame(rows, cols, **kwargs)
        self.rows, self.cols = rows, cols
        obj = self.insulant
        if not obj.long and not obj.h1 and not cols and not rows:
            msg = 'EMPTY ASSET:{0}{0}ZEORES IN: H1, LONG, COLS, ROWS'
            obj.inform(msg.format(chr(10)))

class RandomHouseTest(TestHouse):
    _header_  = str('{0}RANDOM TEST:{0}').format(chr(10))
    _dts_min_ = int(4)      # min details
    _or_min_  = float(100)  # min radius
    _w_t_min_ = float(0.5)  # min frame width or mono thickness
    _frh_min_ = float(20)   # min frame height
    _roots_   = list([Root._dome_, Root._corn_, Root._disc_, Root._thor_])

    def __init__(self, root=None,
            dts_max=int(32), or_max=float(9000), cover_max=float(1000),
            **kwargs):

        assert isinstance(dts_max, int),        "TypeError:  max amount of details must be type of integer"
        assert dts_max >= 32 and dts_max <= 64, "ValueError: max amount of details not in range"
        assert isinstance(or_max, float),       "TypeError:  max OR of assets must be type of float"
        assert or_max >= 9000,                  "ValueError: max OR of assets not in range"
        assert isinstance(cover_max, float),    "TypeError:  max thickness of cover must be type of float"
        assert cover_max >= 1000,               "ValueError: max thickness of cover not in range"

        # BEGIN: Geometry

        dts = self.__int(__class__._dts_min_, dts_max)
        Or  = self.__float(__class__._or_min_, or_max)
        h1  = self.__zero_float_asset(or_max*2)
        lng = self.__zero_float_asset(or_max*2)
        tp  = __class__._roots_[self.__index(0,3)] if root is None else root
        self.__inform(DETAILS=dts, OR=Or, H1=h1, EXTENSION=lng, ROOT=tp)

        # END: Geometry

        # BEGIN: insertion units

        ext = ExtensionPoints(tp, lng, h1, Or, dts)
        inH = ext.insertionH1Units(h1, 0)[0]
        inL = ext.insertionLongUnits(lng, 0)[0]
        mxH = inH if inH != 0 and inH < inL else inL if inL < Or else Or-1
        if mxH < __class__._frh_min_ or mxH > Or:                        # reinit if max height < min hight of frame
            return self.__init__(
            dts_max=dts_max, or_max=or_max, cover_max=cover_max,
            **kwargs)

        # END: insertion units

        # BEGIN: Materials

        frH = self.__float(__class__._frh_min_, mxH)
        frW = self.__float(__class__._w_t_min_, int(frH/1.1))
        frW = (mxH - frH)/4 if frW/2+frH >= mxH else frW
        frm = tuple((frW, frH))

        ins = self.__float(__class__._w_t_min_, frH/1.5)
        cnt = self.__float(0, Or/3)
        if tp != __class__._roots_[3]:                                   # if not thor
            cvr = self.__float(__class__._w_t_min_, cover_max)
        else:
            cvr = self.__float(__class__._w_t_min_, Or-(cnt*1.5))

        # END: Materials

        super().__init__(lng, h1, Or, dts,
            root=tp, FRAME=frm, INSULANT=ins, CONTOUR=cnt, COVER=cvr,
            **kwargs)

        self.__inform(FRAME_W=frW, FRAME_H=frH,
            INSULANT=ins, CONTOUR=cnt, COVER=cvr,
            header=False)
        self.__inform(INS_H1=inH, INS_EXT=inL, header=False)

    def wireFrame(self,
            zero_rows_probability=False, zero_cols_probability=False,    # to produce 0 probability if True
            **kwargs):
        details = self.cover.DETAILS
        rows = self.__zero_probability(zero_rows_probability, int(details/4))
        cols = self.__zero_probability(zero_cols_probability, details)
        TestHouse.wireFrame(self, rows, cols, **kwargs)
        self.__inform(ROWS=rows, COLUMNS=cols, header=False)

    def root(self, **kwargs):
        objs = super().root(**kwargs)
        return objs

    def __inform(self, header=True, **kwargs):
        mr = MacroRoot()
        mr.cprint(__class__._header_) if header else mr.cprint(chr(10))
        msg = '{}: {}'
        [ mr.cprint(msg.format(k, str(v))) for k,v in kwargs.items() ]

    def __int(self, start, stop):
        return int(self.range(start, stop))

    def __float(self, start, stop):
        f = self.__int(0, 9)/10
        return float(self.__int(start, stop) + f)

    def __bool(self):
        return bool(self.__int(0, 1))

    def __index(self, i, j):
        return self.__int(i, j)

    def __zero_float_asset(self, *args):
        return float(self.__zero_asset(*args))

    def __zero_int_asset(self, *args):
        return int(self.__zero_asset(*args))

    def __zero_asset(self, obj_max):
        obj = self.__float(0, obj_max)
        return [0, obj][self.__index(0, 1)]

    def __zero_probability(self, probability, max_assets):
        if probability:
            return self.__zero_int_asset(max_assets)
        return self.__int(0, max_assets)

    def range(self, start, stop):
        return randint(int(start), int(stop))

class TestHouseCompound(HouseCompound):
    _hplb_ = FrameRoot._hplb_
    _hpl_  = MonoRoot._hpl_

    def slicePolys(self):
        if not self.obj.rows or not self.obj.cols: return
        obj, slc = self.obj, list()
        xOr = obj.X_OR*2 if obj.dome or obj.corn else obj.X_OR*4
        hfr_hpl = self.hfr.getRoot(__class__._hplb_)
        ins_hpl = self.ins.getRoot(__class__._hpl_)
        cvr_hpl = self.cvr.getRoot(__class__._hpl_)
        objs = [ hfr_hpl, ins_hpl, cvr_hpl ]
        objs = [ obj.pToSliceZHB(o, cp=True) for o in objs ]
        [ slc.extend(obj.xMirror(o, x=xOr, y=0, cp=False)) for o in objs ]
        sliced = obj.slice(slc)
        r = obj.OR+obj.X_ORreduced
        x = r*2 if not obj.thor else r*4
        obj.move(sliced, x,0,0, 1, cp=False)

# END: Randomized test of House

# BEGIN: Coding

###################################################################################
#
#                               [ coding ]:
#
###################################################################################

main = __name__ == '__main__'

t = time.time()

if main:
    obj = RandomHouseTest(root=None, cleanup=True)

    OBJ = TestHouseCompound

    obj.wireFrame(vis=False,
        zero_rows_probability=False, zero_cols_probability=False
        )

    objs = obj.root(solid=True)

    comp = compoundModel( objs, OBJ, True, True, dict(DO=False), dict(DO=False) )

    comp.slicePolys()

try:
    t = time.time() - t
    m = int(t/60)
    s = t - m*60
    obj.cprint('Executed in: {0} minutes, {1:.1f} seconds'.format(m, s))
except: pass
