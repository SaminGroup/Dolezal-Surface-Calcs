## Dolezal Slab Generator

Welcome! Here you'll find our slab generating tool, slab-generator.py

Make sure to pull both slab-generator.py and the structures/ directory. To initialize, execute slab-generator.py and follow the prompts, 

"python3 slab-generator.py"

 |--------------------------- Welcome ---------------------------|
 
 | Here is a list of supported surfaces, crystal lattices, and   |
 
 | atom/unit cell                                                |
 
 |---------------------------------------------------------------|
 
 | Lat.  | 1 0 0 | 0 1 0 | 0 0 1 | 1 1 0 | 1 0 1 | 0 1 1 | 1 1 1 |
 
 |---------------------------------------------------------------|
 
 |  sc   |   1   |   1   |   1   |   2   |   2   |   2   |   6   |
 
 | bcc   |   2   |   2   |   2   |   4   |   4   |   4   |   12  |
 
 | fcc   |   4   |   4   |   4   |   8   |   8   |   8   |   24  |
 
 | hcp   |   4   |   4   |   4   |   8   |   8   |   8   |   24  |
 
 |---------------------------------------------------------------|
 
 ----------------------------- inputs ----------------------------
 
 *if bulk is not supercell provide: 1 1 1
 
 1. choose a face: 110
 2. lattice geometry of bulk: bcc
 3. if bulk structure is a supercell
    provide the supercell dimensions* (x y z): 4 4 4
 4. surface slab dimensions (x y z): 3 3 2
 5. vacuum thickness: 20
 ---------------------- procedure initiating ----------------------
 1. bulk dimensions applied
 2. slab supercell generated
 3. vacuum layer of 20 A added
 4. updating atomic data
 5. bcc 110 surface slab of dims (3, 3, 2) completed
 ---------------------- procedure complete ------------------------
 ---------------------- please see POSCAR1 ------------------------
