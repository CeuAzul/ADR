import pandas as pd
import numpy as np
import csv
import os


def dict_to_dataframe(dict, column_name, index_name):
    dataframe = pd.DataFrame.from_dict(
        dict, orient="index", columns=[column_name])
    dataframe.index.name = index_name
    return dataframe


def find_df_roots(df, column_name):

    roots = []

    new_df = df.fillna(method="ffill")
    new_df = new_df.fillna(method="bfill")

    index_array = new_df.index.values
    values_array = new_df[column_name].values

    sign_change_array = (np.diff(np.sign(values_array)) != 0) * 1
    # sign_change_array = np.where(np.diff(np.sign(values_array)))[0]

    for index, element in enumerate(sign_change_array):
        if element == 1:
            roots.append(index_array[index])
    return roots


def save_dict(plane_params, perf_params, mtow, state):
    dir_name = "saved_planes"
    dir_path = os.path.dirname(os.path.abspath(
        __file__)).replace("Core", "") + dir_name
    print(dir_path)
    filename = "plane_mtow_"
    filepath = dir_path + "/" + filename + str(round(mtow)) + "_" + state + "-"

    i = 0
    if os.path.isfile(filepath + str(i) + ".csv"):
        already_exist = True
        while already_exist:
            i += 1
            if not os.path.isfile(filepath + str(i) + ".csv"):
                already_exist = False

    filepath = filepath + str(i) + ".csv"
    with open(filepath, "a", newline="") as f:
        w = csv.writer(f)
        for key, val in plane_params.items():
            w.writerow([key, val])
        for key, val in perf_params.items():
            w.writerow([key, val])
