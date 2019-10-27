# whatsmyblob
<img src="/docs/transparent_blob_logo.png" alt="logo" title="Whats my blob logo" height="150" />
A Search engine for unknown cryo-EM densities

## General description
What's my blob (wmb) is a online platform that searches a database of
biomolecular structures using a density map as a query and provides
a list of potential candidate structures with corresponding quality
parameters.

![Whats my blob?][2]

The resolution of many density maps of biomolecular structures is 
insufficient for de novo reconstructions of structures. However, 
for many purposes, the protein databank (PDB) provides sufficient
structural knowledge to identify biomolecular folds using experimentally 
measured low-resolution densities.

What's my blob identifies for given low-resolution densities potential
protein folds by searching a set of CATH domains for corresponding
structures using an efficient ‘Fuzzy correspondence’ search algorithm
that provides retrieval of hits in the millisecond range. 


[2]: docs/graphical_abstract.png "What's my blob graphical abstract"
