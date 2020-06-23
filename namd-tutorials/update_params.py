import os
import sys

def update_config_file (args, input_pdb, box_file):

    top_file = args.topology_file
    params_file = args.params_file
    input_config_file = args.input_config_file 
    output_config_file = args.output_config_file 

    prefix = input_pdb.replace(".pdb","")

    box_params=["cellBasisVector1","cellBasisVector2",\
       "cellBasisVector3","cellOrigin"]

    file_params =["structure","coordinates"]

    skip_lines = box_params + file_params + ["parameters"]

    F= {file_params[0]: prefix+".psf", file_params[1]: prefix+".pdb"}

    with open (input_config_file,"r") as fp:
       param_lines = fp.read().split("\n")

    with open (box_file,"r") as fp:
       box_lines = fp.read().split("\n")

    P = {}
    for line in box_lines:
        parts = line.split(" ")
        if parts[0] in box_params:
           P[parts[0]] = " ".join(parts[1:])

    fp = open (output_config_file, "w")
    for line in param_lines:
       parts = line.split(" ")
       if parts[0] not in skip_lines:
          fp.write(line+"\n")
       if parts[0] in box_params:
          print("updating: ", parts[0])
          fp.write(parts[0] + "   " +  P[parts[0]]+"\n") 
       if parts[0] in file_params:
          print("updating: ", parts[0])
          fp.write(parts[0] + "   " +  F[parts[0]]+"\n") 
       if parts[0]  == "parameters":
          print("updating: ", parts[0])
          fp.write("parameter   " +  params_file+"\n") 

    os.remove(box_file)
    fp.close()
   
