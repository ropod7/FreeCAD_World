#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################################################
#
#        _   _    ____    ____  _____   _____
#       | \_/ |  |  _ \  /  __\|  _  \ /  _  \
#       |      \ | |_\ \|  |___| |_/ /|  |_|  |       [ logic ]:
#       |_|\/\__||_| |__|\____/|_| \__\\_____/
#
#
###################################################################################

import time
import math
from collections.abc import MutableMapping

# BEGIN: Trigonometrical Common Geometry

class Trigon(object):

    def __init__(self, oRadius, details):
        "Receives OR and DETAILS definitions"
        assert isinstance(oRadius, float), "TypeError: oRadius (OR) must be type of float"
        assert isinstance(details, int),   "TypeError: details (DETAILS) must be type of integer"
        assert details >= 4,               "ValueError: details (DETAILS) not in range"
        self.__OR_ = oRadius
        self.__DETAILS = details

    # Semantics of Trigonometry from: https://tinyurl.com/yyrxfd84

    """
        A    == angle A   (or self.DETAIL_A)
        B    == angle B   (or self.DETAIL_B)
        HB   == angle B/2 (or self.DETAIL_HB)
        a    == cathetus
        b    == side b of right triangle
        c    == hypothenuse of right triangle == math.sqrt(a**2 + b**2)
        base == side b*2
    """

    def rightSideB_ByA(self, c, A):
        return c * self.__cos(A)

    def rightSideB_ByAA(self, a, A):
        return a / self.__tan(A)

    def rightSideB_ByCA(self, c, a):
        return math.sqrt(c**2 - a**2)

    def rigthSideB_ByC(self, c):
        return self.isoscelesBase(c)/2

    def rightCathetusA_ByA(self, c, A):
        return c * self.__sin(A)

    def rightCathetusA_ByBA(self, b, A):
        return b * self.__tan(A)

    def rightCathetusA_ByB(self, c, B):
        return c * self.__cos(B)

    def rightCathetusA_ByCB(self, c, b):
        return math.sqrt(c**2 - b**2)

    def rightHypothenuseByB(self, a, B):
        "cathetus / cos(B/2)"
        return a / self.__cos(B/2)

    def rightHypothenuseByA(self, a, A):
        return a / self.__sin(A)

    def rightHypothenuse(self, a):
        return self.rightHypothenuseByB(a, self.DETAIL_B)

    def rightHypothenuse_ByAB(self, a, b):
        return math.sqrt(a**2 + b**2)

    def isoscelesBase(self, c):
        return c * 2 * self.__cos(self.DETAIL_A)

    def tanB_ByAB(self, a, b):
        try:
           return b/a
        except ZeroDivisionError:
            return self.__tan(90)                                      # tan(90 degrees)

    def angleB_ByAB(self, a, b, control=True):
        """
            Receives: a (as x) and b (as y, or z)
            Returns: angle B
        """
        tan_B = self.tanB_ByAB(a, b)
        B = math.degrees(math.atan(tan_B))
        return -B if B < 0 and control else B

    def __cos(self, x):
        return math.cos(math.radians(x))

    def __sin(self, x):
        return math.sin(math.radians(x))

    def __tan(self, x):
        return math.tan(math.radians(x))

    @property
    def CIRCLE(self):
        return 360

    @property
    def HALF_CIRCLE(self):
        return self.CIRCLE / 2

    @property
    def OR(self):
        return self.__OR_

    @OR.setter
    def OR(self, Or):
        assert isinstance(Or, float), "TypeError: Or must be type of float"
        self.__OR_ = Or
        return self.__OR_

    @property
    def DETAILS(self):
        return self.__DETAILS

    @property
    def DETAIL_B(self):
        return self.CIRCLE / self.DETAILS

    @property
    def DETAIL_HB(self):
        return self.DETAIL_B / 2

    @property
    def DETAIL_BO(self):
        "non quatro odd angle of quarter of polygon"
        try: return self.__BO
        except AttributeError:
            even = self.POLY_QUARTER * self.DETAIL_B
            self.__BO = self.HALF_CIRCLE / 2 - even
        return self.DETAIL_BO

    @property
    def POLY_QUARTER(self):
        return int(self.DETAILS / 4)

    @property
    def DETAIL_A(self):
        try: return self.__A
        except AttributeError:
            self.__A = (self.HALF_CIRCLE - self.DETAIL_B) / 2
        return self.DETAIL_A

    @property
    def base(self):
        try: return self.__base_
        except AttributeError:
            self.__base_ = self.isoscelesBase(self.OR)
        return self.base

class PairOfCompasses(Trigon):
    _deviation_ = float(0.01)

    def clockWiseArray(self, x, y):
        """
            Clockwise bottom view
        """
        A = self.DETAIL_A
        B = self.DETAIL_B
        """
            Extra solution for thorus to find proportions
            on y axis of higher 'horison poly wireframe'.
            System-wide single deviation is:
                x == 0.01 mm if 0 on x & y axis
                in case of self.DETAILS % 4 == 0
        """
        if x < self.DEVIATION: x = self.DEVIATION
        base = self.isoscelesBase(x)
        points = list( [[ x, y ]] )
        for i in range(self.POLY_QUARTER):
            x -= self.rightSideB_ByA(base, A)
            y += self.rightCathetusA_ByA(base, A)
            points.append([ x, y ])
            A -= B
        return points

    def clockWiseOnce(self, x, y):
        angle = self.DETAIL_A - self.DETAIL_B/2
        x = self.rightCathetusA_ByA(x, angle)
        y += self.rightSideB_ByAA(x, angle)
        return x, y

    def counterClockWiseOnce_ByB(self, x, y, B):
        c = self.rightHypothenuse_ByAB(x, y)
        x = self.rightCathetusA_ByA(c, 90-B)
        y = self.rightSideB_ByA(c, 90-B)
        return x, y

    def circumscribedClockWiseOnce(self, x, y):
        """
            Receives: x as a cathetus of an isosceless triangle lays on zero y;
            Returns: mid point x of isosceless base on own y position;

        """
        A = self.DETAIL_A
        x = self.rightCathetusA_ByA(x, A)
        y = self.rightSideB_ByAA(x, A)
        return x, y

    def circumscribedCounterClockWiseOnce(self, x, y):
        """
            Receives: x as a cathetus of an isosceless triangle and y;
            Returns: mid point x of isosceless base on zero y;

        """
        x, y = self.rightHypothenuse(x), 0
        return x, y

    def firstSectionToCircumscribed(self, x, y):
        A = self.DETAIL_A
        c = self.rigthSideB_ByC(x)
        x -= self.rightSideB_ByA(c, A)
        y += self.rightCathetusA_ByA(c, A)
        return x, y

    def firstSectionToInscribed(self, x, y):
        a = self.rightHypothenuseByA(x, self.DETAIL_A)
        x = self.rightHypothenuseByA(a, self.DETAIL_A)
        a = self.rigthSideB_ByC(x)
        y -= self.rightCathetusA_ByA(a, self.DETAIL_A)
        return x, y

    def toCircumscribedConverter(self, x, y):
        """
            Receives x, y of iscribed polygon
            and circularly converts them into circumscribed points;
        """
        x, y = self.firstSectionToCircumscribed(x, y)
        return self.clockWiseArray(x, y)

    def toInscribedConverter(self, x, y):
        """
            Receives x, y of circumscribed polygon
            and circularly converts them into inscribed points;
        """
        x, y = self.firstSectionToInscribed(x, y)
        return self.clockWiseArray(x, y)

    def first_3D_SectionToCircumscribed(self, x, y, z, z0=0, reductor=0):
        x, y = self.firstSectionToCircumscribed(x, y)
        if not reductor: return x, y, z
        x, y = self.circumscribedCounterClockWiseOnce(x, y)              # angles A and B away from a given polygon
        c = self.rightHypothenuse_ByAB(x, z-z0)                          # helps Pythagoras: math.sqrt(a**2 + b**2) (x as a cathetus a)
        sin_A = x/c                                                      # - sin(A)? - no problem!
        reduced_c = reductor                                             #------------------------------------------------------------#
        reduced_a = reductor * sin_A                                     # sides a,b,c of triangle of 3D reductor                     #
        reduced_b = self.rightSideB_ByCA(reduced_c, reduced_a)           #------------------------------------------------------------#
        x -= reduced_a
        z -= reduced_b
        x, y = self.circumscribedClockWiseOnce(x, y)
        return x, y, z

    def first_3D_SectionToInscribed(self, x, y, z):
        return *self.firstSectionToInscribed(x, y), z

    def _arrange3DPoints(self, x, y, z):
        """
            Receives: first section sequence of x,y and ZERO_Z;
            Returns: list of all polygonal points on z layer
        """
        points = self.clockWiseArray(x, y)
        return [ [ox, oy-y, z+y] for ox, oy in points ]

    @property
    def DEVIATION(self):
        return __class__._deviation_

class TwoPoints(PairOfCompasses):
    """

        The whole system revolves around these polygonal points.
        (the number of points to identify is: int( DETAILS/4 ))

    """
    _root_ = str('dome')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oPOINTS = list()                                            # outscribed circle points
        self.iPOINTS = list()                                            # circumscribed polygon ponts
        self.zPOINTS = list()                                            # zeroed on y axis circumscribed polygon ponts

    def oPolyPoints(self, Or):
        """
            Receives: OR of inscribed into circle polygon;
            Returns: sequence of x, y on z=0;
        """
        x, y = Or, 0
        return self.clockWiseArray(x, y)

    def iPolyPoints(self, Or, reductor=0):
        """
            Receives: OR of inscribed into circle polygon;
            and reductor (eg. as a material height);
            Returns: sequence of mid x, y points of base
            of isosceless triangle on z=0;
        """
        reductor = self.rightHypothenuse(reductor)
        x, y = Or-reductor, 0
        return self.toCircumscribedConverter(x, y)

    def zPolyPoints(self, Or):
        """
            Receives: OR of inscribed into circle polygon;
            Returns: sequence of mid x, z points of base
            of isosceless triangle on y=0 and ZERO_Z=0;
        """
        oPOINTS = self.oPolyPoints(Or)
        points  = list()
        for x, z in oPOINTS:
            x, y = self.firstSectionToCircumscribed(x, z)
            x, y = self.circumscribedCounterClockWiseOnce(x, y)
            points.append([ x, z ])
        return points

class GraduatedArc(TwoPoints):

    def sequenceByGraduatedArc(self, sequence):
        """
            To work with surface xPOINTS;
        """
        assert isinstance(sequence, list), "TypeError: sequence must be type of list"
        realB = 0
        points = list()
        for x, y in sequence[:-1]:                                       # returns for each:
            next_i = sequence.index([x, y])+1                            #                                  +
            next_x, next_y = sequence[next_i]                            #                                  |\
            next_c = self.rightHypothenuse_ByAB(next_x, next_y)          #                                 a| \
            B = (self.angleB_ByAB(next_x, next_y) - realB)               #                                  |  \
            a = self.rightSideB_ByA(next_c, 90-B)                        # .________________________________|_b_\
            x = self.rightHypothenuse_ByAB(x, y)                         # B                  x
            b = x - self.rightCathetusA_ByBA(a, 90-B)
            realB += B
            points.append([ B, x, a, b ])
        return points

