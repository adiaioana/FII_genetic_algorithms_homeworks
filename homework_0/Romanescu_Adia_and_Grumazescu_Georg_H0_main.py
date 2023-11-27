import math
import random
import time
import numpy as np
EPS = 0.00001

no_it = 0


def rastrigin_function(var_list, nr_dim):
    fct = 10 * nr_dim
    for i in range(0, nr_dim, 1):
        fct += var_list[i] * var_list[i] - 10 * math.cos(2 * math.pi * var_list[i])
    return fct


def michalewicz_function(var_list, nr_dim):
    fct = 0
    for i in range(0, nr_dim, 1):
        x = math.sin(var_list[i])
        for j in range(0, 20, 1):
            x = x * math.sin((i + 1) * var_list[i] * var_list[i] / math.pi)
        fct += x
    return -fct


def sphere_function(var_list, nr_dim):
    fct = 0
    for i in range(0, nr_dim, 1):
        fct += var_list[i] * var_list[i]
    return fct


def griewank_function(var_list, nr_dim):
    summ = 0
    prod = 1
    for i in range(0, nr_dim, 1):
        summ += var_list[i] * var_list[i] / 4000
    for i in range(0, nr_dim, 1):
        prod = prod * math.cos(var_list[i] / math.sqrt(i + 1))
    return summ - prod + 1


def find_local_minimum(left, right, var_list, index, y_value, nr_dim, function, ok):
    nr_searches = 0
    while True:
        nr_searches += 1
        copy_var = var_list[index]
        var_list[index] = round(random.uniform(left, right), 5)
        temp_y_value = function(var_list, nr_dim)
        if left == right or abs(temp_y_value - y_value) <= EPS:
            break
        elif temp_y_value < y_value:
            y_value = temp_y_value
            var_list[index] += EPS
            y_value_right = function(var_list, nr_dim)
            var_list[index] -= EPS
            if y_value_right > y_value:
                right = var_list[index]
            else:
                left = var_list[index]
        elif function == griewank_function:
            if ok == 0:
                right = var_list[index]
            else:
                left = var_list[index]
            var_list[index] = copy_var
    return y_value, var_list[index], nr_searches


def euristic_method(nr_tests, nr_dim, left_ext, right_ext, function):
    var_list = [0] * nr_dim
    y_values_list = []
    nr_search = 0
    start = time.time()

    for i in range(0, nr_tests, 1):
        for j in range(0, nr_dim, 1):
            var_list[j] = round(random.uniform(left_ext, right_ext), 5)

        y_value_min = function(var_list, nr_dim)

        for j in range(0, nr_dim, 1):
            var_init = var_list[j]

            y_value, var1, nr_searches1 = find_local_minimum(var_init, right_ext, var_list, j, y_value_min, nr_dim, function, 0)
            var_list[j] = var_init
            y_value2, var2, nr_searches2 = find_local_minimum(left_ext, var_init, var_list, j, y_value_min, nr_dim, function, 1)

            nr_search += nr_searches1 + nr_searches2 + 1

            if y_value < y_value2:
                y_value_min = y_value
                var_list[j] = var1
            else:
                y_value_min = y_value2


        y_values_list.append(y_value_min)

    minimum = min(y_values_list)
    end = time.time()
    return minimum, (end - start), nr_search


def scenario_bkt(n, k, choices, vec, y_values, function):
    global no_it
    if k == n + 1:
        y_values.append(function(vec, n))
        no_it = no_it + 1
        return
    else:
        for i in choices:
            vec.append(i)
            scenario_bkt(n, k + 1, choices, vec, y_values, function)
            vec.pop()
    return


def deterministic_method_bkt(nr_dim, left_ext, right_ext, step, function):
    global no_it
    no_it = 0
    y_values_list = []
    choices = np.arange(left_ext, right_ext, step)

    start = time.time()
    scenario_bkt(nr_dim, 1, choices, [], y_values_list, function)

    minimum = min(y_values_list)
    end = time.time()

    return minimum, (end - start), no_it


_method = int(input("What algorithm would you like to execute?\n1 - Deterministic, 2 - Heuristic\n"))

if _method == 1:
    _step = float(input("You chose deterministic. What step would you like to have between 2 consecutive neighbors?\n"
                      "Example: 0.5, 0.05, 0.005 etc.\n"
                      "Attention! Be aware that for a small step and for a large dimension, the solving"
                      " time might be unreasonable!\n"))

_nr_func = int(input("What function would you want to solve?\n"
                     "1 - Rastrigin, 2 - Michalewicz, 3 - Sphere, 4 - Griewank\n"))

_nr_dim = int(input("Give me the dimension for the problem:\n"))

if _nr_func == 1:
    _function = rastrigin_function
    _nr_tests = 10
    _left_ext = -5.12
    _right_ext = 5.12
elif _nr_func == 2:
    _function = michalewicz_function
    _nr_tests = 10
    _left_ext = 0
    _right_ext = math.pi
elif _nr_func == 3:
    _function = sphere_function
    _nr_tests = 10
    _left_ext = -5.12
    _right_ext = 5.12
else:
    _function = griewank_function
    _nr_tests = 1000
    _left_ext = -600
    _right_ext = 600

if _method == 1:
    comp_value_min, time_elapsed, nr_searches = deterministic_method_bkt(_nr_dim,
                                                                         _left_ext,
                                                                         _right_ext,
                                                                         _step,
                                                                         _function)
else:
    comp_value_min, time_elapsed, nr_searches = euristic_method(_nr_tests,
                                                                _nr_dim,
                                                                _left_ext,
                                                                _right_ext,
                                                                _function)



print(f"Minimum computed value: {'{:.5f}'.format(comp_value_min)}")
print(f"Elapsed time: {'{:.5f}'.format(time_elapsed)} seconds.")
print(f"Number of searches (different sets of variables): {'{:,}'.format(nr_searches)}.\n")
