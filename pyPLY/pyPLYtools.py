#!/usr/bin/env python
#
# pyPLYTools v.0.01
#
# Copyright (c) 2012 Liviu Armeanu
#
# This file is part of pyPLY.
#
# pyPLYTools is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyPLYTools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyPLY; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# pyPLYTools methods
#

# History:
# 05.02.12 - pyPLYTools v.0.01
#

from __future__ import print_function

#############
# INPUT TOOLS
#############

# 1.Tools for reading data
# 1.1 plyDescr - function to define a ply arrangement using standard ply description
#     see manual for details
#     Warning - for the moment only one level of nesting is permited:
#               a laminate description string like "[0,90,-45,(+45,-45)2,0/]S" is OK.
#               a laminate description string like "[0,90,(+45,(0,90)2,-44)2,0/]S" is NOT OK.

def plyDescr(laminate, descrString, matNo):
    import pyPLY
    """
     1.Tools for reading data
     1.1 plyDescr - function to define a ply arrangement using standard ply description
         see manual for details
         Warning - for the moment only one level of nesting is permited:
                   a laminate description string like "[0,90,-45,(+45,-45)2,0/]S" is OK.
                   a laminate description string like "[0,90,(+45,(0,90)2,-44)2,0/]S" is NOT OK.
    """
    import re
    import sys

    #input string examples
    #descrString = "[0,90,-45,(+45,-45)2,0/]S"
    #descrString = "[0,90,+45,-45,0]S"
    regex = re.compile(r'^(\[)(\S+?)(\/?)(\][ST]$)')
    match = regex.search(descrString)

    lparen = None
    content = None
    mirror = None
    rparen = None

    if match:
       if (len(match.groups()) < 4):
           print("1.Unknown format...")
           sys.exit()

       lparen = match.group(1)
       content = match.group(2)
       mirror = match.group(3)
       rparen = match.group(4)
    else:
       print("2.Unknown format...")
       sys.exit()
# -------------------------------------------------------
    regex = re.compile(r'(\(\S+\)\d)', re.VERBOSE)
    match = regex.search(content)
# -------------------------------------------------------
    def check(content):
        temp = ''
        angleList = re.split(r'(\(\S+?\)\d)', content)
        for i in angleList:
            regex = re.compile(r'(\()(\S+)(\))(\d)', re.VERBOSE)
            match = regex.search(i)
            if match:
                partialContent = match.group(2)
                no = int(match.group(4))
                for j in range(no-1):
                  partialContent = partialContent + "," + partialContent

                match = None
                i = partialContent
            temp = temp + i
        content = temp
        regex = re.compile(r'(\(\S+\)\d)', re.VERBOSE)
        match = regex.search(content)
        if match:
           check(content)
        return temp

# -------------------------------------------------------
    if match:
       contentstring = check(content)
    else:
       contentstring = content

    angleList = contentstring.split(',')
    if (rparen == ']S'):
        if mirror:
            angleList1 = angleList[::-1]
            angleList.extend(angleList1[1:])
        else:
            angleList1 = angleList[::-1]
            angleList.extend(angleList1)

    noPly = len(angleList)

    for i in angleList:
        layer = pyPLY.Lamina()
        layer.define('', matNo, float(i))
        layer.update()
        laminate.add_Lamina(layer)

###############
# OUTPUT TOOLS
###############

# 1.Tools for outputing data
# 1.1 get_angle_list
#     see manual for details

def get_angle_list(laminate):
    """
     1.Tools for outputing data
     1.1 get_angle_list - function which return a list of lamina angles.
         see manual for details
    """
    plyList = laminate.ply_list
    angleList = []
    for i in plyList:
        angleList.append(i.angle)
    return angleList

###############
# PLOTING TOOLS
###############

# 1.Tools for ploting results using mathplotlib
# 1.1 mplotTThk - function to plot stresses/strains trough thickness
#     see manual for details

