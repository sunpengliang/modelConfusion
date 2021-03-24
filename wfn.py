
#"sizes": {
#   "pedestrian": 0.5,
#    "cyclist": 1.0,
#    "car": 3.0
#  }
import numpy as np
import math



def get_ols_btw_objects(obj1, obj2, kappa):
    rng1 = obj1[0]
    agl1 = obj1[1]
    rng2 = obj2[0]
    agl2 = obj2[1]
    x1, y1 = pol2cart_ramap(rng1, agl1)
    x2, y2 = pol2cart_ramap(rng2, agl2)
    dx = x1 - x2
    dy = y1 - y2
    s_square = x1 ** 2 + y1 ** 2
    #kappa = object_sizes[class_str] / 100  # TODO: tune kappa
    e = (dx ** 2 + dy ** 2) / 2 / (s_square * kappa)
    ols = math.exp(-e)
    return ols

def pol2cart_ramap(rho, phi):
    """
    Transform from polar to cart under RAMap coordinates
    :param rho: distance to origin
    :param phi: angle (rad) under RAMap coordinates
    :return: x, y
    """
    x = rho * np.sin(phi)
    y = rho * np.cos(phi)
    return x, y

def cart2pol_ramap(x, y):
    """
    Transform from cart to polar under RAMap coordinates
    :param x: x
    :param y: y
    :return: rho, phi (rad) under RAMap coordinates
    """
    rho = (x * x + y * y) ** 0.5
    phi = np.arctan2(x, y)
    return rho, phi

def weightedmodel(box_car, box_car_new, index, times, class_name,  kappa=3/100):
    box_car_new.append(box_car[0])
    del box_car[0]
    if len(box_car) != 0:
        for r1, thea, conf, _ in box_car:
            ols = get_ols_btw_objects(box_car_new[index][:2], [r1,thea], kappa)
            if ols > 0.3:       #configure, overlap, then combine
                x1, y1 = pol2cart_ramap(box_car_new[index][0], box_car_new[index][1])
                x2, y2 = pol2cart_ramap(r1, thea)
                x = (box_car_new[index][2]*x1 + conf*x2) / (conf + box_car_new[index][2])
                y = (box_car_new[index][2]*y1 + conf*y2) / (conf + box_car_new[index][2])
                conf2 = (box_car_new[index][2] + conf)
                r2, thea2 = cart2pol_ramap(x, y)
                box_car_new[index] = [r2, thea2, conf2, class_name]
                times[index] += 1
                del box_car[box_car.index([r1, thea, conf, class_name])]
        box_car_new[index][2] /= times[index]
    return box_car, box_car_new, times

def weighted(r, thea, conf, classes_):
    box_car, box_ped, box_cyc = [], [], []
    for i in range(len(classes_)):
        if classes_[i] == "car":
            box_car.append([r[i], thea[i], conf[i], 'car'])    #r, thea, conf, car
        elif classes_[i] == "pedestrian":
            box_ped.append([r[i], thea[i], conf[i], 'pedestrian'])    #r, thea, conf, car
        else:
            box_cyc.append([r[i], thea[i], conf[i], 'cyclist'])
    # car
    box_car_new = []
    index = 0
    len_car = len(box_car)
    times = np.ones(len_car)
    while len(box_car) != 0:
        box_car, box_car_new, times = weightedmodel(box_car, box_car_new, index, times, class_name="car")
        index += 1
    for i in range(len(box_car_new)):
        box_car_new[i][2] = box_car_new[i][2] * min(times[i], 4) / 4   # 3 means number of models


    #ped
    box_ped_new = []
    index = 0
    len_ped = len(box_ped)
    times = np.ones(len_ped)
    while len(box_ped) != 0:
        box_ped, box_ped_new, times = weightedmodel(box_ped, box_ped_new, index, times, class_name="pedestrian", kappa=0.5/100)
        index += 1
    for i in range(len(box_ped_new)):
        box_ped_new[i][2] = box_ped_new[i][2] * min(times[i], 4) / 4   # 3 means number of models
    print(times)
    print(box_ped_new)


    #cyc
    box_cyc_new = []
    index = 0
    len_cyc = len(box_cyc)
    times = np.ones(len_cyc)
    while len(box_cyc) != 0:
        box_cyc, box_cyc_new, times = weightedmodel(box_cyc, box_cyc_new, index, times, class_name="cyclist", kappa=1/100)
        index += 1
    for i in range(len(box_cyc_new)):
        box_cyc_new[i][2] = box_cyc_new[i][2] * min(times[i], 4) / 4   # 3 means number of models

    return box_car_new, box_ped_new, box_cyc_new




