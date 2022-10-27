var_ineqs = [
    [0, 1, -1, 0, 0, 0, 1, 0],
    [1, -1, 0, 0, 0, 0, 1, 0],
    [-1, 0, 1, 0, 0, 0, 1, 0],
    [-1, -1, -1, 0, 0, 0, -1, 3],
    [1, 1, 1, 0, 0, 0, -1, 0],
    [0, -1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, -1, 1, 1, 0],
    [0, 1, 0, -1, 1, 1, 1, 0],
    [1, 0, 0, 1, 1, -1, 1, 0],
    [0, 0, 1, -1, -1, -1, 1, 2],
    [0, -1, 0, 1, -1, -1, 1, 2],
    [0, -1, 0, -1, 1, -1, 1, 2],
    [0, -1, 0, -1, -1, 1, 1, 2]
]

var_ineqs_eq = [
    [0, 1, -1, -1, 1],
    [1, -1, 0, -1, 1],
    [-1, 0, 1, -1, 1],
    [-1, -1, -1, 1, 2]
]

[left_offset, right_offset] = [7, 2]


# L_in = (L_in_roundTime_0,L_in_roundTime_1,.....)
# R_in = (R_in_roundTime_0,R_in_roundTime_1,.....)
# eq = eq_roundTime_bit
def left_part_offset(L_in):
    return L_in[9:16] + L_in[0:9]


def right_part_offset(R_in):
    return R_in[2:16] + R_in[0:2]


def getAddIneqs(L_in, R_in, roundTime):
    n = 16
    global eq_s
    global eq_variables
    global count
    global none_zero_diffInput
    L_in = left_part_offset(L_in)
    roundTime = str(roundTime)
    left_out = []
    s = ""
    for var in range(16):
        left_out.append("L_out" + "_" + roundTime + "_" + str(var))
        if var == 15:
            s += "L_out" + "_" + roundTime + "_" + str(var) + " "
        else:
            s += "L_out" + "_" + roundTime + "_" + str(var) + " + "
    s += ">= 1"
    first_condition.append(L_in[n - 1] + " + " + R_in[n - 1] + " + " + left_out[n - 1] + " <= 2")
    first_condition.append("temp" + roundTime + " - " + L_in[n - 1] + " >= 0 ")
    first_condition.append("temp" + roundTime + " - " + R_in[n - 1] + " >= 0 ")
    first_condition.append("temp" + roundTime + " - " + left_out[n - 1] + " >= 0 ")
    first_condition.append(
        left_out[n - 1] + " + " + R_in[n - 1] + " + " + L_in[n - 1] + " - 2 temp" + roundTime + " >= 0")
    for bit in range(15, 0, -1):
        eq = "eq" + str(count)
        count += 1
        eq_variables.append(eq)
        if bit == 1 and roundTime == "5":
            eq_s += eq
        else:
            eq_s += eq + " + "
        a = [L_in[bit], R_in[bit], left_out[bit]]
        b = [L_in[bit - 1], R_in[bit - 1], left_out[bit - 1]]
        container.append(a[1] + ' - ' + a[2] + ' + ' + eq + ' >= 0 ')
        container.append(a[0] + ' - ' + a[1] + ' + ' + eq + ' >= 0 ')
        container.append(a[2] + ' - ' + a[0] + ' + ' + eq + ' >= 0 ')
        container.append(a[0] + ' + ' + a[1] + ' + ' + a[2] + ' + ' + eq + ' <= 3 ')
        container.append(a[0] + ' + ' + a[1] + ' + ' + a[2] + ' - ' + eq + ' >= 0 ')
        container.append(b[0] + ' + ' + b[1] + ' + ' + b[2] + ' + ' + eq + ' - ' + a[1] + ' >= 0 ')
        container.append(a[1] + ' + ' + b[0] + ' - ' + b[1] + ' + ' + b[2] + ' + ' + eq + ' >= 0 ')
        container.append(a[1] + ' - ' + b[0] + ' + ' + b[1] + ' + ' + b[2] + ' + ' + eq + ' >= 0 ')
        container.append(a[0] + ' + ' + b[0] + ' + ' + b[1] + ' - ' + b[2] + ' + ' + eq + ' >= 0 ')
        container.append(a[2] + ' - ' + b[0] + ' - ' + b[1] + ' - ' + b[2] + ' + ' + eq + ' >= -2 ')
        container.append(b[0] + ' - ' + a[1] + ' - ' + b[1] + ' - ' + b[2] + ' + ' + eq + ' >= -2 ')
        container.append(b[1] + ' - ' + a[1] + ' - ' + b[0] + ' - ' + b[2] + ' + ' + eq + ' >= -2 ')
        container.append(b[2] + ' - ' + a[1] + ' - ' + b[0] + ' - ' + b[1] + ' + ' + eq + ' >= -2 ')
    return left_out