class ThorusPoints(GraduatedArc):
    """
    Additional proportionaly elongated point system to extend poly points
      into their proper positions in case of toroidal building geometry.
    """
    _roots_ = [TwoPoints._root_, str('corner'), str('disc'), str('thorus')]

    def __init__(self, tp, oRadius, *args):
        "Receives root type, OR, DETAILS, definitions"
        super().__init__(oRadius, *args)
        self.pointSystem = tp
        self.ZERO_X = oRadius*2 if self.elongated else 0                 # To measure corners on X carriage

    def _x_ORRootXYPoints(self):
        try:
            x, y = self.X_OR + self.X_ORreduced, 0
            x, y = self.clockWiseOnce(x, y)
        except ZeroDivisionError:                                        # in case of DETAILS == 4
            x, y = 0, self.X_OR + self.X_ORreduced
        return x, y

    def __fixedXYRoots(self, x, y, MTL):
        """
        First couple of root X and Y points in case of Y > 0,
        to find complete proportions of toroidal trigonometry.
        """
        root_x, root_y = self._x_ORRootXYPoints()
        root_x = root_x if self.corn else root_x*2 - (root_x - x)
        root_y = root_y if self.corn else root_y*2 - (root_y - y)
        return root_x, root_y

    def __fixedZeroYXRoot(self, x):
        expr = self.pointSystem in __class__._roots_[-2:]
        return x*2 if expr else 0

    def _pntBtmMnr(self, x, y, MTL):
        if self.dome:
            return (x + self._addititionalMove(MTL), y, 0)
        x = self.__cornerXPoint(x, y, MTL)
        y = self.__cornerYPoint(x, y, 0, MTL)
        return (x, y, 0)

    def _h1Points(self, w, MTL):
        disc_r = self.OR*3 - self.X_ORreduced*2
        if self.dome: return self.OR if not w else self.OR-MTL.T
        elif self.disc: return disc_r if not w else disc_r-MTL.T
        return self.X_OR if not w else self.X_OR+MTL.T

    def _pntHPolyMnr(self, x, y, z, MTL):
        if self.dome: return (x, y, z)
        x = self.__cornerXPoint(x, y, MTL)
        y = self.__cornerYPoint(x, y, z, MTL)
        x += self.__cornerMonoXExtend(y, MTL)
        y += self.__cornerMonoYExtend(y, MTL)
        return (x, y, z)

    def _pntVPolyMnr(self, x, z):
        if self.dome: return (x, 0, z+self.ZERO_Z)
        r = self.X_OR + self.X_ORreduced
        if self.disc: x, y, z = (x+r*2, 0, z+self.ZERO_Z)
        else: x, y, z = (x+(r - x)*2, 0, z+self.ZERO_Z)
        return (x, y, z)

    def __cornerXPoint(self, x, y, MTL):
        r = self.X_OR + self.X_ORreduced
        if not round(y, 5):                                              # round till self.DEVIATION according y
            zero_y_x = self.__fixedZeroYXRoot(x)
            x += (r - x)*2 + zero_y_x
            return x
        root_x, _ = self.__fixedXYRoots(x, y, MTL)
        return x + (root_x - x)*2

    def __cornerYPoint(self, x, y, z, MTL):
        _, root_y = self.__fixedXYRoots(x, y, MTL)
        if not round(y, 5): return 0                                     # round till self.DEVIATION according y
        return y + (root_y - y)*2

    def _addititionalMove(self, MTL):
        if MTL.FRAME:
            cmove = MTL.W/(self.DETAILS/2)
            dmove = self.rightCathetusA_ByB(cmove, self.DETAIL_B)
            return cmove if self.corn else dmove
        return 0

    def __cornerMonoXExtend(self, y, MTL):
        if MTL.MONO and self.corn:
            x = self.rightSideB_ByAA(MTL.T, self.DETAIL_A)
            return x if not y else -x
        return 0

    def __cornerMonoYExtend(self, y, MTL):
        if MTL.MONO and self.corn:
            return MTL.T if y else -MTL.T
        return 0

    @property
    def pointSystem(self):
        return self.__type_

    @pointSystem.setter
    def pointSystem(self, tp):
        assert isinstance(tp, str), "TypeError: tp must be type of str"
        assert tp in __class__._roots_, "not in %s" % __class__._roots_
        self.__type_ = tp
        return self.__type_

    @property
    def dome(self):
        return self.pointSystem is __class__._roots_[0]

    @property
    def corn(self):
        return self.pointSystem is __class__._roots_[1]

    @property
    def disc(self):
        return self.pointSystem is __class__._roots_[2]

    @property
    def thor(self):
        return self.pointSystem is __class__._roots_[3]

    @property
    def elongated(self):
        return self.pointSystem in ThorusPoints._roots_[1:]

    @property
    def X_OR(self):
        try: return self.__X_OR_
        except AttributeError:
            self.__X_OR_ = self.OR
        return self.__X_OR_

    @X_OR.setter
    def X_OR(self, reduc):
        assert isinstance(reduc, float),        "TypeError: reductor must be type of float"
        try: assert self.__X_OR_ != self.OR,    "OR already produced"
        except AttributeError: pass
        self.__X_OR_ = reduc
        return self.__X_OR_

    @property
    def X_ORreduced(self):
        try: return self.__X_ORreduced_
        except AttributeError:
            self.__X_ORreduced_ = 0
        return self.__X_ORreduced_

    @X_ORreduced.setter
    def X_ORreduced(self, reduc):
        assert isinstance(reduc, float),      "TypeError: reductor must be type of float"
        try: assert self.__X_ORreduced_ == 0, "OR already produced"
        except AttributeError: pass
        self.__X_ORreduced_ = reduc
        self.__X_OR_ = self.OR - reduc
        self.OR      = self.OR + reduc
        return self.__X_ORreduced_

class ExtensionPoints(ThorusPoints):
    _root_ = str('long')

    def __init__(self, tp, extension, h1, *args):
        "Receives type, LONG and H1 definitions"
        assert isinstance(extension, float), "TypeError: extension (LONG) must be type of float"
        assert isinstance(h1, float),        "TypeError: h1 (H1) must be type of float"
        super().__init__(tp, *args)
        self.ZERO_Y = -extension   # To measure extensions on Y carriage
        self.ZERO_Z =  h1          # To lift all types of polygonal geometry
        self.__long_ = extension
        self.__h1_ = h1

    def extensionPoints(self, l, w, MTW):
        z = self.OR + self.ZERO_Z - w
        point1 = (self.ZERO_X,  -MTW/2, z)
        point2 = (self.ZERO_X, l+MTW/2, z)
        return point1, point2

    def insertionH1Units(self, h, MTT):
        l, n = self.__insertionUnits(h, MTT)
        self.__insH1L_, self.__insH1N_ = l, n
        return self.insH1L, self.insH1N

    def insertionLongUnits(self, l, MTT):
        l, n = self.__insertionUnits(l, MTT)
        self.__insLongL_, self.__insLongN_ = l, n
        return self.insLongL, self.insLongN

    def __insertionUnits(self, size, MTT):
        "Returns dimension and amount of internal orthogonal objects"
        if not size: return 0, 0
        r = self.OR + self.X_ORreduced
        reduc = r/self.DETAILS
        amount = int(size / self.isoscelesBase(r - reduc)) or 1
        return size / amount, amount

    @property
    def long(self):
        return self.__long_

    @property
    def h1(self):
        return self.__h1_

    @property
    def insLongL(self):
        return self.__insLongL_

    @property
    def insLongN(self):
        return self.__insLongN_

    @property
    def insH1L(self):
        return self.__insH1L_

    @property
    def insH1N(self):
        return self.__insH1N_

# END: Trigonometrical Common Geometry

# BEGIN: FreeCAD system covers

import FreeCAD, FreeCADGui
from FreeCAD import Base
import Draft, Part

from PySide import QtGui

class Qt(object):

    def inform(self, msg, info='Information'):
        assert isinstance(msg, str),  "TypeError: message must be type of str"
        assert isinstance(info, str), "TypeError: inforamtion must be type of str"
        return self.__QMessage.information(None, info, msg)

    @property
    def __QMessage(self):
        return QtGui.QMessageBox

class MacroRoot(Qt):
    _nwdoc_ = str('Std_New')
    _fitvw_ = str('ViewFit')
    _ortho_ = str('Std_OrthographicCamera')
    _persp_ = str('Std_PerspectiveCamera')

    def __init__(self):
        self.pl = FreeCAD.Placement()

    def newDoc(self, name):
        name = self.__convertDocName(name)
        name = FreeCAD.newDocument(name).Name
        self.setDoc(name, conv=False)
        return self.fcDoc

    def setDoc(self, name, conv=True):
        name = self.__convertDocName(name) if conv else name
        FreeCAD.setActiveDocument(name)
        self.fcDoc = self.getFCDoc(name)
        self.guiDoc = self.getGuiDoc(name)
        return self.fcDoc

    def getFCDoc(self, name):
        return FreeCAD.getDocument(name)

    def getGuiDoc(self, name):
        return FreeCADGui.getDocument(name)

    def closeDoc(self, name):
        FreeCAD.closeDocument(name)

    def clearDocument(self):
        try:
            name = self.fcDoc.Name
            self.fcDoc.clearDocument()
            self.closeDoc(name)
        except AttributeError: pass
        return self.newDoc(self.type)

    def vector(self, *v):
        return FreeCAD.Vector(*v)

    def recompute(self):
        try: self.fcDoc.recompute()
        except AttributeError: return

    def updateGui(self, sleep, fitV=False):
        if sleep: time.sleep(0.1)
        FreeCADGui.updateGui()
        if fitV: self.fitView()

    def setView(self, ortho=True):
        if ortho: self.setOrthographic()
        else: self.setPerspective()
        self.fitView()

    def guiCommand(self, *cmd):
        FreeCADGui.runCommand(*cmd)

    def guiViewMessage(self, msg):
        FreeCADGui.SendMsgToActiveView(msg)

    def setOrthographic(self):
        self.guiCommand(__class__._persp_, 0)
        self.guiCommand(__class__._ortho_, 1)

    def setPerspective(self):
        self.guiCommand(__class__._ortho_, 0)
        self.guiCommand(__class__._persp_, 1)

    def setIsometric(self):
        self.activeView.viewIsometric()

    def fitView(self):
        self.guiViewMessage(__class__._fitvw_)
        # self.activeView.fitAll()
        self.setIsometric()

    def autogroup(self, obj):
        return Draft.autogroup(obj)

    def cprint(self, *args):
        l = len([*args])
        prefix = self.__prefix(*args, len_args=l)
        s = tuple([ str(a) for a in [*args] ]) if l else tuple([chr(10)])
        FreeCAD.Console.PrintMessage(prefix % s)

    def __prefix(self, *args, len_args=None):
        assert isinstance(len_args, int), "TypeError: lenght must be type of integer"
        n, w, p, pc, s = chr(10), chr(32), chr(37), chr(59), chr(115)
        br = (chr(123) + chr(125))
        if len_args <= 1:
            return (br + s + br).format(p, n)
        return ((br*2) + pc + w).format(p, s) * len_args + br.format(n)

    def __convertDocName(self, name):
        assert isinstance(name, str), "TypeError: doc name must be type of str"
        ords = self.__ords()
        for o in ords: name = name.replace(chr(o), chr(95))
        return name

    def __ords(self):
        "Returns sequence of 'not letter' symbol indexes in ascii table"
        ords = list()
        seqs = [ (32,48), (58,65), (91,97), (123,127) ]
        [ ords.extend(list(range(*r))) for r in seqs ]
        return ords

    @property
    def fcDoc(self):
        return FreeCAD.ActiveDocument

    @fcDoc.setter
    def fcDoc(self, doc):
        FreeCAD.ActiveDocument = doc

    @property
    def guiDoc(self):
        return FreeCADGui.ActiveDocument

    @guiDoc.setter
    def guiDoc(self, doc):
        FreeCADGui.ActiveDocument = doc

    @property
    def activeView(self):
        return self.guiDoc.ActiveView

    @property
    def type(self):
        try: return self.__type
        except AttributeError:
            s = str(type(self))
            self.__type = s[s.rfind('.')+1:].replace('\'>', '_')
        finally: return self.__type

    @type.setter
    def type(self, tp):
        assert isinstance(tp, str), "TypeError: type must be type of string"
        self.__type = tp

    @property
    def roots(self):
        try: return self.fcDoc.RootObjects
        except AttributeError: return list()

class FreeCADObject(MacroRoot):

    def __init__(self, **kwargs):
        "Receives CLEANUP definition"
        super().__init__()
        self.cleanUp(**kwargs)

    def AddObject(self, feature, name):
        return self.fcDoc.addObject(feature, name)

    def Object(self, obj):
        return self.FCObject(obj)

    def remove(self, obj, gui=False):
        self.fcDoc.removeObject(obj)
        if gui: self.updateGui(False)

    def cleanUp(self, cleanup=False, gui=False):
        if not cleanup: return self.recompute()
        if self.fcDoc is None: return self.newDoc(self.type)
        ln = len(self.roots)
        if gui and ln:
            [ self.remove(obj.Name, gui=gui) for obj in self.roots ]
        elif gui and not ln: return
        else: return self.clearDocument()
        return self.cleanUp(cleanup=cleanup, gui=gui)

    def FCObject(self, obj):
        return self.fcDoc.getObject(obj.Name)

    def _setVisibility(self, obj, vis):
        self.FCObject(obj).Visibility = vis
        return obj

    def _setShapeColor(self, obj):
        self.Object(obj).ViewObject.ShapeColor = self.RGB

    def _setLabel(self):
        if self.label == self.name:
            self.label = self.label
        return self.label

    @property
    def name(self):
        return self.active.Name

    @property
    def label(self):
        return self.active.Label

    @label.setter
    def label(self, l):
        assert isinstance(l, str), "TypeError: label must be type of string"
        label = self.type
        label += self.pointSystem.upper() + '_{}'.format(l)
        self.active.Label = label

    @property
    def active(self):
        return self.fcDoc.ActiveObject

    @property
    def RGB(self):
        try: return self.__RGB
        except AttributeError: self.RGB = (0.9,0.9,0.9)
        finally: return self.__RGB

    @RGB.setter
    def RGB(self, color):
        self.__RGB = color

