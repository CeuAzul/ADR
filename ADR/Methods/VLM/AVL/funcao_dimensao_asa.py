import fileinput
i ='ro'
def dimensao_superficie(file,afile1,afile2,afile3,superficie,x,y1,y2,y3,z,c1,c2,c3,angle_incidence,twist1,twist2,twist3):
    with fileinput.input(file,inplace = True) as op:
        is_the_next_dim_gen = False
        is_the_next_dim1 = False
        is_the_next_dim2 = False
        is_the_next_dim3 = False
        is_the_next_angle = False
        is_the_next_afile1 = False
        is_the_next_afile2 = False
        is_the_next_afile3 = False
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
                
            elif is_the_next_afile1 == True: #Altera o arquivo
                print(line.replace(line,'{}'.format(afile1)))
                is_the_next_afile1 = False
                pass
                                    
            elif '#arquivo_1' in line: #Define a linha que tem o arquivo
                print(line.replace('\n',''))
                is_the_next_afile1 = True
                pass
                
            elif is_the_next_afile2 == True: #Altera o arquivo
                print(line.replace(line,'{}'.format(afile2)))
                is_the_next_afile2 = False
                pass
                                    
            elif '#arquivo_2' in line: #Define a linha que tem o arquivo
                print(line.replace('\n',''))
                is_the_next_afile2 = True
                pass
                
            elif is_the_next_afile3 == True: #Altera o arquivo
                print(line.replace(line,'{}'.format(afile3)))
                is_the_next_afile3 = False
                pass
            
            elif '#arquivo_3' in line: #Define a linha que tem o arquivo
                print(line.replace('\n',''))
                is_the_next_afile3 = True
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
                
            
                
            #DIMENSAO DA SEÇAO====================================================================================
            
            elif is_the_next_dim1 == True: #Altera a dimensao
                print(line.replace(line,'{} {} {} {} {} {} {}'.format(x,y1,z,c1,twist1,0,0)))
                is_the_next_dim1 = False
                pass
            
            elif '#Dimensao_{}_secao_1'.format(superficie) in line: #Define a linha que tem a dimensao
                print(line.replace('\n',''))
                is_the_next_dim1 = True
                pass
                
            elif is_the_next_dim2 == True: #Altera a dimensao
                print(line.replace(line,'{} {} {} {} {} {} {}'.format(x,y2,z,c2,twist2,0,0)))
                is_the_next_dim2 = False
                pass
            
            elif '#Dimensao_{}_secao_2'.format(superficie) in line: #Define a linha que tem a dimensao
                print(line.replace('\n',''))
                is_the_next_dim2 = True
                pass
                
            elif is_the_next_dim3 == True: #Altera a dimensao
                print(line.replace(line,'{} {} {} {} {} {} {}'.format(x,y3,z,c3,twist3,0,0)))
                is_the_next_dim3 = False
                pass
            
            elif '#Dimensao_{}_secao_3'.format(superficie) in line: #Define a linha que tem a dimensao
                print(line.replace('\n',''))
                is_the_next_dim3 = True
                pass
                
            else:
                print(line.replace('\n',''))
                pass

dimensao_superficie('testerafa.avl','s1223.dat','sd7037.dat','s1223.dat','wing',0,0,1.0,1.5,0,0.4,0.8,0.6,0,0,3.0,1.0)
