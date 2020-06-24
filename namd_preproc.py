import os
import sys
import argparse 

def write_psfgen (input_pdb):

   prefix = input_pdb.replace(".pdb","")
   out_prefix = prefix + "_tmp"
  
   fp = open("psf.tcl","w")
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
 
   return out_prefix+".pdb"  


def write_solgen(input_pdb):

   prefix = input_pdb.replace(".pdb","")
   out_prefix = prefix + "_sol"
  
   fp = open("solvate.tcl","w")
   fp.write("package require solvate\n")
   fp.write("solvate "  + prefix+".psf"+ " "+ prefix + ".pdb" + " -t 5 -o "+ out_prefix+"\n")
   fp.write("exit")
   fp.close()

   return out_prefix+".pdb"  


def write_iongen(input_pdb):

   prefix = input_pdb.replace(".pdb","")
   out_prefix = prefix + "_ion"

   fp = open("neutrilize.tcl","w")
   fp.write("package require autoionize\n")
   fp.write("autoionize -psf "+ prefix+".psf" + " -pdb "\
      + prefix+".pdb -neutralize\n")
   #   + prefix+".pdb " + " -o " + out_prefix + "  -neutralize\n")
   fp.write("exit")
   fp.close()

   return out_prefix+".pdb"


def write_boxgeb(input_pdb):
   prefix = input_pdb.replace(".pdb","")
   fp = open("boxsize.tcl","w")
   fp.write("mol new  ionized.pdb.psf\n")
   fp.write("mol addfile ionized.pdb\n")
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
  
if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-pdb-file',help='Input pdb file')
   parser.add_argument('-t','--topology-file',help='Input topology file')

   args = parser.parse_args()

   psf_pdb = write_psfgen (args.input_pdb_file)

   print("psf file prefix: ", psf_pdb)

   sol_pdb = write_solgen (psf_pdb)
   print("solvate  file prefix: ", sol_pdb)
    
   ion_pdb = write_iongen (sol_pdb)
   print("ionization  file prefix: ", ion_pdb)
   
   write_boxgeb(ion_pdb)

