def eff_t(t_c, h):
    """
    t: mean temparature of the air
    h: relative humidity
    """
    t = t_c * 1.8 + 32
    c1 = -42.379
    c2 = 2.04901523
    c3 = 10.14333127
    c4 = -0.224755
    c5 = -6.83783e-3
    c6 = -5.481717e-2
    c7 = 1.22874e-3
    c8 = 8.5252e-4
    c9 = -1.99e-6
    if t > 80:
        et = c1 + c2*t + c3*h + c4*t*h + c5*t*t + c6*h*h + c7*t*t*h + c8*t*h*h + c9*t*t*h*h
        if h < 13:
            et -= ((13.-h)/4)*((17-abs(t-95.))/17.)**0.5
        elif t < 87 and h > 85:
            et += ((h-85.)/10.) * ((87-t)/5.)

    else:
        et = 0.5 * (t + 61.0 + ((t-68.0)*1.2) + (h*0.094))
    et_c = (et - 32.) * 5 / 9.
    return et_c


def TC_score(effective_t):
    """
    et: effective temperature
    """
    tc_dict = {(39,100): 0, (37,39):2, (35,37):4, (33,35):5, (31,32):6, (29,31):7,
               (27,29):8, (26,27):9, (23,26):10, (20,23):9, (18,20):7, (15,18):6, (11,15):5,
               (7,11):4, (0,7):3, (-5,0):2, (-100,-5):0}   
    score = classifier(tc_dict, effective_t)

    return score


def A_score(cloud):
    """
    cloud: percentage of cloud cover
    """
    a_dict = {(0,10):9, (10,20):10, (20,30):9, (30,40):8, (40,50):7, (50,60):6, 
              (60,70):5, (70,80):4, (80,90):3, (90,99):2, (99,101):1}
    score = classifier(a_dict, cloud)

    return score

def P_score(precipitation, wind, chill):
    """
    precipitation: daily precipitation(mm)
    wind: wind speed(km/h)
    chill: wind chill(watts/ms/h)
    """
    precip_score = None
    wind_score = None
    precip_dict = {(0,0.01):10., (0.01,3.):9., (3.,6.):8.,
                   (6.,9.):5., (9.,12.):2., (12.,25.):0., (25.,1000.):-1}
    wind_dict = {(0,1):9, (1,10):10, (10,20):9, (20,30):8,
                 (30,40):6, (40,50):3, (50,70):0, (70,100):-5, (100,1000):-10}
    precip_score = classifier(precip_dict, precipitation)
    wind_score = classifier(wind_dict, wind)

    p_score = (precip_score * 3. + wind_score) / 4.

    return p_score


def classifier(target_dict, w_value):
    score = None
    for t_range in target_dict.keys():
        if w_value >= t_range[0] and w_value < t_range[1]:
            score = target_dict[t_range]
            break
    if score == None:
        raise NotImplementedError

    return score

def HCI_index(temperature, humidity, cloud, precipitation, wind, chill):
    effective_t = eff_t(temperature, humidity)
    TC = TC_score(effective_t)
    P = P_score(precipitation, wind, chill)
    A = A_score(cloud)
    hci = 4*TC + 2*P + 4*A
    return hci

if __name__ == "__main__":
    print(TC_score(eff_t(25, 10)))