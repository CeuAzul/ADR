import fileinput

def get_value(output_file, variable_name):
    var = '{}'.format(variable_name)
    with open(output_file,'r') as ex:
        for line in ex:
            line = line.replace('     ','/')
            if var in line:
                line_wo_space = line.replace(' ', '')
                coeficient_list = line_wo_space.split('/')
                for data in coeficient_list:
                    if var in data:
                        coef = data.split('=')
                        return float(coef[1].strip('\n'))

def set_dimensions(config_file, airfoil1_file, airfoil2_file, airfoil3_file,
                   surface_name, x, y1, y2, y3, z, c1, c2, c3,
                   angle_incidence, twist1, twist2, twist3):

    with fileinput.input(config_file,inplace = True) as op:
        is_the_next_dim_gen = False
        is_the_next_dim1 = False
        is_the_next_dim2 = False
        is_the_next_dim3 = False
        is_the_next_angle = False
        is_the_next_airfoil1_file = False
        is_the_next_airfoil2_file = False
        is_the_next_airfoil3_file = False
        for line in op:

            #DIMENSOES REFERENCIA=============================================================================

            if is_the_next_dim_gen == True: #Altera o angulo
                print(line.replace(line,'{} {} {}'.format(round(((c1+c2)*(y2-y1)*0.5+(c2+c3)*(y3-y2)*0.5)*2,4),round((c1+c2+c3)/3,4),round((y3-y1)*2,4))))
                is_the_next_dim_gen = False
                pass

            elif '#Dimensoes_referencia' in line: #Define a linha que tem o angulo
                print(line.replace('\n',''))
                is_the_next_dim_gen = True
                pass

            #ARQUIVO DO PERFIL===========================================================================

            elif is_the_next_airfoil1_file == True: #Altera o arquivo
                print(line.replace(line,'{}'.format(airfoil1_file)))
                is_the_next_airfoil1_file = False
                pass

            elif '#arquivo_1' in line: #Define a linha que tem o arquivo
                print(line.replace('\n',''))
                is_the_next_airfoil1_file = True
                pass

            elif is_the_next_airfoil2_file == True: #Altera o arquivo
                print(line.replace(line,'{}'.format(airfoil2_file)))
                is_the_next_airfoil2_file = False
                pass

            elif '#arquivo_2' in line: #Define a linha que tem o arquivo
                print(line.replace('\n',''))
                is_the_next_airfoil2_file = True
                pass

            elif is_the_next_airfoil3_file == True: #Altera o arquivo
                print(line.replace(line,'{}'.format(airfoil3_file)))
                is_the_next_airfoil3_file = False
                pass

            elif '#arquivo_3' in line: #Define a linha que tem o arquivo
                print(line.replace('\n',''))
                is_the_next_airfoil3_file = True
                pass

            #ANGULO DE INCIDENCIA=============================================================================

            elif is_the_next_angle == True: #Altera o angulo
                print(line.replace(line,'{}'.format(angle_incidence)))
                is_the_next_angle = False
                pass

            elif 'ANGLE' in line: #Define a linha que tem o angulo
                print(line.replace('\n',''))
                is_the_next_angle = True
                pass



            #DIMENSAO DA SECAO====================================================================================

            elif is_the_next_dim1 == True: #Altera a dimensao
                print(line.replace(line,'{} {} {} {} {} {} {}'.format(x,y1,z,c1,twist1,0,0)))
                is_the_next_dim1 = False
                pass

            elif '#Dimensao_{}_secao_1'.format(surface_name) in line: #Define a linha que tem a dimensao
                print(line.replace('\n',''))
                is_the_next_dim1 = True
                pass

            elif is_the_next_dim2 == True: #Altera a dimensao
                print(line.replace(line,'{} {} {} {} {} {} {}'.format(x,y2,z,c2,twist2,0,0)))
                is_the_next_dim2 = False
                pass

            elif '#Dimensao_{}_secao_2'.format(surface_name) in line: #Define a linha que tem a dimensao
                print(line.replace('\n',''))
                is_the_next_dim2 = True
                pass

            elif is_the_next_dim3 == True: #Altera a dimensao
                print(line.replace(line,'{} {} {} {} {} {} {}'.format(x,y3,z,c3,twist3,0,0)))
                is_the_next_dim3 = False
                pass

            elif '#Dimensao_{}_secao_3'.format(surface_name) in line: #Define a linha que tem a dimensao
                print(line.replace('\n',''))
                is_the_next_dim3 = True
                pass

            else:
                print(line.replace('\n',''))
                pass


