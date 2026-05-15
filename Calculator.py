class Calculator:
    """A simple calculator class for addition and subtraction operations."""
    
    def add_two_numbers(self, a, b):
        """Add two numbers and return the result.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            The sum of a and b
        """
        return a + b
    
    def add_three_numbers(self, a, b, c):
        """Add three numbers and return the result.
        
        Args:
            a: First number
            b: Second number
            c: Third number
            
        Returns:
            The sum of a, b, and c
        """
        return a + b + c
    
    def subtract_two_numbers(self, a, b):
        """Subtract two numbers and return the result.
        
        Args:
            a: First number (minuend)
            b: Second number (subtrahend)
            
        Returns:
            The difference of a and b
        """
        return a - b
    
    def subtract_three_numbers(self, a, b, c):
        """Subtract three numbers and return the result.
        
        Args:
            a: First number (minuend)
            b: Second number (subtrahend)
            c: Third number (subtrahend)
            
        Returns:
            The difference of a, b, and c
        """
        return a - b - c


# Example usage:
if __name__ == "__main__":
    calc = Calculator()
    
    # Add two numbers
    result_2 = calc.add_two_numbers(5, 10)
    print(f"5 + 10 = {result_2}")  # Output: 5 + 10 = 15
    
    # Add three numbers
    result_3 = calc.add_three_numbers(5, 10, 15)
    print(f"5 + 10 + 15 = {result_3}")  # Output: 5 + 10 + 15 = 30
    
    # Subtract two numbers
    result_sub_2 = calc.subtract_two_numbers(20, 5)
    print(f"20 - 5 = {result_sub_2}")  # Output: 20 - 5 = 15
    
    # Subtract three numbers
    result_sub_3 = calc.subtract_three_numbers(30, 10, 5)
    print(f"30 - 10 - 5 = {result_sub_3}")  # Output: 30 - 10 - 5 = 15