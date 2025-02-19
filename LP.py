import numpy as np

def get_int_input(prompt, min_value=1):
    """Ensures valid integer input greater than or equal to min_value."""
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
            print(f"Error: Value must be at least {min_value}. Try again.")
        except ValueError:
            print("Invalid input. Enter a valid integer.")

def get_list_input(prompt, expected_length=None):
    """Ensures a valid space-separated list of integers."""
    while True:
        try:
            values = list(map(int, input(prompt).split()))
            if expected_length and len(values) != expected_length:
                print(f"Error: Expected {expected_length} values. You entered {len(values)}. Try again.")
                continue
            return values
        except ValueError:
            print("Invalid input. Enter space-separated integers.")

def main():
    # Step 1: Get Valid Inputs
    n = get_int_input("Enter number of variables: ")
    f_x = get_list_input(f"Enter {n} coefficients of the objective function: ", n)
    while True:  # Loop until the user provides a valid, invertible constraint matrix
        A = [get_list_input(f"Enter row {i + 1} of the constraint matrix ({n} values): ", n) for i in range(n)]
        A = np.array(A)

        if np.linalg.matrix_rank(A) < n:
            print("Error: The constraint matrix is singular (not invertible). Please enter independent constraints.")
            continue  # Ask user to re-enter A
        break  # If A is invertible, proceed

    b = get_list_input(f"Enter {n} constraint limits: ", n)
    b = np.array(b)

    # Compute the balanced solution by solving A*x = b.
    balanced_solution = np.linalg.inv(A).dot(b)


    # Step 2: Print Setup Table (Now Adjusts Based on n)
    variable_headers = " | ".join([f"x{i + 1}(units)" for i in range(n)])  # column names
    print("\n--------------------------------------------------------------")
    print(f" Supply      | {variable_headers} | Profit ")
    print("--------------------------------------------------------------")

    for i in range(n):
        Variable_values = "     |    ".join(str(A[j][i]) for j in range(n))  # format columns
        print(f"Variable {i + 1}   |     {Variable_values}      |  ${f_x[i]}")

    print("--------------------------------------------------------------")
    availability_values = "     |  ".join(str(b[i]) for i in range(n))  # availability row
    print(f" Availability|   {availability_values}      |")
    print("--------------------------------------------------------------")


    # Calculate and print the solo solution for each variable.
    solution = {}
    for i in range(n):
        limits = []
        # For each constraint j, when only variable i is active:
        for j in range(len(b)):
            coeff = A[j][i]
            if coeff != 0:
                limits.append(b[j] / coeff)
        solo_value = min(limits) if limits else float('inf')
        solo_profit = f_x[i] * solo_value
        solution[f"using only Formula {i+1}"] = solo_profit


        print(f"If only variable {i + 1} is made, there would be a profit of: {solo_profit:.1f}. The number of units produced would be {solo_value:.1f}")

    # Compute the profit for the balanced solution.
    balanced_profit = sum(f_x[i] * balanced_solution[i] for i in range(n))
    solution["using the balanced option"] = balanced_profit

    best_option = max(solution, key=solution.get)
    best_value = solution[best_option]

    # printing the balanced solution along with its profit.
    print(f"The balanced amount is ${balanced_profit}. The breakdown is {balanced_solution}")
    print(f"The best possible solution is ${best_value} {best_option}")


if __name__ == "__main__":
    main()

"""
Enter number of variables: 3
Enter 3 coefficients of the objective function: 3000 2000 2000
Enter row 1 of the constraint matrix (3 values): 2 4 5
Enter row 2 of the constraint matrix (3 values): 1 2 4
Enter row 3 of the constraint matrix (3 values): 8 0 3
Enter 3 constraint limits: 300 200 300

--------------------------------------------------------------
 Supply      | x1(units) | x2(units) | x3(units) | Profit 
--------------------------------------------------------------
Variable 1   |     2     |    1     |    8      |  $3000
Variable 2   |     4     |    2     |    0      |  $2000
Variable 3   |     5     |    4     |    3      |  $2000
--------------------------------------------------------------
 Availability|   300     |  200     |  300      |
--------------------------------------------------------------
If only variable 1 is made, there would be a profit of: 112500.0. The number of units produced would be 37.5
If only variable 2 is made, there would be a profit of: 150000.0. The number of units produced would be 75.0
If only variable 3 is made, there would be a profit of: 100000.0. The number of units produced would be 50.0
The balanced amount is $183333.3333333333. The breakdown is [25.         20.83333333 33.33333333]
The best possible solution is $183333.3333333333 using the balanced option

"""