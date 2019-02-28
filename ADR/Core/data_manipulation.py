import pandas as pd
import numpy as np

def dict_to_dataframe(dict, column_name, index_name):
    dataframe = pd.DataFrame.from_dict(dict, orient="index", columns=[column_name])
    dataframe.index.name = index_name
    return dataframe

def find_df_roots(df, column_name):

    roots = []

    new_df = df.fillna(method='ffill')
    new_df = new_df.fillna(method='bfill')

    index_array = new_df.index.values
    values_array = new_df[column_name].values

    sign_change_array = (np.diff(np.sign(values_array)) != 0)*1
    # sign_change_array = np.where(np.diff(np.sign(values_array)))[0]

    for index, element in enumerate(sign_change_array):
        if element == 1:
            roots.append(index_array[index])
    return roots

def replace_forced_parameters(original_parameters, forced_parameters):

    mixed_parameters = {key: forced_parameters.get(key, value) for key, value in original_parameters.items()}
    return mixed_parameters