# TITLE: Baby RE

## CHALLENGE INFOS

Type: Reversing

Task: Show us your basic skills! (P.S. There are 4 ways to solve this, are you willing to try them all?)

## FIRST THOUGHTS

It seems like a simple binary file...
Maybe with strings we can find something
Ghidra can help us

## ATTEMPS

Let's try to run this file... It asks for an input string
Maybe we can try with a buffer overflow?
Let's try to open the binary in Ghidra...
Let's search for the main function and let's see how it works

Code
```

  fgets(local_28,0x14,stdin);
  iVar1 = strcmp(local_28,"abcde122313\n");
  if (iVar1 == 0) {
    local_48 = 0x594234427b425448;
    local_40 = 0x3448545f5633525f;
    local_38 = 0x455f5354;
    local_34 = 0x7d5a;
    puts((char *)&local_48);
  }
  else {
    puts("Try again later.");
  }
```

It just... strcmp the input with a given string so let's try using that.

## SOLUTION

Tools: Ghidra

We used Ghidra to disassembly the binary and found out that we needed to input "abcde122313"

Flag: HTB{B4BY_R3V_TH4TS_EZ}
