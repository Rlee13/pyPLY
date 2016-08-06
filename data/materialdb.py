#!/usr/bin/env python
#
# pyPLY v.0.01
#
# Copyright (c) 2012 Liviu Armeanu
#
# This file is part of pyPLY.
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
# pyPLY main classes
#

# History:
# 05.02.12 - pyPLY v.0.1
#

import pyPLY.pyPLY.pyPLY
#*************************************************************************************************************
# Source:
# Example material from "Basic Mechanics of Laminated Composite Plates"
# A.T. Nettles
# NASA Reference Publication 1351
#
AS4_3501_6 = pyPLY.pyPLY.CompositeMaterial()
AS4_3501_6.define("AS4_3501_6", "imperial", E11=20010000.0, E22=1301000.0, G12=1001000.0, niu12=0.3, thk=0.005,
             Sigma_ut0 = 616.0, Sigma_uc0 = 355.0, Sigma_ut90 = 42.0, Sigma_uc90 = 105.0, Tau_u = 50.0,
             alpha_11 = -0.04e-6, alpha_22 = 18.0e-6, beta_11 = 0.01, beta_22 = 0.35)

#*************************************************************************************************************
# Source:
# Progressive Failure Example Calculation
# From "SE253B Progressive Failure Example Calculation"
# H.Kim UCSD SE253
#
CarbonEpoxy = pyPLY.pyPLY.CompositeMaterial()
CarbonEpoxy.define("CarbonEpoxy", "psi", E11=20e6, E22=1.5e6, G12=1e6, niu12=0.29, thk=0.005,
             Sigma_ut0 = 310e3, Sigma_uc0 = 310e3, Sigma_ut90 = 6e3, Sigma_uc90 = 30e3, Tau_u = 15e3)

#*************************************************************************************************************
# Source:
# Example material from "Structural Analysis of Polymeric Composite Materials"
# Mark. E. Tuttle
#
GraphiteEpoxy = pyPLY.pyPLY.CompositeMaterial()
GraphiteEpoxy.define("GraphiteEpoxy", "metric", E11=170e9, E22=10e9, G12=13e9, niu12=0.3, thk=0.125e-3,
             Sigma_ut0 = 1500e6, Sigma_uc0 = 1200e6, Sigma_ut90 = 50e6, Sigma_uc90 = 100e6, Tau_u = 75e6,
             alpha_11 = -0.9e-6, alpha_22 = 27.0e-6, beta_11 = 150e-6, beta_22 = 4800e-6)
             
#*************************************************************************************************************
# Source:
# Material used AS/3501 carbon epoxy as defined in
# "Principles of composite material mechanics" by Ronald F. Gibson (2007)
#
AS3501 = pyPLY.pyPLY.CompositeMaterial()
AS3501.define("AS3501", "metric", E11=138.0, E22=9.0, G12=6.9, niu12=0.3, thk=0.25, 
                        alpha_11 = 0.88e-6, alpha_22 = 31.0e-6)

#*************************************************************************************************************
# Source:
# Unknown
#
GE170 = pyPLY.pyPLY.CompositeMaterial()
GE170.define("GE170", "GPa", E11=170.0, E22=10.0, G12=13.0, niu12=0.3, thk=0.000125,
             Sigma_ut0 = 616.0, Sigma_uc0 = 355.0, Sigma_ut90 = 42.0, Sigma_uc90 = 105.0, Tau_u = 50.0,
             alpha_11 = -0.9e-6, alpha_22 = 27.0e-6, beta_11 = 150.0e-6, beta_22 = 4800.0e-6)

#*************************************************************************************************************
# Source: ISO12215-5
# CU560_vl (Carbon Unidirectional vacuum laminated 0.66 glass by mass)
#
CU560_vl = pyPLY.pyPLY.CompositeMaterial()
CU560_vl.define("CU560_vacuum_laminated", "N/sqmm;mmm", E11=94827.0, E22=5510.0, G12=3014.0, niu12=0.32, thk=0.66,
             Sigma_ut0 = 947.0, Sigma_uc0 = 512.0, Sigma_ut90 = 25.0, Sigma_uc90 = 75.0, Tau_u = 44.0)

#*************************************************************************************************************
# Source: ISO12215-5
# CU560_hl (Carbon Unidirectional hand laminated 0.55 glass by mass)
#
CU560_hl = pyPLY.pyPLY.CompositeMaterial()
CU560_hl.define("CU560_hand_laminated", "N/sqmm;mmm", E11=72829.0, E22=4758.0, G12=2411.0, niu12=0.32, thk=0.85,
             Sigma_ut0 = 729.0, Sigma_uc0 = 401.0, Sigma_ut90 = 21.0, Sigma_uc90 = 64.0, Tau_u = 35.0)
