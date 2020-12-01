with open('1.in') as f:
  l = [int(x) for x in f.readlines()]
[print((f'{l[j]*l[k]}\n' if l[j]+l[k]==2020 and i==0 else ''), (f'{l[i]*l[j]*l[k]}\n' if l[i]+l[j]+l[k]==2020 else ''), sep='', end='') 
  for i in range(len(l)) for j in range(i+1, len(l)) for k in range(j+1, len(l))]