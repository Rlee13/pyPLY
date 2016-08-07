#!/usr/bin/env python
#
# pyPLY v.0.1
#
# Copyright (c) 2012 Liviu Armeanu (Rlee13)
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
# pyPLY main classes
#

# History:
# 05.02.12 - pyPLY v.0.1
#
import math
from sys import exit

__version_info__ = (0, 0, 1)
__pyPLYversion__ = '.'.join([str(num) for num in __version_info__])
errorString = [
"pyPLY Error: Invalid input value, check material input data! Exit now...",
"pyPLY Error: Error updating data, check layer input data! Exit now...",
"pyPLY Error: Unknown parameter type! It should be and integer or pyPLY.CompositeMaterial type. Exit now...",
"pyPLY Error: Error reading data, check angle value input data! Exit now...",
"pyPLY Error: Error reading data, check load's values input data! Exit now...",
"pyPLY Error: Lamina %d not updated! Exit now...",
"pyPLY Error: Laminate not updated! Exit now...",
"pyPLY Error: Unknown loading type! Exit now...",
]

dependencies = '''This module requires:
	Numpy
'''

try:
    from numpy import *
except ImportError, value:
    print dependencies
    raise

#+++++++++++++++++++++
# Utilities
#+++++++++++++++++++++

def quadratic(a, b, c=None):
    """
    Solve quadratic equation with real coefficients
    Usage
        number, number = quadratic(real, real [, real])
    x^2 + ax + b = 0 (or ax^2 + bx + c = 0)
    By substituting x = y-t and t = a/2, the equation reduces to
       y^2 + (b-t^2) = 0
    which has easy solution
       y = +/- sqrt(t^2-b)
	from Simple Recipes in Python by William Park
	http://www.physics.rutgers.edu/~masud/computing/WPark_recipes_in_python.html
    """
    if c: # (ax^2 + bx + c = 0)
        if a == 0:
            msg = "Invalid coefficient (a = 0, ax^2 + bx + c = 0)! Exit now..."
            print msg
            return 0.0,0.0
        a, b = b / float(a), c / float(a)
    t = a / 2.0
    r = t**2 - b
    if r >= 0: # real roots
        y1 = math.sqrt(r)
    else: # complex roots
        msg = "Complex roots! Exit now..."
        print msg
        return 0.0,0.0
    y2 = -y1
    return y1 - t, y2 - t
#+++++++++++++++++++++
#Initialize parameters
#+++++++++++++++++++++

#+++++++++++++++++++
# Creates R Reuter matrix.
#+++++++++++++++++++
R = matrix([[1,0,0],[0,1,0],[0,0,2]])
#************************************************************************
#	**Resolve Inverse Matrix R
#************************************************************************
Rinv = R.I

#************************************************************************
#	**Define a Composite Material Class
#************************************************************************
class CompositeMaterial:
    """ Defines a Composite Material Class.
        See pyPLY documentation for details.
    """
    total_no_mat = 0
    list_of_mat = {} # it is actualy a dictionary

    def __init__(self):
        self.name = "E-Glass/Vinylester Generic"
        self.units = "N/sqm;m"
        self.E11 = 0.0
        self.E22 = 0.0
        self.G12 = 0.0
        self.niu12 = 0.0
        self.niu21 = 0.0
        self.thk = 0.0
        self.mat_no = 0
        self.extended_props = 0 # the material has got extended properties

    def define(self, name, units, E11, E22, G12, niu12, thk, **extend_props):
        global errorString
        self.name = name
        self.units = units
        try:
            self.E11 = float(E11)
            self.E22 = float(E22)
            self.G12 = float(G12)
            self.niu12 = float(niu12)
            self.thk = float(thk)
        except :
            exit(errorString[0])
        if self.E11 != 0.0:
            self.niu21 = (self.niu12) * (self.E22) / (self.E11)
        else:
            exit(errorString[0])

        if extend_props :
            extended_props = 1
            try:
                if extend_props.has_key('Sigma_ut0'):
                    self.Sigma_ut0 = float(extend_props['Sigma_ut0'])
                if extend_props.has_key('Sigma_uc0'):
                    self.Sigma_uc0 = float(extend_props['Sigma_uc0'])
                if extend_props.has_key('Sigma_ut90'):
                    self.Sigma_ut90 = float(extend_props['Sigma_ut90'])
                if extend_props.has_key('Sigma_uc90'):
                    self.Sigma_uc90 = float(extend_props['Sigma_uc90'])
                if extend_props.has_key('Tau_u'):
                    self.Tau_u = float(extend_props['Tau_u'])
                if extend_props.has_key('alpha_11'):
                    self.alpha_11 = float(extend_props['alpha_11'])
                if extend_props.has_key('alpha_22'):
                    self.alpha_22 = float(extend_props['alpha_22'])
                if extend_props.has_key('beta_11'):
                    self.beta_11 = float(extend_props['beta_11'])
                if extend_props.has_key('beta_22'):
                    self.beta_22 = float(extend_props['beta_22'])
            except :
                exit(errorString[0])

        CompositeMaterial.total_no_mat += 1
        self.mat_no = CompositeMaterial.total_no_mat
        CompositeMaterial.list_of_mat[self] = self.mat_no

    def __del__(self):
        for i in CompositeMaterial.list_of_mat:
            if (i.mat_no == self.mat_no) :
                del CompositeMaterial.list_of_mat[i]
                break

