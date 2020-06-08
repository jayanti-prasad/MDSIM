import sys
import os
import argparse
import configparser


def set_jobdir (args):

   with open(args.input_mdp) as f:
      file_content = '[top]\n' + f.read()

   config_parser = configparser.RawConfigParser()
   config_parser.read_string(file_content)

   prefix = os.path.basename(args.input_mdp).split('.')[0]
   os.makedirs (prefix,exist_ok=True)

   for i in range (0, args.num_lambdas):
       config_parser.set('top', 'init_lambda_state', i)

       tmp_file = prefix + os.sep + prefix + "_"+str(i)+".mdp"

       with open (tmp_file,"w")  as fp:
           config_parser.write(fp)

       with open (tmp_file,"r") as fp:
           lines = fp.readlines()

       with open (tmp_file,"w") as fp:
           for line in lines[1:]:
              fp.write(line)

   print("Please check:",prefix)


if __name__ == "__main__":
 
   parser = argparse.ArgumentParser()
   config_parser = configparser.ConfigParser()

   parser.add_argument ('-i','--input-mdp',help='Input mdp file')
   parser.add_argument ('-n','--num-lambdas',type=int, help='Number of lambdas')

   args = parser.parse_args()

   set_jobdir (args)

