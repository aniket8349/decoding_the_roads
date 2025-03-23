def calculate_percentage_increase(new_value: float, old_value: float, decimals: int = 2) -> float:
    """
    Calculate the percentage of a part in relation to the total.

    Args:
        part (float): The numerator (portion of the total).
        total (float): The denominator (total value).
        decimals (int): Number of decimal places to round to (default: 2).

    Returns:
        float: The calculated percentage. Returns 0.0 if total is 0.
    """

    try:
        if old_value == 0:
            return 0.0  # Prevent division by zero
        return round(((new_value - old_value) / old_value) * 100, decimals)
    except ZeroDivisionError:
        return 0.0
    except Exception as e:
        raise e
    
if __name__ == "__main__":
    # Test the calculate_percentage function
    print(calculate_percentage(5, 10))  # 50.0
    print(calculate_percentage(3, 10))  # 30.0
    print(calculate_percentage(0, 10))  # 0.0
    print(calculate_percentage(0, 0))
