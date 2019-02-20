import pandas as pd

def dict_to_dataframe(dict, column_name, index_name):
    dataframe = pd.DataFrame.from_dict(dict, orient="index", columns=[column_name])
    dataframe.index.name = index_name
    return dataframe