class BaseTools(FreeCADObject):

    def Wire(self, points, vis=False, gui=True, fitV=True, **kwargs):
        self.__typeLenCheck(points, list)
        p = [ self.vector(*ps) for ps in points ]
        w = Draft.makeWire(p,placement=self.pl,closed=False,face=False,**kwargs)
        self.autogroup(w)
        if vis: self.updateGui(vis, fitV=True)
        self._setVisibility(w, vis)
        return w

    def Polygon(self, n, p, f=True, s=None, i=True, vis=False, **kwargs):
        sides = n
        self.pl.Base = self.vector(*p)
        kw = dict(placement=self.pl, inscribed=i, face=f, support=s, **kwargs)
        polygon = Draft.makePolygon(sides, **kw)
        self.autogroup(polygon)
        return self._setVisibility(polygon, vis)

    def Surface(self, edges, vis=False, name='Surface'):
        assert len(edges) == 2, "LengthError: number of edges must be 2"
        edge1, edge2 = edges
        s = self.AddObject('Part::RuledSurface', name)
        s.Curve1 = ( edge1, ['Edge1'] )
        s.Curve2 = ( edge2, ['Edge1'] )
        self.label = name
        return self._setVisibility(s, vis)

    def Cut(self, base, tool, bvis=False, name='Cut'):
        c = self.AddObject('Part::Cut', name)
        self._setShapeColor(tool)
        c.Base = self.FCObject(base)
        c.Tool = self.FCObject(tool)
        self.label = name
        self._setShapeColor(c)
        self._setVisibility(base, bvis)
        self._setVisibility(tool, False)
        return c

    def Fusion(self, shapes, vis=True, name='Fusion'):
        f = self.AddObject('Part::MultiFuse', name)
        f.Shapes = [ self.FCObject(o)   for o in shapes ]
        [ self._setVisibility(o, False) for o in shapes ]
        self.label = name
        self._setShapeColor(f)
        return self._setVisibility(f, vis)

    def Extrude(self, surface, direction, height,
            rev=0, s=True, vis=True, d="Custom", taperA=0, taperARev=0,
            name='Extrude'):
        e = self.AddObject('Part::Extrusion', name)
        e.Base          = surface
        e.DirMode       = d
        e.Dir           = self.vector(direction)
        e.LengthFwd     = height
        e.LengthRev     = rev
        e.Solid         = self.solid
        e.Symmetric     = s
        e.TaperAngle    = taperA
        e.TaperAngleRev = taperARev
        self.label      = name
        self._setShapeColor(e)
        self._setVisibility(surface, False)
        return self._setVisibility(e, vis)

    def FCCompound(self, links, name='FCCompound'):
        c = self.AddObject('Part::Compound', name)
        self.autogroup(links)
        c.Links = links
        self.label = name
        self.recompute()
        return self._setVisibility(c, True)

    def Loft(self, faces, ruled=False, closed=False, name='Loft'):
        assert len(faces) == 2, "LengthError: number of faces must be 2"
        loft = self.AddObject('Part::Loft', name)
        loft.Sections = faces
        loft.Solid = self.solid
        loft.Ruled = ruled
        loft.Closed = closed
        self.label = name
        self._setShapeColor(loft)
        [ self._setVisibility(f, False) for f in faces ]
        return loft

    def Slice(self, obj, vector=(0,1,0), move=0, visobj=False, name='Slice'):
        shape = obj.Shape
        wires = list()
        bv = self.vector(*vector)
        [ wires.append(i) for i in shape.slice(bv, move) ]
        slicer = self.__Feature(name)
        slicer.Shape = self.__Compound(wires)
        slicer.purgeTouched()
        self.label = name
        self._setVisibility(obj, visobj)
        self.updateGui(visobj)
        return slicer

    def Rotate(self, objs, A, z, a, cp=True, vis=True, gui=False, fitV=False):
        Draft.rotate(objs,A,self.vector(*z),axis=self.vector(*a),copy=cp)
        objs = self.roots[-len(objs):] if cp else objs
        [ self._setVisibility(o, vis) for o in objs ]
        if gui: self.updateGui(gui, fitV=fitV)
        return objs

    def Move(self, objs, x, y, z, cp=True, vis=True, gui=False, fitV=False):
        Draft.move(objs, self.vector(x, y, z), copy=cp)
        objs = self.roots[-len(objs):] if cp else objs
        [ self._setVisibility(o, vis) for o in objs ]
        if gui: self.updateGui(gui)
        if fitV: self.fitView()
        return objs

    def __Feature(self, name):
        self.__typeLenCheck(name, str)
        return self.AddObject('Part::Feature', name)

    def __Compound(self, objs):
        self.__typeLenCheck(objs, list)
        return Part.Compound(objs)

    def __typeLenCheck(self, obj, tp):
        assert isinstance(obj, tp), "TypeError: given obj must be iterable"
        assert len(obj),            "LengthError: zero length of obj"

    @property
    def solid(self):
        try: return self.__solid
        except AttributeError: self.solid = False
        finally: return self.__solid

    @solid.setter
    def solid(self, solid):
        self.__solid = solid

class Model(BaseTools):

    def wire(self, points, **kwargs):
        self.recompute()
        return [ self.Wire(points,**kwargs) ]

    def polygon(self, sides, radius, placement, **kwargs):
        return [ self.Polygon(sides, placement, radius=radius, **kwargs) ]

    def cut(self, bases, tools, **kwargs):
        assert isinstance(bases, list) and len(bases), "bases must be not empty list"
        assert isinstance(tools, list),                "tools must be not empty list"
        r = list()
        [ r.extend(self.__cut(b, tools, **kwargs)) for b in bases ]
        self.recompute()
        return r

    def fusion(self, shapes, sort=True, **kwargs):
        assert isinstance(shapes, list) and len(shapes) > 1, "min list length of shapes is 2"
        shapes = self._sortByVolume(shapes, sort=sort)
        f = [ self.Fusion(shapes, **kwargs) ]
        self.recompute()
        return f

    def surface(self, e1, e2, **kwargs):
        assert len(e1) and len(e1) == len(e2), "empty edges list or lists not equal"
        r = list()
        [ r.extend(self.__surface([e1[i],e2[i]],**kwargs)) for i in range(len(e1)) ]
        self.recompute()
        return r

    def extrude(self, surfaces, *args, **kwargs):
        assert isinstance(surfaces, list) and len(surfaces), "bases must be not empty list"
        r = list()
        [ r.extend(self.__extrude(s, *args, **kwargs)) for s in surfaces ]
        self.recompute()
        return r

    def loft(self, f1, f2, **kwargs):
        assert len(f1) and len(f1) == len(f2), "empty faces list or lists not equal"
        l = list()
        [ l.extend(self.__loft([f1[i],f2[i]],**kwargs)) for i in range(len(f1)) ]
        self.recompute()
        return l

    def slice(self, objs, *args, **kwargs):
        assert isinstance(objs, list) and len(objs), "objs must be not empty list"
        r = list()
        [ r.extend([self.Slice(o, *args, **kwargs)]) for o in objs if o.Shape.Volume ]
        self.recompute()
        return r

    def wiresPoints(self, wires):
        "Returns FreeCAD vectorized list of wire points"
        points = list()
        obj = self.Object
        [ points.append([obj(w).Start, obj(w).End]) for w in wires ]
        return points

    def __cut(self, base, tools, **kwargs):
        return [ self.Cut(base, t, **kwargs) for t in tools ]

    def __surface(self, edges, **kwargs):
        return [ self.Surface(edges, **kwargs) ]

    def __loft(self, faces, **kwargs):
        assert isinstance(faces, list) and len(faces) == 2, \
            "TypeError: faces must be type of list with length 2"
        return [ self.Loft(faces, **kwargs) ]

    def __extrude(self, surface, direction, height, **kwargs):
        return [ self.Extrude(surface, direction, height, **kwargs) ]

    def _sortByVolume(self, objs, sort=False):                          # if zero shape after all procedures: remove from objects
        if sort:
            return [ obj for obj in objs if obj.Shape.Volume ]
        return objs

class DometicModel(Model):

    def defineRowsCols(self, ny, nz):
        assert ny <= self.DETAILS/4, "NumberError: ny (ROWS) not in range"
        assert nz <= self.DETAILS,   "NumberError: nz (COLS) not in range"
        self.__rows = ny   # number rows
        self.__cols = nz   # number cols

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    @property
    def quatro(self):
        return not self.DETAILS % 4

    @property
    def less_rows(self):
        return self.rows < self.POLY_QUARTER

    @property
    def equal_rows(self):
        return self.rows == self.POLY_QUARTER

    @property
    def dometic(self):
        expr = self.dome or self.thor or self.disc
        return True if expr else False

    @property
    def abs_quatro(self):                                                # absolute quatro
        return self.quatro and self.equal_rows


    @property
    def singleton(self):
        "If DETAILS / 4 == one row in COLS"
        return self.POLY_QUARTER == 1

    @property
    def coupler(self):
        "If DETAILS / 4 == couple of ROWS in COLS"
        return self.POLY_QUARTER > 1 and self.POLY_QUARTER < 3

    @property
    def fibo(self):
        f1, f2 = 0, 1
        n = self.DETAILS
        for i in range(n+1):
            f1, f2 = f2, f1+f2
            if f1 >= n: break
        return f1 == n

class Movement(DometicModel):

    def rotate(self, objs, angle, zero, axis, times, cp=True, sort=False, **kwargs):
        assert isinstance(objs, list), "TypeError: objs must be type of list"
        if not len(objs): return list()
        objs = self._sortByVolume(objs, sort=sort)
        if times < 0:   # rotate backward feature
            times *= -1
            angle = -angle
        if not cp:
            return self.Rotate(objs, angle*times, zero, axis, cp=cp, **kwargs)
        obj = list()
        for i in range(1, times+1):
            obj.extend(self.Rotate(objs, angle*i, zero, axis, cp=cp, **kwargs))
        self.recompute()
        return obj

    def move(self, objs, x, y, z, times, sort=False, **kwargs):
        assert isinstance(objs, list), "TypeError: objs must be type of list"
        if not len(objs): return list()
        objs = self._sortByVolume(objs, sort=sort)
        obj = list()
        for i in range(1, times+1):
            xi, yi, zi = x*i, y*i, z*i
            obj.extend(self.Move(objs, xi, yi, zi, **kwargs))
        self.recompute()
        return obj

# END: FreeCAD system covers

# BEGIN: Object creation system

class Blocks(MutableMapping, ExtensionPoints):
    """

    Contains grouped dict of object roots. Created to make parametric
      design of any object divided by segments, to insert into them
          standardized constructional parts of common building

    """
    _root_types_ = ThorusPoints._roots_
    _tps_ = str('types')
    _roo_ = str('root')
    _wfr_ = str('wireframe')
    _pts_ = str('points')
    _ext_ = str('extension')
    _plg_ = str('polygonal')

    def __init__(self, *args):
        ExtensionPoints.__init__(self, *args)
        self.types = { __class__._tps_: { } }

    def __getitem__(self, key):
        return self.types[__class__._tps_][self._keytransform(key)]

    def __setitem__(self, key, l):
        self.__valueExtensionChecker(l)
        self.types[__class__._tps_][self._keytransform(key)] = l

    def __delitem__(self, key):
        del self.types[__class__._tps_][self._keytransform(key)]

    def __iter__(self):
        return iter(self.types[__class__._tps_])

    def __len__(self):
        return len(self.types[__class__._tps_])

    def _keytransform(self, key):
        return key

    def _getRoot(self, tp, name):
        try: return self.types[__class__._tps_][tp][name]
        except KeyError: return self._extendRoot(tp, name, list())

    def __createType(self, tp):
        self.__keyExtensionChecker( tp )
        self.types[__class__._tps_][tp] = list()
        return self.types[__class__._tps_][tp]

    def append(self, tp, l):
        self.__keyExtensionChecker( tp )
        self.__valueExtensionChecker(l)
        try: self.types[__class__._tps_][tp].append(l)
        except KeyError: self.__createType(tp)
        finally: self.types[__class__._tps_][tp].append(l)

    def extend(self, name, l):
        self.__keyExtensionChecker( name )
        self.__valueExtensionChecker(l)
        try: self.types[__class__._tps_][name].extend(l)
        except KeyError: self.types[__class__._tps_].update({name:l})
        return self.types[__class__._tps_][name]

    def extendByFunc(self, name, func, *args):
        self.__keyExtensionChecker( name )
        return self.extend(name, func(*args))

    def extendDoubled(self, tp, name, i, l):
        try: isinstance(self[tp][name][i], list)
        except KeyError: self._appendRoot(tp, name, l)

        assert len(self[tp][name]) < 3, \
            "TypeError: max length of doubled is 2"
        self.__keyExtensionChecker( tp, name )
        self.__valueExtensionChecker(l)
        self.types[__class__._tps_][tp][name][i].extend(l)
        return self.types[__class__._tps_][tp][name]

    # BEGIN: Expand system operators

    def extendPlg(self, name, l):
        return self._extendRoot(__class__._plg_, name, l)

    def getPlg(self, name):
        return self._getRoot(__class__._plg_, name)

    def extendExt(self, name, l):
        return self._extendRoot(__class__._ext_, name, l)

    def getExt(self, name):
        return self._getRoot(__class__._ext_, name)

    # END: Expand system operators

    # BEGIN: Concrete operators

    def appendWfr(self, name, l):
        return self._appendRoot(__class__._wfr_, name, l)

    def extendWfr(self, name, l):
        return self._extendRoot(__class__._wfr_, name, l)

    def extendDoubledWfr(self, name, i, l):
        return self.extendDoubled(Blocks._wfr_, name, i, l)

    def getWfr(self, name):
        return self._getRoot(__class__._wfr_, name)

    def extendRoot(self, name, l):
        return self._extendRoot(__class__._roo_, name, l)

    def getRoot(self, name):
        return self._getRoot(__class__._roo_, name)

    # END: Concrete operators

    # BEGIN: Super root operators

    def _appendRoot(self, tp, name, l):
        self.__keyExtensionChecker( tp, name )
        self.__valueExtensionChecker(l)
        self.__rootCreator(tp, name)
        self.types[__class__._tps_][tp][name].append(l)
        return self.types[__class__._tps_][tp][name]

    def _extendRoot(self, tp, name, l):
        self.__keyExtensionChecker( tp, name )
        self.__valueExtensionChecker(l)
        self.__rootCreator(tp, name)
        self.types[__class__._tps_][tp][name].extend(l)
        return self.types[__class__._tps_][tp][name]

    def _extendRootByFunc(self, tp, name, func, *args):
        self.__keyExtensionChecker( tp, name )
        self.__rootCreator(tp, name)
        self.types[__class__._tps_][tp][name].extend(func(*args))
        return self.types[__class__._tps_][tp][name]

    # END: Super root operators

    def __createRootType(self, tp, name):
        assert isinstance(self.get(tp), type(None)), "Root type exists"
        self.types[__class__._tps_].update( { tp: { name: list() } } )
        return self.types[__class__._tps_][tp][name]

    def __extendRootType(self, tp, name):
        try:
            self.types[__class__._tps_][tp].update( { name: list() } )
            return self.types[__class__._tps_][tp][name]
        except KeyError: return False

    def __rootCreator(self, tp, name):
        try: self.types[__class__._tps_][tp][name]
        except KeyError: self.__extendRootType(tp, name)
        try: self.types[__class__._tps_][tp]
        except KeyError: return self.__createRootType(tp, name)

    def __keyExtensionChecker(self, *args):
        for arg in args:
            assert isinstance(arg, str), "TypeError: key must be type of string"

    def __valueExtensionChecker(self, l):
        assert isinstance(l, list), "TypeError: types contains lists"