#************************************************************************
#	**Define a Lamina Class
#************************************************************************
class Lamina:
    """ Defines a Lamina Class.
        See pyPLY documentation for details.
    """
    def __init__(self):
        self.name = "Lamina_0_Class"
        self.mat_no = 0
        self.angle = 0.0
        self.Teta = self.angle
        self.updated = 0
        self.Teta = 0.0
        self.m = 0.0
        self.n = 0.0
        self.S = matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
        self.T = matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
        self.Teps = matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
        self.E11 = 0.0
        self.E22 = 0.0
        self.G12 = 0.0
        self.niu12 = 0.0
        self.thk = 0.0
        self.niu21 = 0.0
# **alpham and betam hygrothermal vectors in 1,2 directions
        self.alpham = matrix([[0.0],[0.0],[0.0]])
        self.betam = matrix([[0.0],[0.0],[0.0]])
# **alphas_xy and betas_xy hygrothermal vectors in x,y directions
        self.alphas_xy = matrix([[0.0],[0.0],[0.0]])
        self.betas_xy = matrix([[0.0],[0.0],[0.0]])

    def define(self, name, mat_no_name, angle):
        """ 
        Method for defining a Lamina Class.
        Parameters:
        name = Lamina name [string];
        mat_no_name = Lamina's material name or number [int/CompositeMaterial];
        angle = Lamina's angle [degrees].
        """
        self.name = name

        if isinstance(mat_no_name, int): self.mat_no = mat_no_name
        elif isinstance (mat_no_name, CompositeMaterial):
            self.mat_no = CompositeMaterial.list_of_mat[mat_no_name]
        else:
            exit(errorString[2])

        try:
            self.angle = float(angle)
        except :
            exit(errorString[3])
        self.Teta = self.angle
# get the values from the material
        lam = CompositeMaterial.list_of_mat
        for k, v in lam.iteritems():
            if (v == self.mat_no) :
                self.E11 = k.E11
                self.E22 = k.E22
                self.G12 = k.G12
                self.niu12 = k.niu12
                self.niu21 = k.niu21
                self.thk = k.thk
                try:
                    k.alpha_11, k.alpha_22
                except:
                    pass
                else:
                    self.alpha_11 = k.alpha_11 ; self.alpham[0] = k.alpha_11
                    self.alpha_22 = k.alpha_22 ; self.alpham[1] = k.alpha_22
                    self.alpham[2] = 0.0

                try:
                    k.beta_11, k.beta_22
                except:
                    pass
                else:
                    self.beta_11 = k.beta_11 ; self.betam[0] = k.beta_11
                    self.beta_22 = k.beta_22 ; self.betam[1] = k.beta_22
                    self.betam[2] = 0.0

        self.updated = 0

    def change_Angle_Lamina(self, new_angle):
        self.angle = new_angle
        self.Teta = new_angle
        self.updated = 0

    def change_Material_No_Lamina(self, new_material_no):
        self.mat_no = new_material_no
# get the values from the material
        lam = CompositeMaterial.list_of_mat
        for k, v in lam.iteritems():
            if (v == self.mat_no) :
                self.E11 = k.E11
                self.E22 = k.E22
                self.G12 = k.G12
                self.niu12 = k.niu12
                self.niu21 = k.niu21
                self.thk = k.thk
                try:
                    k.alpha_11, k.alpha_22
                except:
                    pass
                else:
                    self.alpha_11 = k.alpha_11 ; self.alpham[0] = k.alpha_11
                    self.alpha_22 = k.alpha_22 ; self.alpham[1] = k.alpha_22
                    self.alpham[2] = 0.0

                try:
                    k.beta_11, k.beta_22
                except:
                    pass
                else:
                    self.beta_11 = k.beta_11 ; self.betam[0] = k.beta_11
                    self.beta_22 = k.beta_22 ; self.betam[1] = k.beta_22
                    self.betam[2] = 0.0

        self.updated = 0

    def update(self):
        global errorString
        try:
            m = math.cos (math.pi * self.Teta / 180)
            n = math.sin (math.pi * self.Teta / 180)
#************************************************************************
#	**Resolve Compliance Matrix S
#************************************************************************
            self.S[0, 0] =  1/self.E11
            self.S[0, 1] = -self.niu21/self.E22
            self.S[1, 0] = -self.niu12/self.E11
            self.S[1, 1] = 1/self.E22
            self.S[2, 2] = 1/self.G12
#        print self.S
#************************************************************************
#	**Resolve Stiffness Matrix Q
#************************************************************************
            self.Q = (self.S).I
#     print Q
#************************************************************************
#	**Resolve Transformation Matrix T
#************************************************************************
            self.T[0, 0] = m*m
            self.T[0, 1] = n*n
            self.T[0, 2] = 2*m*n
            self.T[1, 0] = n*n
            self.T[1, 1] = m*m
            self.T[1, 2] = -2*m*n
            self.T[2, 0] = -m*n
            self.T[2, 1] = m*n
            self.T[2, 2] = m*m-n*n
#    print T
#************************************************************************
#	**Resolve Inverse Matrix T
#************************************************************************
            self.Tinv = (self.T).I
#      print Tinv
# ************************************************************************
# 	**Resolve Transformation Matrix Teps (strain transformation)
# ************************************************************************
            self.Teps[0, 0] = m*m
            self.Teps[0, 1] = n*n
            self.Teps[0, 2] = m*n
            self.Teps[1, 0] = n*n
            self.Teps[1, 1] = m*m
            self.Teps[1, 2] = -m*n
            self.Teps[2, 0] = -2*m*n
            self.Teps[2, 1] = 2*m*n
            self.Teps[2, 2] = m*m-n*n
#************************************************************************
#	**Resolve Transformed Stiffness Matrix Qbar
#************************************************************************
            self.Qbar=(self.Tinv)*(self.Q)*R*(self.T)*Rinv
