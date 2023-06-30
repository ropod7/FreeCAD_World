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

    def __init__(self, r, d):
        "Receives OR and DETAILS definitions"
        assert isinstance(r, float), "TypeError: r (OR) must be float"
        self.__OR = r
        self.__DETAILS = d

    # Semantics of Trigonometry from: https://tinyurl.com/yyrxfd84

    def rightSideB_ByA(self, c, A):
        return c * self.__cos(A)

    def rightSideB_ByAA(self, a, A):
        return a / self.__tan(A)

    def rightCathetusA_ByA(self, c, A):
        return c * self.__sin(A)

    def rightCathetusA_ByBA(self, b, A):
        return b * self.__tan(A)

    def rightCathetusA_ByB(self, c, HB):
        "OR * cos(B/2)"
        return c * self.__cos(HB)

    def rightHypothenuseByB(self, a, HB):
        "cathetus / cos(B/2)"
        return a / self.__cos(HB)

    def rightHypothenuseByA(self, a, A):
        return a / self.__sin(A)

    def rightHypothenuse(self, a):
        return self.rightHypothenuseByB(a, self.DETAIL_HB)

    def isoscelesBase(self, Or):
        return Or * 2 * self.__cos(self.DETAIL_A)

    def __cos(self, c):
        return math.cos(math.radians(c))

    def __sin(self, c):
        return math.sin(math.radians(c))

    def __tan(self, c):
        return math.tan(math.radians(c))

    @property
    def CIRCLE(self):
        return 360

    @property
    def HALF_CIRCLE(self):
        return self.CIRCLE / 2

    @property
    def OR(self):
        return self.__OR

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

    @property
    def quatro(self):
        return not self.DETAILS % 4

    @property
    def fibo(self):
        f1, f2 = 0, 1
        n = int(self.DETAILS/2)
        for i in range(n):
            f1, f2 = f2, f1+f2
            if f1 >= n: break
        return f1 == n

class TwoPoints(Trigon):
    """

        The whole system revolves around these polygonal points.
        (the number of points to identify is: int( DETAILS/4 ))

    """
    _root_ = str('dome')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oPOINTS = list()

    def oPolyPoints(self, Or):
        x = y = 0
        B = self.DETAIL_B
        A = self.DETAIL_A
        base = self.isoscelesBase(Or)
        points = [[Or, y]]
        for i in range(self.POLY_QUARTER):
            x += self.rightSideB_ByA(base, A)
            y += self.rightCathetusA_ByA(base, A)
            """
                      extra solution for corner to find proportions
                              at Y axis on higher hPoly wf:
                (
                System-wide single deviation is Y == 0.01mm if 0 on X & Y axis
                            in case of self.DETAILS % 4 == 0
                )
            """
            y = 0.01 if not y and not x and self.quatro else y
            points.extend([ [Or - x, y] ])
            A -= B
        return points

class ThorusPoints(TwoPoints):
    """
    Additional proportionaly elongated point system to extend poly points
      into their proper positions in case of toroidal building geometry.
    """
    _roots_ = [TwoPoints._root_, str('corner'), str('disc'), str('thorus')]

    def __init__(self, tp, r, *args, **kwargs):
        "Receives type, OR definitions"
        super().__init__(r, *args, **kwargs)
        self.pointSystem = tp
        x = r*2 if self.elongated else 0
        self.ZERO_X =  x        # To measure corners on X carriage

    def __fixedXYRoots(self, x, y):
        """
        First couple of root X and Y points in case of Y > 0,
        to find complete proportions of toroidal trigonometry.
        """
        root_x = self.oPOINTS[0][1][0]
        root_y = self.oPOINTS[0][1][1]
        root_x = root_x if self.corn else root_x*2 - (root_x - x)
        root_y = root_y if self.corn else root_y*2 - (root_y - y)
        return root_x, root_y

    def __fixedZeroYXRoot(self, x):
        expr = self.pointSystem in __class__._roots_[-2:]
        return x*2 if expr else 0

    def _pntBtmMnr(self, x, y, MTL):
        if self.dome:
            return (x + self.__addititionalMove(MTL), y, 0)
        x = self.__cornerXPoint(x, y, MTL)
        y = self.__cornerYPoint(x, y, 0)
        return (x, y, 0)

    def _h1Points(self, w, MTL):
        r = self.OR
        if self.dome: return r if not w else r-MTL.T
        elif self.disc: return r*3 if not w else r*3-MTL.T
        return r if not w else r+MTL.T

    def _pntHPolyMnr(self, x, y, z, MTL):
        if self.dome:
            return (x + self.__addititionalMove(MTL), y, z)
        x = self.__cornerXPoint(x, y, MTL)
        y = self.__cornerYPoint(x, y, z)
        x += self.__cornerMonoXMove(y, MTL)
        y += self.__cornerMonoYMove(y, MTL)
        return (x, y, z)

    def _pntVPolyMnr(self, x, z):
        if self.dome: return (x, 0, z+self.ZERO_Z)
        elif self.disc: return (x+self.OR*2, 0, z+self.ZERO_Z)
        return (x+(self.OR - x)*2, 0, z+self.ZERO_Z)

    def __cornerXPoint(self, x, y, MTL):
        if not y:
            zero_y_x = self.__fixedZeroYXRoot(x)
            x += (self.OR - x)*2 + zero_y_x
            return x + self.__addititionalMove(MTL)
        root_x, q = self.__fixedXYRoots(x, y)
        return x + (root_x - x)*2 + self.__addititionalMove(MTL)

    def __cornerYPoint(self, x, y, z):
        root_x, root_y = self.__fixedXYRoots(x, y)
        if not y and z == self.ZERO_Z+self.OR-z and z != self.OR:
            return root_y * 2
        elif not y:
            return 0
        return y + (root_y - y)*2

    def __addititionalMove(self, MTL):
        if MTL.FRAME :
            cmove = MTL.W/(self.DETAILS/2)
            dmove = self.rightCathetusA_ByB(cmove, self.DETAIL_B)
            return cmove if self.corn else dmove
        return 0

    def __cornerMonoXMove(self, y, MTL):
        if MTL.MONO and self.corn:
            x = self.rightSideB_ByAA(MTL.T, self.DETAIL_A)
            return x if not y else -x
        return 0

    def __cornerMonoYMove(self, y, MTL):
        if MTL.MONO and self.corn:
            return MTL.T if y else -MTL.T
        return 0

    @property
    def pointSystem(self):
        return self.__type_

    @pointSystem.setter
    def pointSystem(self, tp):
        assert isinstance(tp, str), "TypeError: tp (type) is str"
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
        return self.pointSystem in __class__._roots_[1:]

    @property
    def dometic(self):
        return True if self.dome or self.thor else False

