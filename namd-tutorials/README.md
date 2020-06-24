# Step by step procedure to run molecular dynamics simulations with NAMD 

## What it is ?

  Molecular dynamics is one of the most important areas of research and in order to be proficient,
  productive and solve real life problems, such as drug design, one must have expertise in 
  physics, chemistry, mathematics, biology, computer science and software engineering !
  This is really an unreasonable requirement and so despite having outstanding numerical codes
  available, such as GROMAX, and NAMD, many users feel helpless.

  Here I am presenting a simple python script which can run a molecular dynamics simulation 
  using NAMD end-to-end in a very smooth way, without requiring any GUI to be running.
  This means that this script can be launched in an automatic way on cloud systems,
  such as amazon AWS, without any difficulty.

  The python script (see how to use below) does the following:

  - Read a 'pdb' file and create a 'psf' as well a new 'pdb' file using a topology file
    supplied by the user.

  - Solvate the system wih water.

  - Neutralize the system with ions.

  - Compute the geometry of the box for carrying out the simulations.

  - Create a config file from a user given config file by making necessary changes.

  
##  A. Software needed :

  - Python 3.6+

  - CHIMERA (optional)  - This is used for visualizing as well well as for molecular 
     docking with the help of AutoDock Vina .

  - VMD - Here  it is mostly used in  command mode for  various operations such as  Solvation
    and neutralization. However, GUI model is useful for post processing.
 
  - NAMD - For carrying out molecular dynamics simulations.

  - Text-Editor - Any  editor such as vi note-pad etc., will be fine.


##  B. Parameter Files:  

  - (i) Topology file [ top_all27_prot_lipid.inp ]

  - (ii) Input parameter for running NAMD simulations - [ par_all27_prot_lipid_na.inp]

  - (iii) Input configuration file : A template  configuration file to run the script [namd_run.conf].
     The actual script to run the simulation will be created by the python program provided.  


##  C. Input Data file 

  - PDB file of the docked ligand and protein 


##  D. Creating the config file 

    - The main purpose of the 'namd_preproc.py' is to create a configuration (input) file for running NMAD simulation.

    - In order to run the script you must give the path to your VMD instllation (see line 5 in namd_preproc.py)
      which for my case looks like :

      VMD="/Applications/VMD\ 1.9.4a42-Catalina-Rev5.app/Contents/vmd/vmd_MACOSXX86_64"

    - Once the path to VMD is set the script can be run in the following way:

    -  python namd_preproc.py  -i test_example.pdb  \
        -t input/top_all27_prot_lipid.inp \
        -p input/par_all27_prot_lipid_na.inp \
        -c input/minimization.conf -o test_minimize.conf 
    
    - If you run the script with option '-h' it prints the help.

    - In the above command :
  
    . test_example.pdb  : input pdb file

    . input/top_all27_prot_lipid.inp : input topology file
    
    . input/par_all27_prot_lipid_na.inp  : input parameter file

    . input/minimization.conf  : template for the configuration file

    . test_minimize.conf : output configuration file 

## E. Running NAMD simulations 
 
    Once the input configuration file is created we can launch the simulation with the following command.

   - ` namd2  +p8  test_minimize.conf > output.log & `

    Here :

    .  +p8 : Means we are using 8 cores 

    . output.log  : Is the output (log) file 


    .  & : For running the job in background 

   - Important :
   
     The above command assumes that 'namd2' is in your path if that is not the case then
     wither give the full path to the command or set the path accordingly.


## F. Post processing : 

    To be added 