class ProductionCalc(object): pass

class Materials(list, ProductionCalc):

    def __init__(self, obj, width=0, height=0, thickn=0, RGB=None, **kwargs):
        assert width and height or thickn, "Undefined material dimensions"
        assert isinstance(RGB, tuple),     "TypeError: color must be type of tuple"
        assert len(RGB) == 3,              "TypeError: wrong RGB format"
        self.__frame = (width, height or thickn)
        obj.RGB = RGB
        return super().__init__(self.__frame)

    @property
    def W(self):
        "Returns frame width"
        return self.__frame[0]

    @property
    def H(self):
        "Returns frame height"
        return self.__frame[1] if self.__frame[0] else 0

    @property
    def T(self):
        "Returns mono thickness"
        return self.__frame[1]

    @property
    def FRAME(self):
        return True if self.__frame[0] and self.__frame[1] else False

    @property
    def MONO(self):
        return False if self.__frame[0] and self.__frame[1] else True

class WireFrame(Movement, Blocks):
    _btm_ = str('bottom')
    _h1_  = str('h1_')
    _hpl_ = str('hPoly')
    _vpl_ = str('vPoly')
    _mp_  = str('marking')

    def _marking(self, MTL):
        if self.thor: return
        zl = [ 0, self.ZERO_Z or MTL.W or MTL.T ]
        points = [ (0, 0, z) for z in zl ]
        wire1 = self.wire(points, vis=True) if set(zl) != {0} else list()
        wire2 = self.wire([(0, 0, 0), (0, -MTL.H or -MTL.T, 0)], vis=True)
        wires = self._markingArray(wire1, wire2)
        return self.FCCompound(wires + wire1)

    def _bottom(self, w, MTL, mtl, **kwargs):
        if not self.h1 or not self.cols: return list()
        w = self.rightHypothenuse(MTL.W) if w and MTL.FRAME else w
        tp = __class__._btm_ + self.pointSystem + mtl
        p = self.oPolyPoints(self.OR - w)[:2]
        wire = self.appendWfr(tp, self.wire(
            [self._pntBtmMnr(x,y,MTL, **kwargs) for x,y in p],
            vis=self.wfVisibility ))
        return self.getWfr(tp)

    def _h1(self, w, height, MTL, mtl, horison=True):
        if self._checkInWfr(height): return list()
        tp = __class__._h1_ + self.pointSystem + mtl
        x = self._h1Points(w, MTL)
        operator = self.appendWfr if horison else self.extendWfr
        operator(tp, self.wire([
            (x, 0, 0), (x, 0, height)
            ], vis=self.wfVisibility))
        return self.getWfr(tp)

    def _horizonPoly(self, mtl, manipulator=0):
        tp = __class__._hpl_ + self.pointSystem + mtl
        Or = self.OR + manipulator                                       # as an additional move
        self.zPOINTS.append( self.zPolyPoints(Or) )
        return tp, self.wire, self._pntHPolyMnr, self.wfVisibility

    def _verticalPoly(self, ny, mtl, horison=True):
        tp = __class__._vpl_ + self.pointSystem + mtl
        if self._checkInWfr(ny): return list()
        points = self.oPOINTS[-1][:2]
        operator = self.appendWfr if horison else self.extendWfr
        operator(tp, self.wire([
            self._pntVPolyMnr(x, z) for x,z in points
            ], vis=self.wfVisibility))
        return [self.getWfr(tp)[-1]]

    def _checkInWfr(self, val):
        return not val or self.thor

    def _getWfType(self, wf, cls=False):
        tp = wf + self.pointSystem
        return tp + cls._mtrl_ if cls else tp

    @property
    def wfVisibility(self):
        try: return self.__vis
        except AttributeError: self.wfVisibility = False
        finally: return self.__vis

    @wfVisibility.setter
    def wfVisibility(self, vis):
        assert isinstance(vis, bool), "wfVisibility is boolean property"
        self.__vis = vis
        return vis

class ObjectMovement(WireFrame):

    """Base movement mechanism of machine tool"""
    def __init__(self, *args, cleanup=False, gui=False, **kwargs):
        Blocks.__init__(self, *args)
        FreeCADObject.__init__(self, cleanup=cleanup, gui=gui, **kwargs)

    def xMirror(self, objs, x=0, y=0, **kwargs):
        angle = 180
        zero = (x or self.ZERO_X, y, 0)
        axis = (0,0,1)
        return self.rotate(objs, angle, zero, axis, 1, sort=True, **kwargs)

    def pArrayYB(self, objs, n, **kwargs):
        angle = self.DETAIL_B
        return self.__pArrayY(objs, angle, n, **kwargs)

    def pArrayYBO(self, objs, n, **kwargs):
        if self.quatro: return objs
        angle = self.DETAIL_BO
        return self.__pArrayY(objs, angle, n, **kwargs)

    def pArrayZB(self, objs, n, **kwargs):
        angle = self.DETAIL_B
        return self.__pArrayZ(objs, angle, n, **kwargs)

    def pToSliceZHB(self, objs, **kwargs):
        angle = -self.DETAIL_B/2
        return self.__pArrayZ(objs, angle, 1, **kwargs)

    def h1DropArray(self, obj, **kwargs):
        dim, amount = self.insH1L, self.insH1N
        if amount > 1:
            return self.move(obj, 0,0,-dim, amount-1, **kwargs)
        return obj

    def h1Drop(self, obj, dim, cp=False, **kwargs):
        return self.move(obj, 0,0,-dim, 1, cp=cp, **kwargs)

    def h1LiftArray(self, obj, **kwargs):
        dim, amount = self.insH1L, self.insH1N
        if amount > 1:
            return self.move(obj, 0,0,dim, amount-1, **kwargs)
        return obj

    def h1Lift(self, obj, dim, cp=False, **kwargs):
        return self.move(obj, 0,0,dim, 1, cp=cp, **kwargs)

    def vLongArray(self, obj, **kwargs):
        dim = self.insLongL
        amount = self.insLongN
        return self.move(obj, 0,-dim,0, amount, **kwargs)

    def hLongArray(self, obj, **kwargs):
        dim = self.insLongL
        amount = self.insLongN - 1
        if not amount: return list()
        return self.move(obj, 0,-dim,0, amount, sort=True, **kwargs)

    def compArray(self, objs, angle, n, **kwargs):
        hypB = -90-angle/2
        x = self.rightCathetusA_ByBA(self.ZERO_Y/2, hypB)
        y = self.ZERO_Y/2
        return self.rotate(objs,angle,(x,y,0),(0,0,1),n, sort=True, fitV=True, **kwargs)

    def _markingArray(self, wire1, wire2, **kwargs):
        wire1.extend(wire2)
        wire1.extend(self.rotate(wire2, 90, (0,0,0),(0,0,1),3,**kwargs))
        return self.move(wire1, 0,self.ZERO_Y,0, 1) if self.long else wire1

    def __pArrayY(self, objs, angle, n, sort=True, **kwargs):
        zero = (self.ZERO_X, 0, self.ZERO_Z)
        axis = (0, self.dirY, 0)
        return self.rotate(objs, angle, zero, axis, n, sort=sort, **kwargs)

    def __pArrayZ(self, objs, angle, n, sort=True, **kwargs):
        zero = (0, 0, 0)
        axis = (0, 0, 1)
        return self.rotate(objs, angle, zero, axis, n, sort=sort, **kwargs)

    @property
    def dirY(self):
        return 1 if self.elongated else -1

class ModelMovement(ObjectMovement):

    # BEGIN: Horison poly torsion to extrude mechanism

    def turnToExtrude(self, objs, **kwargs):
        o, m = list(), self.__turn
        rng = range(len(objs))
        [ o.extend( m( [objs[i]], i, **kwargs ) ) for i in rng ]
        return o

    def turnAfterExtrude(self, objs, **kwargs):
        o = list()
        rng = range(len(objs))
        for i in rng:
            lo = objs[i]
            if not isinstance(lo, list): lo = [lo]
            o.extend( self.__turn( lo, i, backw=True, **kwargs ) )
        return o

    def __turn(self, *args, backw=False, **kw):
        """
        Torsion mechanism to give thickness of horison surfaces of Frame
        or Mono Root poly. Revolves around Z axis by angle B/2 and Y axis
                   by angle B in horisons sequence.
        """
        return self.__after(*args, **kw) if backw else self.__to(*args, **kw)

    def __to(self, obj, *args, gui=True, **kwargs):
        HB, newB, zero_y, a_y = self.__prms(*args, **kwargs)
        obj = self.__turnToFromZero(obj, -HB, gui=gui)
        return self.rotate(obj, newB, zero_y, a_y, 1, gui=gui, cp=False)

    def __after(self, obj, *args, gui=True, **kwargs):
        HB, newB, zero_y, a_y = self.__prms(*args, **kwargs)
        obj = self.rotate(obj, -newB, zero_y, a_y, 1, gui=gui, cp=False)
        return self.__turnToFromZero(obj, HB, gui=gui)

    def __prms(self, i, **kwargs):
        B = self.DETAIL_B
        zPOINTS = self.zPOINTS[0]
        a, b = zPOINTS[i]
        newB = self.angleB_ByAB(a, b)
        newB = self.__monoPrms(i, newB, **kwargs)
        zero_y, a_y = self.__zeroYAxisToTurn()
        return B/2, newB, zero_y, a_y

    def __monoPrms(self, i, newB, framed=True):
        if framed: return newB
        a, b = self.fPOINTS[0][i]
        B = self.angleB_ByAB(a, b)
        return newB + B

    def __turnToFromZero(self, obj, HB, **kwargs):
        zero_z, a_z = (0, 0, self.ZERO_Z), (0,0,1)
        return self.rotate(obj, HB, zero_z, a_z, 1, cp=False, **kwargs)

    def __zeroYAxisToTurn(self):
        x, z = self.ZERO_X, self.ZERO_Z
        if self.dome:   return (0,0,z), (0, 1,0)
        elif self.corn: return (x,0,z), (0,-1,0)
        return (x,0,z), (0,1,0)

    # END: Horison poly torsion to extrude mechanism

    def _rotatePolygonToCut(self, obj, placement):
        return self.rotate(obj, 90, placement, (1, 0, 0), 1, cp=False)

    def _moveBtmHorBarTool(self, tool, MTL, mono=False, cp=False):
        x = self.ZERO_X
        if self.dome:   x =   MTL.W   if not mono else 0
        elif self.corn: x =  -MTL.W   if not mono else 0
        elif self.disc: x =   MTL.W   if not mono else 0
        elif self.thor: x = x-MTL.H/2 if not mono else x-MTL.H
        return self.move(tool, x,0,0, 1, cp=cp)

