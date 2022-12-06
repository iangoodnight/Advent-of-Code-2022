#!/usr/bin/env lua

--[[

<https://adventofcode.com/2022/day/5> 'Advent of Code - Day 5'

# Advent of Code 2022

## Supply Stacks

The expedition can depart as soon as the final supplies have been unloaded from
the ships. Supplies are stored in stacks of marked **crates**, but because the
needed supplies are buried under many other crates, the crates need to be
rearranged.

The ship has a **giant cargo crane** capable of moving crates between stacks. To
ensure none of the crates get crushed or fall over, the crane operator will
rearrange them in a series of carefully-planned steps. After the crates are
rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate
procedure, but they forgot to ask her **which** crate will end up where, and they
want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates **and** the
rearrangement procedure (your puzzle input). For example:

```
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
```

In this example, there are three stacks of crates. Stack 1 contains two crates:
crate `Z` is on the bottom, and crate `N` is on top. Stack 2 contains three
crates; from bottom to top, they are crates `M`, `C`, and `D`. Finally, stack 3
contains a single crate, `P`.

Then, the rearrangement procedure is given. In each step of the procedure, a
quantity of crates is moved from one stack to a different stack. In the first
step of the above rearrangement procedure, one crate is moved from stack 2 to
stack 1, resulting in this configuration:

```
[D]
[N] [C]
[Z] [M] [P]
 1   2   3
```

In the second step, three crates are moved from stack 1 to stack 3. Crates are
moved **one at a time**, so the first crate to be moved (`D`) ends up below the
second and third crates:

```
        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
```

Then, both crates are moved from stack 2 to stack 1. Again, because crates are
moved **one at a time**, crate `C` ends up below crate `M`:

```
        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
```

Finally, one crate is moved from stack 1 to stack 2:

```
        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
```

The Elves just need to know **which crate will end up on top of each stack;** in
this example, the top crates are `C` in stack 1, `M` in stack 2, and `Z` in stack
3, so you should combine these together and give the Elves the message `CMZ`.

**After the rearrangement procedure completes, what crate ends up on top of each
stack?**

--]]

-- Stack class
Stack = {}

-- Stack class method new
function Stack:new (o, ...)
  o = o or {}
  setmetatable(o, self)
  self.__index = self
  local args = {...}
  for i, val in ipairs(args) do
    o[i] = val
  end
  return o
end

-- Stack class method pop
function Stack:pop()
  assert(#self > 0, "Stack underflow")
  local popped = self[#self]
  self[#self] = nil
  return popped
end

-- Stack class method push
function Stack:push(val)
  self[#self + 1] = val
end

-- Utility function split
function split(s, delimiter)
  local parts = {};
  for matched in (s..delimiter):gmatch("(.-)"..delimiter) do
    table.insert(parts, matched)
  end
  return parts
end

-- Utility function findindex
function findindex(list, val)
  for i, v in ipairs(list) do
    if v == val then
      return i
    end
  end
  return nil
end

-- Utility function reverse
function reverse(list)
  local reversed = {}
  for i, val in ipairs(list) do
    reversed[#list + 1 - i] = val
  end
  return reversed
end

-- Builds an array of Stacks from diagram (text block)
function buildstacks(inputblock, stacklimit)
  local key = {}
  local lines = {}
  local stacks = {}

  for line in string.gmatch(inputblock, "([^\n]*)\n?") do
    if string.match(line, "^[%d%s]+$") then
      key["raw"] = line
    end

    if string.match(line, "^[%u%s%[%]]+$") then
      table.insert(lines, line)
    end
  end

  for i=1, stacklimit do
    k = string.find(key.raw, tostring(i))
    key[i] = tonumber(k)
    stacks[i] = Stack:new()
  end

  linesreversed = reverse(lines)

  for _, line in ipairs(linesreversed) do
    for i=1, #line do
      local char = string.sub(line, i, i)
      if string.match(char, "%u") then
        local stackidx = findindex(key, i)
        stacks[stackidx]:push(char)
      end
    end
  end

  return stacks
end

-- Runs instructions (text block) on stacklist
function runinstructions(textblock, stacklist)
  local lines = split(textblock, "\n")

  for _, line in ipairs(lines) do
    amount, from, to = string.match(line, "move%s(%d+)%sfrom%s(%d+)%sto%s(%d+)")
    if amount and from and to then
      for i=1, tonumber(amount) do
        local popped = stacklist[tonumber(from)]:pop()
        stacklist[tonumber(to)]:push(popped)
      end
    end
  end
end

-- Main
function main()
  local file = arg[1] or "input.txt"
  local f = io.open(file, "r")

  if not f then
    print(file .. "Usage: lua ch-1.lua <path to input file>")
    f:close()
    os.exit()
  else
    local data = f:read("*all")

    f:close()

    local dataseparator = string.find(data, "\n\n")
    local initblock = string.sub(data, 1, dataseparator-1)
    local instructionblock = string.sub(data, dataseparator)
    local stacks = buildstacks(initblock, 9)

    runinstructions(instructionblock, stacks)

    local word = {}

    for _, stack in ipairs(stacks) do
      table.insert(word, stack:pop())
    end

    print("Crates on top: " .. table.concat(word)) -- "WSFTMRHPP"
  end
end

main()