#     print "Qbar
#************************************************************************
#	**Resolve Transformed Compliance Matrix Sbar
#************************************************************************
            self.Sbar = (self.Qbar).I
#        print self.Sbar
#************************************************************************
#	**Resolve Invariants
#************************************************************************
#	**Compliance Invariants
#************************************************************************
            self.U1S = 1/8.0 * (3 * self.S[0, 0] + 3 * self.S[1, 1] + 2 * self.S[0, 1] + 4 * self.S[2, 2])
            self.U2S = 1/2.0 * (self.S[0, 0] - self.S[1, 1])
            self.U3S = 1/8.0 * (self.S[0, 0] + self.S[1, 1] - 2 * self.S[0, 1] - 4 * self.S[2, 2])
            self.U4S = 1/8.0 * (self.S[0, 0] + self.S[1, 1] + 6 * self.S[0, 1] - 4 * self.S[2, 2])
            self.U5S = 1/2.0 * (self.S[0, 0] + self.S[1, 1] - 2 * self.S[0, 1] + 4 * self.S[2, 2])
#************************************************************************
#	**Stiffness Invariants
#************************************************************************
            self.U1Q = 1/8.0 * (3 * self.Q[0, 0] + 3 * self.Q[1, 1] + 2 * self.Q[0, 1] + 4 * self.Q[2, 2])
            self.U2Q = 1/2.0 * (self.Q[0, 0] - self.Q[1, 1])
            self.U3Q = 1/8.0 * (self.Q[0, 0] + self.Q[1, 1] - 2 * self.Q[0, 1] - 4 * self.Q[2, 2])
            self.U4Q = 1/8.0 * (self.Q[0, 0] + self.Q[1, 1] + 6 * self.Q[0, 1] - 4 * self.Q[2, 2])
            self.U5Q = 1/2.0 * (self.Q[0, 0] + self.Q[1, 1] - 2 * self.Q[0, 1] + 4 * self.Q[2, 2])
#************************************************************************
#	**Effective Elastic Properties
#************************************************************************
            self.Exx = 1.0/self.Sbar[0, 0]
            self.Eyy = 1.0/self.Sbar[1, 1]
            self.Gxy = 1.0/self.Sbar[2, 2]
            self.niuxy = -self.Sbar[0, 1]/self.Sbar[0, 0]
            self.niuyx = -self.Sbar[0, 1]/self.Sbar[1, 1]
#	**Coefficients of mutual influence 1st kind
            self.eta_xy_xx = self.Sbar[0, 2]/self.Sbar[2, 2]
            self.eta_xy_yy = self.Sbar[1, 2]/self.Sbar[2, 2]
#	**Coefficients of mutual influence 2nd kind
            self.eta_xx_xy = self.Sbar[0, 2]/self.Sbar[0, 0]
            self.eta_yy_xy = self.Sbar[1, 2]/self.Sbar[1, 1]
#************************************************************************
#	**Thermal Effects
#************************************************************************
            try:
                self.alpha_11, self.alpha_22
            except:
                pass
            else:
                self.alphas_xy = (self.Tinv)*(self.alpham)
                self.alphas_xy[2] = 2.0 * self.alphas_xy[2]
#************************************************************************
#	**Moisture Effects
#************************************************************************
            try:
                self.beta_11, self.beta_22
            except:
                pass
            else:
                self.betas_xy = (self.Tinv)*(self.betam)
                self.betas_xy[2] = 2.0 * self.betas_xy[2]
    
            self.updated = 1
        except:
            exit(errorString[1])

#************************************************************************
#	**Define a Laminate Class
#************************************************************************
class Laminate:
    """ Defines a Laminate Class.
        See pyPLY documentation for details.
    """
    def __init__(self):
        name = "Laminate_0_Class"
        no_materials = 0
        self.ply_list = []
        self.A = matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
        self.B = matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
        self.D = matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
        self.QU = []
        self.CTEs = []
        self.CMEs = []
        self.THK = 0.0
        self.ZStack = []
        self.ZStack.append(0.0)
        self.updated = 0

    def add_Lamina(self, lamina):
        self.ply_list.append(lamina)
        self.updated = 0

    def replace_Lamina(self, layer_no, lamina):
        del self.ply_list[layer_no]
        self.ply_list.insert(layer_no, lamina)
        self.updated = 0

    def remove_Lamina(self, layer_no):
        del self.ply_list[layer_no]
        self.updated = 0

    def update(self):
        global errorString
        self.A = matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
        self.B = matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
        self.D = matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
        self.QU = []
        self.CTEs = []
        self.CMEs = []
        self.THK = 0.0
        self.ZStack = []
        self.ZStack.append(0.0)

        for lamina in self.ply_list[:]:
            if (lamina.updated == 0):
               layer_no = self.ply_list.index(lamina)
               exit(errorString[5] % (layer_no + 1))

            (self.QU).append(lamina.Qbar)
            (self.CTEs).append(lamina.alphas_xy)
            (self.CMEs).append(lamina.betas_xy)
            self.THK = self.THK + lamina.thk
            (self.ZStack).append(self.THK)

#************************************************************************
#	**Resolve A, B, D Matrix
#************************************************************************
        noPly = len(self.ply_list)
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, noPly):
                    qtemp = self.QU[k]
                    self.A[i, j] = self.A[i, j] + (self.ZStack[k + 1] - self.ZStack [k]) * qtemp[i, j]
                    self.B[i, j] = self.B[i, j] + ((self.ZStack[k + 1] - (self.THK)/2) ** 2 - (self.ZStack[k] - (self.THK)/2) ** 2) * qtemp[i, j] / 2.0
                    self.D[i, j] = self.D[i, j] + ((self.ZStack[k + 1] - (self.THK)/2) ** 3 - (self.ZStack[k] - (self.THK)/2) ** 3) * qtemp[i, j] / 3.0
