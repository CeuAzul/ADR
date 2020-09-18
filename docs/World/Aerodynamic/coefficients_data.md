# coefficients_data

This file contains several functions for calculating the lift, drag and moment coefficients for a fictional airfoil based on the Selig1223. It also contains the same functions for calculating the coefficient of the inverted version of the airfoil (usually used on horizontal stabilizers).

This fictional airfoil stalls for 15 degrees and -5 degrees of AoA.

One just need to call the corresponding function with the desired angle-of-attack as argument:
```python
from adr.World.Aerodynamic.coefficients_data import get_CL, get_CD, get_CM, get_CL_inv, get_CD_inv, get_CM_inv

print(get_CL(18))
>>> 0
print(get_CL(12))
>>> 1.8
print(get_CL(-2))
>>> 0.399
print(get_CL(-12))
>>> 0


print(get_CD(18))
>>> 2.1
print(get_CD(12))
>>> 0.18


print(get_CM(18))
>>> 0
print(get_CM(12))
>>> -0.251


print(get_CL_inv(18))
>>> 0
print(get_CL_inv(-12))
>>> -1.8


print(get_CD_inv(12))
>>> 2.1
print(get_CD_inv(-18))
>>> 2.1


print(get_CM_inv(18))
>>> 0
print(get_CM_inv(-12))
>>> 0.251
```