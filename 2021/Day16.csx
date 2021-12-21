using System;
using System.Collections.Generic;

/*****************************************************************************/
// Classes for Lexer / Parser

class Token {
    public ulong address { get; set; }
    public ulong typeId { get; set; }
    public ulong lengthType { get; set; }
    public ulong length { get; set; }
    public ulong value { get; set; }
}

interface Packet {
    void Accept(IVisitor visitor);
}

class Operator {
    public ulong lengthType { get; set; }
    public ulong length { get; set; }
}

class Literal : Packet { 
    public ulong value { get; set; }
    
    public void Accept(IVisitor visitor) {
        visitor.Visit(this);
    }
}

class Sum : Operator, Packet { 
    public List<Packet> subpackets { get; set; }
    
    public void Accept(IVisitor visitor) {
        visitor.Visit(this);
    }
}

class Product : Operator, Packet { 
    public List<Packet> subpackets { get; set; }

    public void Accept(IVisitor visitor) {
        visitor.Visit(this);
    }
}

class Minimum : Operator, Packet { 
    public List<Packet> subpackets { get; set; }

    public void Accept(IVisitor visitor) {
        visitor.Visit(this);
    }
}

class Maximum : Operator, Packet { 
    public List<Packet> subpackets { get; set; }

    public void Accept(IVisitor visitor) {
        visitor.Visit(this);
    }
}

class GreaterThan : Operator, Packet { 
    public Packet lhs { get; set; }
    public Packet rhs { get; set; }

    public void Accept(IVisitor visitor) {
        visitor.Visit(this);
    }
}

class LessThan : Operator, Packet {
    public Packet lhs { get; set; }
    public Packet rhs { get; set; }
    
    public void Accept(IVisitor visitor) {
        visitor.Visit(this);
    }
}

class EqualTo : Operator, Packet { 
    public Packet lhs { get; set; }
    public Packet rhs { get; set; }

    public void Accept(IVisitor visitor) {
        visitor.Visit(this);
    }
}

interface IVisitor {
    void Visit(Literal packet);
    void Visit(Sum packet);
    void Visit(Product packet);
    void Visit(Minimum packet);
    void Visit(Maximum packet);
    void Visit(GreaterThan packet);
    void Visit(LessThan packet);
    void Visit(EqualTo packet);
}

/*****************************************************************************/
// Parser
class Parser {
    List<Token> tokens;
    int parserIdx;

    public Parser(List<Token> tokens) {
        this.tokens = tokens;
        this.parserIdx = 0;
    }

    public Packet Parse() {
        Packet root;

        switch (tokens[parserIdx].typeId) {
            case 0:  root = Add();     break;
            case 1:  root = Times();   break;
            case 2:  root = Min();     break;
            case 3:  root = Max();     break;
            case 5:  root = Greater(); break;
            case 6:  root = Less();    break;
            case 7:  root = Equal();   break;
            default: root = Number();  break;
        }

        return root;
    }

    List<Packet> SubPackets() {
        Token curr = tokens[parserIdx];
        List<Packet> subpackets = new List<Packet>();
        if (curr.lengthType == 1) {
            for (ulong i = 0; i < curr.length; ++i) {
                ++parserIdx;
                subpackets.Add(Parse());
            }
        } else {
            while (++parserIdx < tokens.Count && tokens[parserIdx].address != curr.address + 22 + curr.length) {
                subpackets.Add(Parse());
            }
            --parserIdx;
        }

        return subpackets;
    }

    Sum Add() {
        return new Sum() { subpackets = SubPackets() };
    }

    Product Times() {
        return new Product() { subpackets = SubPackets() };
    }

    Minimum Min() {
        return new Minimum() { subpackets = SubPackets() };
    }

    Maximum Max() {
        return new Maximum() { subpackets = SubPackets() };
    }

    GreaterThan Greater() {
        List<Packet> subpackets = SubPackets();
        if (subpackets.Count < 2)
            throw new Exception("Not enough arguments for GreaterThan operator");
        return new GreaterThan() { lhs = subpackets[0], rhs = subpackets[1] };
    }

    LessThan Less() {
        List<Packet> subpackets = SubPackets();
        if (subpackets.Count < 2)
            throw new Exception("Not enough arguments for LessThan operator");
        return new LessThan() { lhs = subpackets[0], rhs = subpackets[1] };
    }

    EqualTo Equal() {
        List<Packet> subpackets = SubPackets();
        if (subpackets.Count < 2)
            throw new Exception("Not enough arguments for EqualTo operator");
        return new EqualTo() { lhs = subpackets[0], rhs = subpackets[1] };
    }

