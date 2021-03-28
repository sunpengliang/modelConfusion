import math
import numpy as np

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


def calculate_x(r, thea):
    x1, y1 = pol2cart_ramap(r, thea)
    return x1, y1


def calculate_thea(x, y):
    r1, thea1 = cart2pol_ramap(x, y)
    return r1, thea1

def weightedmodel(box_car, box_car_new, index, class_name,  kappa=3/100):
    total_box = []
    box_car_new.append(box_car[0])
    flag = False
    total_box.append(box_car[0][:3])
    del box_car[0]
    if len(box_car) == 0:
        del box_car_new[index]

    if len(box_car) != 0:
        box_car_copy = box_car.copy()
        for r1, thea, conf, _ in box_car:
            #print("index",index)
            ols = get_ols_btw_objects(box_car_new[index][:2], [r1,thea], kappa)
            if ols > 0.3:       #configure, overlap, then combine
                total_box.append([r1,thea,conf])
                del box_car_copy[box_car_copy.index([r1, thea, conf, class_name])]

        box_car = box_car_copy

        if len(total_box) > 1:
            x, y, conf = [], [], []
            for r1,thea1,conf1 in total_box:
                x1, y1 = calculate_x(r1,thea1)
                x.append(x1)
                y.append(y1)
                conf.append(conf1)
            up_result_x = np.multiply(conf, x)
            up_result_y = np.multiply(conf, y)
            up_xnew = np.sum(up_result_x) / np.sum(conf)
            up_ynew = np.sum(up_result_y) / np.sum(conf)
            r_final, thea_final = calculate_thea(up_xnew, up_ynew)
            box_car_new[index] = [r_final,thea_final,np.sum(conf)/len(total_box) * min(len(total_box), 4) / 4, class_name]
        else:
            if index == 0:
                flag = True

    return box_car, box_car_new,total_box, flag

def weighted(r, thea, conf, classes_):
    box_car, box_ped, box_cyc = [], [], []
    for i in range(len(classes_)):
        if classes_[i] == "car":
            box_car.append([r[i], thea[i], conf[i], 'car'])    #r, thea, conf, car
        elif classes_[i] == "pedestrian":
            box_ped.append([r[i], thea[i], conf[i], 'pedestrian'])    #r, thea, conf, car
        else:
            box_cyc.append([r[i], thea[i], conf[i], 'cyclist'])

    def cal_box(total_box, flag, box_car_new):

        if len(total_box) <= 1:
            if len(box_car_new) == 0:
                return 0,box_car_new
            del box_car_new[-1]
            if flag:
                return 0,box_car_new
            else:
                return -1,box_car_new
        else:
            return 1, box_car_new

    # car
    box_car_new = []
    index = 0
    len_car = len(box_car)
    while len(box_car) != 0:
        box_car, box_car_new,total_box, flag= weightedmodel(box_car, box_car_new, index,  class_name="car")
        index1,box_car_new = cal_box(total_box, flag,box_car_new)
        index += index1

    #ped
    box_ped_new = []
    index = 0
    len_ped = len(box_ped)
    while len(box_ped) != 0:
        box_ped, box_ped_new,total_box,flag= weightedmodel(box_ped, box_ped_new, index,  class_name="pedestrian", kappa=0.5/100)
        index1, box_ped_new = cal_box(total_box, flag, box_ped_new)
        index += index1

    #cyc
    box_cyc_new = []
    index = 0
    len_cyc = len(box_cyc)

    while len(box_cyc) != 0:
        box_cyc, box_cyc_new,total_box,flag = weightedmodel(box_cyc, box_cyc_new, index, class_name="cyclist", kappa=1/100)
        index1, box_cyc_new = cal_box(total_box, flag, box_cyc_new)
        index += index1


    return box_car_new, box_ped_new, box_cyc_new




