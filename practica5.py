
def __main__(self, v_i, s_i):
    # Ri(N) = [Ni(N-1)+1] x Si
    # (N-1) es el número de trabajos
    r_i = []
    r = 0
    self.s_i = s_i
    x = 0
    x_i = 0
    n_i = 0
    self.v_i = v_i
    u_i = 0
    z = 0
    trabajos = 0

    for i in range(trabajos):
        r_i[i] = (n_i * (trabajos - 1)) * s_i
        r = sum(v_i * r_i)
        x = i / (z * r)
        n_i = x * v_i
        x_i = x * v_i
        u_i = x * v_i * s_i

    # Imprimir id + ri + r + x + ni
    # Imprimir r y x como los datos más importantes

if __name__ == '__main__':
    __main__()