import time
import random
import math


def rastrigin_function(var_list):
    nr_dim = len(var_list)
    fct = 10 * nr_dim
    for i in range(0, nr_dim, 1):
        fct += var_list[i] * var_list[i] - 10 * math.cos(2 * math.pi * var_list[i])
    return fct


def michalewicz_function(var_list):
    nr_dim = len(var_list)
    fct = 0
    for i in range(0, nr_dim, 1):
        x = math.sin(var_list[i])
        for j in range(0, 20, 1):
            x = x * math.sin((i + 1) * var_list[i] * var_list[i] / math.pi)
        fct += x
    return -fct


def schwefel_function(var_list):
    nr_dim = len(var_list)
    fct = 0
    for i in range(0, nr_dim, 1):
        fct += var_list[i] * math.sin(math.sqrt(abs(var_list[i])))
    return -fct


def dejong_function(var_list):
    nr_dim = len(var_list)
    fct = 0
    for i in range(0, nr_dim, 1):
        fct += var_list[i] * var_list[i]
    return fct


def bitstring_to_float(bit_array):
    float_array = [0] * dim
    for i in range(0, dim, 1):
        for j in range(0, nr_bit_1var, 1):
            float_array[i] *= 2
            float_array[i] += bit_array[i * nr_bit_1var + j]
        float_array[i] = float_array[i] / (2 ** nr_bit_1var - 1)
        float_array[i] *= (right_ext - left_ext)
        float_array[i] += left_ext
    return float_array


def best_improvement(best_value, bits, nr_bits, function):
    best_bits = bits.copy()
    for i in range(0, nr_bits, 1):
        bits[i] = 1 - bits[i]
        value = function(bitstring_to_float(bits))
        if best_value > value:
            best_value = value
            best_bits = bits.copy()
        bits[i] = 1 - bits[i]
    return best_value, best_bits


def worst_improvement(best_value, bits, nr_bits, function):
    best_bits = bits.copy()
    ok = False
    for i in range(0, nr_bits, 1):
        bits[i] = 1 - bits[i]
        value = function(bitstring_to_float(bits))
        if best_value > value:
            if not ok:
                ok = True
                possible_value = value
                possible_i = i
            elif value > possible_value:
                possible_value = value
                possible_i = i
        bits[i] = 1 - bits[i]
    if ok:
        best_value = possible_value
        best_bits[possible_i] = 1 - best_bits[possible_i]
    return best_value, best_bits


def first_improvement(best_value, bits, nr_bits, function):
    best_bits = bits.copy()
    indexes = random.sample(range(0, nr_bits), nr_bits)
    for i in range(0, nr_bits, 1):
        bits[indexes[i]] = 1 - bits[indexes[i]]
        value = function(bitstring_to_float(bits))
        if best_value > value:
            best_value = value
            best_bits = bits.copy()
            break
        bits[indexes[i]] = 1 - bits[indexes[i]]
    return best_value, best_bits


def simulated_annealing(nr_iter, nr_bits, function, improve_function):
    start = time.time()
    t = 0
    bits = [0] * nr_bits
    best = float('inf')
    nr = 0
    epsilon = 0.0001

    while True:
        for i in range(0, nr_bits, 1):
            bits[i] = random.randint(0, 1)
        val_cand = cpy_val_cand = function(bitstring_to_float(bits))

        T = 1000
        cooling_ratio = 0.99
        iter2 = 0
        bit_place = -1
        ok = True

        while T > epsilon and ok:
            iter = 0

            while True:
                val_neigh, bits = improve_function(val_cand, bits, nr_bits, function)
                if val_neigh == cpy_val_cand and bit_place < nr_bits - 1:
                    bit_place += 1
                    val_cand = val_neigh
                else:
                    if bit_place + 1 == nr_bits:
                        ok = False
                        break
                    bit_place = -1

                if val_neigh < val_cand:
                    val_cand = cpy_val_cand = val_neigh
                else:
                    if iter >= 30:
                        break

                    bits[bit_place] = 1 - bits[bit_place]
                    val_neigh = function(bitstring_to_float(bits))
                    x = random.uniform(0, 1)
                    p = math.exp(-(val_neigh - val_cand) / T)

                    if x < p:
                        nr = nr + 1
                        val_cand = val_neigh
                    else:
                        bits[bit_place] = 1 - bits[bit_place]
                        break

                iter += 1

            iter2 += 1
            T = pow(cooling_ratio, iter2) * 1000

            if val_cand < best:
                best = val_cand

        t += 1
        if t == nr_iter:
            break

    end = time.time()
    return best, end - start


