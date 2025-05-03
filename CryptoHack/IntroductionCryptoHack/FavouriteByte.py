flag = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

for j in range(0,255):
    if chr(int(flag[0:2],16)^j) == "c":
        print("".join(chr(int(flag[o:o+2],16)^j) for o in range(0,len(flag),2)))