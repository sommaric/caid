# -*- coding: UTF-8 -*-
#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="root"
__date__ ="$Dec 22, 2011 9:42:24 AM$"
__all__ ="boundary_conditions"

def indices_face(nrb, ai_face, shift):
    li_dim = nrb.dim
    if li_dim == 1:
        return _indices_face_1D(nrb, ai_face, shift)
    if li_dim == 2:
        return _indices_face_2D(nrb, ai_face, shift)
    if li_dim == 3:
        return _indices_face_3D(nrb, ai_face, shift)

def _indices_face_1D(nrb, ai_face, shift):
    """
    this routine return the list of indices that are on the face n ai_face
    """
    list_n = nrb.shape

    list_ind = []

    # face n : 1
    if ai_face == 0:
        li_i = 0 + shift
        list_ind.append([li_i])
        return list_ind

    # face n : 2
    if ai_face == 1:
        li_i = list_n[0] - 1 + shift
        list_ind.append([li_i])
        return list_ind

    print("Error _indices_face_1D: you gave a wrong face id. Given face ", ai_face)

    import sys
    sys.exit(1)

def _indices_face_2D(nrb, ai_face, shift):
    """
    this routine return the list of indices that are on the face n ai_face
    """
    list_n = nrb.shape

    list_ind = []

    # face n : 1
    if ai_face == 0:
        for li_i in range (0, list_n[0]):
            li_j = 0 + shift
            list_ind.append([li_i,li_j])
        return list_ind

    # face n : 3
    if ai_face == 2:
        for li_i in range (0, list_n[0]):
            li_j = list_n[1] - 1 + shift
            list_ind.append([li_i,li_j])
        return list_ind

    # face n : 2
    if ai_face == 1:
        for li_j in range (0, list_n[1]):
            li_i = 0 + shift
            list_ind.append([li_i,li_j])
        return list_ind

    # face n : 4
    if ai_face == 3:
        for li_j in range (0, list_n[1]):
            li_i = list_n[0] - 1 + shift
            list_ind.append([li_i,li_j])
        return list_ind

    print("Error _indices_face_2D: you gave a wrong face id. Given face ", ai_face)
    import sys
    sys.exit(1)

def _indices_face_3D(nrb, ai_face, shift):
    """
    this routine return the list of indices that are on the face n ai_face
    """
    list_n = nrb.shape

    list_ind = []

    # face n : 1
    if ai_face == 0:
        for li_k in range (0, list_n[2]):
            for li_j in range (0, list_n[1]):
                li_i = 0 + shift
                list_ind.append([li_i,li_j,li_k])
        return list_ind

    # face n : 4
    if ai_face == 3:
        for li_k in range (0, list_n[2]):
            for li_j in range (0, list_n[1]):
                li_i = list_n[0] - 1 + shift
                list_ind.append([li_i,li_j,li_k])
        return list_ind

    # face n : 2
    if ai_face == 1:
        for li_j in range (0, list_n[1]):
            for li_i in range (0, list_n[0]):
                li_k = 0 + shift
                list_ind.append([li_i,li_j,li_k])
        return list_ind

    # face n : 5
    if ai_face == 4:
        for li_j in range (0, list_n[1]):
            for li_i in range (0, list_n[0]):
                li_k = list_n[2] - 1 + shift
                list_ind.append([li_i,li_j,li_k])
        return list_ind

    # face n : 3
    if ai_face == 2:
        for li_i in range (0, list_n[0]):
            for li_k in range (0, list_n[2]):
                li_j = 0 + shift
                list_ind.append([li_i,li_j,li_k])
        return list_ind

    # face n : 6
    if ai_face == 5:
        for li_i in range (0, list_n[0]):
            for li_k in range (0, list_n[2]):
                li_j = list_n[1] - 1 + shift
                list_ind.append([li_i,li_j,li_k])
        return list_ind

    print("Error : you gave a wrong face id")
    import sys
    sys.exit(1)