#************************************************************************
#	**Resolve Astar, Bstar, Cstar, Dstar Matrix
#************************************************************************
        self.Astar = (self.A).I
        self.Bstar = (-1)*(self.Astar)*(self.B)
        self.Cstar = (self.B)*(self.Astar)
        self.Dstar = (self.D)-(self.B)*(self.Astar)*(self.B)
#************************************************************************
#	**Resolve Aprim, Bprim, Cprim, Dprim Matrix
#	**Resolve a,     b,     c,     d Matrix
#************************************************************************
        self.d = (self.Dstar).I
        self.a = (self.Astar)-(self.Bstar)*(self.d)*(self.Cstar)
        self.b = (self.Bstar)*(self.d)
        self.c = (-1)*(self.d)*(self.Cstar)
#************************************************************************
#	**Resolve Egineering constants
#************************************************************************
        self.ABD = bmat([[self.A,self.B],[self.B,self.D]])
        self.abd = (self.ABD).I
        self.detABD = linalg.det(self.ABD)

        self.INPx = matrix([[self.A[1,1], self.A[1,2], self.B[0,1], self.B[1,1], self.B[1,2]],
                            [self.A[1,2], self.A[2,2], self.B[0,2], self.B[1,2], self.B[2,2]],
                            [self.B[0,1], self.B[0,2], self.D[0,0], self.D[0,1], self.D[0,2]],
                            [self.B[1,1], self.B[1,2], self.D[0,1], self.D[1,1], self.D[1,2]],
                            [self.B[1,2], self.B[2,2], self.D[0,2], self.D[1,2], self.D[2,2]]])
#
#	**"Extensional in-plane property, Ex, laminate effective Young's moduli in x-direction"
        self.Ex = self.detABD/(linalg.det(self.INPx) * self.THK)
#
        self.INPy = matrix([[self.A[0,0], self.A[0,2], self.B[0,0], self.B[0,1], self.B[0,2]],
                            [self.A[0,2], self.A[2,2], self.B[0,2], self.B[1,2], self.B[2,2]],
                            [self.B[0,0], self.B[0,2], self.D[0,0], self.D[0,1], self.D[0,2]],
                            [self.B[0,1], self.B[1,2], self.D[0,1], self.D[1,1], self.D[1,2]],
                            [self.B[0,2], self.B[2,2], self.D[0,2], self.D[1,2], self.D[2,2]]])
#
#	**"Extensional in-plane property, Ey, laminate effective Young's moduli in y-direction"
        self.Ey = self.detABD/(linalg.det(self.INPy) * self.THK)
#
        self.INPxy = matrix([[self.A[0,0], self.A[0,1], self.B[0,0], self.B[0,1], self.B[0,2]],
                             [self.A[0,1], self.A[1,1], self.B[0,1], self.B[1,1], self.B[1,2]],
                             [self.B[0,0], self.B[0,1], self.D[0,0], self.D[0,1], self.D[0,2]],
                             [self.B[0,1], self.B[1,1], self.D[0,1], self.D[1,1], self.D[1,2]],
                             [self.B[0,2], self.B[1,2], self.D[0,2], self.D[1,2], self.D[2,2]]])
#
#	**"Extensional in-plane properties, Gxy, laminate effective shear moduli"
        self.Gxy = self.detABD/(linalg.det(self.INPxy) * self.THK)
#
        self.SUPxy = matrix([[self.A[0,1], self.A[1,2], self.B[0,1], self.B[1,1], self.B[1,2]],
                             [self.A[0,2], self.A[2,2], self.B[0,2], self.B[1,2], self.B[2,2]],
                             [self.B[0,0], self.B[0,2], self.D[0,0], self.D[0,1], self.D[0,2]],
                             [self.B[0,1], self.B[1,2], self.D[0,1], self.D[1,1], self.D[1,2]],
                             [self.B[0,2], self.B[2,2], self.D[0,2], self.D[1,2], self.D[2,2]]])
#
        self.niuxy = - linalg.det(self.SUPxy)/linalg.det(self.INPx)
#
#	**"Flexural properties, Exxfl, laminate effective Young's moduli in flexure"
        self.Exxfl = 12.0/(self.d[0,0] * (self.THK) ** 3.0)
#	**"Flexural properties, Eyyfl, laminate effective Young's moduli in flexure"
        self.Eyyfl = 12.0/(self.d[1,1] * (self.THK) ** 3.0)
#	**"Flexural properties, NIUxyfl, laminate effective Young's moduli in flexure"
        self.niuxyfl = -self.d[0,1] / (self.d[0,0])
#	**"Flexural properties, NIUyxfl, laminate effective Young's moduli in flexure"
        self.niuyxfl = -self.d[0,1] / (self.d[1,1])

        self.updated = 1
#************************************************************************
#	**Define a Loading Class
#************************************************************************
class Loading():
    """ Defines a Loading Class.
        See pyPLY documentation for details.
    """
    def __init__(self):
        self.Nx = 0.0 ; self.Ny = 0.0 ; self.Nz = 0.0
        self.Mx = 0.0 ; self.My = 0.0 ; self.Mz = 0.0
        self.deltaT = 0.0 ; self.deltaM = 0.0
        self.load = matrix([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]])
        self.thermal_load = matrix([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]])
        self.moisture_load = matrix([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]])
        self.epsilon_K = matrix([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]])
        self.laminate_name = self
        self.loadType = 0
        self.define_Load = self.change_Load
        self.updated = 0

    def apply_To(self, laminate):
        global errorString
        self.list_ply_strains_xy = []
        self.list_ply_stresses_xy = []
        self.list_ply_strains_12 = []
        self.list_ply_stresses_12 = []

        self.laminate_name = laminate
        if (self.laminate_name.updated == 0):
            exit(errorString[6])

        noPly = len(laminate.ply_list)
        
        if (self.loadType == 0):
		    pass
        elif (self.loadType == 1):
            self.load = self.laminate_name.ABD * self.load
        else:
            exit(errorString[7])

