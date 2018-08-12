###############################
# This is just a Demo Version #
###############################

import re

# To make simple analysis of a ASM
# just open that file in OllyDebugger and copy the instructions
# into a new file and specify the filename below
filename = "1.txt"
RegisterToParse = "EAX"

# If you want a more simpler version
# set 1 else set 0
SimpleVersion = 1

with open(filename, "rb") as f:
  # Reading all file data..
  s = f.read()

# f consists of all registers used in 32bit ASM
f = ["EAX", "EBX", "ECX", "EDX", "ESI", "EDI", "ESP", "EIP", "AL", "BL", "CL", "DL", "AH", "BH", "CH", "DH"]

def gene(k):
  # In TextProcessing some variable names like 
  # [EBP-43C] or [EBP+98A] will make a problem
  # Therefore in this function these variables will convert
  # [EBP-43C] --> m43c because of subtraction
  # [EBP+98A] --> p98a because of addition..
  
  k = k[4:] # ignoring first 4 chars because k will always starts from "[EBP"
  a = re.findall("[A-Z0-9]+", k)
  k = 'm' if '-' in k else 'p'
  return k + a[0]

def h(a):
  # These are some texts that can make problem
  # like MOV DWORD PTR SS:[EBP+48],EAX  in this "DWORD PTR SS:" is useless..
  a = a.replace("DWORD PTR ", "")
  a = a.replace("WORD PTR ", "")
  a = a.replace("BYTE PTR ", "")
  a = a.replace("SS:", "")
  a = a.replace("DS:", "")
  return a

s = h(s)

# Below process is just converting [EBP(+|-)offset] registers into simplified variables
k = re.findall("(\[EBP\-\w+\])|(\[EBP\+\w+\])", s)
po = []
for i in k:
  i = i[0] if i[0] else i[1]
  io = gene(i)
  if io not in po:
    po += [io]
  s = s.replace(i, gene(i))
  
# appending registers array with new variables
f += po

g = s.split("\n")[::-1]
# g is set of all instruction strings..
# like g[34] is "10001001  |. 8B7424 08      MOV ESI,m34"

k = 0
# This global count will holds current index of instruction

EEEEE = 28

def GetAttrs(a):
  global f
  if len(re.findall("\w+", a[EEEEE:])) < 1:
    return False
  A = a
  n = []
  if "MOV" in a:
    a = " ".join(x for x in re.findall("\w+", a[EEEEE:])[2:])
    for i in f:
      if i in a:
        n += [i]
  else:
    A = h(A)
    for i in f:
      if i in A:
        n += [i]
  if len(n) == 0:
    return False
  return n


def isIn(a, b):
  l = re.findall("\w+", a[EEEEE:])
  if len(l) > 1:
    return re.findall("\w+", a[EEEEE:])[1] == b
  return False

def GetLine(i):
  global k
  if "MUL" in g[k]:
    return [g[k], k]
  kl = k
  while "00" not in g[k]:
    k += 1
  while k < len(g):
    E = isIn(g[k], i)
    if E:
      return [g[k], k]
    k += 1
  if "DIV" in g[kl]:
    print "====", g[kl]
    return [g[kl], kl]
  if k == len(g):
    k = 0
  return False

zz = -1
lll = []

def ff(i):
  global k
  global zz, lll
  t = k
  a = GetLine(i)
  if a != False:
    k = a[1]
    a = a[0]
    L1 = GetAttrs(a)
    if zz != k:
      lll += [a]
    zz = k
    if "MUL" in a or "DIV" in a:
      if "EAX" not in L1:
        L1 += ["EAX"]
    if L1:
      for i in L1:
        k += 1
        ff(i)
        k = t

def getsimple(i):
  o = i[EEEEE:].split(" ")
  if o[0] == "MOV":
    o1 = o[1].split(",")
    print o1[0],"=","".join(x for x in o1[1:])
  elif o[0] == "ADD":
    o1 = o[1].split(",")
    print o1[0],"+=","".join(x for x in o1[1:])
  elif o[0] == "SUB":
    o1 = o[1].split(",")
    print o1[0],"-=","".join(x for x in o1[1:])
  else:
    print i[EEEEE:]

def asort():
  global lll
  n = []
  l = [int(re.findall("00\w+", li)[0], 16) for li in lll]
  l.sort()
  for i in l:
    for xx in lll:
      if hex(i)[2:].upper() in xx:
        n += [xx]
        while xx in lll:
          lll.remove(xx)
  global SimpleVersion
  if SimpleVersion == 1:
    for i in n:
      getsimple(i)
    return
  for i in n:
    print i

def ff1(ss):
  global lll
  ff(ss)
  return lll

ff(RegisterToParse)

asort()



