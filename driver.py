import os
import argparse 
from  subprocess import Popen, PIPE

gmx='/usr/local/gromacs/bin/gmx'

def run_grompp  (**kwargs):

   os.makedirs ("Lambda_"+str(kwargs['l']),exist_ok=True)

   proc = Popen([gmx,"grompp","-f",kwargs['f'],\
      '-c',kwargs['c'],'-p',kwargs['p'],\
      '-o',kwargs['o']], stdout=PIPE,\
          stderr=PIPE, universal_newlines=True)

   outs, errs = proc.communicate(timeout=15)

   return outs


def run_mdrun (sim, input_file,n):

   out_dir =  sim + os.sep + "out"
   log_dir =  sim + os.sep + "log"
   gro_dir =  sim + os.sep + "gro"
   cpo_dir =  sim + os.sep + "cpi"
 
   os.makedirs(out_dir, exist_ok=True)
   os.makedirs(log_dir, exist_ok=True)
   os.makedirs(gro_dir, exist_ok=True)
   os.makedirs(cpo_dir, exist_ok=True)

   #os.chdir(sim)


   proc = Popen([gmx,"mdrun","-s",\
      input_file,'-o',out_dir,'-g',log_dir,'-c',gro_dir,'-cpo',cpo_dir],\
      stdout=PIPE, stderr=PIPE, universal_newlines=True)

   outs, errs = proc.communicate(timeout=15)

   return outs


if __name__ == "__main__":

   parser = argparse.ArgumentParser()

   parser.add_argument ('-i','--input-mdp',help='Input mdp file')
   parser.add_argument ('-n','--num-lambdas',type=int, help='Number of lambdas')
   parser.add_argument ('-w','--work-dir',help='Workspace directory')

   args = parser.parse_args()

   kwargs = {}
     
   case = "em_steep"

   for l in range(0, 10):
      tpr_file= case + os.sep + "min"+str(l)+".tpr"
      kwargs['f'] = case+ os.sep + case +"_"+str(l)+".mdp"
      kwargs['c'] = "config_files/methane_water.gro"
      kwargs['p'] = "config_files/topol.top" 
      kwargs['o'] = tpr_file 
      kwargs['l'] = l 
      outs  = run_grompp (**kwargs)
      #print(outs) 

      run_mdrun (case, tpr_file, 4) 

      print(outs) 
