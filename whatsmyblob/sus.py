import mrcfile
import numpy as np
from itertools import product
from random import random


def sus(vol_file, samples=256, apix=1.5, replace=False):
    """ Simple stochastic universal sampling """

    # Load map
    with mrcfile.open(vol_file) as mrc:
        if not apix:
            apix = mrc.voxel_size
        volume = mrc.data

    # Generate coordinate list and flattened image
    sh, d = volume.shape, len(volume.shape)
    c = [b for b in product(*[range(-n//2, n//2) for n in sh])]

    im = volume.flatten()

    s = np.argsort(-im)    
    im,c = im[s]-im.min(), np.array(c)[s]

    # stochastic sampling loop
    samp_w = im.sum() / float(len(im))
    w_sofar = -random()*samp_w
    outsamp_id = -1

    o = []
    i = 0

    while len(o)<samples:
        s_dist = i*samp_w
        while (s_dist >= w_sofar) and (outsamp_id < len(im)):
            outsamp_id += 1
            w_sofar += im[outsamp_id]

        if replace:
            o.append(c[outsamp_id])
            i+=1

        else:
            c_out_id = list(c[outsamp_id])
            if not c_out_id in o:
                o.append(c_out_id)
            i+=1

    return np.array(o)*apix


def xyz_file(o, fname):
    # Produces an xyz file for a point cloud
    with open(fname, 'w') as f:
        f.write("{0}\n".format(len(o)))
        f.write("Point cloud with origin at 0,0,0\n")
        for l in o:
             f.write("C {0} {1} {2}\n".format(*l))


if __name__=="__main__":
    from time import time
    t0 = time()
    o = sus("7mdhA01.mrc")
    print(time()-t0)
    xyz_file(o, "7mdhA01_test.xyz")
