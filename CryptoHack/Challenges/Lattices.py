import numpy as np

A = np.array([
    [6, 2, -3],
    [5, 1,  4],
    [2, 7,  1]
])

# Compute the determinant
determinant = round(np.linalg.det(A)) 
volume = abs(determinant)

print("Matrix A:")
print(A)
print("\nDeterminant of A:", determinant)
print("Volume of the fundamental domain:", volume)
