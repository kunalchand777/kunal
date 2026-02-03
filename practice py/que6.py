rows = int(input("Enter the row size for the pattern: "))
for i in range(1, rows + 1):  # Outer loop for rows
    for j in range(1, rows + 1):  # Inner loop for columns
        if i == 1 or i == rows or j == 1 or j == rows :  # Print star only on borders
            print("*", end=" ")
        else:
            print(" ", end=" ")  # Print space inside
    print()