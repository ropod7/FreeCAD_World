#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################################################
#
#        ____       ____        _____ _____
#       |__  \     |__  \      /  __ \ __  \
#        / __/ _П_  / __/ === |  |__\ \__|  |       [ logic ]:
#       |____| ¯U¯ |____| ===  \_____\_____/
#
#
###################################################################################

import time
import math, decimal
import importlib

import domeFCMacro
importlib.reload(domeFCMacro)

import config
importlib.reload(config)
from config import DETAILS, OR, NICETY

pi = """
3,1415926535 8979323846 2643383279 5028841971 6939937510
  5820974944 5923078164 0628620899 8628034825 3421170679
  8214808651 3282306647 0938446095 5058223172 5359408128
  4811174502 8410270193 8521105559 6446229489 5493038196
  4428810975 6659334461 2847564823 3786783165 2712019091
  4564856692 3460348610 4543266482 1339360726 0249141273
  7245870066 0631558817 4881520920 9628292540 9171536436
  7892590360 0113305305 4882046652 1384146951 9415116094
  3305727036 5759591953 0921861173 8193261179 3105118548
  0744623799 6274956735 1885752724 8912279381 8301194912
  9833673362 4406566430 8602139494 6395224737 1907021798
  6094370277 0539217176 2931767523 8467481846 7669405132
  0005681271 4526356082 7785771342 7577896091 7363717872
  1468440901 2249534301 4654958537 1050792279 6892589235
  4201995611 2129021960 8640344181 5981362977 4771309960
  5187072113 4_999999_8 3729780499 5105973173 2816096318
  5950244594 5534690830 2642522308 2533446850 3526193118
  8171010003 1378387528 8658753320 8381420617 1776691473
  0359825349 0428755468 7311595628 6388235378 7593751957
  7818577805 3217122680 6613001927 8766111959 0921642019 ...
"""                                                                      # 999 decimal digits of modern π (not constant)

pi = pi.replace(chr(10),   str())
pi = pi.replace(chr(32),   str())
pi = pi.replace(chr(46),   str())
pi = pi.replace(chr(95),   str())
pi = pi.replace(chr(44), chr(46))

PI999 = decimal.Decimal(pi)

domeFCMacro.MacroRoot().cprint('NICETY 999:', PI999)

def modernPi(precision):
    """
        Compute Pi to the current precision;
        https://docs.python.org/3.10/library/decimal.html?#recipes
    """
    precision += 2                                                       # extra digits for intermediate steps
    decimal.getcontext().prec = precision
    three = decimal.Decimal(3)                                           # substitute "three=3.0" for regular floats
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n+na, na+8
        d, da = d+da, da+32
        t = (t * n) / d
        s += t
    decimal.getcontext().prec -= 2
    return +s                                                            # unary plus applies the new precision

PI = modernPi(NICETY)

domeFCMacro.MacroRoot().cprint('NICETY {}:'.format(NICETY), PI)

# затык