class ExtensionPoints(ThorusPoints):
    _root_ = str('long')

    def __init__(self, tp, l, h, *args, **kwargs):
        "Receives type, LONG and H1 definitions"
        assert isinstance(l, float), "TypeError: l (LONG) must be float"
        assert isinstance(h, float), "TypeError: h (H1)   must be float"
        super().__init__(tp, *args, **kwargs)
        self.ZERO_Y = -l   # To measure extensions on Y carriage
        self.ZERO_Z =  h   # To lift all types of polygonal geometry
        self.__long_ = l
        self.__h1_ = h

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
        reduc = self.OR/10
        MTT = reduc if MTT > reduc else MTT
        amount = int(size / self.isoscelesBase(self.OR - MTT)) or 1
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

class RightPoints(ExtensionPoints):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rightSidePoint(self, x):
        """
         Receives X as cathetus length of right triangle
        and returns Y as length of side of right triangle.
        Points Y till -Y gives base of isosceles triangle,
              which rotated on Z axis by -(B/2).
        """
        return self.rightSideB_ByAA(x, self.DETAIL_A)

# END: Trigonometrical Common Geometry

# BEGIN: FreeCAD system covers

import FreeCAD, FreeCADGui
from FreeCAD import Base
import Draft, Part

class MacroRoot(object):

    def __init__(self):
        self.pl = FreeCAD.Placement()

    def newDoc(self, name):
        name = self.__convertDocName(name)
        FreeCAD.newDocument(name)
        self.getDoc(name, conv=False)

    def setDoc(self, name, conv=True):
        name = self.__convertDocName(name) if conv else name
        FreeCAD.setActiveDocument(name)
        for doc in [self.fcDoc, self.guiDoc]:
            doc = doc.getDocument(name)

    def vector(self, *v):
        return FreeCAD.Vector(*v)

    def recompute(self):
        self.fcDoc.recompute()

    def autogroup(self, obj):
        return Draft.autogroup(obj)

    def cprint(self, *args):
        l = len([*args])
        s = "%s; " * l + "\n" if l > 1 else "%s\n"
        args = tuple([ str(a) for a in [*args] ])
        FreeCAD.Console.PrintMessage(s % args)

    def __convertDocName(self, name):
        assert isinstance(name, str), "TypeError: doc name must be str"
        ords = self.__ords()
        for o in ords: name = name.replace(chr(o), '_')
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
    def roots(self):
        return self.fcDoc.RootObjects

class FreeCADObject(MacroRoot):

    def __init__(self, cleanup=False):
        "Receives CLEANUP definition"
        super().__init__()
        self.cleanUp(cleanup=cleanup)

    def AddObject(self, feature, name):
        return self.fcDoc.addObject(feature, name)

    def Object(self, obj):
        return self.GuiObject(obj).Object

    def remove(self, obj):
        self.fcDoc.removeObject(obj)

    def cleanUp(self, cleanup=False):
        lr = len(self.roots)
        if not lr or not cleanup: return self.recompute()
        [ self.remove(obj.Name) for obj in self.roots ]
        return self.cleanUp(cleanup=cleanup)

    def GuiObject(self, obj):
        return self.guiDoc.getObject(obj.Name)

    def FCObject(self, obj):
        return self.fcDoc.getObject(obj.Name)

    def _setVisibility(self, obj, vis):
        self.GuiObject(obj).Visibility = vis
        return obj

    def _setShapeColor(self, obj):
        self.Object(obj).ViewObject.ShapeColor = self.RGB

    @property
    def ActiveObject(self):
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

    def Wire(self, points, vis=False, **kwargs):
        self.__typeLenCheck(points, list)
        p = [ self.vector(*ps) for ps in points ]
        w = Draft.makeWire(p,placement=self.pl,closed=False,face=False,**kwargs)
        self.autogroup(w)
        self._setVisibility(w, vis)
        return w

    def Polygon(self, n, p, f=True, s=None, i=True, vis=False, **kwargs):
        sides = n
        self.pl.Base = self.vector(*p)
        kw = dict(placement=self.pl, inscribed=i, face=f, support=s, **kwargs)
        polygon = Draft.makePolygon(sides, **kw)
        self.autogroup(polygon)
        return self._setVisibility(polygon, vis)

    def Surface(self, edges, vis=False):
        assert len(edges) == 2, "LengthError: number of edges must be 2"
        edge1, edge2 = edges
        s = self.AddObject('Part::RuledSurface', 'Surface')
        self.ActiveObject.Curve1 = ( edge1, ['Edge1'] )
        self.ActiveObject.Curve2 = ( edge2, ['Edge1'] )
        return self._setVisibility(s, vis)

    def Cut(self, base, tool, bvis=False):
        c = self.AddObject('Part::Cut', 'Cut')
        c.Base = self.FCObject(base)
        c.Tool = self.FCObject(tool)
        self._setShapeColor(c)
        self._setVisibility(base, bvis)
        self._setVisibility(tool, False)
        return c

    def Extrude(self, surface, direction, height, s=True, vis=True, d="Custom"):
        e = self.AddObject('Part::Extrusion', 'Extrude')
        e.Base = surface
        e.DirMode = d
        e.Dir = self.vector(direction)
        e.LengthFwd = height
        e.Solid = self.solid
        e.Symmetric = s
        self._setShapeColor(e)
        self._setVisibility(surface, False)
        return self._setVisibility(e, vis)

    def Loft(self, faces, ruled=False, closed=False):
        assert len(faces) == 2, "LengthError: number of faces must be 2"
        loft = self.AddObject('Part::Loft', 'Loft')
        loft.Sections = faces
        loft.Solid = self.solid
        loft.Ruled = ruled
        loft.Closed = closed
        self._setShapeColor(loft)
        [ self._setVisibility(f, False) for f in faces ]
        return loft

    def Slice(self, obj, vector=(0,1,0), move=0, hideobj=True):
        wires = list()
        shape = obj.Shape
        bv = self.vector(*vector)
        [ wires.append(i) for i in shape.slice(bv, move) ]
        feature = self.__Feature()
        feature.Shape = self.__Compound(wires)
        feature.purgeTouched()
        return self._setVisibility(obj, hideobj) if hideobj else obj

    def Rotate(self, objs, A, z, a, cp=True, vis=True):
        Draft.rotate(objs,A,self.vector(*z),axis=self.vector(*a),copy=cp)
        objs = self.roots[-len(objs):] if cp else objs
        [ self._setVisibility(o, vis) for o in objs ]
        return objs

    def Move(self, objs, x, y, z, cp=True, vis=True):
        Draft.move(objs, self.vector(x, y, z), copy=cp)
        objs = self.roots[-len(objs):] if cp else objs
        [ self._setVisibility(o, vis) for o in objs ]
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

    def cut(self, bases, tool, **kwargs):
        assert isinstance(bases, list) and len(bases), "bases must be not empty list"
        assert isinstance(tool, list) and len(tool) == 1, "one tool must be in list"
        r = list()
        [ r.extend(self.__cut(base, tool, **kwargs)) for base in bases ]
        self.recompute()
        return r

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

    def wiresPoints(self, wires):
        "Returns FreeCAD vectorized list of wire points"
        points = list()
        obj = self.Object
        [ points.append([obj(w).Start, obj(w).End]) for w in wires ]
        return points

    def __cut(self, base, tool, **kwargs):
        return [ self.Cut(base, tool[0], **kwargs) ]

    def __surface(self, edges, **kwargs):
        return [ self.Surface(edges, **kwargs) ]

    def __loft(self, faces, **kwargs):
        assert isinstance(faces, list) and len(faces) == 2, \
            "TypeError: faces must be list with length 2"
        return [ self.Loft(faces, **kwargs) ]

    def __extrude(self, surface, direction, height, **kwargs):
        return [ self.Extrude(surface, direction, height, **kwargs) ]

