import numpy as np
import pickle
from h5py import File
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from sklearn.neighbors import BallTree
from tqdm import tqdm


def make_1GW(input_file="training_data.hdf", samples=64):
    """ Reads an HDF file with distance matrices and computes 1D GWs """

    # Load distance matrices
    dbank = File(input_file, "a")
    dist_mats = dbank['dist_mats']
    pdb_list = [key for key in dist_mats.keys()]

    # Create 1D GW distances
    output_file = input_file.split(".")[0] + "_GW.pkl"
    shape_dists = {}

    for pdb in tqdm(pdb_list, desc="Shape-dists", total=len(pdb_list)):
        try:
            dist_mat = dist_mats[pdb]
            shape_dist = get_inv_cdf(dist_mat, samples)
            shape_dists[pdb] = shape_dist

        except:
            print(f'{pdb} is corrupt or already has a shape distribution...')
            pass

    return shape_dists


def make_GW_tree(shape_dists, treename="nn_tree_1dgw.pkl"):
    """ Make tree for nearest neighbors """

    # Get PDB ids and save the array
    ids = np.array([pdb for pdb in shape_dists.keys()])
    id_file = treename.split(".")[0] + "_ids.npy"
    np.save(id_file, ids)

    # Construct and save the tree
    shape_dists_array = np.array([shape_dists[pdb] for pdb in ids])
    tree = BallTree(shape_dists_array)

    # Test
    n = 20
    query = shape_dists[ids[n]]
    print(ids[n], query_bt(query, tree, ids))

    # Dump the pickle
    tree_pickle = pickle.dumps(tree)
    with open(treename, "wb") as handle:
         handle.write(tree_pickle)


def get_distmat(coords):
    """ Computes square distance matrix given Nx3 coordinates """
    dists = pdist(coords)
    dm = squareform(dists)
    return dm


def get_inv_cdf(dist_mat, samples=64):
    """ Computes the inverse cumulative distance distribution for 1D GW """
    dist_mat = np.array(dist_mat)
    dists = dist_mat[np.triu_indices_from(dist_mat)] 
    
    samples = np.linspace(0,1,samples)
    order = np.linspace(0,1,len(dists))
    
    return np.interp(samples, order, np.sort(dists))


def load_balltree(treename):
    with open(treename, "rb") as handle: 
        bt = pickle.loads(handle.read())
    return bt


def query_bt(query, bt, ind2id, k=10):
    """ Query is a 64 element vector """
    q = query.reshape(1,-1)
    dists,inds = bt.query(q, k=k)
    ids = [ind2id[ind] for ind in inds[0]]
    # return [(ids[ind],dis) for ind,dis in zip(inds[0],dists[0])]
    return ids, dists[0]


if __name__ == "__main__":
    shape_dists = make_1GW(samples=64)
    GW_tree = make_GW_tree(shape_dists)
