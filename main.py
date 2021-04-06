# Author: Vinayak Sethi
# Design Activity 1

from sympy import *
import os


def notGate(va):
    not_sim = "p A vdd nA 2 4\nn A nA gnd 2 4\n"  #Output in sim file contains order as Gate  Source  Drain
    not_out = not_sim.replace("A", va)
    return not_out


def andGate(in1, in2, w1): 
    and_sim = "p A vdd wire2 2 4\np B vdd wire2 2 4\nn A wire2 wire1 2 4\nn B wire1 gnd 2 4\n\np wire2 vdd Y 2 4\nn wire2 " \
         "gnd Y 2 4\n\n"  #Output in sim file contains order as Gate  Source  Drain
    and_out = and_sim.replace("A", in1)
    and_out = and_out.replace("B", in2)
    n1 = "n" + str(w1)
    and_out = and_out.replace("wire1", n1)
    n2 = "n" + str(w1 + 1)
    and_out = and_out.replace("wire2", n2)
    ou = "n" + str(w1 + 2)
    and_out = and_out.replace("Y", ou)
    return and_out


def orGate(in1, in2, w1):
    or_sim = "p A vdd wire1 2 4\np B wire1 wire2 2 4\nn A wire2 gnd 2 4\nn B wire2 gnd 2 4\n\np wire2 vdd Y 2 4\nn wire2 " \
         "gnd Y 2 4\n\n"  #Output in sim file contains order as Gate  Source  Drain
    or_out = or_sim.replace("A", in1)
    or_out = or_out.replace("B", in2)
    n1 = "n" + str(w1)
    or_out = or_out.replace("wire1", n1)
    n2 = "n" + str(w1 + 1)
    or_out = or_out.replace("wire2", n2)
    ou = "n" + str(w1 + 2)
    or_out = or_out.replace("Y", ou)
    return or_out


def simplifyAnd(exprAnd, wcAnd):
    a1And = ""
    b1And = ""
    itAnd = exprAnd.find("&")

    # Loop till no & gates remain.
    while itAnd != -1:
        tempAnd = itAnd - 1
        while True:
            if exprAnd[tempAnd] == "(" or exprAnd[tempAnd] == "&":
                break
            a1And = exprAnd[tempAnd] + a1And
            tempAnd -= 1
            if tempAnd < 0:
                break
        tempAnd = itAnd + 1
        while True:
            if exprAnd[tempAnd] == ")" or exprAnd[tempAnd] == "&":
                break
            b1And = b1And + exprAnd[tempAnd]
            tempAnd += 1
            if tempAnd >= len(exprAnd):
                break
        wrAnd = andGate(a1And, b1And, wcAnd)
        wcAnd += 2
        repAnd = a1And + "&" + b1And
        outAnd = "n" + str(wcAnd)
        wcAnd += 1
        fp.write(wrAnd)
        exprAnd = exprAnd.replace(repAnd, outAnd)
        a1And = ""
        b1And = ""
        itAnd = exprAnd.find("&")
    return exprAnd, wcAnd


def simplifyOr(exprOr, wcOr):
    a1Or = ""
    b1Or = ""
    itOr = exprOr.find("|")

    # Loop till no | gates remain.
    while itOr != -1:
        tempOr = itOr - 1
        while True:
            if exprOr[tempOr] == "(" or exprOr[tempOr] == "|":
                break
            a1Or = exprOr[tempOr] + a1Or
            tempOr -= 1
            if tempOr < 0:
                break
        tempOr = itOr + 1
        while True:
            if exprOr[tempOr] == ")" or exprOr[tempOr] == "|":
                break
            b1Or = b1Or + exprOr[tempOr]
            tempOr += 1
            if tempOr >= len(exprOr):
                break
        wrOr = orGate(a1Or, b1Or, wcOr)
        wcOr += 2
        repOr = a1Or + "|" + b1Or
        outOr = "n" + str(wcOr)
        wcOr += 1
        fp.write(wrOr)
        exprOr = exprOr.replace(repOr, outOr)
        a1Or = ""
        b1Or = ""
        itOr = exprOr.find("|")
    return exprOr, wcOr

# To convert all xor gates: a^b = (~a & b)|(a & ~b)
def simplifyXor(exprXor):
    a1Xor = ""
    b1Xor = ""
    count = 0
    itXor = exprXor.find("^")

    # Loop till no ^ gates remain.
    while itXor != -1:
        tempXor = itXor - 1
        if exprXor[tempXor] == ")":
            count += 1
            a1Xor += ")"
            while count != 0:
                tempXor -= 1
                if tempXor < 0:
                    break
                if exprXor[tempXor] == ")":
                    count += 1
                if exprXor[tempXor] == "(":
                    count -= 1
                a1Xor = exprXor[tempXor] + a1Xor
            if tempXor != 0:
                if exprXor[tempXor-1] == "~":
                    a1Xor = "~" + a1Xor
        else:
            while True:
                if exprXor[tempXor] == "^" or exprXor[tempXor] == "|" or exprXor[tempXor] == "&" or exprXor[tempXor] == "(" or exprXor[tempXor] == ")":
                    break
                a1Xor = exprXor[tempXor] + a1Xor
                tempXor -= 1
                if tempXor < 0:
                    break
