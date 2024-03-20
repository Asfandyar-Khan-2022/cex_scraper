import re

# Original string
original_string = '£140.00\n£49.00Trade-in for Voucher\n£28.00Trade-in for Cash'

# Extracting numbers using regular expressions
numbers = re.findall(r'\d+\.\d+', original_string)

# Converting to float and then to int
numbers = [int(float(num)) for num in numbers]

print(numbers)