#	**Thermal Load
        if (self.deltaT):
            for k in range(0, noPly):
                self.thermal_load[0:3] = self.thermal_load[0:3] + self.laminate_name.QU[k] * \
                                    self.deltaT * self.laminate_name.ply_list[k].alphas_xy * \
                                    (self.laminate_name.ZStack[k + 1] - self.laminate_name.ZStack[k])
                self.thermal_load[3:6] = self.thermal_load[3:6] + self.laminate_name.QU[k] * \
                                    (self.deltaT * 0.5) * self.laminate_name.ply_list[k].alphas_xy * \
                                    ((self.laminate_name.ZStack[k + 1] - self.laminate_name.THK / 2) ** 2 - \
                                    (self.laminate_name.ZStack[k] - self.laminate_name.THK / 2) ** 2)

            self.load = self.load + self.thermal_load
#	**Moisture Load
        if (self.deltaM):
            for k in range(0, noPly):
                self.moisture_load[0:3] = self.moisture_load[0:3] + self.laminate_name.QU[k] * \
                                    self.deltaM * self.laminate_name.ply_list[k].betas_xy * \
                                    (self.laminate_name.ZStack[k + 1] - self.laminate_name.ZStack[k])
                self.moisture_load[3:6] = self.moisture_load[3:6] + self.laminate_name.QU[k] * \
                                    (self.deltaM * 0.5) * self.laminate_name.ply_list[k].betas_xy * \
                                    ((self.laminate_name.ZStack[k + 1] - self.laminate_name.THK / 2) ** 2 - \
                                    (self.laminate_name.ZStack[k] - self.laminate_name.THK / 2) ** 2)

            self.load = self.load + self.moisture_load

#	**Midplane Strains and Curvatures
        self.epsilon_K = self.laminate_name.abd * self.load

        self.epsilon_xx = self.epsilon_K[0,0]
        self.epsilon_yy = self.epsilon_K[1,0]
        self.gamma_xy = self.epsilon_K[2,0]
        self.k_xx = self.epsilon_K[3,0]
        self.k_yy = self.epsilon_K[4,0]
        self.k_xy = self.epsilon_K[5,0]

#	**Laminate Ply Strains and Stresses, x-y coordinate system
#	**Laminate Ply Strains and Stresses, 1-2 coordinate system (ply coordinate)
        for k in range(0, noPly):
# **Strains and Stresses for the BOTTOM of the k ply.
            strain_ply = self.epsilon_K[0:3] + (-self.laminate_name.THK/2 +
                         self.laminate_name.ZStack[k]) * self.epsilon_K[3:6]
            strain_ply12 = laminate.ply_list[k].Teps * strain_ply
            self.list_ply_strains_xy.append(strain_ply)
            self.list_ply_strains_12.append(strain_ply12)

            stress_ply = self.laminate_name.QU[k] * (strain_ply - self.deltaT * self.laminate_name.ply_list[k].alphas_xy - \
                                                                  self.deltaM * self.laminate_name.ply_list[k].betas_xy)
            stress_ply12 = laminate.ply_list[k].T * stress_ply
            self.list_ply_stresses_xy.append(stress_ply)
            self.list_ply_stresses_12.append(stress_ply12)
# **Strains and Stresses for the CENTROID of the k ply.
            strain_ply = self.epsilon_K[0:3] + (-self.laminate_name.THK/2 +
                         self.laminate_name.ZStack[k] + (self.laminate_name.ZStack[k+1] - self.laminate_name.ZStack[k])/ 2.0) * \
                         self.epsilon_K[3:6]
            strain_ply12 = laminate.ply_list[k].Teps * strain_ply
            self.list_ply_strains_xy.append(strain_ply)
            self.list_ply_strains_12.append(strain_ply12)

            stress_ply = self.laminate_name.QU[k] * (strain_ply - self.deltaT * self.laminate_name.ply_list[k].alphas_xy - \
                                                                  self.deltaM * self.laminate_name.ply_list[k].betas_xy)
            stress_ply12 = laminate.ply_list[k].T * stress_ply
            self.list_ply_stresses_xy.append(stress_ply)
            self.list_ply_stresses_12.append(stress_ply12)

# **Strains and Stresses for the TOP of the k ply.
            strain_ply = self.epsilon_K[0:3] + (-self.laminate_name.THK/2 +
                             self.laminate_name.ZStack[k+1]) * self.epsilon_K[3:6]
            strain_ply12 = laminate.ply_list[k].Teps * strain_ply
            self.list_ply_strains_xy.append(strain_ply)
            self.list_ply_strains_12.append(strain_ply12)

            stress_ply = self.laminate_name.QU[k] * (strain_ply - self.deltaT * self.laminate_name.ply_list[k].alphas_xy - \
                                                                  self.deltaM * self.laminate_name.ply_list[k].betas_xy)
            stress_ply12 = laminate.ply_list[k].T * stress_ply
            self.list_ply_stresses_xy.append(stress_ply)
            self.list_ply_stresses_12.append(stress_ply12)

        self.updated = 1

    def change_Load(self, Nx, Ny, Nz, Mx, My, Mz, deltaT = 0.0, deltaM = 0.0, loadType = 0):
        global errorString
        self.load = matrix([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]])
        self.thermal_load = matrix([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]])
        self.moisture_load = matrix([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]])
        self.epsilon_K = matrix([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]])

        try:
            self.Nx = float(Nx) ; self.load[0] = float(Nx)
            self.Ny = float(Ny) ; self.load[1] = float(Ny)
            self.Nz = float(Nz) ; self.load[2] = float(Nz)
            self.Mx = float(Mx) ; self.load[3] = float(Mx)
            self.My = float(My) ; self.load[4] = float(My)
            self.Mz = float(Mz) ; self.load[5] = float(Mz)
        except:
            exit(errorString[4])

        if (deltaT):
            self.deltaT = deltaT
        else:
		    self.deltaT = 0.0

        if (deltaM):
            self.deltaM = deltaM
        else:
		    self.deltaM = 0.0

        if (loadType):
            self.loadType = loadType
        else:
		    self.loadType = 0

        self.updated = 0

