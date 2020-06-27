import sys
import pandas as pd
import re
import matplotlib.pyplot as plt 
import argparse

if __name__ == "__main__":
  
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-log-file',help='Input log file')
    parser.add_argument('-o','--output-file',help='output csv file',default="test.csv")
    parser.add_argument('-p','--plot-param',help='Plotting column',default="TOTAL")

    args = parser.parse_args()

    with open (args.input_log_file,"r") as fp:
       data = fp.read().split("\n")

  
    for line in data:
       parts = line.split(" ")
       if parts[0] == 'ETITLE:':
           columns = [p for p in parts[1:] if p] 
           break

    print(columns)

    df = pd.DataFrame(columns=columns)
    count = 0 
    for line in data:
       text = re.sub(' +',' ',line)  
       cols = text.split(" ")
       if len (cols) == len (columns)+1:
          df.loc[count] = cols[1:] 
          count +=1
         

    df = df[~df['TOTAL'].str.contains("[a-zA-Z]").fillna(False)]
    df = df.astype(float)

    x = df['TS'].to_list()
    y1 = df['POTENTIAL'].to_list()
    y2 = df['TOTAL'].to_list()
    
    plt.plot(x[10:],y1[10:])
    plt.plot(x[10:],y2[10:])

    plt.ylabel(args.plot_param)
    plt.xlabel('time')
    plt.show()     



