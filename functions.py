def baby_step_giant_step_dl(mod, gen, order, target):
    """Uses the baby step giant step algorithm to compute discrete log of
    target with respect to gen.

    Parameters:
        mod (int): The prime modulus over which computation is carried out.
        gen (int): An element of Z*_mod.
        order (int): The order of the subgroup generated by gen.
        target (int): The element whose discrete log is to be computed.

    Returns:
        int: The discrete log of target with respect to gen.
    """
    m = int(order ** 0.5) + 1
    table = {}
    v = 1
    for j in range(m):
        table[v] = j
        v = (v * gen) % mod

    invg = pow(gen, -m, mod)
    current = target
    for i in range(m):
        if current in table:
            return i * m + table[current]
        current = (current * invg) % mod


def crt(vals, mods):
    """Solves a system of congruences.

    Parameters:
        vals (list(int)): A list of values.
        mods (list(int)): A list of moduli which are pairwise coprime i.e., mod[i] and mod[j] are
            coprime for any i ≠ j. The length of this list is equal to that of vals.

    Returns:
        int: An integer z such that for every i in {0, .., len(vals) - 1}, z ≡ vals[i] mod mods[i].
    """
    n = len(vals)
    x = 0

    M = 1
    for i in range(n):
        M *= mods[i]
    for i in range(n):
        m_div = M // mods[i]
        n_div = pow(m_div, -1, mods[i])
        x = (x + vals[i] * m_div * n_div) % M
    
    return x


def discrete_log_prime_power(mod, gen, p, e, target):
    x = 0

    gamma = pow(gen, pow(p, e - 1), mod)

    p_pow = 1
    for k in range(0, e):
        h_k = pow(pow(gen, -x, mod) * target % mod, pow(p, e-1-k), mod)

        x_curr = baby_step_giant_step_dl(mod, gamma, p, h_k)

        x += x_curr * p_pow
        p_pow *= p

    return x


def pohlig_hellman(mod, gen, factors, target):
    """Uses the Pohlig-Hellman algorithm to compute discrete log of target with
    respect to gen, given the factorization of the order of the subgroup
    generated by gen.

    Parameters:
        mod (int): The prime modulus over which computation is carried out.
        gen (int): An element of Z*_mod.
        factors (list(int, int)): A list of values [(p_1, e_1), ..., (p_n, e_n)] such that the order
            of the subgroup generated by gen is p_1^{e_1} * ... * p_n^{e_n}.
        target (int): The element whose discrete log is to be computed.

    Returns:
        int: The discrete log of target with respect to gen.
    """

    vals = []
    mods = []

    order = mod - 1

    for p, e in factors:
        print(p, e)
        small_mod = p ** e
        y = order // small_mod

        gen_y = pow(gen, y, mod)
        target_y = pow(target, y, mod)

        x = discrete_log_prime_power(mod, gen_y, p, e, target_y)
        vals.append(x)
        mods.append(small_mod)
    return crt(vals, mods)


def elgamal_attack(params, pk):
    """
    Given an ElGamal public key in Z*_mod, where mod is prime, recovers the corresponding secret
    key when mod - 1 has sufficiently many 'small' prime factors.

    Parameters:
        params (Params): ElGamal parameters. It is an instance of the Params class defined in
            problem.py.
        pk (int): The ElGamal public key.

    Returns:
        int: The discrete log of pk with respect to gen.
    """
    subgroup_order = 1
    selected_factors = []

    for p, e in params.factors:
        factor_group_size = p ** e

        subgroup_order *= factor_group_size
        selected_factors.append([p, e])

        if (subgroup_order >= params.exp_bound):
            break

    return pohlig_hellman(params.mod, params.gen, selected_factors, pk)
