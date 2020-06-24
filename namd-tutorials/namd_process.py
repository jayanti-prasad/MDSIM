import os
import argparse 
from shutil import copyfile

def copy_files (args,pdb_file,psf_file):
   
   os.makedirs (args.run_dir, exist_ok=True)

   files_to_copy = [args.topology_file,args.params_file,\
     args.output_config_file,psf_file,pdb_file]

   for f in files_to_copy:
      copyfile(f,args.run_dir + os.sep + os.path.basename (f))     
    

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-pdb-file',help='Input pdb file')
   parser.add_argument('-r','--run-dir',help='Run dir')

   parser.add_argument('-t','--topology-file',help='Input topology file',\
       default='input/top_all27_prot_lipid.inp')
   parser.add_argument('-p','--params-file',help='NAMD input param file',\
       default='input/par_all27_prot_lipid_na.inp')
   parser.add_argument('-c','--input-config-file',help='NAMD config file',\
       default='input/minimization.conf')
   parser.add_argument('-o','--output-config-file',help='NAMD output config file',\
       default='namd_minimize.conf')

   args = parser.parse_args()
   namd_process (args) 