def mplotTThk(loadingCase, sors, ax):
    """
     1.Tools for ploting results using mathplotlib
     1.1 mplotTThk - function to plot stresses/strains trough thickness
         see manual for details
    """
    import sys
    import matplotlib.pyplot as plt


    lamName = loadingCase.laminate_name
    stackThk = lamName.ZStack
    x = []; y = []; temp = []
    for i in stackThk:
        temp.append (i), temp.append (i)

    y = temp[1:len(temp)-1]
    print(y)
    for i in range (0, 4):
        if (sors == "stress"):
            if (ax == "xy"):
                stress = loadingCase.list_ply_stresses_xy[i*3 + 0]
                x.append(stress[0,0])
                stress = loadingCase.list_ply_stresses_xy[i*3 + 2]
                x.append(stress[0,0])
            elif (ax == "12"):
                stress = loadingCase.list_ply_stresses_12[i*3 + 0]
                x.append(stress[0,0])
                stress = loadingCase.list_ply_stresses_12[i*3 + 2]
                x.append(stress[0,0])
            else:
                from sys import exit
                print("Unknown parameter. Exit now...")
                sys.exit()
        elif (sors == "strain"):
            if (ax == "xy"):
                stress = loadingCase.list_ply_strains_xy[i*3 + 0]
                x.append(stress[0,0])
                stress = loadingCase.list_ply_strains_xy[i*3 + 2]
                x.append(stress[0,0])
            elif (ax == "12"):
                stress = loadingCase.list_ply_strains_12[i*3 + 0]
                x.append(stress[0,0])
                stress = loadingCase.list_ply_strains_12[i*3 + 2]
                x.append(stress[0,0])
            else:
                print("Unknown parameter. Exit now...")
                sys.exit()
        else:
                print("Unknown parameter. Exit now...")
                sys.exit()

    print(x)
    plt.plot(x,y)
    plt.axvline(x = 0, linestyle = '-')
    for i in stackThk:
        plt.axhline(y = i, linestyle = '--')

    plt.xlabel(r'Normal stress $\sigma_{11}$')
    plt.ylabel('Through thickness position, z')
    plt.title(r'Through thickness plot')

    plt.show()

###############
# REPORT TOOLS
###############

# 1.Tools for ploting results using mathplotlib
# 1.1 mplotTThk - function to plot stresses/strains trough thickness
#     see manual for details

#************************************************************************
#	**Define a Report Class
#************************************************************************
class Report:
    """ Defines a Report Class.
        See pyPLY documentation for details.
    """

    def __init__(self, title = None):

        self.texDocument = ''
        if (not title): title = "Report_0"

        no_laminate = 0
        self.documentclass = '\\documentclass[10pt]{article}\n'
        self.texDocument = self.texDocument + self.documentclass

    def use_Package(self, package):
        self.package = package
        self.texDocument = self.texDocument + '\\usepackage{' + package + '}\n'

    def start_Document(self):
        self.texDocument = self.texDocument + '\\begin{document}\n'

    def add_Header(self):
        pass

    def add_Text(self, text):
        self.texDocument = self.texDocument + text

    def add_Footer(self):
        pass

    def add_Matrix(self, matrix, formatMask=None):
        """
        Generates and returns the LaTeX code for
        a matrix.
        """
        if not formatMask: formatMask = ''
        from numpy import shape
        i, j = shape(matrix)
        text = ''.join([
            r'\left[',
            r'\begin{array}{%s}' % (j*'c',), '\n\t',
            '\\\\\n\t'.join(' & '.join(format(matrix[i,j], formatMask) for j in range(j))
                            for i in range(j)), '\n\t',
            r'\end{array}',
            r'\right]',
        ])
        return Report.add_Text(self, '$' + text + '$')

    def close_Document(self):
        self.texDocument = self.texDocument + '\n\\end{document}\n'

    def view(self):
        pass

    def writeto_TexFile(self, filename):
        f = open(filename,'w')
        f.write(self.texDocument)

    def writeto_PDFFile(self, filename):
        f = open(filename + '.tex','w')
        f.write(self.texDocument)
        f.close()

        import subprocess
        import shlex
        import os
        proc=subprocess.Popen(shlex.split('pdflatex -interaction=nonstopmode ' + filename + '.tex'))
        proc.communicate()
        #Remove unneeded files:

        os.remove(filename + '.log')
        os.remove(filename + '.aux')

###############
# Miscelaneous TOOLS
###############

# 1.return a text in Latex code (used in IPython)
#************************************************************************
#	**return a Matrix code in LATEX code
#************************************************************************
def LXMatrix(matrix, formatMask, ipython=True):
    """
    Generates and returns the LaTeX code for
    a matrix.
    """
    if not formatMask: formatMask = ''
    from numpy import shape
    i, j = shape(matrix)
    text = ''.join([
            r'\left[',
            r'\begin{array}{%s}' % (j*'c',), '\n\t',
            '\\\\\n\t'.join(' & '.join(format(matrix[i,j], formatMask) for j in range(j))
                            for i in range(i)), '\n\t',
            r'\end{array}',
            r'\right]',
        ])
    return text