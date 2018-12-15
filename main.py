import random
import math


def f(x):
    return math.sin(x) + 0.5


def generate_alpha(r, M):
    alpha_M_1 = random.uniform(0, 1)
    alpha = list()
    alpha.append(alpha_M_1)
    r_range = int((r - 1) / 2)
    for _ in range(r_range):
        el = 0.5 * random.uniform(0, 1 - sum(i for i in alpha))
        alpha.append(el)
        alpha.insert(0, el)
    return alpha


def Chebyshev_dis_f_for_w(f_filter):
    m_max = 0
    for index in range(1, len(f_filter), 1):
        el = abs(f_filter[index] - f_filter[index - 1])
        m_max = max(el, m_max)
    return m_max


def Chebyshev_dis_f_for_d(f_filter, f_noize):
    f_noize = f_noize[1:-1:1]
    m_max = 0
    for index in range(0, len(f_filter), 1):
        el = abs(f_filter[index] - f_noize[index])
        m_max = max(el, m_max)
    return m_max


def Chebyshev_dis_w_d(w, d):
    return max(w, d)


def fun_J(h, w, d):
    return h * w + (1 - h) * d


def f_noize(a, K):
    x_min = 0
    x_max = math.pi
    f_list = list()
    for k in K:
        x_k = x_min + k * (x_max - x_min) / (len(K) - 1)
        el = f(x_k) + random.uniform(-a, a)
        f_list.append(el)
        # print('(', x_k, ";", el, ')')
    return f_list


def f_filter(f_noiz, alpha, K, M):
    f_list = list()
    for k in K:
        if k < M + 1:
            continue
        j_start = k - M
        j_end = k + M + 1
        s = 0
        x_k = x_min + k * (x_max - x_min) / (len(K) - 1)
        for j in range(j_start, j_end, 1):
            f_n_el = f_noiz[j - 1]
            alpha_el = alpha[j + M + 1 - k - 1]
            el = (f_n_el ** 2 * alpha_el) ** 0.5
            s += el
        # print('(', x_k, ";", s, ')')
        f_list.append(el)
    return f_list


r = 3  # r = 5
M = int((r - 1) / 2)
x_min = 0
x_max = math.pi
K = [i for i in range(101)]
a = 0.5 / 2
H = [i / 10 for i in range(11)]
P = 0.95
e = 0.01
N = math.log(1 - P, math.e) / math.log(1 - (e / (x_max - x_min)), math.e)
N = math.ceil(N)

# aa = generate_alpha(r, M)
# f_n = f_noize(a, K)
# f_f = f_filter(f_n, aa, K, M)
# new_f_n = f_n[1:-1:1]
# print(len(new_f_n), len(f_f))

dict_h = {}
for h in H:
    min_J = 100
    min_alpha = [0, 0, 0]
    min_w = 0
    min_d = 0
    min_f_f = None
    min_f_n = None
    for _ in range(N):
        alpha = generate_alpha(r, M)
        f_n = f_noize(a, K)
        f_f = f_filter(f_n, alpha, K, M)
        w = Chebyshev_dis_f_for_w(f_f)
        d = Chebyshev_dis_f_for_d(f_f, f_n)
        J = fun_J(h, w, d)
        if J < min_J:
            min_alpha = alpha
            min_J = J
            min_w = w
            min_d = d
            min_f_f = f_f
            min_f_n = f_n
    dict_h.update({h: [min_J, min_alpha, min_w, min_d, min_f_f, min_f_n]})

need_h = -1

min_dis = 100
for h, l in dict_h.items():
    dis = Chebyshev_dis_w_d(l[2], l[3])
    if dis > min_dis:
        break
    if dis < min_dis:
        min_dis = dis
        need_h = h

print(need_h, dict_h[need_h])