class Movement(Model):

    def rotate(self, objs, angle, zero, axis, times, cp=True, **kwargs):
        assert isinstance(objs, list), "TypeError: objs must be list"
        if not len(objs): return list()
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

    def move(self, objs, x, y, z, times, vis=True, **kwargs):
        assert isinstance(objs, list), "TypeError: objs must be list"
        if not len(objs): return list()
        obj = list()
        for i in range(1, times+1):
            xi, yi, zi = x*i, y*i, z*i
            obj.extend(self.Move(objs, xi, yi, zi, **kwargs))
        self.recompute()
        return obj

# END: FreeCAD system covers

# BEGIN: Object creation system

class ObjectMovement(Movement):

    """Base movement mechanism of machine tool"""
    def __init__(self, *args, cleanup=False, **kwargs):
        Blocks.__init__(self, *args, **kwargs)
        FreeCADObject.__init__(self, cleanup=cleanup)

    def xMirror(self, objs, x=0, y=0, **kwargs):
        angle = 180
        zero = (x or self.ZERO_X, y, 0)
        axis = (0,0,1)
        return self.rotate(objs, angle, zero, axis, 1, **kwargs)

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

    def h1DropArray(self, obj, **kwargs):
        dim, amount = self.insH1L, self.insH1N
        return self.move(obj, 0,0,-dim, amount-1, **kwargs)

    def h1LiftArray(self, obj, **kwargs):
        dim, amount = self.insH1L, self.insH1N
        return self.move(obj, 0,0,dim, amount-1, **kwargs)

    def vLongArray(self, obj, **kwargs):
        dim = self.insLongL
        amount = self.insLongN
        return self.move(obj, 0,-dim,0, amount, **kwargs)

    def hLongArray(self, obj, **kwargs):
        dim = self.insLongL
        amount = self.insLongN - 1
        if not amount: return list()
        return self.move(obj, 0,-dim,0, amount, **kwargs)

    def compArray(self, objs, angle, n, **kwargs):
        hypB = -90-angle/2
        x = self.rightCathetusA_ByBA(self.ZERO_Y/2, hypB)
        y = self.ZERO_Y/2
        return self.rotate(objs,angle,(x,y,0),(0,0,1),n,**kwargs)

    def _markingArray(self, wire1, wire2, **kwargs):
        wire1.extend(wire2)
        wire1.extend(self.rotate(wire2, 90, (0,0,0),(0,0,1),3,**kwargs))
        return self.move(wire1, 0,self.ZERO_Y,0, 1) if self.long else wire1

    def __pArrayY(self, objs, angle, n, **kwargs):
        zero = (self.ZERO_X, 0, self.ZERO_Z)
        axis = (0, self.dirY, 0)
        return self.rotate(objs, angle, zero, axis, n, **kwargs)

    def __pArrayZ(self, objs, angle, n, **kwargs):
        zero = (0, 0, 0)
        axis = (0, 0, 1)
        return self.rotate(objs, angle, zero, axis, n, **kwargs)

    @property
    def dirY(self):
        return 1 if self.elongated else -1