#************************************************************************
#	**Define a Ply Failure Criterion Class
#************************************************************************

class PlyFailure:
    """ Defines a PlyFailure Class.
        See pyPLY documentation for details.
    """
    def __init__(self, default = None):
        self.Sigma_ut0 = 0.0
        self.Sigma_uc0 = 0.0
        self.Sigma_ut90 = 0.0
        self.Sigma_uc90 = 0.0
        self.Tau_u = 0.0

##########################
# Maximum Stress Criterion
##########################
    def MaxStressCrit(self, loading, plyNo):
# get strength data of each ply
        for i in CompositeMaterial.list_of_mat:
            if (i.mat_no == loading.laminate_name.ply_list[plyNo].mat_no) :
                self.Sigma_ut0 = i.Sigma_ut0
                self.Sigma_uc0 = i.Sigma_uc0
                self.Sigma_ut90 = i.Sigma_ut90
                self.Sigma_uc90 = i.Sigma_uc90
                self.Tau_u = i.Tau_u
                break
# get the resulting stresses from loading
        stresses_list_bottom = loading.list_ply_stresses_12[3*plyNo]
        stresses_list_centroid = loading.list_ply_stresses_12[3*plyNo+1]
        stresses_list_top = loading.list_ply_stresses_12[3*plyNo+2]

        sigma11_bottom = stresses_list_bottom[0,0]
        sigma22_bottom = stresses_list_bottom[1,0]
        tau12_bottom = stresses_list_bottom[2,0]

        sigma11_centroid = stresses_list_centroid[0,0]
        sigma22_centroid = stresses_list_centroid[1,0]
        tau12_centroid = stresses_list_centroid[2,0]

        sigma11_top = stresses_list_top[0,0]
        sigma22_top = stresses_list_top[1,0]
        tau12_top = stresses_list_top[2,0]

# Calculate
        self.ret_bottom = []
        if (sigma11_bottom < 0):
            self.ret_bottom.append(sigma11_bottom / self.Sigma_uc0)
        else:
		    self.ret_bottom.append(sigma11_bottom / self.Sigma_ut0)

        if (sigma22_bottom < 0):
            self.ret_bottom.append(sigma22_bottom / self.Sigma_uc90)
        else:
		    self.ret_bottom.append(sigma22_bottom / self.Sigma_ut90)

        self.ret_bottom.append(abs(tau12_bottom) / self.Tau_u)
#+++++++++++++++++++++
        self.ret_centroid = []
        if (sigma11_centroid < 0):
            self.ret_centroid.append(sigma11_centroid / self.Sigma_uc0)
        else:
		    self.ret_centroid.append(sigma11_centroid / self.Sigma_ut0)

        if (sigma22_centroid < 0):
            self.ret_centroid.append(sigma22_centroid / self.Sigma_uc90)
        else:
		    self.ret_centroid.append(sigma22_centroid / self.Sigma_ut90)

        self.ret_centroid.append(abs(tau12_centroid) / self.Tau_u)
#+++++++++++++++++++++
        self.ret_top = []
        if (sigma11_top < 0):
            self.ret_top.append(sigma11_top / self.Sigma_uc0)
        else:
		    self.ret_top.append(sigma11_top / self.Sigma_ut0)

        if (sigma22_top < 0):
            self.ret_top.append(sigma22_top / self.Sigma_uc90)
        else:
		    self.ret_top.append(sigma22_top / self.Sigma_ut90)

        self.ret_top.append(abs(tau12_top) / self.Tau_u)

# Return results (lamina failed if any of these results are bigger than 1.0 or smaller than -1.0)
        self.ret_list = [self.ret_bottom, self.ret_centroid, self.ret_top]

##########################
# Maximum Strain Criterion
##########################
    def MaxStrainCrit(self, loading, plyNo):
# get strength data of each ply
        for i in CompositeMaterial.list_of_mat:
            if (i.mat_no == loading.laminate_name.ply_list[plyNo].mat_no) :
                self.Sigma_ut0 = i.Sigma_ut0
                self.Sigma_uc0 = i.Sigma_uc0
                self.Sigma_ut90 = i.Sigma_ut90
                self.Sigma_uc90 = i.Sigma_uc90
                self.Tau_u = i.Tau_u
                self.E11 = i.E11
                self.E22 = i.E22
                self.G12 = i.G12
                self.niu12 = i.niu12
                break
