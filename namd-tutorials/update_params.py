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

    skip_lines = box_params + file_params + ["parameters","outputName"]

    F= {file_params[0]: os.path.basename(prefix+".psf"), file_params[1]: os.path.basename(prefix+".pdb")}

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
          tt = P[parts[0]].split(" ") 
          print("updating: ", parts[0])
          fp.write(parts[0] + "   " +  P[parts[0]]+"\n") 

       if parts[0] in file_params:
          print("updating: ", parts[0])
          fp.write(parts[0] + "   " +  F[parts[0]]+"\n") 
       if parts[0]  == "parameters":
          print("updating: ", parts[0])
          fp.write("parameters         " +  os.path.basename(params_file)+"\n") 
       if parts[0] == "outputName":
          fp.write("outputName          " + args.output_prefix +"\n") 
           
    os.remove(box_file)
    fp.close()

def update_nvt_file (args, input_pdb):
    nvt_dir = args.run_dir + os.sep  + "nvt"
    os.makedirs (nvt_dir, exist_ok=True)

 

    prefix = input_pdb.replace(".pdb","")

    with open (args.run_dir + os.sep + args.output_config_file,"r") as fp:
       lines = fp.read()
    lines = lines.split("\n")

    lines = [l for l in lines if l]

    lines_to_comment=["temperature","minimize"]
    lines_to_change=["#run","parameters","outputName","structure","coordinates","#binCoordinates","binVelocities"]

    lines_not_to_copy = lines_to_comment + lines_to_change    

    fp = open (nvt_dir + os.sep + "nvt.conf","w")
    for line in lines:
       parts = line.split(" ") 

       if parts[0] not in lines_not_to_copy: 
           fp.write(line+"\n")

       if parts[0] in lines_to_comment: 
           fp.write("#"+line+"\n")

       if parts[0] == 'outputName':
             fp.write("outputName   " + args.output_prefix+"_nvt\n")

       if parts[0] == "#binCoordinates":
          fp.write("binCoordinates   " + "../"+args.output_prefix+".restart.coor\n") 
       if parts[0] == "#binVelocities":
          fp.write("binVelocities   " +  "../"+args.output_prefix+".restart.vel\n")
          fp.write("firsttimestep     5000            ;# last step of previous run\n")
          fp.write("numsteps          50000 \n")
       if parts[0] == "structure":
          fp.write("structure   " + "../"+prefix+".psf\n")

       if parts[0] == "#run":
          fp.write("run          50000 \n")


       if parts[0] == "coordinates":
          fp.write("coordinates   " + "../"+prefix+".pdb\n")

       if parts[0] == "parameters":
          fp.write("parameters   " + "../"+os.path.basename(args.params_file)+"\n")

    fp.close()

