import pandas as pd
import avlwrapper as avl
import os


def get_aero_coefs(data, airfoil_clmax):
    filedir = os.path.dirname(os.path.abspath(__file__))

    # append avlwrapper_io directory to PATH so AVL executables can be found
    os.environ["PATH"] += os.pathsep + filedir

    airfoil1_filename = data['airfoil1_name'] + '.dat'
    airfoil1_filepath = filedir + '/' + airfoil1_filename

    airfoil2_filename = data['airfoil2_name'] + '.dat'
    airfoil2_filepath = filedir + '/' + airfoil2_filename

    airfoil3_filename = data['airfoil3_name'] + '.dat'
    airfoil3_filepath = filedir + '/' + airfoil3_filename

    c1 = data['chord1']
    c2 = data['chord2']
    c3 = data['chord3']
    x1 = 0
    x2 = 0
    x3 = 0
    y1 = 0
    y2 = data['span1']
    y3 = data['span1'] + data['span2']
    z1 = 0
    z2 = 0
    z3 = 0

    aerosurface_root_chord = data['chord1']
    aerosurface_mid_chord = data['chord2']
    aerosurface_tip_chord = data['chord3']

    aerosurface_root_le_pnt = avl.Point(x=x1,
                                        y=y1,
                                        z=z1)
    aerosurface_mid_le_pnt = avl.Point(x=x2,
                                       y=y2,
                                       z=z2)
    aerosurface_tip_le_pnt = avl.Point(x=x3,
                                       y=y3,
                                       z=z3)

    root_section = avl.Section(leading_edge_point=aerosurface_root_le_pnt,
                               chord=aerosurface_root_chord,
                               airfoil=avl.FileAirfoil(airfoil1_filepath))
    mid_section = avl.Section(leading_edge_point=aerosurface_mid_le_pnt,
                              chord=aerosurface_mid_chord,
                              airfoil=avl.FileAirfoil(airfoil2_filepath))
    tip_section = avl.Section(leading_edge_point=aerosurface_tip_le_pnt,
                              chord=aerosurface_tip_chord,
                              airfoil=avl.FileAirfoil(airfoil3_filepath))

    # y_duplicate=0.0 duplicates the wing over a XZ-plane at Y=0.0
    aerosurface = avl.Surface(name='aerosurface',
                              n_chordwise=8,
                              chord_spacing=avl.Spacing.cosine,
                              n_spanwise=12,
                              span_spacing=avl.Spacing.cosine,
                              y_duplicate=0.0,
                              sections=[root_section, mid_section, tip_section])

    mach = 0.01

    area_section1 = (c1 + c2) * (y2 - y1) * 0.5
    area_section2 = (c2 + c3) * (y3 - y2) * 0.5

    aerosurface_area = 2 * (area_section1 + area_section2)

    MAC_section1 = c1 - (2 * (c1 - c2) * (0.5 * c1 + c2) / (3 * (c1 + c2)))

    MAC_section2 = c2 - (2 * (c2 - c3) * (0.5 * c2 + c3) / (3 * (c2 + c3)))

    aerosurface_mac = (
        MAC_section1 * area_section1 / (area_section1 + area_section2)
        + MAC_section2 * area_section2 / (area_section1 + area_section2)
    )

    aerosurface_span = 2 * (y3 - y1)

    # calculate the m.a.c. leading edge location

    # not really sure if this point is correct for the three section surface

    def mac_le_pnt(root_chord, tip_chord, root_pnt, tip_pnt):
        pnt = ((2*root_chord*root_pnt[dim] +
                root_chord*tip_pnt[dim] +
                tip_chord*root_pnt[dim] +
                2*tip_chord*tip_pnt[dim]) /
               (3*(root_chord+tip_chord))
               for dim in range(3))
        return avl.Point(*pnt)

    le_pnt = mac_le_pnt(aerosurface_root_chord, aerosurface_tip_chord,
                        aerosurface_root_le_pnt, aerosurface_tip_le_pnt)

    ref_pnt = avl.Point(x=le_pnt.x + 0.25*aerosurface_mac,
                        y=le_pnt.y, z=le_pnt.z)

    aircraft = avl.Geometry(name='aircraft',
                            reference_area=aerosurface_area,
                            reference_chord=aerosurface_mac,
                            reference_span=aerosurface_span,
                            reference_point=ref_pnt,
                            mach=mach,
                            surfaces=[aerosurface])

    alphas = list(range(-10, 26, 1))
    results = {}
    CL_dict = {}
    CD_dict = {}
    Cm_dict = {}
    for alpha in alphas:
        case = avl.Case(name='sweep',
                        alpha=alpha)
        session = avl.Session(geometry=aircraft, cases=[case])
        results[alpha] = session.run_all_cases()['sweep']

        if (max(results[alpha]['StripForces']['aerosurface']['cl']) > airfoil_clmax):
            break
        else:
            CL_dict[float(alpha)] = (
                results[alpha]['SurfaceForces']['aerosurface']['CL']
            )
            CD_dict[float(alpha)] = (
                results[alpha]['SurfaceForces']['aerosurface']['CD']
            )
            Cm_dict[float(alpha)] = (
                results[alpha]['SurfaceForces']['aerosurface']['Cm']
            )

    CL_df = pd.DataFrame.from_dict(CL_dict, orient="index", columns=["CL"])
    CL_df.index.name = "alpha"
    CD_df = pd.DataFrame.from_dict(CD_dict, orient="index", columns=["CD"])
    CD_df.index.name = "alpha"
    Cm_df = pd.DataFrame.from_dict(Cm_dict, orient="index", columns=["Cm"])
    Cm_df.index.name = "alpha"

    return CL_dict, CD_dict, Cm_dict, CL_df, CD_df, Cm_df