class ModelMovement(ObjectMovement):

    # BEGIN: Horison poly torsion to extrude mechanism

    def _turnToExtrude(self, objs, **kwargs):
        o = list()
        rng = range(len(objs))
        [ o.extend(self.__turn([objs[i]], i, **kwargs)) for i in rng ]
        return o

    def _turnAfterExtrude(self, objs, **kwargs):
        o = list()
        rng = range(len(objs))
        [ o.extend(self.__turn([objs[i]],i,backw=True,**kwargs)) for i in rng ]
        return o

    def __turn(self, obj, i, backw=False, **kwargs):
        """
        Torsion mechanism to give thickness of horison surfaces of Frame
          Root poly. Revolves around Z axis by angle B/2 and Y axis by
                   angle B*position in horisons sequence.
        """
        return self.__after(obj,i,**kwargs) if backw else self.__to(obj,i,**kwargs)

    def __to(self, obj, i, **kwargs):
        angle, n, zero_y, a_y, mono = self.__prms(i, **kwargs)
        obj = self.__turnToFromZero(obj, -angle/2)
        return self.rotate(obj, angle*n-mono, zero_y, a_y, 1, cp=False)

    def __after(self, obj, i, **kwargs):
        angle, n, zero_y, a_y, mono = self.__prms(i, **kwargs)
        obj = self.rotate(obj, -angle*n+mono, zero_y, a_y, 1, cp=False)
        return self.__turnToFromZero(obj, angle/2)

    def __prms(self, i):
        zero_y, a_y = self.__zeroYAxisToTurn()
        angle = self.DETAIL_B
        n = self.__numberToTurn(self.rows - i)
        mono = self.__monoPrms(angle)
        return angle, n, zero_y, a_y, mono

    def __monoPrms(self, angle):
        if self.MTL.FRAME: return 0
        mono = angle/2
        if self.dometic and self.quatro and not self.less_rows:
            mono -= angle
        if self.coupler:
            op = ( 1.0984 ** (self.DETAILS - 3) ) / (self.DETAILS/2)
            mono += (self.DETAIL_A ** op) / (self.DETAILS - 3)
        return mono

    def __turnToFromZero(self, obj, angle):
        zero_z, a_z = (0, 0, self.ZERO_Z), (0,0,1)
        return self.rotate(obj, angle, zero_z, a_z, 1, cp=False)

    def __numberToTurn(self, ny):
        if self.dome and self.equal_rows and self.quatro:
            return ny-1
        elif self.thor and self.quatro:
            return ny if not self.equal_rows else ny-1
        return ny

    def __zeroYAxisToTurn(self):
        x, z = self.ZERO_X, self.ZERO_Z
        if self.dome:   return (0,0,z), (0, 1,0)
        elif self.corn: return (x,0,z), (0,-1,0)
        return (x,0,z), (0,1,0)

    # END: Horison poly torsion to extrude mechanism

    def _rotatePolygonToCut(self, obj, placement):
        return self.rotate(obj, 90, placement, (1, 0, 0), 1, cp=False)

class Blocks(MutableMapping, RightPoints):
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

    def __init__(self, *args, **kwargs):
        RightPoints.__init__(self, *args, **kwargs)
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
        assert isinstance(self[tp][name][i], list), \
            "TypeError: doubled types must be created before extend"
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
            assert isinstance(arg, str), "TypeError: key is string"

    def __valueExtensionChecker(self, l):
        assert isinstance(l, list), "TypeError: types contains lists"

class ProductionCalc(object): pass

class Materials(list, ProductionCalc):

    def __init__(self, obj, width=0, height=0, thickn=0, RGB=None, **kwargs):
        assert width and height or thickn, "Undefined material dimensions"
        assert isinstance(RGB, tuple), "TypeError: color not tuple"
        assert len(RGB) == 3,         "TypeError: wrong RGB format"
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

class WireFrame(ModelMovement, Blocks):
    _btm_ = str('bottom')
    _hpl_ = str('hPoly')
    _h1_  = str('h1')
    _vpl_ = str('vPoly')
    _mp_  = str('marking')

    def _marking(self, MTL):
        if self.thor: return
        zl = [0, self.ZERO_Z or MTL.W]
        points = [(0, 0, z) for z in zl]
        wire1 = self.wire(points, vis=True) if set(zl) != {0} else list()
        wire2 = self.wire([(0, 0, 0), (0, -MTL.H or -MTL.T, 0)], vis=True)
        wires = self._markingArray(wire1, wire2)
        return wires

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

    def _horizonPoly(self, ny, w, mtl, MTL):
        if not self.cols: return list()
        tp = __class__._hpl_ + self.pointSystem + mtl
        if MTL.FRAME:
            self.appendWfr(tp, [ ] )
        hpll = len(self.getWfr(tp))-1
        amount = self.__hPolyNumber(ny) if ny else 1
        for i in range(amount, -1, -1):
            points = self.oPOINTS[0][i]
            angle = self.DETAIL_B*i
            reduc = self.rightSideB_ByA(w or MTL.H, angle)
            Or = points[0]-reduc if w else points[0]
            drop = self.rightCathetusA_ByA(MTL.H, angle)
            h1 = points[1] + self.ZERO_Z
            h1 = h1 - drop if w else h1
            points = self.oPolyPoints(Or)[:2]
            wire = self.wire([
                self._pntHPolyMnr(x,y,h1,MTL) for x,y in points
                ], vis=self.wfVisibility)
            self.extendDoubledWfr(tp, hpll, wire)
        return self.getWfr(tp)

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

    def __hPolyNumber(self, ny):
        expr = self.equal_rows and self.quatro
        expr0 = self.dome and expr
        expr1 = self.thor and expr and not self.MTL.MONO
        return ny-1 if expr0 or expr1 else ny

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

class ModelLayer(WireFrame):

    def _polygonCutTool(self, height, direction=(0,1,0), **kwargs):
        placement = (self.ZERO_X, 0, self.ZERO_Z)
        sides = 20 if self.DETAILS < 20 else self.DETAILS
        p = self.polygon(sides, self.OR+height*4, placement)
        p = self._rotatePolygonToCut(p, placement)
        h = height if self.MTL.FRAME else height * 2
        return self.extrude(p, direction, h, vis=False, **kwargs)

class Root(ModelLayer):
    _dome_ = ThorusPoints._roots_[0]
    _corn_ = ThorusPoints._roots_[1]
    _disc_ = ThorusPoints._roots_[2]
    _thor_ = ThorusPoints._roots_[3]

    def wireFrame(self, ny, nz, vis=False):
        assert ny <= self.DETAILS/4, "NumberError: ny (ROWS) not in range"
        assert nz <= self.DETAILS,   "NumberError: nz (COLS) not in range"
        self.__rows = ny   # number rows
        self.__cols = nz   # number cols
        self.wfVisibility = vis

    def _build(self, solid=False):
        wfr = self.get(Blocks._wfr_)
        self.solid = solid
        assert isinstance(wfr, dict) and len(wfr), "call wireFrame before build"
        return wfr

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    @property
    def less_rows(self):
        return self.rows < self.POLY_QUARTER

    @property
    def equal_rows(self):
        return self.rows == self.POLY_QUARTER

    @property
    def coupler(self):
        "If DETAILS / 4 == just couple of ROWS in COLS"
        return self.POLY_QUARTER < 3

    @rows.setter
    def rows(self, number):
        self.__rows = number

    @cols.setter
    def cols(self, number):
        self.__cols = number

