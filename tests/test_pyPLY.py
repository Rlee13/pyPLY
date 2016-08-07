#!/usr/bin/env python
#
# pyPLY v.0.1
#
# Copyright (c) 2016 J. Hahn
#
# This file is part of pyPLY.
# An up to date version of the software is to be found at:
# https://github.com/Rlee13/pyPLY/
#
# pyPLY is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyPLY is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyPLY; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# pyPLY test file
#

import pyPLY

# data from docs/examples/NASA RP1351-ex1.ipynb

def test_CompositeMaterial():
    global material
    material = pyPLY.CompositeMaterial()
    material.define("AS4_3501_6", "imperial", E11=20010000.0, E22=1301000.0, G12=1001000.0, niu12=0.3, thk=0.005)

def test_Lamina():
    import numpy as np
    global material, layer1, layer2, layer3, layer4
    layer1 = pyPLY.Lamina()
    layer2 = pyPLY.Lamina()
    layer3 = pyPLY.Lamina()
    layer4 = pyPLY.Lamina()

    layer1.define("Layer_1", 1, 0)
    layer2.define("Layer_2", material, -45)
    layer3.define("Layer_3", material, 45)
    layer4.define("Layer_4", 1, 0)

    layer1.update()
    layer2.update()
    layer3.update()
    layer4.update()

    assert np.isclose(layer1.Qbar[0, 0], 20127779)
    assert np.isclose(layer1.Qbar[1, 0], 392597)
    assert np.isclose(layer1.Qbar[1, 1], 1308658)
    assert np.isclose(layer1.Qbar[0, 2], 0)
    assert np.isclose(layer1.Qbar[2, 2], 1001000)

    assert np.isclose(layer2.Qbar[0, 0], 6556408)
    assert np.isclose(layer2.Qbar[1, 0], 4554408)
    assert np.isclose(layer2.Qbar[1, 1], 6556408)
    assert np.isclose(layer2.Qbar[0, 2], -4704780)
    assert np.isclose(layer2.Qbar[2, 2], 5162811)

def test_Laminate():
    import numpy as np
    global layer1, layer2, layer3, layer4

    laminate = pyPLY.Laminate()
    laminate.add_Lamina(layer1)
    laminate.add_Lamina(layer2)
    laminate.add_Lamina(layer3)
    laminate.add_Lamina(layer4)
    laminate.update()

    assert np.isclose(laminate.A[0, 0], 266842)
    assert np.isclose(laminate.A[0, 1], 49470)
    assert np.isclose(laminate.A[1, 1], 78651)
    assert np.isclose(laminate.A[1, 2], 0)
    assert np.isclose(laminate.A[2, 1], 0)
    assert np.isclose(laminate.A[2, 2], 61638)

    assert np.isclose(laminate.Ex, 11672709)
