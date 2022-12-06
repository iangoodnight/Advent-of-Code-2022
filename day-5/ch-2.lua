#!/usr/bin/env lua

--[[

<https://adventofcode.com/2022/day/5> 'Advent of Code - Day 5'

# Advent of Code 2022

## Part Two

As you watch the crane operator expertly rearrange the crates, you notice the
process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe
it away. The crane isn't a CrateMover 9000 - it's a **CrateMover 9001**.

The CrateMover 9001 is notable for many new and exciting features: air
conditioning, leather seats, an extra cup holder, and the **ability to pick up
and move multiple crates at once**.

Again considering the example above, the crates begin in the same configuration:

```
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3
```

Moving a single crate from stack 2 to stack 1 behaves the same as before:

```
[D]
[N] [C]
[Z] [M] [P]
 1   2   3
```

However, the action of moving three crates from stack 1 to stack 3 means that
those three moved crates **stay in the same order**, resulting in this new
configuration:

```
        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
```

Next, as both crates are moved from stack 2 to stack 1, they **retain their order
as well**:

```
        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
```

Finally, a single crate is still moved from stack 1 to stack 2, but now it's
crate `C` that gets moved:

```
        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
```

In this example, the CrateMover 9001 has put the crates in a totally different
order: `MCD`.

Before the rearrangement process finishes, update your simulation so that the
Elves know where they should stand to be ready to unload the final supplies.
**After the rearrangement procedure completes, what crate ends up on top of each
stack?**

--]]

-- Stack Meta class
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
      local tmp = Stack:new()
      for i=1, tonumber(amount) do
        local popped = stacklist[tonumber(from)]:pop()
        tmp:push(popped)
      end
      for i=1, #tmp do
        local popped = tmp:pop()
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

    print("Crates on top: " .. table.concat(word)) -- "GSLCMFBRP"
  end
end

main()