# END: Object creation system

# BEGIN: Mono root creation system

class MonoMovement(Root):

    def _rotateMoveHiddenMonoWires(self, w):
        a = self.DETAIL_B/2
        c = (0,0,0)
        z = (0,0,1)
        w = self.rotate(w, a, c, z, 1, cp=False)
        if self.dome: return w
        p1, p2 = self.oPOINTS[0][:2]
        x = self.OR - (p1[0] - p2[0]) / 2
        y = (p2[1] - p1[1]) / 2
        return self.xMirror(w, x=x, y=y, cp=False)

    def _horisonToolsRotation(self, t, bw=False):
        angle = self.DETAIL_B/2 if bw else -self.DETAIL_B/2
        return self.rotate(t, angle, (0,0,0), (0,0,1), 1, cp=False)

    def _verticalToolsRotation(self, t, n, mid=False, bw=False):
        B = -self.DETAIL_B if self.corn else self.DETAIL_B
        A = self.DETAIL_A
        n = n if mid else n-1
        x = self.OR*2
        x = x if self.dome else self.rightCathetusA_ByA(x, A)-self.MTL.T
        z = self.h1
        dir_y = -1 if bw else 1
        return self.rotate(t, B*n, (x,0,z), (0,dir_y,0), 1, cp=False)

class MonoBlocks(MonoMovement):
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

    def _createMonoWireFrame(self, ny, MTL, **kwargs):
        mtl = __class__._mtl_
        self.oPOINTS.append( self.oPolyPoints(self.OR) )
        self.insertionLongUnits(self.long, 0)
        c1, c2 = 0, self.rightHypothenuse(MTL.T)
        c3 = self.rightHypothenuse(c2)
        hd, _ = self.insertionH1Units(self.h1, MTL.T)
        [ self._bottom(z, MTL, mtl) for z in [c1, c2] ]
        for c in [c1, c2]:
            if self.thor: continue
            self.oPOINTS.append( self.oPolyPoints(self.OR-c) )
            self._h1(c, hd, MTL, mtl, horison=False)
            self._verticalPoly(ny, mtl)
        self.__createHPolyWires(ny, mtl, MTL)
        self.__createToolWire()
        self._marking(MTL)
        return self.get(Blocks._wfr_)

    def __createToolWire(self):
        if not self.rows or self.thor: return
        y = self.OR*2 if self.elongated and self.coupler else self.OR
        w = self.wire([
            (0, y, self.h1), (0, -y, self.h1)
            ], vis=self.wfVisibility)
        self.toolWire = self._rotateMoveHiddenMonoWires(w)
        return self.toolWire

    def __createHPolyWires(self, ny, mtl, MTL):
        if not self.rows: return
        tp = WireFrame._hpl_ + self.pointSystem + mtl
        self.appendWfr(tp, [ ] )
        if self.less_rows or not self.quatro or not self.dome:
            return self._horizonPoly(ny, 0, mtl, MTL)
        w = self.wire([
            (0, 1, self.h1+self.OR), (0, -1, self.h1+self.OR)
            ], vis=self.wfVisibility)
        self.extendDoubledWfr(tp, 0, self._rotateMoveHiddenMonoWires(w))
        self._horizonPoly(ny, 0, mtl, MTL)
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

    def _createPolyFaces(self, tp):
        wf   = self.getWfr(tp)[0]
        ext  = self.extendFcs
        surf = self.surface
        rng  = range(len(wf)-1)
        [ ext(tp, surf( [wf[i]], [wf[i+1]] )) for i in rng ]
        self.__buildTools(tp)
        return self.getFcs(tp)

    def _createExtPolyFaces(self, tp, cls=None):
        w, f = self.getWfr(tp)
        f = self.surface(w, f)
        return self.extendFcs(tp, f)

    def __buildTools(self, tp):
        f, tp = self.__createPolyToolFaces(tp)
        self.__cuttingPolygons()
        first, mid, last = self.__prepareTools(f)
        self.appendTool(tp, mid)
        return self.getTool(tp)

    def __cuttingPolygons(self):
        if self.thor: return
        t = self.MTL.T
        self.FrontPTool = self._polygonCutTool(t, s=False)
        self.RearPTool  = self._polygonCutTool(t, direction=(0,-1,0), s=False)

    def __createPolyToolFaces(self, tp):
        hpwf = self.getWfr(tp)
        tp   = __class__._tool_ + self.pointSystem
        ext  = self.extendFcs
        surf = self.surface
        rng  = range(len(hpwf[0]))
        [ ext(tp, surf([self.toolWire[0]], [hpwf[0][i]])) for i in rng ]
        return self.getFcs(tp), tp

    def __prepareTools(self, f):
        b = self._horisonToolsRotation(f)
        first = self.__createFirstBottomTool(b)
        mid   = self.__createMedianTools(b)
        last  = self.__createLastTopTool(b)
        return first, mid, last

    def __createFirstBottomTool(self, f):
        t = self.__toolsExtrude([f[-1]], btm=True)
        self.firstBottomTool = self._horisonToolsRotation(t, bw=True)
        return self.firstBottomTool

    def __createLastTopTool(self, f):
        t = self._verticalToolsRotation([f[0]], len(f))
        t = self.__toolsExtrude(t)
        t = self._verticalToolsRotation(t, len(f), bw=True)
        self.lastTopTool = self._horisonToolsRotation(t, bw=True)
        return self.lastTopTool

    def __createMedianTools(self, f):
        temp, mid, l, f, i = list(), list(), len(f), f[1:-1], 2
        for j in range(len(f)):
            k = self._verticalToolsRotation([f[j]], l-i, mid=True)
            b = self.__toolsExtrude(k, btm=True)
            b = self._verticalToolsRotation(b, l-i, mid=True, bw=True)
            t = self.__toolsExtrude(k)
            t = self._verticalToolsRotation(t, l-i, mid=True, bw=True)
            [ temp.append(o) for o in [b, t] ]
            i += 1
        rotate = self._horisonToolsRotation
        [mid.append(rotate(o, bw=True)) for o in temp]
        return mid

    def __toolsExtrude(self, f, btm=False):
        dir_z = -1 if btm else 1
        return self.extrude(f, (0,0,dir_z), self.MTL.T, s=False)

    def _cutPolyPolys(self, e):
        tp = __class__._tool_ + self.pointSystem
        tools = self.getTool(tp)[0]
        e = self.__cutRotateByPolygon(e, self.RearPTool, z=-1)
        r = self.__cutRotateByPolygon(e, self.FrontPTool)
        tools.insert(0, self.lastTopTool)
        tools.append(self.firstBottomTool)
        obj, blocks, k = list(), list(), 0
        for i in range(len(r)):
            j = (i+1) * 2 - 1
            obj.append(   self.cut([r[i]], tools[j]))
            blocks.extend(self.cut(obj[i], tools[k]))
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

    def __init__(self, tp, thickn, *args, **kwargs):
        assert thickn, "No Mono thickness defined"
        self.MTL = Materials(self, thickn=thickn, RGB=(0.4,0.2,0.1), **kwargs)
        super().__init__(tp, *args, **kwargs)

    def wireFrame(self, ny, nz, **kwargs):
        super().wireFrame(ny, nz, **kwargs)
        self._createMonoWireFrame(ny, self.MTL, **kwargs)

    def _build(self, **kwargs):
        super()._build(**kwargs)
        self.__buildPolyH1()
        self.__buildExtH1()
        self.__buildPolyPoly()
        self.__buildExtPoly()

    def __buildPolyH1(self):
        if not self.h1 or not self.cols: return
        tp = WireFrame._btm_
        tpf = self._getWfType(tp, cls=__class__) # thor
        ph1f = self._createPolyH1Face(tpf)
        f = self.getFcs(tpf)
        assert ph1f is f, "Lists of faces not equal"
        block = self.extrude(f, (0,0,1), self.insH1L, s=False)
        return self.extendRoot(tp, block)

    def __buildExtH1(self):
        if not self.h1 or not self.long or self.thor: return
        tp = __class__._h1_
        tpf = self._getWfType(tp, cls=__class__) # not thor
        h1f = self._createH1Face(tpf)
        f = self.getFcs(tpf)
        assert h1f is f, "Lists of faces not equal"
        block = self.extrude(f, (0,-1,0), self.insLongL, s=False)
        return self.extendRoot(tp, block)

    def __buildPolyPoly(self):
        if not self.rows or not self.cols: return
        tp = __class__._hpl_
        tpf  = self._getWfType(tp, cls=__class__) # thor
        hpf = self._createPolyFaces(tpf)
        f = self.getFcs(tpf)
        assert hpf is f, "Lists of faces not equal"
        f = self._turnToExtrude(f)
        dir_x = 1 if self.corn else -1
        e = self.extrude(f, (dir_x,0,0), self.MTL.T, s=False)
        e = self._turnAfterExtrude(e)
        blocks = self._cutPolyPolys(e)
        return self.extendRoot(tp, blocks)

    def __buildExtPoly(self):
        if not self.long or self.thor or not self.rows: return
        tp = __class__._vpl_
        tpf = self._getWfType(tp, cls=__class__) # not thor
        epf = self._createExtPolyFaces(tpf)
        f = self.getFcs(tpf)
        assert epf is f, "Lists of faces not equal"
        block = self.extrude(f, (0,-1,0), self.insLongL, s=False)
        return self.extendRoot(tp, block)

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

    def wireFrame(self, ny, nz, **kwargs):
        Root.wireFrame(self, ny, nz)
        self.__cornWireFrame(ny, **kwargs)
        self.__thorWireFrame(ny, **kwargs)
        return self.get(Blocks._wfr_)

    def root(self, **kwargs):
        self.__cornRoot(**kwargs)
        self.__thorRoot(**kwargs)
        return self.get(Blocks._roo_)

    def __cornWireFrame(self, ny, **kwargs):
        self.pointSystem = Root._corn_
        return self.__wireFrame(ny, **kwargs)

    def __thorWireFrame(self, ny, **kwargs):
        self.pointSystem = Root._thor_
        return self.__wireFrame(ny, **kwargs)

    def __wireFrame(self, ny, **kwargs):
        return self._createMonoWireFrame(ny, self.MTL, **kwargs)

    def __cornRoot(self, **kwargs):
        self.pointSystem = Root._corn_
        return self._build(**kwargs)

    def __thorRoot(self, **kwargs):
        self.pointSystem = Root._thor_
        return self._build(**kwargs)

