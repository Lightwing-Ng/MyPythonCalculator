# -*- coding:utf-8 -*-
# Author: Lightwing Ng

import re
import functools


def formatNum(num):
    float = num - int(num)
    num = str(int(num))
    result = ''
    count = 0

    for i in num[::-1]:
        count += 1
        result += i
        if count % 3 == 0:
            result += ','

    result = result[::-1].strip(',')
    float = str(float)
    result += float[1:5]
    return result


def remove_duplicates(formula):
    formula = formula.replace("++", "+")
    formula = formula.replace("+-", "-")
    formula = formula.replace("-+", "-")
    formula = formula.replace("--", "+")
    formula = formula.replace("- -", "+")
    return formula


def compute_mutiply_and_dividend(formula):
    operators = re.findall("[*/]", formula)
    calc_list = re.split("[*/]", formula)
    res = None
    for index, i in enumerate(calc_list):
        if res:
            if operators[index - 1] == "*":
                res *= float(i)
            elif operators[index - 1] == "/":
                res /= float(i)
        else:
            res = float(i)
    return res


def handle_special_occactions(plus_and_minus_operators, multiply_and_dividend):
    for index, i in enumerate(multiply_and_dividend):
        i = i.strip()
        if i.endswith("*") or i.endswith("/"):
            multiply_and_dividend[index] = multiply_and_dividend[index] + plus_and_minus_operators[index] + \
                                           multiply_and_dividend[index + 1]
            del multiply_and_dividend[index + 1]
            del plus_and_minus_operators[index]

    return plus_and_minus_operators, multiply_and_dividend


def compute(formula):
    formula = formula.strip("()")
    formula = remove_duplicates(formula)
    plus_and_minus_operators = re.findall("[+-]", formula)
    multiply_and_dividend = re.split("[+-]", formula)

    if len(multiply_and_dividend[0].strip()) == 0:
        multiply_and_dividend[1] = plus_and_minus_operators[0] + multiply_and_dividend[1]
        del multiply_and_dividend[0]
        del plus_and_minus_operators[0]

    plus_and_minus_operators, multiply_and_dividend = handle_special_occactions(
        plus_and_minus_operators, multiply_and_dividend)

    for index, i in enumerate(multiply_and_dividend):
        if re.search("[*/]", i):
            sub_res = compute_mutiply_and_dividend(i)
            multiply_and_dividend[index] = sub_res

    total_res = None
    for index, item in enumerate(multiply_and_dividend):
        if total_res:
            if plus_and_minus_operators[index - 1] == '+':
                total_res += float(item)
            elif plus_and_minus_operators[index - 1] == '-':
                total_res -= float(item)
        else:
            total_res = float(item)
    return total_res


def calc(formula):
    parenthesise_flag = True
    calc_res = None
    while parenthesise_flag:
        m = re.search("\([^()]*\)", formula)
        if m:
            sub_res = compute(m.group())
            formula = formula.replace(m.group(), str(sub_res))
        else:
            calc_res = compute(formula)
            parenthesise_flag = False
    return calc_res


if __name__ == '__main__':
    f = "1 - 2 * ( (60-30 +(-9-2-5-2*3-5/3-40*4/2-3/5+6*3) * (-9-2-5-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )"
    print('''
    The Final Result of 
    %s 
    is: %s
    ''' % (f, formatNum(calc(f))))