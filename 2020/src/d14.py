import fileinput

lines = [l.strip() for l in fileinput.input()]

def pad_bin(b, l):
  return ('0' * (l-len(str(b)))) + b

mem = {}
float_mem = {}
i = 0
while i < len(lines):
  mask = lines[i].split('=')[1][1:]
  i += 1
  while i < len(lines) and lines[i][3] == '[':
    addr, entry = lines[i].split(' = ')
    
    dec_addr = int(addr.strip('mem[] '))
    bin_addr = bin(dec_addr)[2:]
    bin_addr = pad_bin(bin_addr, 36)
    
    dec_entry = int(entry)
    bin_entry = bin(dec_entry)[2:]
    bin_entry = pad_bin(bin_entry, 36)
    
    res = ''
    float_addr = ''
    x_count = 0
    for m,e,a in zip(mask, bin_entry, bin_addr):
      res += m if m != 'X' else e
      float_addr += m if m != '0' else a
      x_count += float_addr[-1] == 'X'
    res = int(res, 2)
    mem[dec_addr] = res

    for x in range(2**x_count):
      x_digits = bin(x)[2:]
      new_addr = ''
      # sub all x's with digits of x_digits :)
      x_idx = len(x_digits)-1
      for m in float_addr:
        if m == 'X':
          if x_idx >= 0:
            new_addr += x_digits[x_idx]
            x_idx -= 1
          else:
            new_addr += '0'
        else:
          new_addr += m
      float_mem[int(new_addr, 2)] = dec_entry
    i += 1

print(sum(mem.values()))
print(sum(float_mem.values()))