class Mono(MonoRoot):
    def __init__(self, root=None, *args, **kwargs):
        assert root is not None, "Type of Root of creature not defined"
        assert root in ThorusPoints._roots_,   "Given type not in list"
        return super().__init__(root, *args, **kwargs)

# END: Mono root creation system

# BEGIN: Frame root creation system

class FrameMovement(Root):

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

    def _moveBtmHorBarTool(self, tool, MTL):
        x = self.ZERO_X
        if self.dome: x = MTL.W
        elif self.corn: x = -MTL.W
        elif self.disc: x =  MTL.W
        elif self.thor: x = x-MTL.H/2
        return self.move(tool, x,0,0, 1, cp=False)

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

class FrameBlocks(FrameMovement):
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

    def _createFrameWireFrame(self, ny, MTL, **kwargs):
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
            self._horizonPoly(ny, w, mtl, MTL)
        self._marking(MTL)
        return self.get(Blocks._wfr_ + mtl)

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

class FrameModelLayer(FrameWireFrame):

    def _extrudeHPolys(self, n, MTW, hplwf):
        s = list()
        edges1, edges2 = self.getWfr(hplwf)
        edges1 = edges1[-n-1:]
        edges2 = edges2[-n-1:]
        tool = self._polygonCutTool(MTW)
        s = self.surface(edges1, edges2)
        s = self._turnToExtrude(s)
        e = self.extrude(s, (0,0,1), MTW)
        extruded = self._turnAfterExtrude(e)
        return self.__cutHPolys(extruded, tool)

    def _extrudeVertical(self, edges, MTW):
        assert isinstance(edges, list) and len(edges), "empty or wrong edges list"
        edges1, edges2 = edges
        s = self.surface(edges1, edges2)
        f = self.extrude(s, (0,1,0), MTW)
        return f

    def _cutBtmHorBar(self, base, MTL, h1wf):
        "In Thorus and Disc mode as tool works h1 bar of Corner"
        tool = self.surface(*self.getWfr(h1wf)) # wires as made H1 bar of
        tool = self.extrude(tool, (0, 1, 0), MTL.W)
        tool = self._moveBtmHorBarTool(tool, MTL)
        tool2 = self.pArrayZB(tool, 1)
        prebar = self.cut( base,  tool )
        return self.cut( prebar, tool2 )

    def __cutHPolys(self, e, tool):
        s1 = self.cut(e, tool)
        s1 = self.pArrayZB(s1, -1, cp=False)
        s = self.cut(s1, tool)
        return self.pArrayZB(s, 1, cp=False)

