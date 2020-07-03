import ADR
import pandas as pd


def get_filepath(folder, filename):

    package_filepath = ADR.__file__.replace("__init__.py", "")
    complete_filepath = package_filepath + folder + filename

    return complete_filepath


def import_airfoil_aerodynamic_data(airfoil_name):

    airfoil_aerodynamic_data_filepath = get_filepath(
        "World/Profiles/AerodynamicData/", "xf-" + airfoil_name + "-il-200000.csv"
    )

    airfoil_df = pd.read_csv(
        airfoil_aerodynamic_data_filepath, skiprows=10, index_col=0
    )
    Cl_alpha = airfoil_df[["Cl"]]
    Cd_alpha = airfoil_df[["Cd"]]
    Cm_alpha = airfoil_df[["Cm"]]

    return Cl_alpha, Cd_alpha, Cm_alpha


def import_airfoil_coordinates(airfoil_name):

    # Aqui o arquivo de coordenadas no formato de arquivo de texto, conforme copiado e colado de um banco de dados é lido e editado
    # removendo espaços em branco adicionais para facilitar a separação em data frames. O formato do arquivo de coordenadas deve ser
    # o formato selig.

    airfoil_coordinates_filepath = get_filepath(
        "World/Profiles/Coordinates/", airfoil_name + ".dat"
    )

    file1 = open(airfoil_coordinates_filepath, "r")
    file2 = open(airfoil_coordinates_filepath.replace(
        ".dat", "_edited.dat"), "wt")
    file2.write("x y \n")
    for line in file1:
        file2.write(" ".join(line.split()) + "\n")
    file1.close()
    file2.close()

    # -----Criação do dataframe e transformação de dataframe em vetores (listas)-----
    # A partir do arquivo de texto é criado o dataframe com as coordenadas dos pontos do perfil. Esse dataframe é separado em coordendas
    # horizontais e verticais e em seguida transformados em vetores (listas).

    df = pd.read_csv(
        airfoil_coordinates_filepath.replace(".dat", "_edited.dat"),
        sep=" ",
        skiprows=[1],
    )
    df_array_x = df.loc[:, "x"]
    df_array_y = df.loc[:, "y"]

    return (
        df_array_x.values,
        df_array_y.values,
    )  # vetores de coordenadas horizontais e verticais
