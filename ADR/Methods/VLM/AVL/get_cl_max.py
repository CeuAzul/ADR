import pandas as pd
import fileinput
def get_clmax(output):
    with fileinput.input(output, inplace=True) as op:
        for line in op:
            if 'c cl' in line:
                print(line.replace('c cl','c_cl'))
            else:
                print(line.replace('\n',''))


    fid_df = pd.read_csv(output, skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20], skipfooter=28, delim_whitespace=True)
    fid_df.set_index('j', inplace=True)
    cl_max = fid_df['cl'].max()
    return cl_max