    Literal Number() {
        return new Literal() { value = tokens[parserIdx].value };
    }
}

/*****************************************************************************/

class PrintVisitor : IVisitor {
    private int indent;
    private StreamWriter file;

    public PrintVisitor(StreamWriter file) {
        indent = -1;
        this.file = file;
    }

    public void Print(string value) {
        string str = "";
        for (int i = 0; i < indent; ++i) {
            str += "  ";
        }

        file.WriteLine(str + value);
    }

    public void Visit(Literal packet) {
        indent += 1;
        Print("Literal: " + packet.value);
        indent -= 1;
    }

    public void Visit(Sum packet) {
        indent += 1;
        
        Print("Sum");
        foreach (Packet subpacket in packet.subpackets) {
            subpacket.Accept(this);
        }

        indent -= 1;
    }

    public void Visit(Product packet) {
        indent += 1;
        
        Print("Product");
        foreach (Packet subpacket in packet.subpackets) {
            subpacket.Accept(this);
        }

        indent -= 1;
    }

    public void Visit(Minimum packet) {
        indent += 1;
        
        Print("Minimum");
        foreach (Packet subpacket in packet.subpackets) {
            subpacket.Accept(this);
        }

        indent -= 1;
    }

    public void Visit(Maximum packet) {
        indent += 1;
        
        Print("Maximum");
        foreach (Packet subpacket in packet.subpackets) {
            subpacket.Accept(this);
        }

        indent -= 1;
    }

    public void Visit(GreaterThan packet) {
        indent += 1;
        
        Print("GreaterThan");
        packet.lhs.Accept(this);
        packet.rhs.Accept(this);

        indent -= 1;
    }

    public void Visit(LessThan packet) {
        indent += 1;
        
        Print("LessThan");
        packet.lhs.Accept(this);
        packet.rhs.Accept(this);

        indent -= 1;
    }

    public void Visit(EqualTo packet) {
        indent += 1;
        
        Print("EqualTo");
        packet.lhs.Accept(this);
        packet.rhs.Accept(this);

        indent -= 1;
    }
}

/*****************************************************************************/
class EvalVisitor : IVisitor {
    public ulong result{ get; set; }

    public void Visit(Literal packet) {
        result = packet.value;
    }

    public void Visit(Sum packet) {
        ulong sum = 0;

        foreach (Packet subpacket in packet.subpackets) {
            subpacket.Accept(this);
            sum += result;
        }

        result = sum;
    }

    public void Visit(Product packet) {
        ulong prod = 1;

        foreach (Packet subpacket in packet.subpackets) {
            subpacket.Accept(this);
            prod *= result;
        }

        result = prod;
    }

    public void Visit(Minimum packet) {
        ulong min = ulong.MaxValue;

        foreach (Packet subpacket in packet.subpackets) {
            subpacket.Accept(this);
            if (min > result)
                min = result;
        }

        result = min;
    }

    public void Visit(Maximum packet) {
        ulong max = 0;

        foreach (Packet subpacket in packet.subpackets) {
            subpacket.Accept(this);
            if (max < result)
                max = result;
        }

        result = max;
    }

    public void Visit(GreaterThan packet) {
        packet.lhs.Accept(this);
        ulong a = result;
        packet.rhs.Accept(this);
        ulong b = result;

        result = a > b ? 1UL : 0UL;
    }

    public void Visit(LessThan packet) {
        packet.lhs.Accept(this);
        ulong a = result;
        packet.rhs.Accept(this);
        ulong b = result;

        result = a < b ? 1UL : 0UL;
    }

    public void Visit(EqualTo packet) {
        packet.lhs.Accept(this);
        ulong a = result;
        packet.rhs.Accept(this);
        ulong b = result;

        result = a == b ? 1UL : 0UL;
    }
}
/*****************************************************************************/

class CodeVisitor : IVisitor {
    public ulong result{ get; set; }

    public void Visit(Literal packet) {
        Console.Write(packet.value);
        result = packet.value;
    }

    public void Visit(Sum packet) {
        Console.Write("(");
        for (int i = 0; i < packet.subpackets.Count; ++i) {
            packet.subpackets[i].Accept(this);
            if (i < packet.subpackets.Count - 1) {
                Console.Write(" + ");
            }
        }
        Console.Write(")");
    }

    public void Visit(Product packet) {

        Console.Write("(");
        for (int i = 0; i < packet.subpackets.Count; ++i) {
            packet.subpackets[i].Accept(this);
            if (i < packet.subpackets.Count - 1) {
                Console.Write(" * ");
            }
        }
        Console.Write(")");
    }

