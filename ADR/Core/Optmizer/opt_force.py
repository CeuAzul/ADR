from ADR.Core.data_manipulation import replace_forced_parameters

def get_forced_parameters(original_parameters, geneticized_parameters):
    mixed_parameters = replace_forced_parameters(original_parameters, geneticized_parameters)
    mp = mixed_parameters

    # Prevent wings and HSs with increasing chord spanwise and make thw wings equal
    if mp.get("wing1_chord2") > mp.get("wing1_chord1"):
        mp["wing1_chord2"] = mp["wing1_chord1"]
    if mp.get("wing1_chord3") > mp.get("wing1_chord2"):
        mp["wing1_chord3"] = mp["wing1_chord2"]

    mp["wing2_span1"] = mp["wing1_span1"]
    mp["wing2_span2"] = mp["wing1_span2"]
    mp["wing2_chord1"] = mp["wing1_chord1"]
    mp["wing2_chord2"] = mp["wing1_chord2"]
    mp["wing2_chord3"] = mp["wing1_chord3"]

    if mp.get("hs_chord2") > mp.get("hs_chord1"):
        mp["hs_chord2"] = mp["hs_chord1"]
    if mp.get("hs_chord3") > mp.get("hs_chord2"):
        mp["hs_chord3"] = mp["hs_chord2"]

    wing1_chord2 = mp["wing1_chord2"]
    wing1_chord3 = mp["wing1_chord3"]

    wing2_span1 = mp["wing2_span1"]
    wing2_span2 = mp["wing2_span2"]
    wing2_chord1 = mp["wing2_chord1"]
    wing2_chord2 = mp["wing2_chord2"]
    wing2_chord3 = mp["wing2_chord3"]

    hs_chord2 = mp["hs_chord2"]
    hs_chord3 = mp["hs_chord3"]

    # Get MAC aproximation and use it to get the zero reference for the CG
    MAC_aprox = ( mp.get("wing1_chord1")/4 + mp.get("wing1_chord2")/4 + mp.get("wing1_chord3")/4 ) / 3
    cg_x = - MAC_aprox + mp.get("cg_x")

    # Get the TPR position zeroed on the CG position (TPR always after CG)
    tpr_x = cg_x + mp.get("tpr_x")

    # Get the max span (wings or HS) and max HS's chord to max the HS's x postion
    wing1_span = 2 * ( mp.get("wing1_span1") + mp.get("wing1_span2") )
    wing2_span = 2 * ( mp.get("wing2_span1") + mp.get("wing2_span2") )
    hs_span = 2 * ( mp.get("hs_span1") + mp.get("hs_span2") )
    y_max = max(wing1_span, wing2_span, hs_span)
    hs_max_chord = max(mp.get("hs_chord1"), mp.get("hs_chord2"), mp.get("hs_chord3"))
    hs_x = -(3.70 - y_max - hs_max_chord - mp.get("motor_x"))

    forced_parameters = {
        "cg_x": cg_x,
        "tpr_x": tpr_x,
        "hs_x": hs_x,
        "wing1_chord2": wing1_chord2,
        "wing1_chord3": wing1_chord3,
        "wing2_span1": wing2_span1,
        "wing2_span2": wing2_span2,
        "wing2_chord1": wing2_chord1,
        "wing2_chord2": wing2_chord2,
        "wing2_chord3": wing2_chord3,
        "hs_chord2": hs_chord2,
        "hs_chord3": hs_chord3,
    }

    return forced_parameters