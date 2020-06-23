# Step by step procedure to run molecular dynamics simulations with NAMD 


##  A. Software needed :

  - CHIMERA  - This is used for visualizing as well well as for molecular docking with the help of AutoDock Vina .

  - VMD  - VMD is used in  GUI/Visual mode as well as command mode of various operations such as solvate, ionization, running namd simulation etc. Note that everything that can be done with the GUI can be done with the command line also.

  - NAMD - For carrying out molecular dynamics simulations.

  - Text-Editor - Any  editor such as vi note-pad etc will be fine.


##  B. Parameter Files:  

  - (i) Topology file [ top_all27_prot_lipid.inp ]

  - (ii) Input parameter for running NAMD simulations - [ par_all27_prot_lipid_na.inp]

  - (iii) Configuration file : The main configuration file to run the script [namd_run.conf]


## C. Scripts : 
  
  - (i) A TCL file for creating psf file from pdb file.

  - (ii) A TCL file for creating the geometry of the simulation (in case of periodic boundary box).


##  D. Input Data 

  - PDB file of the docked ligand and protein 


## E. Procedure

  - (i) Generating 'psf' file :- 

   There is a script as mentioned in C(i) and given [here](config_files/psf.gen) that can 
   be used to generate the 'psf' file (as well as a modified pdb file).

   Input to this script are two files : (a) topology file mentioned in B(i) and pdb data file mentioned in D.

   You must give the name of the output psf file and pdb file by editing the script appropriately.

   Once the script is changed accordingly the following command can be used to create the psf & pdb files.

   - `/Applications/VMD\ 1.9.4a42-Catalina-Rev5.app/Contents/vmd/vmd_MACOSXX86_64 -dispdev text -e psf.gen`
 
   Note that the first part of the command depends in the installation of vmd on your computer so do not try to
   copy the command and file the path for the command for your machine.

  - (ii) Solvation :- 

   Once we have generated the 'psf' and modified 'pdb' file in step (i) we can do the solvation by running
    the following command on the 'VMD' console.
  
  - ` package require solvate `	
 
  - ` solvate ubq.psf ubq.pdb -t 5 -o ubq_wb`

  IMPORTANT :

   -  You change the directory path (PWD) to the path where we have generated the 'psf' 
      and modified 'pdb' file.

   - This command again creates one 'psf' and one 'pdb' file and the prefix for those can 
     be given by the option '-o' as shown the in above command.


  - (iii) Ionization :- 

     This also works exactly in the same was as (ii) and takes two input files (solvated psf and pdb files)
     and generates two output files (solvated + ionized psf and pdb file). By default, it will add 
     the prefix 'ionized' but if you want something else you can use that also with option '-o'.

   - `autoionize -psf ubq_wb.psf -pdb ubq_wb.pdb -neutralize`

   - (iv) Run the NAMD simulations:

      The simulation can be run with the following command.

   - ` namd2  +p8  input.conf > output.log & `

