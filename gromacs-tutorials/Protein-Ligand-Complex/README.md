# GROMACS Tutorial : Protein-Ligand Complex

## What it is ?

-  This is a tutorial to simulate a protein-ligand system using molecular dynamics with 
   Gromacs.

-  Reference to the original tutorial is given below.

## Why this tutorial is written ?

- I have noticed that the original tutorial is too length and that makes hard to read 
  each and every detail and so does not help much.

- The original tutorial also misses many important steps in between and so the chains of
  steps to reach the last step is broken.

## What I am giving here ?

 * A set of scripts 

 * Explanations

 * Reference 



## Contact :
   
   Jayanti Prasad Ph.D (prasad.jayanti@gmail.com)

## Reference 

# Tutorial 

## Requirements :

  * Python 3.0 

  * [GROMACS version: 2020.2-UNCHECKED](http://manual.gromacs.org/)

  * [UCSF ChimeraX version 1.0 (2020-05-29)](http://www.rbvi.ucsf.edu/chimerax)

  * [AVAGADRO](http://manual.gromacs.org/)

  * [NETWORKX (1.11)](https://networkx.github.io/documentation/stable/)
  

## Getting the data :

  -  Step 1: Download the data (.pdb) file from [here](https://www.rcsb.org/structure/3HTB)

  -  Step 2: Now we will extract chain A (lysozyme) and a ligand (JZ4) from the combined pdb 
     file with the following commands. Note that you can confirm the structure and content 
     of the pdb file by loading it into [ChiemaraX)(https://www.rbvi.ucsf.edu/chimerax/)

  -  Extracting the chain A :

    `pdb_selchain -A data/3htb.pdb  | pdb_delhetatm | pdb_tidy > 3HTB_clean.pdb` 

  - Extracting the ligand JZ4 :

    `grep JZ4 data/3htb.pdb  > jz4.pdb` 
      
    Please check the path of your downloaded file (I am having it in 'data' folder). In fact 
    you do not need it to download and you can just use what I have. 

    <figure>
    <img src="images/raw.png" height="50%" width="50%">
    <figcaption> Raw image </figcaption>
    </figure>

    <figure>
    <img src="images/lysozyme.png" height="50%" width="50%">
    <figcaption> Protein Chain A (Lysozyme) </figcaption>
    </figure>

    <figure>
    <img src="images/jz4.png" height="50%" width="50%">
    <figcaption> Ligand JZ4 </figcaption>
    </figure>

## Preparing the scripts 

    Now we have two pdb files, one for the protein and another for the ligand. In order to
    carry out molecular dynamics simulations we need at least the following three files:

    - Protein + ligand in a single file (pdb or gmx format)

    - A topology file which has topology of both the protein and ligand. 

    - A parameter files (mdp) specifying the parameters for this simulations.
   
     We may also need few other files (such as for adding ions etc. and will be explained below).


     The hardest part is to create a topology file which is consistent with GROMACS convention 
     and is acceptable. At present it is not possible to create a topology file for an input (pdb)
     file which is having a ligand also. Again, the topology file must be consistent with the 'force field'
     and the 'water model' being used. 

     There are many online tools which can be used to create a topology file but there is no guarantee that
     they will work. You can check [here](http://manual.gromacs.org/2019/reference-manual/topologies.html) for more. 


### Create the topology file for the protein 

     We already have protein pdb file (3HTB_clean.pdb) so we can apply 'pb2gmx' on it in the following way. 

    `gmx pdb2gmx -f 3HTB_clean.pdb -o 3HTB_processed.gro`

     Please note the following :

     - Make sure you have 'charmm36-mar2019.ff'  available in your local directory before running this command.

     - You must give input '1' and '1' when asked for giving the force field an 'water model'.

     Once the above command is successful you will have the following output files:

     - 3HTB_processed.gro  : Coordinate file in 'gro' format. 
  
     - topol.top  : Topology file for the protein 

     - posre.itp  : Position information file.  
 


 






  