def hill_climbing(nr_iter, nr_bits, function, improve_function):
    start = time.time()
    t = 0
    bits = [0] * nr_bits
    best = float('inf')

    while True:
        for i in range(0, nr_bits, 1):
            bits[i] = random.randint(0, 1)
        val_cand = function(bitstring_to_float(bits))

        while True:
            val_neigh, bits = improve_function(val_cand, bits, nr_bits, function)
            if val_neigh < val_cand:
                val_cand = val_neigh
            else:
                break

        if val_cand < best:
            best = val_cand

        t += 1
        if t == nr_iter:
            break

    end = time.time()
    return best, (end - start)


x = int(input("What function would you like to test?\n"
              "1 - Rastrigin's Function\n"
              "2 - De Jong's Function\n"
              "3 - Michalewicz's Function\n"
              "4 - Schwefel's Function\n"
              "Your option: "))

while x != 1 and x != 2 and x != 3 and x != 4:
    x = int(input("This isn't a valid option. Please, try again!\nYour option: "))

dim = int(input("Please enter a dimension for the function: "))

precision = 3
nr_iter = 2 * [0]
function_name = ['Rastrigin', 'De Jong 1', 'Michalewicz', 'Schwefel']

if x == 1:
    function = rastrigin_function
    left_ext = -5.12
    right_ext = 5.12
    if dim == 30:
        nr_iter[0] = 1000
        nr_iter[1] = 10
    elif dim == 10:
        nr_iter[0] = 1000
        nr_iter[1] = 10
    else:
        nr_iter[0] = 10000
        nr_iter[1] = 100
elif x == 2:
    function = dejong_function
    left_ext = -5.12
    right_ext = 5.12
    nr_iter[1] = 1
    if dim == 30:
        nr_iter[0] = 10
    elif dim == 10:
        nr_iter[0] = 100
    else:
        nr_iter[0] = 1000
elif x == 3:
    function = michalewicz_function
    left_ext = 0
    right_ext = math.pi
    if dim == 30:
        nr_iter[0] = 100
        nr_iter[1] = 10
    elif dim == 10:
        nr_iter[0] = 1000
        nr_iter[1] = 100
    else:
        nr_iter[0] = 10000
        nr_iter[1] = 1000
else:
    function = schwefel_function
    left_ext = -500
    right_ext = 500
    if dim == 30:
        nr_iter[0] = 10
        nr_iter[1] = 10
    elif dim == 10:
        nr_iter[0] = 100
        nr_iter[1] = 100
    else:
        nr_iter[0] = 1000
        nr_iter[1] = 1000

nr_val_1D = (right_ext - left_ext) * (10 ** precision)
nr_val = nr_val_1D ** dim
nr_bit_1var = math.ceil(math.log2(nr_val_1D))
nr_bit_dvar = nr_bit_1var * dim

alg = int(input("What algorithm do you want to apply?\n"
                "1 - Hill Climbing\n"
                "2 - Simulated Annealing\n"
                "Your option: "))

while alg != 1 and alg != 2:
    alg = int(input("This isn't a valid option. Please, try again!\nYour option: "))

if alg == 1:
    improve = int(input("What kind of improvement (in searching for the neighbours) would you like to be used?\n"
                        "1 - Best Improvement\n"
                        "2 - First Improvement\n"
                        "3 - Worst Improvement\n"
                        "Your option: "))

    while improve != 1 and improve != 2 and improve != 3:
        improve = int(input("This isn't a valid option. Please, try again!\nYour option: "))

    if improve == 1:
        improve_function = best_improvement
    elif improve == 2:
        improve_function = first_improvement
    else:
        improve_function = worst_improvement

    minValue, elapsed_time = hill_climbing(nr_iter[0], nr_bit_dvar, function, improve_function)

    print(f"\nFunction: {function_name[x-1]} --- Dimension: {dim} --- Iterations: {nr_iter[0]}")
    print(f"Elapsed Time: {'{:.5f}'.format(elapsed_time)}s")

    if improve == 1:
        print(f"Hill Climbing with Best Improvement: {'{:.5f}'.format(minValue)}")
    elif improve == 2:
        print(f"Hill Climbing with First Improvement: {'{:.5f}'.format(minValue)}")
    else:
        print(f"Hill Climbing with Worst Improvement: {'{:.5f}'.format(minValue)}")
else:
    minValue, elapsed_time = simulated_annealing(nr_iter[1], nr_bit_dvar, function, best_improvement)

    print(f"\nFunction: {function_name[x-1]} --- Dimension: {dim} --- Iterations: {nr_iter[1]}")
    print(f"Elapsed Time: {'{:.5f}'.format(elapsed_time)}s")
    print(f"Simulated Annealing: {'{:.5f}'.format(minValue)}")
