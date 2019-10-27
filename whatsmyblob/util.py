# Copyright (C) 2018 Daniel Asarnow
# University of California, San Francisco
import json
import mrcfile
import os
import time
from django.conf import settings
from whatsmyblob import constants
from whatsmyblob import job_control
from whatsmyblob import sus
from whatsmyblob import neighbor_tree
from whatsmyblob import run_colores


def handle_upload_mrc(upload):
    with open(upload.map_file.path, 'wb+') as f:
        for c in upload.chunks():
            f.write(c)
    try:
        with mrcfile.open(upload.map_file.path, permissive=True) as f:
            pass
    except:
        return False
    return True


def run_search(job):
    query_map_file = job.query_map_file.map_file.path
    query_pc = sus.sus(query_map_file, samples=256)
    query_distmat = neighbor_tree.get_distmat(query_pc)
    query_inv_cdf = neighbor_tree.get_inv_cdf(query_distmat)
    tree = neighbor_tree.load_balltree(os.path.join(settings.MEDIA_ROOT, "nn_tree_1dgw.pkl"))
    ids = neighbor_tree.np.load(os.path.join(settings.MEDIA_ROOT, "nn_tree_1dgw_ids.npy"))
    hits, nn_scores = neighbor_tree.query_bt(query_inv_cdf, tree, ids, k=10)
    # tpc = neighbor_tree.two_point_correlation(query_inv_cdf)
    jobdir = job_control.create_tmp_dir(constants.TEMP_ROOT, job.id)
    json_file = os.path.join(jobdir, "result.json")
    t = time.time()
    cc_scores = run_colores.pool_colores(query_map_file, hits, jobdir)
    print("CoLoRes done in %d sec" % (time.time() - t))
    results = [{'CATH_domain': h, 'neighbor_score': nn, 'corr_coef': cc}
            for h, nn, cc in zip(hits, nn_scores, cc_scores)]
    # Return the output as a JSON file
    with open(json_file, "w") as handle:
        handle.write(json.dumps(results, indent=4))
    return True

