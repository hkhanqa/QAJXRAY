import unittest
from Calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Test cases for the Calculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()
    #---------------------------------------------------------------------------------
    # def test_PC_101_add_two_numbers_positive(self):
    def test_PC_3_add_two_numbers_positive(self):
        """Test adding two positive numbers."""
        result = self.calc.add_two_numbers(5, 10)
        print(f"-------------------------------------------------------------------")
        print(f"Test adding two positive numbers.")
        print(f"Input Values : 5 , 10")
        print(f"Expected Output : 15")
        print(f"Actual Output : {result}")
        print(f"-------------------------------------------------------------------")
        self.assertEqual(result, 25)
    #---------------------------------------------------------------------------------
    def test_PC_4_add_three_numbers_positive(self):
        """Test adding three positive numbers."""
        result = self.calc.add_three_numbers(5, 10, 15)
        print(f"-------------------------------------------------------------------")
        print(f"Test adding three positive numbers.")
        print(f"Input Values : 5 , 10 , 15")
        print(f"Expected Output : 30")
        print(f"Actual Output : {result}")
        print(f"-------------------------------------------------------------------")
        self.assertEqual(result, 30)
    #---------------------------------------------------------------------------------
    def test_PC_11_subtract_two_numbers_negative(self):
        """Test subtracting two negative numbers."""
        result = self.calc.subtract_two_numbers(-10, -5)
        #−10−(−5)=−5
        print(f"-------------------------------------------------------------------")
        print(f"Test subtracting two negative numbers.")
        print(f"Input Values : -10 , -5")
        print(f"Expected Output : -5")
        print(f"Actual Output : {result}")
        print(f"-------------------------------------------------------------------")
        self.assertEqual(result, -5)
    #---------------------------------------------------------------------------------
    def test_PC_12_subtract_three_numbers_negative(self):
        """Test subtracting three negative numbers."""
        result = self.calc.subtract_three_numbers(-30, -10, -5)
        # −30−(−10)−(−5)  , −30+10+5=−15
        print(f"-------------------------------------------------------------------")
        print(f"Test subtracting three negative numbers.")
        print(f"Input Values : -30 , -10 , -5")
        print(f"Expected Output : -15")
        print(f"Actual Output : {result}")
        print(f"-------------------------------------------------------------------")
        self.assertEqual(result, -15)
    #---------------------------------------------------------------------------------
    # def test_add_two_numbers_negative(self):
    #     """Test adding two negative numbers."""
    #     result = self.calc.add_two_numbers(-5, -10)
    #     self.assertEqual(result, -15)
    
    # def test_add_two_numbers_mixed(self):
    #     """Test adding positive and negative numbers."""
    #     result = self.calc.add_two_numbers(10, -3)
    #     self.assertEqual(result, 7)
    
    # def test_add_two_numbers_zero(self):
    #     """Test adding with zero."""
    #     result = self.calc.add_two_numbers(5, 0)
    #     self.assertEqual(result, 5)
    
    # def test_add_three_numbers_negative(self):
    #     """Test adding three negative numbers."""
    #     result = self.calc.add_three_numbers(-5, -10, -15)
    #     self.assertEqual(result, -30)
    
    # def test_add_three_numbers_mixed(self):
    #     """Test adding mixed positive and negative numbers."""
    #     result = self.calc.add_three_numbers(10, -5, 3)
    #     self.assertEqual(result, 8)
    
    # def test_add_three_numbers_zero(self):
    #     """Test adding three numbers with zero."""
    #     result = self.calc.add_three_numbers(0, 0, 0)
    #     self.assertEqual(result, 0)
    
    # def test_subtract_two_numbers_positive(self):
    #     """Test subtracting two positive numbers."""
    #     result = self.calc.subtract_two_numbers(20, 5)
    #     self.assertEqual(result, 15)
    
  
    
    # def test_subtract_two_numbers_mixed(self):
    #     """Test subtracting mixed positive and negative numbers."""
    #     result = self.calc.subtract_two_numbers(10, -5)
    #     self.assertEqual(result, 15)
    
    # def test_subtract_two_numbers_zero(self):
    #     """Test subtracting with zero."""
    #     result = self.calc.subtract_two_numbers(5, 0)
    #     self.assertEqual(result, 5)
    
    # def test_subtract_three_numbers_positive(self):
    #     """Test subtracting three positive numbers."""
    #     result = self.calc.subtract_three_numbers(30, 10, 5)
    #     self.assertEqual(result, 15)
    

    
    # def test_subtract_three_numbers_mixed(self):
    #     """Test subtracting mixed positive and negative numbers."""
    #     result = self.calc.subtract_three_numbers(20, -5, 3)
    #     self.assertEqual(result, 22)
    
    # def test_subtract_three_numbers_zero(self):
    #     """Test subtracting three numbers with zero."""
    #     result = self.calc.subtract_three_numbers(0, 0, 0)
    #     self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='reports'),
        verbosity=2
    )
