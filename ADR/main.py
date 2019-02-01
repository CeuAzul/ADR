# Teste de instancia de objeto p do tipo Plane

#from ADR.Components.Planes.Plane import Plane

from ADR.Components.Planes.Plane import Plane

#--- Por exemplo ---#
CL_alpha_asa = range(0, 2)
span_EH = 0.5
chord_EV = 0.2
# "data" sao os dados do aviao recebidos do codigo genetico
# Coloca-os em um dicionario para facilitar sua busca futura
data = {"CL_alpha_asa" : CL_alpha_asa, "span_EH" : span_EH, "chord_EV" : chord_EV}
#-------------------#

p = Plane(data)
print(p.eh.span)