class ModelLayer(ModelMovement):

    def copy(self, o):
        assert isinstance(o, list) and len(o), "TypeError: not a type of list or zero lenght"
        return self.rotate(o, 0, (0,0,0), (0,0,0), 1, cp=True) # just copy

    def _polygonCutTool(self, height, direction=(0,1,0), **kwargs):
        placement = (self.ZERO_X, 0, self.ZERO_Z)
        sides = 20 if self.DETAILS < 20 else self.DETAILS
        r = self.OR + self.X_ORreduced
        p = self.polygon(sides, r+height*4, placement)
        p = self._rotatePolygonToCut(p, placement)
        h = height if self.MTL.FRAME else height * 2
        return self.extrude(p, direction, h, vis=False, **kwargs)

    def _cutHPolysByTool(self, e, tool):
        s1 = self.cut(e, tool)
        s1 = self.pArrayZB(s1, -1, cp=False)
        s = self.cut(s1, tool)
        return self.pArrayZB(s, 1, cp=False)

class ModelRoot(ModelLayer):

    def _setMaterial(self, **kwargs):
        self.MTL = Materials(self, **kwargs)

    def wireFrame(self, ny, nz, vis=False):
        super().defineRowsCols(ny, nz)
        self.wfVisibility = vis

    def _build(self, solid=False):
        if self.get(Blocks._wfr_) is None:
            msg = 'EMPTY ASSET:{0}{0}ZEORES IN: H1, LONG, COLS, ROWS'
            self.inform(msg.format(chr(10)))
            return
        self.setView()
        wfr = self.get(Blocks._wfr_)
        self.solid = solid
        assert isinstance(wfr, dict) and len(wfr), "call wireFrame before build"
        return wfr

class Root(object):
    _dome_ = ThorusPoints._roots_[0]
    _corn_ = ThorusPoints._roots_[1]
    _disc_ = ThorusPoints._roots_[2]
    _thor_ = ThorusPoints._roots_[3]

    def __new__(cls, clss, *args, **kwargs):
        obj = clss.__new__(clss, *args, **kwargs)
        if isinstance(obj, clss):
            clss.__init__(obj, *args, **kwargs)
        return obj

# END: Object creation system

# BEGIN: Mono root creation system

class Mono3DPoints(ModelRoot):

    def mono3DPolyPoints(self, Or, z=0, manipulator=0):
        Or += manipulator
        OPOINTS = self.oPolyPoints(Or)
        points  = list([[ [x, y, z] for x, y in OPOINTS ]])
        for i in range(1, len(OPOINTS)):
            x, y, z = *OPOINTS[i], z
            outer = self._arrange3DPoints(x, y, z)
            points.append(outer)
        return points

class MonoGraduatedArc(Mono3DPoints):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fPOINTS = list()

    def monoSurfaceMidPoints(self, Or, manipulator=0):
        """
            Receives: Or and manipulator;
            Operates with: GraduatedArc.sequenceByGraduatedArc(list);
            Returns: surface mid points, where cathetus lies
            on face at an angle of 90 degrees;
            All _bottom wires_ of faces lies on z=y=0;
        """
        Or += manipulator
        zPOINTS = self.zPolyPoints(Or)
        arc = self.sequenceByGraduatedArc(zPOINTS)
        points  = list()                                                 # returns for each:                 +
        for B, x, a, b in arc:                                           #                                    \
            B = self.angleB_ByAB(a, b)                                   #                          mid point _\
            c = self.rightCathetusA_ByA(x, 90-B)                         #                                     |\
            a = self.rightCathetusA_ByA(c, 90-B)                         #                                    b| \
            b = self.rightSideB_ByCA(c, a)                               # .___________________________________|__\
            points.append([ a, b ])                                      #                     a
        return points

class MonoBlocks(MonoGraduatedArc):
    _face_ = str('faces')
    _tool_ = str('tools')

    def extendFcs(self, name, l):
        return self._extendRoot(__class__._face_, name, l)

    def appendFcs(self, name, l):
        return self._appendRoot(__class__._face_, name, l)

    def getFcs(self, name):
        return self._getRoot(__class__._face_, name)

    def appendTool(self, name, l):
        return self._appendRoot(__class__._tool_, name, l)

    def extendTool(self, name, l):
        return self._extendRoot(__class__._tool_, name, l)

    def getTool(self, name):
        return self._getRoot(__class__._tool_, name)

class MonoWireFrame(MonoBlocks):
    _mtl_ = str('mono')

    def _createMonoWireFrame(self, ny, MTL, mtl=None, marking=False, **kwargs):
        mtl = __class__._mtl_ if mtl is None else mtl
        self.insertionLongUnits(self.long, 0)
        c1, c2 = 0, self.rightHypothenuse(MTL.T)
        c3 = self.rightHypothenuse(c2)
        hd, _ = self.insertionH1Units(self.h1, 0)
        [ self._bottom(z, MTL, mtl) for z in [c1, c2] ]
        for c in [c1, c2]:
            if self.thor: break
            self.oPOINTS.append( self.oPolyPoints(self.OR-c) )
            self._h1(c, hd, MTL, mtl, horison=False)
            self._verticalPoly(ny, mtl)
        self.__horizonPoly(ny, mtl, MTL, **kwargs)
        self.__createToolWire()
        if marking: self._marking(MTL)
        return self.get(Blocks._wfr_)

    def __createToolWire(self):
        if not self.rows or self.thor: return
        r = self.X_OR + self.X_ORreduced
        r = r*2 if self.elongated else r
        base = self.isoscelesBase(r)
        c, A = base, self.DETAIL_A
        c = c if self.elongated else c/2
        x = self.rightSideB_ByA(c, A)
        y = self.rightCathetusA_ByA(c, A)
        x1, x2 = (-x, 0) if self.elongated else (-x,  x)
        y1, y2 = ( y, 0) if self.elongated else ( y, -y)
        self.toolWire = self.wire([
            (x1+self.ZERO_X, y1, self.ZERO_Z), (x2+self.ZERO_X, y2, self.ZERO_Z)
            ], vis=self.wfVisibility)
        return self.toolWire

    def __horizonPoly(self, ny, mtl, MTL, **kwargs):
        if not self.cols: return list()
        Or, z = self.OR, self.ZERO_Z
        self.fPOINTS.append(self.monoSurfaceMidPoints(Or, **kwargs))
        points3D = self.mono3DPolyPoints(Or, z=z, **kwargs)
        tp, wr, mngr, vis = super()._horizonPoly(mtl, **kwargs)
        for i in range(ny+1):
            points = points3D[i][:2]
            wire = wr([ mngr(x,y,z, MTL) for x,y,z in points ], vis=vis)
            self.extendWfr(tp, wire)
        return self.getWfr(tp)

class MonoModelLayer(MonoWireFrame):
    _tool_ = str('tools')

    def _createPolyH1Face(self, tp):
        w, f = self.getWfr(tp)
        f = self.surface(w, f)
        return self.extendFcs(tp, f)

    def _createH1Face(self, tp):
        wf = self.getWfr(tp)
        f  = self.surface([wf[0]], [wf[1]])
        return self.extendFcs(tp, f)

    def _createPolyPolyFaces(self, tp):
        wf   = self.getWfr(tp)
        ext  = self.extendFcs
        surf = self.surface
        rng  = range(len(wf)-1)
        [ ext(tp, surf( [wf[i]], [wf[i+1]] )) for i in rng ]
        return self.getFcs(tp)

    def _buildPolyPolyTools(self, tp, **kwargs):
        f, tp = self.__createPolyToolFaces(tp)
        self.__cuttingPolygons(**kwargs)
        tools = self.__prepareTools(f, **kwargs)
        self.appendTool(tp, tools)
        return self.getTool(tp)

    def _createExtPolyFaces(self, tp, cls=None):
        w, f = self.getWfr(tp)
        f = self.surface(w, f)
        return self.extendFcs(tp, f)

    def __createPolyToolFaces(self, tp):
        hpwf = self.getWfr(tp)
        tp   = __class__._tool_ + self.pointSystem
        ext  = self.extendFcs
        surf = self.surface
        rng  = range(len(hpwf))
        [ ext(tp, surf([self.toolWire[0]], [hpwf[i]])) for i in rng ]
        return self.getFcs(tp), tp

    def __cuttingPolygons(self, rev=0):
        if self.thor: return
        t = self.MTL.T * 4 if self.DETAILS > 8 else self.MTL.T * 8
        cut = self._polygonCutTool
        self.FrontPTool = cut(t, s=False, rev=rev)
        self.RearPTool  = cut(t, direction=(0,-1,0), rev=rev, s=False)

    def __prepareTools(self, faces, **kwargs):
        f = self.turnToExtrude(faces)
        first = self.__extrudeFirstBottomTool(f, **kwargs)
        mid   = self.__extrudeMedianTools(f, **kwargs)
        last  = self.__extrudeLastTopTool(f, **kwargs)
        tools = [first] + mid + [last]
        return self.turnAfterExtrude(tools)

    def __extrudeFirstBottomTool(self, f, rev=0):
        if not self.h1: rev *= 2
        return self.__toolsExtrude([f[0]], btm=True, rev=rev)

    def __extrudeMedianTools(self, faces, **kwargs):
        mid = list()
        for o in faces[1:-1]:
            btm = self.__toolsExtrude([ o ], btm=True, **kwargs)
            top = self.__toolsExtrude([ o ], **kwargs)
            mid.append([ *top, *btm ])
        return mid

    def __extrudeLastTopTool(self, f, **kwargs):
        return self.__toolsExtrude([f[-1]], **kwargs)

    def __toolsExtrude(self, f, btm=False, **kwargs):
        t = self.MTL.T
        dir_z = -1 if btm else 1
        direction = (0, 0, dir_z)
        return self.extrude(f, direction, t, s=False, vis=False, **kwargs)

    def _cutPolyPolys(self, e):
        tp = __class__._tool_ + self.pointSystem
        tools = self.getTool(tp)[0]
        e = self.__cutRotateByPolygon(e, self.RearPTool, z=-1)
        trimmed = self.__cutRotateByPolygon(e, self.FrontPTool)
        obj, blocks, k = list(), list(), 0
        for i in range(len(trimmed)):
            j = (i+1) * 2 - 1
            obj.append(   self.cut([trimmed[i]], [tools[j]]))
            blocks.extend(self.cut(obj[i],       [tools[k]]))
            k += 2
        return blocks

    def __cutRotateByPolygon(self, e, tool, z=1):
        e = self.cut(e, tool)
        b = self.DETAIL_B
        return self.rotate(e, b, (0,0,0), (0,0,z), 1, cp=False)

class MonoRoot(MonoModelLayer):
    _mtrl_ = MonoWireFrame._mtl_
    _tool_ = MonoModelLayer._tool_
    _btm_  = WireFrame._btm_
    _h1_   = WireFrame._h1_
    _vpl_  = WireFrame._vpl_
    _hpl_  = WireFrame._hpl_

    def __init__(self, tp, thickn, *args, RGB=(0.5,0.3,0.2), **kwargs):
        assert thickn, "No Mono thickness defined"
        self._setMaterial(thickn=thickn, RGB=RGB, **kwargs)
        super().__init__(tp, *args, **kwargs)

    def wireFrame(self, ny, nz, marking=False, manipulator=0, **kwargs):
        super().wireFrame(ny, nz, **kwargs)
        self._createMonoWireFrame(
            ny, self.MTL, manipulator=manipulator, marking=marking
        )

    def _build(self, **kwargs):
        if not self.rows and not self.h1: return
        super()._build(**kwargs)
        self._buildPolyH1()
        self._buildExtH1()
        self._buildPolyPoly()
        self._buildExtPoly()
        return self.get(Blocks._roo_)

    def _buildPolyH1(self, cls=None, w=0):
        if not self.h1 or not self.cols: return
        tp = WireFrame._btm_
        cls = __class__ if cls is None else cls
        tpf  = self._getWfType(tp, cls=cls) # thor
        ph1f = self._createPolyH1Face(tpf)
        f = self.getFcs(tpf)
        assert ph1f is f, "Lists of faces not equal"
        block = self.extrude(f, (0,0,1), w or self.insH1L, s=False)
        if cls == __class__:
            self.updateGui(True, fitV=True)
            return self.extendRoot(tp, block)
        return block, tp

    def _buildExtH1(self, cls=None, reduc=0):
        if not self.h1 or not self.long or self.thor: return
        tp = __class__._h1_
        cls = __class__ if cls is None else cls
        tpf  = self._getWfType(tp, cls=cls) # not thor
        h1f = self._createH1Face(tpf)
        f = self.getFcs(tpf)
        assert h1f is f, "Lists of faces not equal"
        block = self.extrude(f, (0,-1,0), self.insLongL-reduc, s=False)
        if cls == __class__:
            self.updateGui(True, fitV=True)
            return self.extendRoot(tp, block)
        return block, tp

    def _buildPolyPoly(self, cls=None, rev=0):
        if not self.rows or not self.cols: return
        tp = __class__._hpl_
        cls = __class__ if cls is None else cls
        tpf  = self._getWfType(tp, cls=cls) # thor
        hpf = self._createPolyPolyFaces(tpf)
        self._buildPolyPolyTools(tpf, rev=rev)
        f = self.getFcs(tpf)
        assert hpf is f, "Lists of faces not equal"
        f = self.turnToExtrude(f, framed=False)
        dir_x = 1 if self.corn else -1
        e = self.extrude(f, (dir_x,0,0), self.MTL.T, s=False)
        e = self.turnAfterExtrude(e, framed=False)
        blocks = self._cutPolyPolys(e)
        return self.extendRoot(tp, blocks)

    def _buildExtPoly(self, cls=None, reduc=0):
        if not self.long or self.thor or not self.rows: return
        tp = __class__._vpl_
        cls = __class__ if cls is None else cls
        tpf  = self._getWfType(tp, cls=cls) # not thor
        epf = self._createExtPolyFaces(tpf)
        f = self.getFcs(tpf)
        assert epf is f, "Lists of faces not equal"
        block = self.extrude(f, (0,-1,0), self.insLongL-reduc, s=False)
        if cls == __class__:
            self.updateGui(True, fitV=True)
            return self.extendRoot(tp, block)
        return block, tp

