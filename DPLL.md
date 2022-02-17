```
function DPLL(Φ)  
   if Φ is a consistent set of literals  
       then return true;  
   if Φ contains an empty clause  
       then return false;  
   for every unit clause l in Φ  
      Φ ← unit-propagate(l, Φ);  
   for every literal l that occurs pure in Φ  
      Φ ← pure-literal-assign(l, Φ);  
   l ← choose-literal(Φ);  
   return DPLL(ΦΛl) or DPLL(ΦΛnot(l)); 
```

```
      1∨2,  2∨~3∨4,   ~1∨~2,  ~1∨~3∨~4,   1
1           2 ~3 4     ~2      ~3 ~4       
1,-2        -3 4               -3 -4
1,-2,3      4                  -4
1 -2 3 4                        0

```
