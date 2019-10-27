import numpy as np
import pickle
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from sklearn.neighbors import BallTree


def get_distmat(coords):
    """ Computes square distance matrix given Nx3 coordinates """
    dists = pdist(coords)
    dm  = squareform(dists)
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


def query_bt(query, bt, ids, k=10):
    """ Query is a 64 element vector """
    q = query.reshape(1,-1)
    dists,inds = bt.query(q, k=k)
    return [(ids[ind],dis) for ind,dis in zip(inds[0],dists[0])]