class MonoDome(MonoRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(Root._dome_, *args, **kwargs)

    def root(self, **kwargs):
        self._build(**kwargs)

class MonoCorner(MonoRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(Root._corn_, *args, **kwargs)

    def root(self, **kwargs):
        return self._build(**kwargs)

class MonoDisc(MonoRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(Root._disc_, *args, **kwargs)

    def root(self, **kwargs):
        return self._build(**kwargs)

class MonoThorus(MonoRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(Root._corn_, *args, **kwargs)

    def wireFrame(self, *args, **kwargs):
        self.__cornWireFrame(*args, **kwargs)
        self.__thorWireFrame(*args, **kwargs)
        return self.get(Blocks._wfr_)

    def root(self, **kwargs):
        self.__cornRoot(**kwargs)
        self.__thorRoot(**kwargs)
        return self.get(Blocks._roo_)

    def __cornWireFrame(self, *args, **kwargs):
        self.pointSystem = Root._corn_
        return self.__wireFrame(*args, **kwargs)

    def __thorWireFrame(self, *args, **kwargs):
        self.pointSystem = Root._thor_
        return self.__wireFrame(*args, **kwargs)

    def __wireFrame(self, *args, **kwargs):
        return MonoRoot.wireFrame(self, *args, **kwargs)

    def __cornRoot(self, **kwargs):
        self.pointSystem = Root._corn_
        return self._build(**kwargs)

    def __thorRoot(self, **kwargs):
        self.pointSystem = Root._thor_
        return self._build(**kwargs)

class Mono(Root):
    _roots_ = {
        Root._dome_ : MonoDome,
        Root._corn_ : MonoCorner,
        Root._disc_ : MonoDisc,
        Root._thor_ : MonoThorus
    }

    def __new__(cls, *args, root=None, **kwargs):
        assert root in __class__._roots_.keys(), "TypeError: unknown type of building"
        clss = __class__._roots_.get(root)
        return super().__new__(cls, clss, *args, **kwargs)

# END: Mono root creation system

# BEGIN: Frame root creation system

class Frame3DPoints(ModelRoot):

    def frame3DConverter(self, x, y, z, **kwargs):
        """
            To align well reduced root 3D points of dome on x,y,z axis
        """
        assert kwargs['reductor'] > 0, "ValueError: zero length of reductor"
        x, y, z = self.first_3D_SectionToCircumscribed(x,y,z, **kwargs)
        x, y, z = self.first_3D_SectionToInscribed(x, y, z)
        points = self.clockWiseArray(x, y)
        return [ [x, y, z] for x, y in points ]

    def frame3DPolyPoints(self, Or, z=0, manipulator=0, **kwargs):
        """
            Receives:
                Or of inscribed polygon;
                global z (or ZERO_Z) of construction;
                z_correct as an additional move in/out frame
                reductor as a material (frame) height;
            Returns:
                list of all 3D points of quarter of dome;
        """
        Or += manipulator
        OPOINTS = self.oPolyPoints(Or)
        IPOINTS = self.iPolyPoints(Or, **kwargs)
        outer   = [ [x, y, z] for x, y in OPOINTS ]
        REDUCED = self.toInscribedConverter(*IPOINTS[0])
        inner   = [ [x, y, z] for x, y in REDUCED ]
        points  = list([[ outer, inner ]])
        for i in range(1, len(OPOINTS)):
            x, y, z = *OPOINTS[i], z
            outer = self._arrange3DPoints(x, y, z)
            x, y, z3d = outer[0]
            inner = self.frame3DConverter(x, y, z3d, z0=z, **kwargs)
            points.append([ outer, inner ])
        return points

class FrameBlocks(Frame3DPoints):
    """Frame Root blocks management system"""
    _drf_ = str('roof')

    def extendDrf(self, name, l):
        return self._extendRoot(__class__._drf_, name, l)

    def getDrf(self, name):
        return self._getRoot(__class__._drf_, name)

class FrameWireFrame(FrameBlocks):
    _mtl_ = str('bar')
    _sht_ = str('short')
    _rof_ = str('long')

    def _createFrameWireFrame(self, ny, MTL, marking=True, **kwargs):
        self.insertionH1Units(self.h1, MTL.H)
        self.insertionLongUnits(self.long, MTL.H)
        ws = self.rightHypothenuse(MTL.H)
        mtl = __class__._mtl_
        for w in [0, ws]:
            self.oPOINTS.append( self.oPolyPoints(self.OR-w) )
            self._h1(w, self.h1, MTL, mtl)
            self.__horisonLong(w, ny, MTL)
            self.__horisonShort(w, self.rows, MTL)
            self._verticalPoly(ny, mtl)
            self._bottom(w, MTL, mtl)
        self.__horizonPoly(ny, mtl, MTL, **kwargs)
        if marking: self._marking(MTL)
        return self.get(Blocks._wfr_ + mtl)

    def __horizonPoly(self, ny, mtl, MTL, **kwargs):
        if not self.cols: return list()
        Or, z = self.OR, self.ZERO_Z
        points3D = self.frame3DPolyPoints(Or, z=z, reductor=MTL.H, **kwargs)
        tp, wire, mngr, vis = super()._horizonPoly(mtl, **kwargs)
        outer, inner = list(), list()
        for i in range(self.__hPolyNumber(ny)):
            OUTER = points3D[i][0][:2]
            INNER = points3D[i][1][:2]
            outer.extend(wire([ mngr(x,y,z, MTL) for x,y,z in OUTER ], vis=vis))
            inner.extend(wire([ mngr(x,y,z, MTL) for x,y,z in INNER ], vis=vis))
        [ self.appendWfr(tp, wires) for wires in [outer, inner] ]
        return self.getWfr(tp)

    def __horisonShort(self, w, rows, MTL):
        if not self.long or not rows and not self.h1: return list()
        tp = __class__._sht_ + self.pointSystem + __class__._mtl_
        dim, amount = self.insertionLongUnits(self.long, MTL.H)
        w1 = 0 if not w else MTL.H
        points = self.extensionPoints(-dim, w1, MTL.W)
        wire = self.wire( [ *points ], vis=self.wfVisibility )
        return self.appendWfr(tp, wire)

    def __horisonLong(self, w, rows, MTL):
        if self._checkInWfr(self.ZERO_Y): return list()
        tp = __class__._rof_ + self.pointSystem + __class__._mtl_
        w1 = 0 if not w else MTL.H
        points = self.extensionPoints(self.ZERO_Y, w1, MTL.W)
        self.appendWfr(tp, self.wire(
            [*points], vis=self.wfVisibility))
        return self.getWfr(tp)

    def __hPolyNumber(self, ny):
        expr  = self.abs_quatro
        expr0 = self.dome and expr
        expr1 = self.thor and expr
        return ny if expr0 or expr1 else ny+1

class FrameMovement(FrameWireFrame):

    def rotateAndDrop(self, obj, MTL, **kwargs):
        "Bottom extension bar creation in case of H1 > 0"
        if not len(obj): return list()
        r = self.OR
        r = r if not self.disc else r*3
        center = (r + MTL.W/2, 0, self.h1)
        dirr = (0,self.dirY,0)
        obj = self.rotate(obj,90,center,dirr,1,**kwargs)
        if self.dirY > 0:
            x = 0 if not self.disc else -MTL.W
            z = -self.ZERO_Z+MTL.H-MTL.W/2
            z = z if not self.disc else z-MTL.H
        else:
            x = -MTL.W
            z = -self.h1+MTL.H+MTL.W/2
        return self.move(obj, x,0,z, 1, cp=False)

    def _moveBottomToZero(self, b, MTW):
        if self.h1: return b
        z = MTW/2
        return self.move(b, 0,0,z, 1, cp=False)

    def _shortToZero(self, ext, MTW):
        if self.h1: return ext
        return self.move(ext, 0,0,-MTW/2, 1, cp=False)

    def _shortBack(self, ext, MTW):
        if self.h1: return ext
        return self._moveBottomToZero(ext, MTW)

    def _alignHorisonShortBar(self, bar, MTW):
        r = self.rows
        t = self.POLY_QUARTER if self.less_rows else r
        t = -t if self.pointSystem in ThorusPoints._roots_[-2:] else t
        bar = self.pArrayYB( bar, -t, cp=False)
        t = -1 if not self.disc else 1
        return self.pArrayYBO(bar, t, cp=False) # in case of not self.quatro

    def _alignHorisonLongBar(self, bar, MTW):
        if not self.less_rows and self.quatro: return bar
        odd = self.POLY_QUARTER - self.rows
        odd = odd if not self.disc else -odd
        lng = self.pArrayYB( bar, -odd, cp=False)
        t = -1 if not self.disc else 1
        return self.pArrayYBO(bar, t, cp=False)

class FrameModelLayer(FrameMovement):

    def _extrudeHPolys(self, n, MTW, hplwf):
        s = list()
        edges1, edges2 = self.getWfr(hplwf)
        edges1 = edges1[-n-1:]
        edges2 = edges2[-n-1:]
        tool = self._polygonCutTool(MTW)
        s = self.surface(edges1, edges2)
        s = self.turnToExtrude(s)
        e = self.extrude(s, (0,0,1), MTW)
        extruded = self.turnAfterExtrude(e)
        return self._cutHPolysByTool(extruded, tool)

    def _extrudeVertical(self, edges, MTW):
        assert isinstance(edges, list) and len(edges), "TypeError: empty or wrong type of edges"
        edges1, edges2 = edges
        s = self.surface(edges1, edges2)
        f = self.extrude(s, (0,1,0), MTW)
        return f

    def _cutBtmHorBar(self, base, h1bar):
        "In Thorus mode as tool works h1 bar of Corner"
        tool = self.copy(h1bar)
        if not self.thor:
            tools = tool
            tools.extend(self._moveBtmHorBarTool(tool, self.MTL, cp=True))
        else:
            tools = self._moveBtmHorBarTool(tool, self.MTL, cp=False)
            tools.extend(self.move(tools, -self.MTL.W/2,0,0, 1, cp=True))
        tool = self.fusion(tools)
        return self._cutHPolysByTool(base, tool)

class FrameRoot(FrameModelLayer):
    """Creator of bar root objects"""
    _mtrl_ = FrameWireFrame._mtl_
    _botm_ = WireFrame._btm_
    _h1ba_ = WireFrame._h1_
    _hdrp_ = str('h1drops')
    _vplb_ = WireFrame._vpl_ + _mtrl_
    _hplb_ = FrameWireFrame._hpl_
    _lnge_ = FrameWireFrame._rof_
    _shte_ = FrameWireFrame._sht_

    def __init__(self, tp, matW, matH, *args, **kwargs):
        self._setMaterial(width=matW, height=matH, RGB=(1.0,0.8,0.0), **kwargs)
        super().__init__(tp, *args, **kwargs)

    def wireFrame(self, ny, nz, marking=True, **kwargs):
        super().wireFrame(ny, nz, **kwargs)
        mnp = (self.MTL.W/2)/self.POLY_QUARTER
        mnp = mnp/self.DETAILS if self.dometic else -mnp
        return self._createFrameWireFrame(
            ny, self.MTL, manipulator=mnp, marking=marking
        )

    def _build(self, **kwargs):
        super()._build(**kwargs)
        h1bar = self.__h1WallBar()
        self.__bottomHorizonBar(h1bar)
        self.__verticalPolyBar()
        self.__horizonPolyBars(self.rows)
        self.__longHorisonBar()
        return self.get(Blocks._roo_)

    def __h1WallBar(self):
        tp = __class__._h1ba_
        if self.h1 and self.thor: return self.getRoot(tp)
        elif not self.h1: return
        h1wfr = self._getWfType(WireFrame._h1_, cls=__class__)
        h1wfr = self.getWfr(h1wfr)
        h1 = self._extrudeVertical( h1wfr, self.MTL.W )
        self.updateGui(True, fitV=True)
        return self.extendRoot(tp, h1)

    def __bottomHorizonBar(self, h1bar):
        if not self.h1 or not self.cols: return
        tp = __class__._botm_
        btmwf = self._getWfType(tp, cls=__class__)
        s = self.surface(*self.getWfr(btmwf))
        e = self.extrude(s, (0, 0, 1), self.MTL.H, s=False)
        bb = self._cutBtmHorBar(e, h1bar)
        self.updateGui(True, fitV=True)
        return self.extendRoot(tp, bb)

    def __horizonPolyBars(self, n):
        if not self.cols: return
        tp = __class__._hplb_
        hplwf = self._getWfType(tp, cls=__class__)
        bs = self._extrudeHPolys(n, self.MTL.W, hplwf)
        self._moveBottomToZero( [bs[0]], self.MTL.W )
        self.updateGui(True, fitV=True)
        return self.extendRoot(tp, bs)

    def __verticalPolyBar(self):
        tp = __class__._vplb_
        vplwf = self._getWfType(WireFrame._vpl_,  cls=__class__)
        if not len(self.getWfr(vplwf)): return self.extendRoot(tp, list())
        v = self._extrudeVertical( self.getWfr(vplwf), self.MTL.W )
        self.updateGui(True)
        return self.extendRoot(tp, v)

    def __longHorisonBar(self):
        if not self.ZERO_Y or self.thor: return list()
        tp = __class__._lnge_
        rofwf = self._getWfType(tp, cls=__class__)
        s = self.surface(*self.getWfr(rofwf))
        b = self.extrude(s, (1,0,0), self.MTL.W)
        b = self._alignHorisonLongBar(b, self.MTL.W)
        self.extendRoot(tp, b)
        self.__shortHorisonBar()
        self.updateGui(True, fitV=True)

    def __shortHorisonBar(self):
        tp = __class__._shte_
        shtwf = self._getWfType(tp, cls=__class__)
        if not self.rows and not self.h1: return list()
        elif not len(self.getWfr(shtwf)): return list()
        s = self.surface(*self.getWfr(shtwf))
        b = self.extrude(s, (1,0,0), self.MTL.W)
        b = self._alignHorisonShortBar(b, self.MTL.W)
        self.updateGui(True)
        return self.extendRoot(tp, b)

class FrameDome(FrameRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(Root._dome_, *args, **kwargs)

    def root(self, **kwargs):
        self._build(**kwargs)

class FrameCorner(FrameRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(Root._corn_, *args, **kwargs)

    def root(self, **kwargs):
        return self._build(**kwargs)

class FrameDisc(FrameRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(Root._disc_, *args, **kwargs)

    def root(self, **kwargs):
        return self._build(**kwargs)

class FrameThorus(FrameRoot):

    def __init__(self, *args, **kwargs):
        super().__init__(Root._corn_, *args, **kwargs)

    def wireFrame(self, *args, **kwargs):
        self.__cornWireFrame(*args, **kwargs)
        self.__thorWireFrame(*args, **kwargs)
        return self.get(Blocks._wfr_)

    def root(self, **kwargs):
        self.__cornRoot(**kwargs)
        self.__thorRoot(**kwargs)
        return self.get(Blocks._roo_)

    def __wireFrame(self, *args, **kwargs):
        return FrameRoot.wireFrame(self, *args, **kwargs)

    def __cornWireFrame(self, *args, **kwargs):
        self.pointSystem = Root._corn_
        return self.__wireFrame(*args, **kwargs)

    def __thorWireFrame(self, *args, **kwargs):
        self.pointSystem = Root._thor_
        return self.__wireFrame(*args, **kwargs)

    def __cornRoot(self, **kwargs):
        self.pointSystem = Root._corn_
        return self._build(**kwargs)

    def __thorRoot(self, **kwargs):
        self.pointSystem = Root._thor_
        return self._build(**kwargs)

class Frame(Root):
    _roots_ = {
        Root._dome_ : FrameDome,
        Root._corn_ : FrameCorner,
        Root._disc_ : FrameDisc,
        Root._thor_ : FrameThorus
    }

    def __new__(cls, *args, root=None, **kwargs):
        assert root in __class__._roots_.keys(), "TypeError: unknown type of building"
        clss = __class__._roots_.get(root)
        return super().__new__(cls, clss, *args, **kwargs)

# END: Frame root creation system

# BEGIN: Extend and compound super system

class Extend(object):
    """
    Creating Extend of any Root object, begin from
       most massive system using given sequence.
        System eg to start implementing Extend:
              Thorus + long + h1 - rows
    """
    _vert_ = str('vertical')
    _hori_ = str('horison')
    _allp_ = str('allpoly')
    _alle_ = str('allext')

    def __init__(self, cls, obj, cols):
        known = obj.pointSystem in ThorusPoints._roots_
        assert isinstance(obj, cls), "TypeError: obj must be one of Root objects"
        assert known,                "TypeError: Unknown compound type"
        self.__obj  = obj
        self.__cols = cols

    # BEGIN: Concrete Y revolving system

    def _revVertPolyY(self, obj, torev):
        tps = __class__._allp_, __class__._vert_
        extm = obj.extendPlg
        return self.__revPolyY(obj, torev, tps, extm)

    def _revVertExtY(self, obj, torev):
        tps = __class__._alle_, __class__._vert_
        extm = obj.extendExt
        return self.__revPolyY(obj, torev, tps, extm)

    def _revHoriExtY(self, obj, torev):
        tps = __class__._alle_, __class__._hori_
        extm = obj.extendExt
        return self.__revPolyY(obj, torev, tps, extm)

    # END: Concrete Y revolving system

    # BEGIN: Concrete horisons drop system

    def _dropPolyH1s(self, obj, todrp):
        "todrp contains all horison poly [bars]"
        if not self.cols: return
        tps = __class__._allp_, __class__._hori_
        extm = obj.extendPlg
        to = [todrp[0]]
        if obj.thor:
            last = [ todrp[self.rows] ]
            to = to + last
        [ extm(t, todrp) for t in tps ]
        return self.__dropH1s(obj, to, tps, extm)

    def _dropExtH1s(self, obj, todrp):
        "todrp contains one horison poly obj"
        if not obj.h1: return obj._moveBottomToZero(todrp, obj.MTL.W)
        tps = __class__._alle_, __class__._hori_
        extm = obj.extendExt
        return self.__dropH1s(obj, todrp, tps, extm)

    # END: Concrete horisons drop system

    # BEGIN: Concrete horisons lift system

    def _liftPolyH1s(self, obj, tolft):
        tps = Extend._allp_, Extend._vert_
        extm = obj.extendPlg
        return self.__liftH1s(obj, tolft, tps, extm)

    def _liftExtH1s(self, obj, tolft):
        tps = Extend._alle_, Extend._vert_
        extm = obj.extendExt
        return self.__liftH1s(obj, tolft, tps, extm)

    # END: Concrete horisons lift system

    # BEGIN: Concrete thor mirroring system

    def _movePolyVToThor(self, obj, tomove, **kwargs):
        tps = __class__._allp_, __class__._vert_
        extm = obj.extendPlg
        return self.__moveToThor(obj, tomove, tps, extm, **kwargs)

    def _moveExtVToThor(self, obj, tomove, **kwargs):
        tps = __class__._alle_, __class__._vert_
        extm = obj.extendExt
        return self.__moveToThor(obj, tomove, tps, extm, **kwargs)

    def _moveExtHToThor(self, obj, tomove, y=0, **kwargs):
        tps = __class__._alle_, __class__._hori_
        extm = obj.extendExt
        y = -(obj.insLongL/2) if not y else y
        return self.__moveToThor(obj, tomove, tps, extm, y=y, **kwargs)

    # END: Concrete thor mirroring system

    def _revPolyZ(self, obj, n):
        "revolving mechanism of all polys around Z axis"
        if not self.cols: return
        objs = list()
        allp, nms = __class__._allp_, [__class__._vert_,__class__._hori_]
        [ objs.extend(obj.getPlg(n).copy()) for n in nms ]
        obj.extendPlg(allp, obj.pArrayZB(objs, n, gui=True).copy())

    # BEGIN: Concrete horison long array system

    def _vertLngPArray(self, obj):
        tps = __class__._alle_, __class__._vert_
        meths = obj.getPlg, obj.extendExt
        return self.__vertYArray(obj, tps, meths)

    def _vertExtArray(self, obj):
        tps = __class__._alle_, __class__._vert_
        meths = obj.getExt, obj.extendExt
        return self.__horiYArray(obj, tps, meths)

    def _horiLongArray(self, obj):
        tps = __class__._alle_, __class__._hori_
        meths = obj.getExt, obj.extendExt
        return self.__horiYArray(obj, tps, meths)

    # END: Concrete horison long array system

    def _collectPartial(self, obj, parts):
        if not self.cols: return
        tps = Extend._allp_, Extend._hori_
        extm = obj.extendPlg
        [ extm(t, parts.copy()) for t in tps ]

    def _rotate(self, objs, angle, center, axis, n, copy):
        return self.obj.rotate(objs, angle, center, axis, n, cp=copy, gui=True)

    def _move(self, objs, x,y,z, n, copy):
        return self.obj.move(objs, x,y,z, n, cp=copy, gui=True)

    def __dropH1s(self, obj, todrp, tps, extm, **kwargs):
        "array mechanism to fill up h1 by horisons"
        if not self.h1 or obj.insH1N == 1: return
        drop = obj.h1DropArray(todrp, gui=True, **kwargs).copy()
        [ extm(t, drop) for t in tps ]
        return drop

    def __liftH1s(self, obj, tolft, tps, extm, **kwargs):
        "array mechanism to fill up h1 by horisons"
        if not self.h1: return #[ extm(t, []) for t in tps ]
        if obj.insH1N > 1:
            lift = obj.h1LiftArray(tolft, gui=True, **kwargs).copy()
            lift = tolft + lift
        else:
            lift = tolft
        [ extm(t, lift) for t in tps ]
        return lift

    def __revPolyY(self, obj, torev, tps, extm):
        "revolving mechanism of all polys around Y axis"
        assert len(torev), "Empty items list"
        assert len(torev) == 1, "Too many items to revolve"
        if not self.rows: return list()
        elif self.rows == 1:
            [ extm(t, torev) for t in tps ]
            return torev
        n = (self.rows-1)*-1 if obj.disc else self.rows-1
        vpl = obj.pArrayYB(torev, n, gui=True)
        toall = torev + vpl.copy()
        [ extm(t, toall.copy()) for t in tps ]
        return toall.copy()

    def __moveToThor(self, obj, tomove, tps, extm, **kwargs):
        "thorus mirroring mechanism"
        if not obj.thor or not len(tomove): return
        r = 2 if self.rows < obj.DETAILS/4 else 1
        moved = obj.xMirror(tomove, gui=True, **kwargs).copy()
        [ extm(t, moved) for t in tps ]
        return moved

    def __vertYArray(self, obj, tps, meths):
        arr = obj.vLongArray
        return self.__yArray(obj, tps, arr, meths)

    def __horiYArray(self, obj, tps, meths):
        arr = obj.hLongArray
        return self.__yArray(obj, tps, arr, meths)

    def __yArray(self, obj, tps, arr, meths):
        allt, tp = tps
        geto, exto = meths
        toarr = geto(tp).copy()
        made = arr(toarr, gui=True, fitV=True)
        [ exto(t, made.copy()) for t in tps ]
        return made

    @property
    def obj(self):
        return self.__obj

    @property
    def rows(self):
        return self.__obj.rows

    @property
    def cols(self):
        return self.__cols

    @property
    def long(self):
        return self.__obj.long

    @property
    def h1(self):
        return self.__obj.h1

class Compound(Extend):
    """Extended array system"""
    _totl_ = str('total')

    def __init__(self, cls, obj, *args, **kwargs):
        hd = int(obj.DETAILS/2)
        cols = hd if obj.cols > hd and obj.long else obj.cols
        super().__init__(cls, obj, cols, *args, **kwargs)

    def compound(self, obj=None):
        """
        Trigonometry based compound extended object:
            moved by: -X carriage on Y: LONG/2
        """
        assert isinstance(obj, ModelRoot), "TypeError: unknown type of building"
        expr = not obj.long and obj.cols<obj.DETAILS-1
        if expr and obj.cols: return
        totl  = __class__._totl_
        total = obj.get(totl)
        cols  = self.cols
        circ  = obj.CIRCLE
        B     = obj.DETAIL_B
        times = circ / (cols*B) if cols else 2
        angle = circ / times
        times = int(times-1)
        comp = obj.compArray(total, angle, times, gui=True)
        return obj.extend(totl, comp)

    def _collectTotal(self, obj):
        total = __class__._totl_
        allp = obj.getPlg(Extend._allp_)
        obj.extend(total, allp.copy())
        alle = obj.getExt(Extend._alle_)
        obj.extend(total, alle.copy())
        return obj.get(total)

    def rotate(self, *args):
        objs = self.obj.get(__class__._totl_)
        return super()._rotate(objs, *args)

    def move(self, vector, *args):
        objs = self.obj.get(__class__._totl_)
        return super()._move(objs, *vector, *args)

# END: Extend and compound super system

# BEGIN: Basic flexible Mono Root extends and compound

class MonoExtend(Compound):

    def __init__(self, obj, **kwargs):
        super().__init__(MonoRoot, obj, **kwargs)
        if not self.h1 and not self.rows: return
        self.__completePartialPoly(obj)
        self._revPolyZ(obj, self.cols-1)
        self.__completeMonoExtension(obj)

    def __completePartialPoly(self, obj):
        self._liftPolyH1s(obj)
        lofts = obj.getRoot(MonoRoot._hpl_)
        self._collectPartial(obj, lofts)

    def __completeMonoExtension(self, obj):
        if not self.long: return
        self._liftExtH1s(obj)
        revs = self._revHoriExtY(obj)
        self._moveExtVToThor(obj)
        self._moveExtHToThor(obj, revs)
        self._horiLongArray(obj)
        self._vertExtArray(obj)

    def _liftPolyH1s(self, obj):
        tolft = obj.getRoot(MonoRoot._btm_)
        return super()._liftPolyH1s(obj, tolft.copy())

    def _liftExtH1s(self, obj):
        tolft = obj.getRoot(MonoRoot._h1_)
        return super()._liftExtH1s(obj, tolft.copy())

    def _revHoriExtY(self, obj):
        expr = obj.rows and obj.long
        pl = obj.getRoot(MonoRoot._vpl_).copy()
        return super()._revHoriExtY(obj, pl) if len(pl) else list()

    def _moveExtHToThor(self, obj, tomove):
        if not len(tomove): return
        return super()._moveExtHToThor(obj, tomove)

    def _moveExtVToThor(self, obj):
        tomove = obj.getExt(Extend._vert_)
        y = -(obj.insLongL/2)
        return super()._moveExtVToThor(obj, tomove, y=y)

class MonoCompound(MonoExtend):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._collectTotal(self.obj)

# END: Basic flexible Mono Root extends and compound

# BEGIN: Basic flexible Frame Root extends and compound

class FrameExtend(Compound):
    """
    Frame Root objects extend tool and over layer of movement
           system, which works just with given objects
    """
    _roof_ = str('roof')

    def __init__(self, obj, **kwargs):
        super().__init__(FrameRoot, obj, **kwargs)
        self.__completePartialPoly(obj)
        self._revPolyZ(obj, self.cols-1)
        self.__completeFrameExtension(obj)

    def __completePartialPoly(self, obj):
        "vPoly array, horison drops"
        verts = self.__revolvePoly(obj) or list()
        self.__moveVertsToThor(obj, verts)
        self.__dropHoriPolys(obj)
        self._collectPartial(obj)

    def __completeFrameExtension(self, obj):
        "shorts array, horisons drop, bottoms, long array"
        if not self.long: return obj.extendExt(Extend._alle_, list())
        extm = obj.extendExt
        short, lng, revs = self._revHoriExtY(obj)
        drops = self._dropExtH1s(obj, short) or []
        puts = self.__dropAndPutBottomExt(obj, short)
        self.__moveExtH1ToThor(obj, puts, drops, extm)
        self._moveExtHToThor(obj, revs)
        self.__moveRoofToThor(obj, lng, extm)
        self.__collectRoof(obj, lng, extm)
        self._vertLngPArray(obj)
        self._horiLongArray(obj)

    # BEGIN: Polygonal expand system

    def __revolvePoly(self, obj):
        torev = obj.getRoot(FrameRoot._vplb_).copy() if obj.rows else []
        return self._revVertPolyY(obj, torev) if len(torev) else None

    def __moveVertsToThor(self, obj, verts):
        tos = obj.getRoot(FrameRoot._h1ba_).copy() if obj.h1 else list()
        tps = Extend._allp_, Extend._vert_
        [ obj.extendPlg(t, tos.copy()) for t in tps ]
        tos.extend(verts.copy())
        if not len(tos): return
        return self._movePolyVToThor(obj, tos)

    def __dropHoriPolys(self, obj):
        hplb = obj.getRoot(FrameRoot._hplb_) or list()
        return self._dropPolyH1s(obj, hplb.copy())

    def _collectPartial(self, obj):
        if not self.h1: return
        btm = obj.getRoot(FrameRoot._botm_)
        return super()._collectPartial(obj, btm)

    # END: Polygonal expand system

    # BEGIN: Extension expand system

    def _revHoriExtY(self, obj):
        lng = obj.getRoot(FrameRoot._lnge_).copy()
        to = obj.getRoot(FrameRoot._shte_).copy()
        to = lng if not len(to) else to
        return to, lng, super()._revHoriExtY(obj, to)

    def __dropAndPutBottomExt(self, obj, short):
        if not self.long or not self.h1: return
        cp = True if self.rows else False
        return obj.rotateAndDrop(short, obj.MTL, cp=cp)

    def __moveExtH1ToThor(self, obj, puts, drops, extm):
        if not self.h1: return
        tps = Extend._alle_, Extend._hori_
        [ extm(t, puts) for t in tps ]
        if not obj.thor: return
        self._moveExtHToThor(obj, puts + drops)

    def __moveRoofToThor(self, obj, lng, extm):
        if not obj.thor: return
        ok = obj.equal_rows and obj.quatro
        tp = Extend._alle_
        if ok: return extm(tp, lng)
        moved = obj.xMirror(lng, y=obj.ZERO_Y/2)
        tocol = moved
        extm(tp, tocol.copy())

    def __collectRoof(self, obj, lng, extm):
        ok = obj.equal_rows and obj.quatro
        tp = Extend._alle_
        if   obj.thor and ok: return
        elif obj.dome and ok: return
        return extm(tp, lng)

    # END: Extension expand system

class FrameCompound(FrameExtend):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._collectTotal(self.obj)

    def compound(self, obj=None, **kwargs):
        total = super().compound(obj=obj, **kwargs)
        expr = obj.dome and obj.equal_rows and obj.quatro
        if not expr: return total
        lng = obj.getRoot(FrameRoot._lnge_)
        return obj.extend(Compound._totl_, lng)

# END: Basic flexible Frame Root extends and compound

# BEGIN: Coding

###################################################################################
#
#                               [ coding ]:
#
###################################################################################

def inform(msg=None):
    if msg is None:
        q = 'config'
        msg =  '{0} is OFF{2}Set in {1}.py: {2}{2}'
        msg += '# Extra options:{2}{0} = bool(True)'
        return Qt().inform(msg.format(q.upper(), q, chr(10)))
    return Qt().inform(msg)

def assertionInform(tb):
    conf = 'config'
    syntax_msg = 'Syntax error in {0}.py{1}{1}'.format(conf, chr(10))
    syntax_msg += 'Check all brackets and comma separators'
    import traceback
    tb_info = traceback.extract_tb(tb)
    fn, line, func, text = tb_info[-1]
    if conf in fn:
        msg = 'Check {0}.py:{3}{3}Line: {1}{3}{2}'
        return Qt().inform(msg.format(conf, line, text, chr(10)))
    return Qt().inform(syntax_msg)

def convert(MTL, lng, h1, Or, dets, thor, comp, p3d):
    """3D printer scale converter"""
    def s(val, scale): return val*scale
    prnt = p3d[0] > 0 and p3d[1] > 0
    if not comp or not prnt:
        bm = MTL if isinstance(MTL, tuple) else tuple([MTL])
        args = (lng, h1, Or, dets)
        return (*bm, *args)
    prntdim = p3d[0] if p3d[1] > p3d[0] else p3d[1]
    if thor.get('DISC'):
        scale = prntdim / (lng + Or*3*2)
    elif not thor.get('DISC') and thor.get('CORNER'):
        scale = prntdim / (lng + Or*2*2)
    else:
        scale = prntdim / (lng + Or*2)
    converted = (s(lng, scale), s(h1, scale), s(Or, scale), dets)
    if isinstance(MTL, tuple):
        mtl = s(MTL[0], scale), s(MTL[1], scale)
    else:
        mtl = [s(MTL, scale)]
    return (*mtl, *converted)

def compoundModel(obj, OBJ, EXTEND, COMPOUND, ROTATE, MOVE):
    o = None
    if EXTEND:
        o = OBJ(obj)
    if EXTEND and COMPOUND:
        o.compound(obj=obj)
    if EXTEND and COMPOUND and ROTATE.get('DO'):                         # at first rotate
        angle  = ROTATE.get('ANGLE')
        center = ROTATE.get('CENTER')
        axis   = ROTATE.get('AXIS')
        copy   = ROTATE.get('COPY')
        times  = ROTATE.get('TIMES') if copy else 1
        o.rotate(angle, center, axis, times, copy)
    if EXTEND and COMPOUND and MOVE.get('DO'):                           # next move
        vector = MOVE.get('VECTOR')
        copy   = MOVE.get('COPY')
        times  = MOVE.get('TIMES') if copy else 1
        o.move(vector, times, copy)
    return o

main = __name__ == '__main__'

t = time.time()

if main:
    import importlib

    CONFIG = None

    try:
        import config
        importlib.reload(config)

        from config import DETAILS, OR, H1, LONG, THORUS, ROWS, COLS,  \
                MONO, FRAME, EXTEND, COMPOUND, ROTATE, MOVE, WIREFRAME, \
                ROOT, SOLID, PRINT3D, CLEANUP, GUI_CLEANUP, CONFIG
    except (AssertionError, SyntaxError):
        import sys
        assertionInform(sys.exc_info()[2])
    finally:
        if CONFIG is None: exit(0)                                       # To repair CONFIG before coding

if main and CONFIG:

    MTL = MONO or FRAME

    args = convert(MTL, LONG, H1, OR, DETAILS, THORUS, COMPOUND, PRINT3D)
       # = (MONO or FRAME, LONG, H1, OR, DETAILS)

    kwargs = dict(cleanup=CLEANUP, gui=GUI_CLEANUP)

    OBJ = Mono if MONO else Frame

    if       THORUS.get('CORNER') and not THORUS.get('DISC'):
        root = Root._corn_
        obj = OBJ(*args, root=root, **kwargs)

    elif not THORUS.get('CORNER') and     THORUS.get('DISC'):
        root = Root._disc_
        obj = OBJ(*args, root=root, **kwargs)

    elif     THORUS.get('CORNER') and     THORUS.get('DISC'):
        root = Root._thor_
        obj = OBJ(*args, root=root, **kwargs)

    else:
        root = Root._dome_
        obj = OBJ(*args, root=root, **kwargs)

    OBJ = FrameCompound if not MONO else MonoCompound

    obj.wireFrame(ROWS, COLS, vis=WIREFRAME)
    if not ROOT: exit(0)

    obj.root(solid=SOLID)

    comp = compoundModel( obj, OBJ, EXTEND, COMPOUND, ROTATE, MOVE )

elif main and not CONFIG:
    "Start coding here disabling CONFIG and TEST"
    class FibonacciTrigon(Trigon):

        def __init__(self, *args):
            super().__init__(*args)
            if not self.fibo:
                raise TypeError

    class FibonacciMonoRoot(MonoRoot, FibonacciTrigon):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class FibonacciMonoDome(MonoDome, FibonacciMonoRoot):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class Fibonacci(Root):
        _roots_ = { Root._dome_ : FibonacciMonoDome }

        def __new__(cls, *args, root=None, **kwargs):
            assert root in __class__._roots_.keys(), "TypeError: unknown type of building"
            clss = __class__._roots_.get(root)
            return super().__new__(cls, clss, *args, **kwargs)

    def fibonacci_range(at_least, maximum):
        f1, f2 = 0, 1
        n = maximum
        rng = list()
        for i in range(n):
            f1, f2 = f2, f1+f2
            if f1 >= at_least: rng.append(f1)
            if f1 >= maximum:  break
        return rng

    rng = fibonacci_range(3, 20000)

    inform()

try:
    t = time.time() - t
    m = int(t/60)
    s = t - m*60
    obj.cprint('Executed in: {0} minutes, {1:.1f} seconds'.format(m, s))
except: pass