def getRightOut(L_in, R_in, roundTime):
    global none_zero_diffInput
    roundTime = str(roundTime)
    R_in = right_part_offset(R_in)
    right_out = []
    for i in range(16):
        right_out.append("R_out" + "_" + roundTime + "_" + str(i))
    for i in range(16):
        xorContainer.append(L_in[i] + " + " + R_in[i] + " + " + right_out[i] + " <= 2 ")
        xorContainer.append("temp_" + roundTime + "_" + str(i) + " - " + L_in[i] + " >= 0 ")
        xorContainer.append("temp_" + roundTime + "_" + str(i) + " - " + R_in[i] + " >= 0 ")
        xorContainer.append("temp_" + roundTime + "_" + str(i) + " - " + right_out[i] + " >= 0 ")
        xorContainer.append(
            L_in[i] + " + " + R_in[i] + " + " + right_out[i] + " - 2 temp_" + roundTime + "_" + str(i) + " >= 0 ")
    return right_out


def generator():
    for i in range(16):
        left_in.append("L_in_1_" + str(i))
    for j in range(16):
        right_in.append("R_in_1" + "_" + str(j))


# def getVariable():
#     right_out = []
#     left_out = []
#     for i in range(1, 10):
#         for var in range(16):
#             left_out.append("L_out" + "_" + str(i) + "_" + str(var))
#         for j in range(16):
#             right_out.append("R_out" + "_" + str(i) + "_" + str(j))
#     for i in range(1, 10):
#         temp_container.append("temp" + str(i))
#         for j in range(16):
#             temp_container.append("temp_" + str(i) + "_" + str(j))
#     global variables
#     variables += left_out + right_out


def getVariables(C):
    V = set([])
    for s in C:
        temp = s.strip()
        temp = temp.replace('+', ' ')
        temp = temp.replace('-', ' ')
        temp = temp.replace(' >=', ' ')
        temp = temp.replace(' <=', ' ')
        temp = temp.split()
        for v in temp:
            if not v.isdecimal():  # isdecimal () 方法检查字符串是否只包含十进制字符
                V.add(v)
    return V


count = 1
left_in = []
right_in = []
container = []
xorContainer = []
eqContainer = []
variables = []
eq_variables = []
none_zero_diffInput = []
first_condition = []
temp_container = []
eq_s = ""
s = ""
stp_container = []
if __name__ == '__main__':
    generator()
    for i in range(16):
        s += left_in[i] + " + "
    for i in range(16):
        if i == 15:
            s += right_in[i] + " "
        else:
            s += right_in[i] + " + "
    s += ">= 1 "
    none_zero_diffInput.append(s)

    variables += left_in + right_in
    for i in range(1, 6):
        left_in = getAddIneqs(left_in, right_in, i)
        right_in = getRightOut(left_in, right_in, i)
    res = getVariables(none_zero_diffInput + container + xorContainer + first_condition)
    print(len(res))
    with open("diff-speck.lp", "w") as f:
        f.write("Minimize")
        f.write("\n")
        f.write(eq_s)
        f.write("\n")
        f.write('Subject To\n')
        for j in none_zero_diffInput:
            f.write(" ")
            f.write(j)
            f.write("\n")
        for v in container:
            f.write(" ")
            f.write(v)
            f.write("\n")
        for e in xorContainer:
            f.write(" ")
            f.write(e)
            f.write("\n")
        for k in first_condition:
            f.write(" ")
            f.write(k)
            f.write("\n")
        f.write('Binary')
        f.write("\n")
        for item in res:
            f.write(" ")
            f.write(item)
            f.write("\n")
        f.write("End")
        f.write("\n")
    f.close()
