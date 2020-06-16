import sys
import re

if __name__ == "__main__":

   with open (sys.argv[1],"r") as fp:
      data = fp.read()
   data = data.replace('*****',sys.argv[2]) 
   data = data.replace('JZ4167',sys.argv[2]) 
   data = data.replace('UNL1',sys.argv[2]) 
   data = data.replace('167','1') 

   print(data)

 
 
