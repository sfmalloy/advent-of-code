{:ok, ipt} = File.read("inputs/Day24.in")
# {:ok, ipt} = File.read("inputs/test.in")

elems = String.split(ipt, "\n")

# registers defined as [w, x, y, z]
defmodule Computer do
  def run(program, ipt) do
    run(program, [0, 0, 0, 0], ipt)
  end

  defp run([""], reg, _) do
    IO.puts "done"
    reg
  end

  defp run([curr | rest], reg, ipt) do
    {reg, ipt} = eval(String.split(curr, " "), reg, ipt)
    run(rest, reg, ipt)
  end

  defp eval(["inp", r], [w, x, y, z], [curr_ipt | rest]) do
    reg = case r do
      "w" -> [curr_ipt, x, y, z]
      "x" -> [w, curr_ipt, y, z]
      "y" -> [w, x, curr_ipt, z]
      "z" -> [w, x, y, curr_ipt]
    end
    {reg, rest}
  end

  defp eval(["add", a, b], reg, ipt) do
    res = arg(a, reg) + arg(b, reg)
    {updated_reg(a, res, reg), ipt}
  end

  defp eval(["mul", a, b], reg, ipt) do
    res = arg(a, reg) * arg(b, reg)
    {updated_reg(a, res, reg), ipt}
  end

  defp eval(["div", a, b], reg, ipt) do
    res = div(arg(a, reg), arg(b, reg))
    {updated_reg(a, res, reg), ipt}
  end

  defp eval(["mod", a, b], reg, ipt) do
    res = rem(arg(a, reg), arg(b, reg))
    {updated_reg(a, res, reg), ipt}
  end

  defp eval(["eql", a, b], reg, ipt) do
    res = if arg(a, reg) == arg(b, reg) do 1 else 0 end
    {updated_reg(a, res, reg), ipt}
  end

  defp arg(a, [w, x, y, z]) do
    case a do
      "w" -> w
      "x" -> x
      "y" -> y
      "z" -> z
      _ -> String.to_integer(a)
    end
  end

  defp updated_reg(key, val, reg) do
    case {key, reg} do
      {"w", [_, x, y, z]} -> [val, x, y, z]
      {"x", [w, _, y, z]} -> [w, val, y, z]
      {"y", [w, x, _, z]} -> [w, x, val, z]
      {"z", [w, x, y, _]} -> [w, x, y, val]
    end
  end
end

[w, x, y, z] = Computer.run(elems, [9, 9, 5, 9, 9])
IO.puts("#{w} #{x} #{y} #{z}")
