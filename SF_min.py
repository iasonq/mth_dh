# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###

import sys
import salome
import numpy as np

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'./')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS
import os
###Choose structural properties

h = 1918
RR = 68.3 #Helix Radius
r = 56.5 #Nanowire Radius
N = 6 
geompy = geomBuilder.New(theStudy)



O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

def make_new_path(radius, beta = 0.0, phi = 0.0):
    vertices = []
    for a in np.linspace(-np.pi, N*np.pi, 1000):
        x = radius*np.cos((1.- beta/(360.))*a + phi)
        y = radius*np.sin((1.- beta/(360.))*a + phi)
        z = h/(2.*np.pi)*a
        vertices.append(geompy.MakeVertex(x, y, z))
    lines = []
    Curve_1 = geompy.MakeInterpol(vertices, False, False)
    return Curve_1, np.array([x,y,z])


def make_DH(h, RR, r, beta, mlmax=9.6,N=3,  mlmin=8.4):
    #Create first Nw with phase phi = 0.0
    Circle_1, np_array = make_new_path(RR, beta) 
    Vertex_1 = geompy.MakeVertex(RR, 0, 0)
    Vector_1 = geompy.MakeVectorDXDYDZ(0, RR, (h/(2.*np.pi)))
    Disk_1 = geompy.MakeDiskPntVecR(Vertex_1, Vector_1, r)
    Pipe0_1 = geompy.MakePipe(Disk_1, Circle_1)
    #Create second NW with phase phi = pi
    Circle_2, np_array = make_new_path(RR, beta, phi = np.pi) 
    Vertex_2 = geompy.MakeVertex(-RR, 0, 0)
    Vector_2 = geompy.MakeVectorDXDYDZ(0, -1.*RR, (h/(2.*np.pi)))
    Disk_2 = geompy.MakeDiskPntVecR(Vertex_2, Vector_2, r)
    Pipe0_2 = geompy.MakePipe(Disk_2, Circle_2)

    Box_1 = geompy.MakeBoxDXDYDZ(500, 500, 2*1918)
    geompy.TranslateDXDYDZ(Box_1, -250, -250, 0)
    Pipe_1 = geompy.MakeCommonList([Pipe0_1, Box_1], True)
    Pipe_2 = geompy.MakeCommonList([Pipe0_2, Box_1], True)



    #Publish NWs in Salome
    geompy.addToStudy( Pipe_1, 'Pipe1')
    geompy.addToStudy( Pipe_2, 'Pipe2')
    volumes = [Pipe_1, Pipe_2]


    #Combine the NWs to a partition
    Partition_1 = geompy.MakePartitionNonSelfIntersectedShape(volumes, [], [], [], geompy.ShapeType["SOLID"], 0, [], 0, True)
    geompy.addToStudy( Partition_1, 'Part' )

    geompy.addToStudy( O, 'O' )
    geompy.addToStudy( OX, 'OX' )
    geompy.addToStudy( OY, 'OY' )
    geompy.addToStudy( OZ, 'OZ' )


    import  SMESH, SALOMEDS
    from salome.smesh import smeshBuilder


    smesh = smeshBuilder.New(theStudy)
    Mesh_1 = smesh.Mesh(Partition_1)
    NETGEN_1D_2D_3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
    NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
    NETGEN_3D_Parameters_1.SetMaxSize( mlmax )
    NETGEN_3D_Parameters_1.SetMinSize( mlmin )
    NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
    NETGEN_3D_Parameters_1.SetOptimize( 1 )
    NETGEN_3D_Parameters_1.SetFineness( 2 )
    NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 0 )
    NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
    NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )


    all_ids=geompy.SubShapeAllIDs(Partition_1, geompy.ShapeType["SOLID"])
    print("IDs of edges:",all_ids)
    groups_for_meshing=[]
    for i in range(len(all_ids)):
        vol1=geompy.CreateGroup(Partition_1, geompy.ShapeType["SOLID"])
        groups_for_meshing.append(vol1)
        geompy.UnionIDs(vol1, [all_ids[i]])
        geompy.addToStudyInFather( Partition_1, vol1, 'vol%d'%(i+1) )
        vol1_m = Mesh_1.GroupOnGeom(vol1,'vol%d'%(i+1),SMESH.VOLUME)
        smesh.SetName(vol1_m,'vol%d'%(i+1))


    #################################################################################
    #################################################################################


    smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
    smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
    smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')






    isDone = Mesh_1.Compute()
    smesh.SetName(Mesh_1, 'Mesh_Pitch_%g_Hradius_%g_NWradius_%g_beta_%g'% (h, RR, r, beta))
    try:
        Mesh_1.ExportMED( r'./Mesh_Pitch_%g_Hradius_%g_NWradius_%g_beta_%g.med'% (h, RR, r, beta), 0, SMESH.MED_MINOR_1, 1, None ,1)
        #os.system(r'gmsh -3 Mesh_Pitch_%g_Hradius_%g_NWradius_%g.med Mesh_Pitch_%g_Hradius_%g_NWradius_%g.msh '% (h, RR, r, h, RR, r))
        pass
    except:
        print('ExportToMEDX() failed. Invalid file name?')


make_DH(h, RR, r, 0)

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)


