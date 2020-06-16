import os
import sys
import argparse
from  subprocess import Popen, PIPE

gmx='/usr/local/gromacs/bin/gmx'

def run_grompp  (**kwargs):
   proc = Popen([gmx,"grompp","-f",kwargs['f'],\
      '-c',kwargs['c'],'-p',kwargs['p'],\
      '-o',kwargs['o']], stdout=PIPE,\
          stderr=PIPE, universal_newlines=True)

   outs, errs = proc.communicate(timeout=15)
   if errs:
      return errs, -1
   else:
      return outs, 0

def run_mdrun (input_file):

   print("Input file:",input_file)
   proc = Popen([gmx,"mdrun","-s",input_file],\
      stdout=PIPE, stderr=PIPE, universal_newlines=True)

   outs, errs = proc.communicate(timeout=15)

   if errs:
      return errs, -1
   else:
      return outs, 0

def clean (args):
  
   del_ext = ['log','tpr','xtc','trr','xvg','tpr','edr']

   root = os.getcwd()
   files = os.listdir(root)
 
   for f in files:
      if f.split(".")[-1] in del_ext or "#" in f or "step" in f:
         print("Deleting:", f)
         os.remove(f)

if __name__ == "__main__":

   parser = argparse.ArgumentParser()

   parser.add_argument ('-f','--input-mdp',help='grompp input file with MD parameters',\
      default='config_files/em_steep.mdp')
   parser.add_argument ('-c','--input_file',help='Structure file: gro g96 pdb brk ent esp tpr')
   parser.add_argument ('-p','--top-file',help='Topology file')
   parser.add_argument ('-o','--run-file',help='Output file',default='run.tpr')
   parser.add_argument('-e', '--erase', help='Erase index', action='store_true')

   args = parser.parse_args()

   if args.erase:
      print("Cleaning everything")
      clean(args)
      sys.exit()

   kwargs={'f': args.input_mdp,'c': args.input_file, 'p': args.top_file,'o': args.run_file}

   print("Runing grompp with options:\n",kwargs)
   out, status  = run_grompp  (**kwargs) 
   print(out)
   #if status < 0:
   #    sys.exit() 

   print("Running mdrun simulations with input file:", args.run_file)
   out, status = run_mdrun (args.run_file)
   print(out)

