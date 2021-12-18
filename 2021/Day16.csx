using System;
using System.Collections.Generic;

var text = System.IO.File.ReadAllText("inputs/test.in").TrimEnd();
var bits = new byte[text.Length * 4];
var bitdex = 0;

foreach (var c in text) {
    var s = Byte.Parse(Char.ToString(c), System.Globalization.NumberStyles.HexNumber);
    
    bits[bitdex] = (byte) ((s & 8) >> 3);
    bits[bitdex + 1] = (byte) ((s & 4) >> 2);
    bits[bitdex + 2] = (byte) ((s & 2) >> 1);
    bits[bitdex + 3] = (byte) (s & 1);
    bitdex += 4;
}

int Decode(byte[] bits, int start, int length) {
    var total = 0;
    for (int b = start + length - 1, pow2 = 1; b >= start; --b, pow2 *= 2)
        total += pow2 * bits[b];
    return total;
}

int ip = 0;
int versionSum = 0;
while (Decode(bits, ip, bits.Length - ip) != 0) {
    // Console.WriteLine("IP => {0} (len={1})", ip, bits.Length);
    int version = Decode(bits, ip, 3);
    Console.WriteLine("Version => {0}", version);

    versionSum += version;
    ip += 3;

    int typeId = Decode(bits, ip, 3);
    ip += 3;
    Console.WriteLine("Type ID => {0}", typeId);

    if (typeId == 4) {
        while (bits[ip] != 0) {
            ip += 5;
        }
        ip += 5;
    } else {
        int lengthTypeId = bits[ip];
        ++ip;
        Console.WriteLine("Length Type ID => {0}", lengthTypeId);
        
        if (lengthTypeId == 1) {
            int N = Decode(bits, ip, 11);
            // Console.WriteLine("Number of subpackets => {0}", N);
            ip += 11;
        } else {
            int L = Decode(bits, ip, 15);
            // Console.WriteLine("Total length of packets => {0}", L);
            ip += 15;
        }
    }

    Console.WriteLine();
}

Console.WriteLine(versionSum);
