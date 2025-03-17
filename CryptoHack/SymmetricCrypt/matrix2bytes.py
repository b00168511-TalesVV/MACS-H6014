def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array. """
    return bytes([byte for row in matrix for byte in row])

# Given matrix
matrix = [
    [99, 114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97, 116],
    [114, 105, 120, 125],
]

# Convert matrix to bytes
result = matrix2bytes(matrix)

# Print the result
print(result)