#
        count = 0
        tempXor = itXor + 1
        if exprXor[tempXor] == "~":
            b1Xor = b1Xor + "~"
            tempXor += 1
        if exprXor[tempXor] == "(":
            count += 1
            b1Xor += "("
            while count != 0:
                tempXor += 1
                if tempXor >= len(exprXor):
                    break
                if exprXor[tempXor] == "(":
                    count += 1
                if exprXor[tempXor] == ")":
                    count -= 1
                b1Xor = b1Xor + exprXor[tempXor]

        else:
            while True:
                if exprXor[tempXor] == "^" or exprXor[tempXor] == "|" or exprXor[tempXor] == "&":
                    break
                b1Xor = b1Xor + exprXor[tempXor]
                tempXor += 1
                if tempXor >= len(exprXor):
                    break
        # replace the old a^b with (~a&b)|(a&~b)
        old = a1Xor + "^" + b1Xor
        new = "((" + a1Xor + "&~" + b1Xor + ")|(~" + a1Xor + "&" + b1Xor + "))"
        exprXor = exprXor.replace(old, new)
        itXor = exprXor.find("^")
        a1Xor = ""
        b1Xor = ""
    return exprXor


if __name__ == '__main__':
    print("Operators to be used for Boolean Expression:\n\t~ ---> NOT Gate\n\t& ---> AND Gate\n\t| ---> OR Gate\n\t^ ---> XOR Gate")
    f1 = input("Enter the boolean expression: ")
    f1 = f1.replace(" ", "")

    # Simplify the xor gates: a^b = (~a & b)|(a & ~b)
    f1 = simplifyXor(f1)
    f1 = f1.replace(" ", "")
    print("Simplification for XOR Gates: " + f1)
    min_out = str(simplify(f1))
    min_out = min_out.replace(" ", "")
    print("Simplified Output is: ")
    print(min_out)

    #iNPUT file name
    file1 = input("Enter a file name without any extension: ") + ".sim"
    os.chdir("Circuits")

    #Open the Output File
    fp = open(file1, "w")
    varDone = set()

    #Removing Duplicate NOT Gates
    for index in range(len(min_out)):
        if min_out[index] == "~":
            index1 = index + 1
            if min_out[index1] not in varDone:
                varDone.add(min_out[index1])
            else:
                continue
            wr = notGate(min_out[index1])
            fp.write(wr)

    #Initializing input variables
    min_out = min_out.replace("~", "n")
    a1 = ""
    b1 = ""
    wireCount = 0

    if min_out.find(")|") != -1 or min_out.find("|(") != -1:
        min_out, wireCount1 = simplifyAnd(min_out, wireCount)
        wireCount += wireCount1
        min_out = min_out.replace("(", "")
        min_out = min_out.replace(")", "")
        min_out = "(" + min_out + ")"
        min_out, wireCount1 = simplifyOr(min_out, wireCount)
        min_out = min_out.replace("(", "")
        min_out = min_out.replace(")", "")
        wireCount += wireCount1


    elif min_out.find(")&") != -1 or min_out.find("&(") != -1:
        min_out, wireCount1 = simplifyOr(min_out, wireCount)
        wireCount += wireCount1
        min_out = min_out.replace("(", "")
        min_out = min_out.replace(")", "")
        min_out = "(" + min_out + ")"
        min_out, wireCount1 = simplifyAnd(min_out, wireCount)
        min_out = min_out.replace("(", "")
        min_out = min_out.replace(")", "")
        wireCount += wireCount1

    #At this step we just have & and | gates in expression
    #Simplifying remaining & Gate
    elif min_out.find("&") != -1:
        min_out, wireCount1 = simplifyAnd(min_out, wireCount)
        wireCount += wireCount1
        min_out = min_out.replace("(", "")
        min_out = min_out.replace(")", "")

    #Simplifying remaining | Gate
    elif min_out.find("|") != -1: 
        min_out, wireCount1 = simplifyOr(min_out, wireCount)
        wireCount += wireCount1
        min_out = min_out.replace("(", "")
        min_out = min_out.replace(")", "")

    fp.close()

    with open(file1, "r") as fp:
        fileData = fp.read()
    fileData = fileData.replace(min_out, "y")
    with open(file1, "w") as fp:
        fp.write(fileData)
    min_out = min_out.replace(min_out, "y")
    print("Final output variable is : " + min_out)