class FrameRoot(FrameModelLayer):
    """Creator of bar root objects"""
    _mtrl_ = FrameWireFrame._mtl_
    _h1ba_ = WireFrame._h1_
    _vplb_ = WireFrame._vpl_ + _mtrl_
    _botm_ = WireFrame._btm_
    _hplb_ = FrameWireFrame._hpl_
    _lnge_ = FrameWireFrame._rof_
    _shte_ = FrameWireFrame._sht_
    _hdrp_ = str('h1drops')

    def __init__(self, tp, matW, matH, *args, **kwargs):
        self.MTL = Materials(self, width=matW, height=matH, RGB=(1.0,0.8,0.0))
        super().__init__(tp, *args, **kwargs)

    def wireFrame(self, ny, nz, **kwargs):
        super().wireFrame(ny, nz, **kwargs)
        return self._createFrameWireFrame(ny, self.MTL, **kwargs)

    def _build(self, **kwargs):
        super()._build(**kwargs)
        self.__bottomHorizonBar()
        self.__h1WallBar()
        self.__verticalPolyBar()
        self.__horizonPolyBars(self.rows)
        self.__longHorisonBar()
        return self.get(Blocks._roo_)

    def __bottomHorizonBar(self):
        if not self.h1 or not self.cols: return
        tp = __class__._botm_
        btmwf = self._getWfType(tp, cls=__class__)
        WFh1 = __class__._h1ba_
        h1wf  = self._getWfType(WFh1, cls=__class__)
        cornwf = WFh1 + Root._corn_ + __class__._mtrl_
        h1wf = cornwf if self.thor else h1wf
        s = self.surface(*self.getWfr(btmwf))
        e = self.extrude(s, (0, 0, 1), self.MTL.H, s=False)
        bb = self._cutBtmHorBar(e, self.MTL, h1wf)
        return self.extendRoot(tp, bb )

    def __h1WallBar(self):
        if not self.h1 or self.thor: return
        tp = __class__._h1ba_
        h1wfr = self._getWfType(WireFrame._h1_, cls=__class__)
        h1wfr = self.getWfr(h1wfr)
        h1 = self._extrudeVertical( h1wfr, self.MTL.W )
        return self.extendRoot(tp, h1)

    def __horizonPolyBars(self, n):
        if not self.cols: return
        tp = __class__._hplb_
        hplwf = self._getWfType(tp, cls=__class__)
        bs = self._extrudeHPolys(n, self.MTL.W, hplwf)
        self._moveBottomToZero( [bs[-1]], self.MTL.W )
        return self.extendRoot(tp, bs)

    def __verticalPolyBar(self):
        tp = __class__._vplb_
        vplwf = self._getWfType(WireFrame._vpl_,  cls=__class__)
        if not len(self.getWfr(vplwf)): return self.extendRoot(tp, list())
        v = self._extrudeVertical( self.getWfr(vplwf), self.MTL.W )
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

    def __shortHorisonBar(self):
        tp = __class__._shte_
        shtwf = self._getWfType(tp, cls=__class__)
        if not self.rows and not self.h1: return list()
        elif not len(self.getWfr(shtwf)): return list()
        s = self.surface(*self.getWfr(shtwf))
        b = self.extrude(s, (1,0,0), self.MTL.W)
        b = self._alignHorisonShortBar(b, self.MTL.W)
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

    def wireFrame(self, ny, nz, **kwargs):
        Root.wireFrame(self, ny, nz)
        self.__cornWireFrame(ny, **kwargs)
        self.__thorWireFrame(ny, **kwargs)
        return self.get(Blocks._wfr_)

    def root(self, **kwargs):
        self.__cornRoot(**kwargs)
        self.__thorRoot(**kwargs)
        return self.get(Blocks._roo_)

    def __wireFrame(self, ny, **kwargs):
        return self._createFrameWireFrame(ny, self.MTL, **kwargs)

    def __cornWireFrame(self, ny, **kwargs):
        self.pointSystem = Root._corn_
        return self.__wireFrame(ny, **kwargs)

    def __thorWireFrame(self, ny, **kwargs):
        self.pointSystem = Root._thor_
        return self.__wireFrame(ny, **kwargs)

    def __cornRoot(self, **kwargs):
        self.pointSystem = Root._corn_
        return self._build(**kwargs)

    def __thorRoot(self, **kwargs):
        self.pointSystem = Root._thor_
        return self._build(**kwargs)

