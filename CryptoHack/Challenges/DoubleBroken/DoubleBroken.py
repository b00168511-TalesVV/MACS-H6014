import json

with open('./collected_data.txt') as f:
    traces = json.load(f) 


means = [sum(t[i] for t in traces)/len(traces) for i in range(len(traces[0]))]

sm = sorted(means)
gaps = [sm[i+1] - sm[i] for i in range(len(sm)-1)]
idx = gaps.index(max(gaps))
thr = (sm[idx] + sm[idx+1]) / 2

bits = [1 if m > thr else 0 for m in means]

bits_rev = bits[::-1]
d = int(''.join(str(b) for b in bits_rev), 2)
flag = d.to_bytes((d.bit_length()+7)//8, 'big').decode()
print(flag)
