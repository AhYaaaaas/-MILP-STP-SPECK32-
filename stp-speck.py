roundTimes = 9
left_input, right_input, left_output, right_output = [[] for i in range(4)]
a, b = [7, 2]
r = []
variables = []
BITVETOR = []
BITCONDITION = []
edge = "0bin" + "{:08b}".format(30)


def move_left(left_word, time, f):
    temp = F"L_MOV_{time}"
    BITVETOR.append(F"{temp} : BITVECTOR(16);")
    BITCONDITION.append(f"ASSERT({temp} = {left_word}[6:0]@{left_word}[15:7]);")
    return temp


def left_part(left_word, right_word, result_word, time, f):
    left_word = move_left(left_word, time, f)
    L = eq(f'({left_word}<<1)[15:0]', f'({right_word}<<1)[15:0]', f'({result_word}<<1)[15:0]')
    R_temp = f"BVXOR({left_word},BVXOR({right_word},{result_word}))"
    R = f"BVXOR(({right_word}<<1)[15:0],{R_temp})"
    R = f"({L})" + " & " + f"({R})"
    return f"ASSERT(({R}) = 0bin0000000000000000);"


def eq(a, b, c):
    return f"BVXOR(~({a}),{b})" + ' & ' + f"BVXOR(~({a}),{c})"


def funct_r(a, b, c):
    return f"~({eq(a, b, c)})"


for i in range(1, roundTimes + 1):
    left_input.append(f'L_I_{i}')
    left_output.append(f'L_O_{i}')
    right_input.append(f'R_I_{i}')
    right_output.append(f'R_O_{i}')
    r.append(f"r{i}")
with open('speck_stp1.cvc', 'w') as f:
    for i in range(roundTimes):
        BITVETOR.append(left_input[i] + " : BITVECTOR(16);")
        BITVETOR.append(left_output[i] + " : BITVECTOR(16);")
        BITVETOR.append(right_input[i] + " : BITVECTOR(16);")
        BITVETOR.append(right_output[i] + " : BITVECTOR(16);")
        BITVETOR.append(r[i] + " : BITVECTOR(16);")
    # build right
    for j in range(1, roundTimes + 1):
        if not j == 1:
            BITCONDITION.append(f"ASSERT(R_I_{j} = R_O_{j - 1});")
            BITCONDITION.append(f"ASSERT(L_I_{j} = L_O_{j - 1});")
        BITCONDITION.append(f"ASSERT(R_O_{j} = BVXOR(L_O_{j},R_I_{j}[13:0]@R_I_{j}[15:14]));")
    # build left
    for k in range(1, roundTimes + 1):
        BITCONDITION.append(left_part(left_input[k - 1], right_input[k - 1], left_output[k - 1], k, f))
        BITCONDITION.append(f"ASSERT(r{k} = {funct_r(f'L_MOV_{k}', right_input[k - 1], left_output[k - 1])});")
    QUERY = 'ASSERT(BVPLUS(8,'
    for top_index in range(1, roundTimes + 1):
        for bottom_index in range(1, 16):
            if not (top_index == roundTimes and bottom_index == 15):
                QUERY += f"0bin0000000@{r[top_index - 1]}[{bottom_index - 1}:{bottom_index - 1}],"
            else:
                QUERY += f"0bin0000000@{r[top_index - 1]}[{bottom_index - 1}:{bottom_index - 1}]"
    QUERY += f")={edge});"
    # 0bin00011101
    BITCONDITION.append(QUERY)
    BITCONDITION.append("QUERY(FALSE);")
    for vector in BITVETOR:
        f.write(vector)
        f.write("\n")
    head = "ASSERT(BVGT(BVPLUS(16,L_I_1,R_I_1), 0bin0000000000000000));"
    f.write(head)
    f.write("\n")
    for c in BITCONDITION:
        f.write(c)
        f.write("\n")
    f.write("COUNTEREXAMPLE;")
    f.close()
