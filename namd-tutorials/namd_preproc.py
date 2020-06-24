import os
import sys
import argparse 
from  update_params import update_config_file
from shutil import copyfile


VMD="/Applications/VMD\ 1.9.4a42-Catalina-Rev5.app/Contents/vmd/vmd_MACOSXX86_64"

def run_scripts (script):
   print("Running script:", script)
   os.system(VMD + "  -dispdev text -e " + script)
   os.remove(script)

def del_files (prefix):
   os.remove(prefix+".pdb")
   os.remove(prefix+".psf")


def write_psfgen (input_pdb):

   prefix = input_pdb.replace(".pdb","")
   out_prefix = prefix + "_tmp"
  
   fp = open("tmp.tcl","w")
   fp.write("package require psfgen\n")
   fp.write("topology"+" "+ args.topology_file+"\n")
   fp.write("pdbalias residue HIS HSE\n")
   fp.write("pdbalias atom ILE CD1 CD\n")
   fp.write("segment U {pdb "+" "+ args.input_pdb_file +"}\n")
   fp.write("coordpdb"+" "+ args.input_pdb_file + " "+ "U\n")
   fp.write("guesscoord \n")
   fp.write("writepdb " +" " + out_prefix +".pdb\n")
   fp.write("writepsf " +" " + out_prefix +".psf\n")
   fp.write("exit")
   fp.close()
   run_scripts ("tmp.tcl")
 
   return out_prefix+".pdb"  


def write_solgen(input_pdb):

   prefix = input_pdb.replace(".pdb","")
   out_prefix = prefix + "_sol"

   fp = open("tmp.tcl","w")
   fp.write("package require solvate\n")
   fp.write("solvate "  + prefix+".psf"+ " "+ prefix + ".pdb" + " -t 5 -o "+ out_prefix+"\n")
   fp.write("exit")
   fp.close()
   run_scripts ("tmp.tcl")

   del_files (prefix)

   return out_prefix + ".pdb"  


def write_iongen(input_pdb):

   prefix = input_pdb.replace(".pdb","")

   out_prefix = prefix.replace("tmp_","") + "_ion"
 
   fp = open("tmp.tcl","w")
   fp.write("package require autoionize\n")
   fp.write("autoionize -psf "+ prefix + ".psf" + " -pdb "\
      + prefix+".pdb " + " -o " + out_prefix + "  -neutralize\n")
   fp.write("exit")
   fp.close()
   run_scripts ("tmp.tcl")
 
   del_files (prefix)

   return out_prefix+".pdb"


def find_box(input_pdb):

   prefix = input_pdb.replace(".pdb","")

   fp = open("tmp.tcl","w")
   fp.write("mol new  " + prefix +".psf\n")
   fp.write("mol addfile " + prefix + ".pdb\n")
   fp.write("proc get_cell {{molid top}} { \n")
   fp.write("set all [atomselect $molid all]\n")
   fp.write("set minmax [measure minmax $all]\n")
   fp.write("set vec [vecsub [lindex $minmax 1] [lindex $minmax 0]]\n")
   fp.write("puts \"cellBasisVector1 [lindex $vec 0] 0 0\"\n")
   fp.write("puts \"cellBasisVector2 0 [lindex $vec 1] 0\"\n")
   fp.write("puts \"cellBasisVector3 0 0 [lindex $vec 2]\"\n")
   fp.write("set center [measure center $all]\n")
   fp.write("\puts \"cellOrigin $center\"\n")
   fp.write("$all delete\n")
   fp.write("}\n")
   fp.write("get_cell\n")
   fp.write("exit\n")
   fp.close()

   os.system(VMD + "  -dispdev text -e tmp.tcl > box.txt")
   os.remove("tmp.tcl")


def copy_files (args,pdb_file):

   os.makedirs (args.run_dir,exist_ok=True)
 
   psf_file = pdb_file.replace(".pdb",".psf")

   files_to_copy = [args.topology_file,args.params_file,\
     args.output_config_file,psf_file,pdb_file]

   for f in files_to_copy:
      copyfile(f,args.run_dir + os.sep + os.path.basename (f))

   os.remove(pdb_file)
   os.remove(psf_file)


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-pdb-file',help='Input pdb file')
   parser.add_argument('-r','--run-dir',help='Run dir',default="test_run")
   parser.add_argument('-f','--output-prefix',help='Output prefix',default="test")
   parser.add_argument('-t','--topology-file',help='Input topology file',\
       default='input/top_all27_prot_lipid.inp')
   parser.add_argument('-p','--params-file',help='NAMD input param file',\
       default='input/par_all27_prot_lipid_na.inp')
   parser.add_argument('-c','--input-config-file',help='NAMD config file',\
       default='input/minimization.conf')
   parser.add_argument('-o','--output-config-file',help='NAMD output config file',\
       default='namd_minimize.conf')

   args = parser.parse_args()

   psf_pdb = write_psfgen (args.input_pdb_file)

   print("Creating psf file : ", psf_pdb)

   sol_pdb = write_solgen (psf_pdb)
   print("Solvation : ", sol_pdb)
    
   ion_pdb = write_iongen (sol_pdb)
   print("Neutrilization: ", ion_pdb)
   
   find_box(ion_pdb)

   print("Updating config file:", args.output_config_file)

   update_config_file (args, ion_pdb,"box.txt")

   copy_files (args,ion_pdb)