class boundary_conditions(object):
    def __init__(self, geometry \
                 , list_Dirichlet_ind = [], list_Neumann_ind = [] \
                 , list_Periodic_ind = [], list_duplicated_ind = [] \
                 , list_duplicata_ind = [] \
                , isPeriodic=None):
        self._geo                   = geometry
        self.DirFaces               = [[]]*geometry.npatchs
        self.DuplicatedFaces        = []
        self.DuplicataFaces         = []
        self.list_Dirichlet_ind     = list_Dirichlet_ind
        self.list_Neumann_ind       = list_Neumann_ind
        self.list_Periodic_ind      = list_Periodic_ind
        self.list_duplicated_ind    = list_duplicated_ind
        self.list_duplicata_ind     = list_duplicata_ind
        # initialization with respect to the number of patchs
        li_npatch = geometry.npatchs
        list_empty = [[]] * li_npatch
        self.dirichlet(geometry, list_empty)

        self._isPeriodic = isPeriodic
        self.duplicate(geometry)

    @property
    def geometry(self):
        return self._geo

    @property
    def dim(self):
        return self._geo.dim

    def all_dirichlet_1d(self, list_interior_ind=[[]]):
        """
        bc = 10 with the old version of PyIGA
        we must exlude interior boundaries between 2 (or more) patchs,
        this is given in list_interior_ind
        """
        geometry = self.geometry
        dim = self.dim

        self.list_Dirichlet_ind = []

        # computing the number of patchs
        li_npatch = geometry.npatchs

        for li_id in range(0, li_npatch):
            lo_domain = geometry[li_id]

            list_n = lo_domain.shape

            list_Dirichlet_ind = []

            li_i = 0
            if [li_i] not in list_interior_ind :
                list_Dirichlet_ind.append([li_i])

            li_i = list_n[0] - 1
            if [li_i] not in list_interior_ind :
                list_Dirichlet_ind.append([li_i])

            self.list_Dirichlet_ind.append(list_Dirichlet_ind)

    def all_dirichlet_2d(self, list_interior_ind=[[]]):
        """
        bc = 10 with the old version of PyIGA
        we must exlude interior boundaries between 2 (or more) patchs,
        this is given in list_interior_ind
        """
        geometry = self.geometry
        dim = self.dim

        self.list_Dirichlet_ind = []

        # computing the number of patchs
        li_npatch = geometry.npatchs

        for li_id in range(0, li_npatch):
            lo_domain = geometry[li_id]

            list_n = lo_domain.shape

            list_Dirichlet_ind = []

            for li_i in range (0, list_n[0]):
                li_j = 0
                if [li_i,li_j] not in list_interior_ind :
                    list_Dirichlet_ind.append([li_i,li_j])

                li_j = list_n[1] - 1
                if [li_i,li_j] not in list_interior_ind :
                    list_Dirichlet_ind.append([li_i,li_j])

            for li_j in range (0, list_n[1]):
                li_i = 0
                if [li_i,li_j] not in list_interior_ind :
                    list_Dirichlet_ind.append([li_i,li_j])

                li_i = list_n[0] - 1
                if [li_i,li_j] not in list_interior_ind :
                    list_Dirichlet_ind.append([li_i,li_j])

            self.list_Dirichlet_ind.append(list_Dirichlet_ind)

            print("list_Dirichlet_ind=", list_Dirichlet_ind)

    def all_dirichlet_3d(self, list_interior_ind=[[]]):
        """
        bc = 10 with the old version of PyIGA
        we must exlude interior boundaries between 2 (or more) patchs,
        this is given in list_interior_ind
        """
        geometry = self.geometry
        dim = self.dim
        self.list_Dirichlet_ind = []

        # computing the number of patchs
        li_npatch = geometry.npatchs

        for li_id in range(0, li_npatch):
            lo_domain = geometry[li_id]

            list_n = lo_domain.shape

            list_Dirichlet_ind = []

            for li_k in range (0, list_n[2]):
                for li_j in range (0, list_n[1]):
                    li_i = 0
                    if [li_i,li_j,li_k] not in list_interior_ind :
                        list_Dirichlet_ind.append([li_i,li_j,li_k])

                    li_i = list_n[0] - 1
                    if [li_i,li_j,li_k] not in list_interior_ind :
                        list_Dirichlet_ind.append([li_i,li_j,li_k])

            for li_j in range (0, list_n[1]):
                for li_i in range (0, list_n[0]):
                    li_k = 0
                    if [li_i,li_j,li_k] not in list_interior_ind :
                        list_Dirichlet_ind.append([li_i,li_j,li_k])

                    li_k = list_n[2] - 1
                    if [li_i,li_j,li_k] not in list_interior_ind :
                        list_Dirichlet_ind.append([li_i,li_j,li_k])

            for li_i in range (0, list_n[0]):
                for li_k in range (0, list_n[2]):
                    li_j = 0
                    if [li_i,li_j,li_k] not in list_interior_ind :
                        list_Dirichlet_ind.append([li_i,li_j,li_k])

                    li_j = list_n[1] - 1
                    if [li_i,li_j,li_k] not in list_interior_ind :
                        list_Dirichlet_ind.append([li_i,li_j,li_k])

            self.list_Dirichlet_ind.append(list_Dirichlet_ind)

    def all_dirichlet(self, list_interior_ind=[[]]):
        geometry = self.geometry
        dim      = self.dim
        if dim == 1:
            self.all_dirichlet_1d(geometry, list_interior_ind=[[]])
        if dim == 2:
            self.all_dirichlet_2d(geometry, list_interior_ind=[[]])
        if dim == 3:
            self.all_dirichlet_3d(geometry, list_interior_ind=[[]])

    def dirichlet(self, geometry, faces):
        """
        we must exlude interior boundaries between 2 (or more) patchs,
        this is given in list_interior_ind
        for each patch we must give the list of the correspondant faces
        on which we would like to put the boundary condition
        """
        self.DirFaces = faces

        self.list_Dirichlet_ind = []

        # computing the number of patchs
        li_npatch = geometry.npatchs

        for li_id in range(0, li_npatch):
            nrb = geometry[li_id]
            list_faces = faces[li_id]
            list_Dirichlet_ind = []
            list_shift = [0] * len(list_faces)

            for (F, Sh) in zip(list_faces, list_shift):
                list_indices = indices_face(nrb, F, Sh)
                for Ind in list_indices:
                    list_Dirichlet_ind.append(Ind)

            self.list_Dirichlet_ind.append(list_Dirichlet_ind)

    def duplicate(self, geometry):
        """
        this routine is used to duplicate the basis fct
        faces_base and faces, must be of the form : list of [patch_id, face_id, shift]
        """
        # ...
        list_DuplicatedFaces            = []
        list_DuplicataFaces             = []
        list_DuplicatedFacesPeriodic    = []

        list_connectivity = self.geometry.connectivity

        for dict_con in list_connectivity:
            list_DuplicatedFaces.append(dict_con['original'])
            list_DuplicataFaces.append(dict_con['clone'])
            try:
                list_DuplicatedFacesPeriodic.append(dict_con['periodic'])
            except:
                list_DuplicatedFacesPeriodic.append(False)
        # ...

        faces_base = list_DuplicatedFaces
        faces      = list_DuplicataFaces
        isPeriodic = list_DuplicatedFacesPeriodic

        if faces_base is None:
            li_npatch = geometry.npatchs
            self.list_duplicated_ind = [[]] * li_npatch
            self.list_duplicata_ind  = [[]] * li_npatch
            return
        else:
            self.DuplicatedFaces = faces_base
            self.DuplicataFaces = faces

        # verifier que l'indice de face_base est < a celui de face
        for (pf_base, pf) in zip(faces_base, faces):
            pbase_id = pf_base[0] ; fbase_id = pf_base[1]
            p_id = pf[0] ; f_id = pf[1]
            if ( pbase_id == p_id ) and (fbase_id > f_id) :
                print("Error indices for faces: fbase_id must be smaller than or equal to f_id")
                import sys; sys.exit(0)

        self.list_duplicated_ind = []
        self.list_duplicata_ind  = []
        for (pf_base, pf) in zip(faces_base, faces):
#            print "pf_base =", pf_base, "       pf =", pf
            pbase_id = pf_base[0] ; fbase_id = pf_base[1]
            p_id = pf[0] ; f_id = pf[1]
            # if shift has been given
            if len(pf) == 2:
                shbase = 0
                sh = 0
            else:
                shbase = pf_base[2]
                sh = pf[2]

            # getting domains
            nrb_base = geometry[pbase_id]
            nrb       = geometry[p_id]

            list_ind_base = indices_face(nrb_base, fbase_id,shbase)
            list_indices  = indices_face(nrb, f_id,sh)
            for (Ind_base, Ind) in zip(list_ind_base, list_indices):
#                print "Ind_base = ", Ind_base, "     Ind = ", Ind
                list_Indbase = [pbase_id]
                for I in Ind_base:
                    list_Indbase.append(I)
                list_Ind = [p_id]
                for I in Ind:
                    list_Ind.append(I)
                self.list_duplicated_ind.append(list_Indbase)
                self.list_duplicata_ind.append(list_Ind)
#        print "self.list_duplicated_ind=", self.list_duplicated_ind
#        print "self.list_duplicata_ind=", self.list_duplicata_ind
