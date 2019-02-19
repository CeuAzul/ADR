
def read1(variable):
    var = '{}'.format(variable)
    with open('export.txt','r') as ex:
        for line in ex:
            line = line.replace('     ','/')
            if var in line:
                line_wo_space = line.replace(' ', '')
                coeficient_list = line_wo_space.split('/')
                for data in coeficient_list:
                    if var in data:
                        coef = data.split('=')
                        return coef[1]

    