# get the resulting strains from loading
        self.strains_list_bottom = loading.list_ply_strains_12[3*plyNo]
        self.strains_list_centroid = loading.list_ply_strains_12[3*plyNo+1]
        self.strains_list_top = loading.list_ply_strains_12[3*plyNo+2]

        self.epsilon11_bottom = self.strains_list_bottom[0,0]
        self.epsilon22_bottom = self.strains_list_bottom[1,0]
        self.gamma12_bottom = self.strains_list_bottom[2,0]

        self.epsilon11_centroid = self.strains_list_centroid[0,0]
        self.epsilon22_centroid = self.strains_list_centroid[1,0]
        self.gamma12_centroid = self.strains_list_centroid[2,0]

        self.epsilon11_top = self.strains_list_top[0,0]
        self.epsilon22_top = self.strains_list_top[1,0]
        self.gamma12_top = self.strains_list_top[2,0]

# Calculate
        self.ret_bottom = []
        if (self.epsilon11_bottom < 0):
		    Epsilon_uc0 = self.Sigma_uc0 / self.E11
		    self.ret_bottom.append(self.epsilon11_bottom / Epsilon_uc0)
        else:
		    Epsilon_ut0 = self.Sigma_ut0 / self.E11
		    self.ret_bottom.append(self.epsilon11_bottom / Epsilon_ut0)

        if (self.epsilon22_bottom < 0):
		    Epsilon_uc90 = self.Sigma_uc90 / self.E22
		    self.ret_bottom.append(self.epsilon22_bottom / Epsilon_uc90)
        else:
		    Epsilon_ut90 = self.Sigma_ut90 / self.E22
		    self.ret_bottom.append(self.epsilon22_bottom / Epsilon_ut90)

        Gamma_u = self.Tau_u / self.G12
        self.ret_bottom.append(abs(self.gamma12_bottom) / Gamma_u)
#+++++++++++++++++++++
        self.ret_centroid = []
        if (self.epsilon11_centroid < 0):
		    Epsilon_uc0 = self.Sigma_uc0 / self.E11
		    self.ret_centroid.append(self.epsilon11_centroid / Epsilon_uc0)
        else:
		    Epsilon_ut0 = self.Sigma_ut0 / self.E11
		    self.ret_centroid.append(self.epsilon11_centroid / Epsilon_ut0)

        if (self.epsilon22_centroid < 0):
		    Epsilon_uc90 = self.Sigma_uc90 / self.E22
		    self.ret_centroid.append(self.epsilon22_centroid / Epsilon_uc90)
        else:
		    Epsilon_ut90 = self.Sigma_ut90 / self.E22
		    self.ret_centroid.append(self.epsilon22_centroid / Epsilon_ut90)

        Gamma_u = self.Tau_u / self.G12
        self.ret_centroid.append(abs(self.gamma12_centroid) / Gamma_u)
#+++++++++++++++++++++
        self.ret_top = []
        if (self.epsilon11_top < 0):
		    Epsilon_uc0 = self.Sigma_uc0 / self.E11
		    self.ret_top.append(self.epsilon11_top / Epsilon_uc0)
        else:
		    Epsilon_ut0 = self.Sigma_ut0 / self.E11
		    self.ret_top.append(self.epsilon11_top / Epsilon_ut0)

        if (self.epsilon22_top < 0):
		    Epsilon_uc90 = self.Sigma_uc90 / self.E22
		    self.ret_top.append(self.epsilon22_top / Epsilon_uc90)
        else:
		    Epsilon_ut90 = self.Sigma_ut90 / self.E22
		    self.ret_top.append(self.epsilon22_top / Epsilon_ut90)

        Gamma_u = self.Tau_u / self.G12
        self.ret_top.append(abs(self.gamma12_top) / Gamma_u)

# Return results (lamina failed if any of these results are bigger than 1.0 or smaller than -1.0)
        self.ret_list = [self.ret_bottom, self.ret_centroid, self.ret_top]


##########################
# Azzi-Tsai-Hill Criterion
##########################
    def AzziTsaiHillCrit(self, loading, plyNo):
# get strength data of each ply
        for i in CompositeMaterial.list_of_mat:
            if (i.mat_no == loading.laminate_name.ply_list[plyNo].mat_no) :
                self.Sigma_ut0 = i.Sigma_ut0
                self.Sigma_uc0 = i.Sigma_uc0
                self.Sigma_ut90 = i.Sigma_ut90
                self.Sigma_uc90 = i.Sigma_uc90
                self.Tau_u = i.Tau_u
                break

# get resulting stresses from loading
        stresses_list_bottom = loading.list_ply_stresses_12[3*plyNo]
        stresses_list_centroid = loading.list_ply_stresses_12[3*plyNo+1]
        stresses_list_top = loading.list_ply_stresses_12[3*plyNo+2]

        sigma11_bottom = stresses_list_bottom[0,0]
        sigma22_bottom = stresses_list_bottom[1,0]
        tau12_bottom = stresses_list_bottom[2,0]

        sigma11_centroid = stresses_list_centroid[0,0]
        sigma22_centroid = stresses_list_centroid[1,0]
        tau12_centroid = stresses_list_centroid[2,0]

        sigma11_top = stresses_list_top[0,0]
        sigma22_top = stresses_list_top[1,0]
        tau12_top = stresses_list_top[2,0]

# Calculate
        self.ret_bottom = (sigma11_bottom/self.Sigma_ut0)**2 - \
                          (sigma11_bottom * sigma22_bottom/self.Sigma_ut0)**2 + \
                          (sigma22_bottom/self.Sigma_ut90)**2 + \
                          (tau12_bottom/self.Tau_u)**2

        self.ret_centroid = (sigma11_centroid/self.Sigma_ut0)**2 - \
                          (sigma11_centroid * sigma22_centroid/self.Sigma_ut0)**2 + \
                          (sigma22_centroid/self.Sigma_ut90)**2 + \
                          (tau12_centroid/self.Tau_u)**2

        self.ret_top = (sigma11_top/self.Sigma_ut0)**2 - \
                          (sigma11_top * sigma22_top/self.Sigma_ut0)**2 + \
                          (sigma22_top/self.Sigma_ut90)**2 + \
                          (tau12_top/self.Tau_u)**2

