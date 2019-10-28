import os
import shutil
import subprocess
from multiprocessing import Pool
from django.conf import settings


def colores(query_file, hit_file, cwd, i=0, res=8):
    crdir = os.path.join(cwd, "colores_%d" % i)
    os.mkdir(crdir)
    cathdb = os.path.join(settings.MEDIA_ROOT, settings.CATHDB)
    hit_file = os.path.join(cathdb, hit_file)
    try:
        proc = subprocess.run(["colores", query_file, hit_file,
                             "-explor", "1", "-res", "%0.2f" % res],
                             cwd=crdir,
                             stdout=subprocess.PIPE)
        with open(os.path.join(cwd, "colores_%d.log" % i), 'w') as f:
            f.write(proc.stdout.decode("utf-8"))
        fit_pdb = os.path.join(cwd, os.path.basename(hit_file) + "_fit.pdb")
        best_pdb = os.path.join(crdir, "col_best_001.pdb")
        os.rename(best_pdb, fit_pdb)
        shutil.rmtree(crdir)
        with open(fit_pdb, "r") as f:
            for l in f:
                tok = l.strip().split()
                if len(tok) == 5 and tok[0] == "REMARK" and tok[1] == "Unnormalized":
                    cc_score = float(tok[-1])
                    break
    except IOError as e:
        print(e)
        return -1
    return cc_score


def pool_colores(query_file, hit_files, cwd, nproc=10):
    """ Run SITUS colores function on hits, renames output 
        fited PDB file and returns score """
    with Pool(processes=nproc) as pool:
        scores = pool.starmap(colores, ((query_file,h,cwd,i) for i, h in enumerate(hit_files)))
    return scores