class Frame(FrameRoot):
    def __init__(self, root=None, *args, **kwargs):
        assert root is not None, "Type of Root of creature not defined"
        assert root in ThorusPoints._roots_,   "Given type not in list"
        return super().__init__(root, *args, **kwargs)

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
        self.__obj = obj
        obj.cols = cols

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
        to = [todrp[-1]]
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
        obj.extendPlg(allp, obj.pArrayZB(objs, n).copy())

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
        return self.obj.rotate(objs, angle, center, axis, n, cp=copy)

    def _move(self, objs, x,y,z, n, copy):
        return self.obj.move(objs, x,y,z, n, cp=copy)

    def __dropH1s(self, obj, todrp, tps, extm, **kwargs):
        "array mechanism to fill up h1 by horisons"
        if not self.h1: return
        drop = obj.h1DropArray(todrp, **kwargs).copy()
        [ extm(t, drop) for t in tps ]
        return drop

    def __liftH1s(self, obj, tolft, tps, extm):
        "array mechanism to fill up h1 by horisons"
        if not self.h1: return [ extm(t, []) for t in tps ]
        lift = obj.h1LiftArray(tolft)
        [ extm(t, tolft + lift.copy()) for t in tps ]
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
        vpl = obj.pArrayYB(torev, n)
        toall = torev + vpl.copy()
        [extm(t, toall.copy()) for t in tps]
        return toall.copy()

    def __moveToThor(self, obj, tomove, tps, extm, **kwargs):
        "thorus mirroring mechanism"
        if not obj.thor or not len(tomove): return
        r = 2 if self.rows < obj.DETAILS/4 else 1
        moved = obj.xMirror(tomove, **kwargs).copy()
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
        made = arr(toarr)
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
        return self.__obj.cols

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

    def compound(self):
        """
        Trigonometry based compound extended object:
            moved by: -X carriage on Y: LONG/2
        """
        obj  = self.obj
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
        comp = obj.compArray(total, angle, times)
        return obj.extend(totl, comp)

    def _collectTotal(self, obj):
        total = __class__._totl_
        allp = obj.getPlg(Extend._allp_)
        alle = obj.getExt(Extend._alle_)
        obj.extend(total, allp.copy())
        obj.extend(total, alle.copy())
        return obj.get(total)

    def rotate(self, *args):
        objs = self.obj.get(__class__._totl_)
        return super()._rotate(objs, *args)

    def move(self, vector, *args):
        objs = self.obj.get(__class__._totl_)
        x,y,z = vector
        return super()._move(objs, x,y,z, *args)

# END: Extend and compound super system

# BEGIN: Basic flexible Mono Root extends and compound

class MonoExtend(Compound):

    def __init__(self, obj, **kwargs):
        super().__init__(MonoRoot, obj, **kwargs)
        if not self.h1 and not self.rows: return
        self.__completePartialPoly(obj)
        self._revPolyZ(obj, self.cols-1)
        self.__completeExtension(obj)

    def __completePartialPoly(self, obj):
        self._liftPolyH1s(obj)
        lofts = obj.getRoot(MonoRoot._hpl_)
        self._collectPartial(obj, lofts)

    def __completeExtension(self, obj):
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
        self.__completeExtension(obj)

    def __completePartialPoly(self, obj):
        "vPoly array, horison drops"
        verts = self.__revolvePoly(obj) or list()
        self.__moveVertsToThor(obj, verts)
        self.__dropHoriPolys(obj)
        self._collectPartial(obj)

    def __completeExtension(self, obj):
        "shorts array, horisons drop, bottoms, long array"
        if not self.long: return obj.extendExt(Extend._alle_, list())
        extm = obj.extendExt
        short, lng, revs = self._revHoriExtY(obj)
        short = short.copy()
        drops = self._dropExtH1s(obj, short)
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
        if obj.thor and ok: return
        # elif obj.dome and ok or not self.rows: return extm(tp, lng)
        return extm(tp, lng)

    # END: Extension expand system

class FrameCompound(FrameExtend):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._collectTotal(self.obj)

# END: Basic flexible Frame Root extends and compound

# BEGIN: Conveyor system

class Conveyor(object): pass

# END: Conveyor system

# BEGIN: Coding

###################################################################################
#
#                               [ coding ]:
#
###################################################################################

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

def compoundModel(OBJ, obj, s, root, EXTEND, COMPOUND, ROTATE, MOVE):
    if not OBJ is str(s): return list()
    o = None
    if EXTEND:
        o = root(obj)
    if COMPOUND:
        o.compound()
    if ROTATE.get('DO'):                # at first rotate
        angle  = ROTATE.get('ANGLE')
        center = ROTATE.get('CENTER')
        axis   = ROTATE.get('AXIS')
        copy   = ROTATE.get('COPY')
        times  = ROTATE.get('TIMES') if copy else 1
        o.rotate(angle, center, axis, times, copy)
    if MOVE.get('DO'):                  # next move
        vector = MOVE.get('VECTOR')
        copy   = MOVE.get('COPY')
        times  = MOVE.get('TIMES') if copy else 1
        o.move(vector, times, copy)
    return o

main = __name__ == '__main__'

if main:
    import importlib

    import config
    importlib.reload(config)

    from config import DETAILS, OR, H1, LONG, THORUS, ROWS,    \
            COLS, MONO, FRAME, EXTEND, COMPOUND, ROTATE, MOVE,  \
            WIREFRAME, ROOT, SOLID, PRINT3D, CLEANUP, CONFIG

if main and CONFIG:

    t = time.time()

    MTL = MONO or FRAME

    args = convert(MTL, LONG, H1, OR, DETAILS, THORUS, COMPOUND, PRINT3D)

    if       THORUS.get('CORNER') and not THORUS.get('DISC'):
        OBJ = FrameCorner if not MONO else MonoCorner
        obj = OBJ(*args, cleanup=CLEANUP)
        OBJ = str('CORNER')

    elif not THORUS.get('CORNER') and     THORUS.get('DISC'):
        OBJ = FrameDisc if not MONO else MonoDisc
        obj = OBJ(*args, cleanup=CLEANUP)
        OBJ = str('DISC')

    elif     THORUS.get('CORNER') and     THORUS.get('DISC'):
        OBJ = FrameThorus if not MONO else MonoThorus
        obj = OBJ(*args, cleanup=CLEANUP)
        OBJ = str('THORUS')

    else:
        OBJ = FrameDome if not MONO else MonoDome
        obj = OBJ(*args, cleanup=CLEANUP)
        OBJ = str('DOME')

    COMP = FrameCompound if not MONO else MonoCompound

    obj.wireFrame(ROWS, COLS, vis=WIREFRAME)
    if not ROOT: exit(0)

    obj.root(solid=SOLID)

    for o in ['DOME', 'CORNER', 'DISC', 'THORUS']:
        compoundModel( OBJ, obj, o, COMP, EXTEND, COMPOUND, ROTATE, MOVE )

    t = time.time() - t
    m = int(t/60)
    s = t - m*60
    obj.cprint('Executed in: {0} minutes, {1:.1f} seconds'.format(m, s))

elif main and not CONFIG:
    "Start coding here disabling CONFIG and TEST"
    # As example created "heart system":
    pass