# Return results (lamina failed if any of these results are bigger than 1.0 or smaller than -1.0)
        self.ret_list = [self.ret_bottom, self.ret_centroid, self.ret_top]

###################
# Tsai-Wu Criterion
###################
    def TsaiWuCrit(self, loading, plyNo):
# get strength data of each ply
        for i in CompositeMaterial.list_of_mat:
            if (i.mat_no == loading.laminate_name.ply_list[plyNo].mat_no) :
                self.Sigma_ut0 = i.Sigma_ut0
                self.Sigma_uc0 = i.Sigma_uc0
                self.Sigma_ut90 = i.Sigma_ut90
                self.Sigma_uc90 = i.Sigma_uc90
                self.Tau_u = i.Tau_u
                break

# get resulting stresses from loading
        self.stresses_list_bottom = loading.list_ply_stresses_12[3*plyNo]
        self.stresses_list_centroid = loading.list_ply_stresses_12[3*plyNo+1]
        self.stresses_list_top = loading.list_ply_stresses_12[3*plyNo+2]

        self.sigma11_bottom = self.stresses_list_bottom[0,0]
        self.sigma22_bottom = self.stresses_list_bottom[1,0]
        self.tau12_bottom = self.stresses_list_bottom[2,0]

        self.sigma11_centroid = self.stresses_list_centroid[0,0]
        self.sigma22_centroid = self.stresses_list_centroid[1,0]
        self.tau12_centroid = self.stresses_list_centroid[2,0]

        self.sigma11_top = self.stresses_list_top[0,0]
        self.sigma22_top = self.stresses_list_top[1,0]
        self.tau12_top = self.stresses_list_top[2,0]

# Calculate the strength coefficients
        F1 = 1.0 / self.Sigma_ut0 - 1.0 / self.Sigma_uc0
        F11 = 1.0 / (self.Sigma_ut0 * self.Sigma_uc0)
        F2 = 1.0 / self.Sigma_ut90 - 1.0 / self.Sigma_uc90
        F22 = 1.0 / (self.Sigma_ut90 * self.Sigma_uc90)
        F66 = 1.0 / self.Tau_u ** 2
# In the absence of biaxial tests
        F12 = -0.5 * math.sqrt(F11 * F22)
#
        self.ret_bottom = F1 * self.sigma11_bottom + F2 * self.sigma22_bottom + \
						  F11 * self.sigma11_bottom ** 2 + F22 * self.sigma22_bottom ** 2 - \
						  F12 * self.sigma11_bottom * self.sigma22_bottom + \
						  F66 * self.tau12_bottom ** 2
# Failure strength ratio measured at the bottom of the ply
        Fa = F11 * self.sigma11_bottom ** 2 + F22 * self.sigma22_bottom ** 2 + \
             F66 * self.tau12_bottom ** 2 + F12 * self.sigma11_bottom * self.sigma22_bottom
        Fb = F1 * self.sigma11_bottom + F2 * self.sigma22_bottom  # + F66 * self.tau12_bottom ????
#        print Fa, Fb, F1, F11, F2, F22, F12, F66
        R1_bottom, R2_bottom = quadratic(Fa, Fb, -1)

        self.ret_centroid = F1 * self.sigma11_centroid + F2 * self.sigma22_centroid + \
						  F11 * self.sigma11_centroid ** 2 + F22 * self.sigma22_centroid ** 2 - \
						  F12 * self.sigma11_centroid * self.sigma22_centroid + \
						  F66 * self.tau12_centroid ** 2
# Failure strength ratio measured at the centroid of the ply
        Fa = F11 * self.sigma11_centroid ** 2 + F22 * self.sigma22_centroid ** 2 + \
             F66 * self.tau12_centroid ** 2 + F12 * self.sigma11_centroid * self.sigma22_centroid
        Fb = F1 * self.sigma11_centroid + F2 * self.sigma22_centroid  # + F66 * self.tau12_bottom ????
        R1_centroid, R2_centroid = quadratic(Fa, Fb, -1)

        self.ret_top = F1 * self.sigma11_top + F2 * self.sigma22_top + \
						  F11 * self.sigma11_top ** 2 + F22 * self.sigma22_top ** 2 - \
						  F12 * self.sigma11_top * self.sigma22_top + \
						  F66 * self.tau12_top ** 2
# Failure strength ratio measured at the top of the ply
        Fa = F11 * self.sigma11_top ** 2 + F22 * self.sigma22_top ** 2 + \
             F66 * self.tau12_top ** 2 + F12 * self.sigma11_top * self.sigma22_top
        Fb = F1 * self.sigma11_top + F2 * self.sigma22_top  # + F66 * self.tau12_bottom ????
        R1_top, R2_top = quadratic(Fa, Fb, -1)

# Return results (lamina failed if any of these results are bigger than 1.0 or smaller than -1.0)
        self.ret_list = [self.ret_bottom, R1_bottom, R2_bottom, \
					     self.ret_centroid, R1_centroid, R2_centroid, \
						 self.ret_top, R1_top, R2_top]

##########################
# Hashin Criterion
##########################
# TO BE IMPLEMENTED
    def Hashin(self, loading, plyNo, HashinAlpha):
        pass

#************************************************************************
#	**Define a Scenario Class
#************************************************************************
# TO BE IMPLEMENTED
class Scenario:
    """ Defines a Scenario Class.
        See pyPLY documentation for details.
    """
    name = "Scenario_0_Class"
    no_laminate = 0

    def add_Laminate(self):
        self.no_laminate += 1

