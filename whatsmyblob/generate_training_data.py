#! /usr/bin/env python3
# Copyright (C) 2018 Eugene Palovcak
# University of California, San Francisco
#
# Function to sample distance matrices from protein PDBs 
# given a large database of such proteins. 
#
# To train NN, we need anchor, positive, and negative examples
#
# Uses nearest-neighbor search and 1D wasserstein to find 
# harder negative examples
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import numpy as np
import h5py as h5
import os
import pickle
from glob import glob
from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist
from numpy.random import normal
from tqdm import tqdm
from prody import parsePDB
from prody import confProDy
# from . import neighbor_tree


def make_distmats(protein_structures="/storage/datasets/cath/dompdb/*", 
                  output_file='training_data.hdf'):
    """ Creates and HDF5 file with samples distance matrices and 1D CDFs 
        protein_structures: path to all domains to parse
    """


    dbank = h5.File(output_file, 'a')
    dist_mats = dbank.create_group('dist_mats')
    confProDy(verbosity='none')

    pdb_list = glob(protein_structures)

    for pdb_file in tqdm(pdb_list, desc="Dist-mats", total=len(pdb_list)):
        try:
            pdb = parsePDB(pdb_file).select('name CA CB')
            pdb_id = pdb_file.split("/")[-1]

            coords = pdb.getCoords()
            coords -= coords.mean(axis=0)

            dists = pdist(coords)
            dm = squareform(dists)
            dist_mats[pdb_id] = dm

        except:
            print(f"File {pdb} was not properly parsed...")
            pass


# def get_triplets(triplet_file="triplets_noise3.csv",
#                  id_file="nn_tree_1dgw_ids.npy",
#                  protein_structures="./dompdb/*",
#                  balltree_file="nn_tree_1dgw.pkl", noise=3):
#     """ Generate triplets for training """
#
#     # Load id file and ball tree
#     ids = np.load(id_file)
#     with open(balltree_file, "rb") as f:
#         tree = pickle.loads(f.read())
#
#     confProDy(verbosity='none')
#     pdb_list = glob(protein_structures)
#
#     with open(triplet_file, "w") as handle:
#         for pdb_file in tqdm(pdb_list, desc="Triplets", total=len(pdb_list)):
#             try:
#                 pdb = parsePDB(pdb_file).select('name CA CB')
#                 pdb_id = pdb_file.split("/")[-1]
#
#                 coords = pdb.getCoords()
#                 coords -= coords.mean(axis=0)
#
#                 coords += normal(scale=noise, size=coords.shape)
#
#                 dists = pdist(coords)
#                 dm = squareform(dists)
#
#                 shape_dist = neighbor_tree.get_inv_cdf(dm)
#                 nns = neighbor_tree.query_bt(shape_dist, tree, ids)
#
#                 for nn in nns[0]:
#                     if nn != pdb_id:
#                         triplet = f"{pdb_id},{pdb_id},{nn}\n"
#                         handle.write(triplet)
#
#             except:
#                 print(f"File {pdb} was not properly parsed...")
#                 pass

if __name__=="__main__":
    make_distmats()