    public void Visit(Minimum packet) {
        Console.Write("min(");
        for (int i = 0; i < packet.subpackets.Count; ++i) {
            packet.subpackets[i].Accept(this);
            if (i < packet.subpackets.Count - 1) {
                Console.Write(", ");
            }
        }
        Console.Write(")");
    }

    public void Visit(Maximum packet) {
        Console.Write("max(");
        for (int i = 0; i < packet.subpackets.Count; ++i) {
            packet.subpackets[i].Accept(this);
            if (i < packet.subpackets.Count - 1) {
                Console.Write(", ");
            }
        }
        Console.Write(")");
    }

    public void Visit(GreaterThan packet) {
        Console.Write("(");
        packet.lhs.Accept(this);
        Console.Write(" > ");
        packet.rhs.Accept(this);
        Console.Write(")");
    }

    public void Visit(LessThan packet) {
        Console.Write("(");
        packet.lhs.Accept(this);
        Console.Write(" < ");
        packet.rhs.Accept(this);
        Console.Write(")");
    }

    public void Visit(EqualTo packet) {
        Console.Write("(");
        packet.lhs.Accept(this);
        Console.Write(" == ");
        packet.rhs.Accept(this);
        Console.Write(")");
    }
}
/*****************************************************************************/
// Helper functions

ulong Decode(byte[] bits, ulong start, ulong length) {
    ulong total = 0;
    for (ulong b = start + length - 1, pow2 = 1; b + 1 >= start + 1; --b, pow2 *= 2) {
        total += pow2 * bits[b];
    }
    return total;
}

/*****************************************************************************/
// Setup
string filename = "inputs/Day16.in";
if (Args.Count > 0)
    filename = Args[0];
string text = System.IO.File.ReadAllText(filename).TrimEnd();
byte[] bits = new byte[text.Length * 4];
ulong bitdex = 0;

foreach (var c in text) {
    byte s = Byte.Parse(Char.ToString(c), System.Globalization.NumberStyles.HexNumber);
    
    bits[bitdex] = (byte) ((s & 8) >> 3);
    bits[bitdex + 1] = (byte) ((s & 4) >> 2);
    bits[bitdex + 2] = (byte) ((s & 2) >> 1);
    bits[bitdex + 3] = (byte) (s & 1);
    bitdex += 4;
}


/*****************************************************************************/
// Part 1 / Lexer
ulong ip = 0;
ulong versionSum = 0;
List<Token> tokens = new List<Token>();
while (Decode(bits, ip, ((ulong) (bits.Length)) - ip) != 0) {
    ulong address = ip;
    ulong version = Decode(bits, ip, 3);
    versionSum += version;
    ip += 3;

    ulong typeId = Decode(bits, ip, 3);
    ip += 3;

    if (typeId == 4) {
        List<byte> literal = new List<byte>();
        while (bits[ip] != 0) {
            literal.Add(bits[ip + 1]);
            literal.Add(bits[ip + 2]);
            literal.Add(bits[ip + 3]);
            literal.Add(bits[ip + 4]);

            ip += 5;
        }
        
        literal.Add(bits[ip + 1]);
        literal.Add(bits[ip + 2]);
        literal.Add(bits[ip + 3]);
        literal.Add(bits[ip + 4]);

        ip += 5;
        tokens.Add(new Token() { 
            address = address, 
            typeId = typeId, 
            value = Decode(literal.ToArray(), 0, (ulong) literal.Count) 
        });

    } else {
        ulong lengthTypeId = bits[ip];
        ulong length;
        ++ip;

        if (lengthTypeId == 1) {
            length = Decode(bits, ip, 11);
            ip += 11;
        } else {
            length = Decode(bits, ip, 15);
            ip += 15;
        }

        tokens.Add(new Token() {
            address = address,
            typeId = typeId,
            lengthType = lengthTypeId,
            length = length
        });
    }
}

/*****************************************************************************/
// Part 2, Parse and Eval

Parser parser = new Parser(tokens);
CodeVisitor pyVisitor = new CodeVisitor();
EvalVisitor eVisitor = new EvalVisitor();

Packet root = parser.Parse();
root.Accept(eVisitor);

using (var file = File.CreateText("AST.txt")) {
    PrintVisitor pVisitor = new PrintVisitor(file);
    root.Accept(pVisitor);
}
Console.WriteLine(versionSum);
Console.WriteLine(eVisitor.result);
