from typing import List, Set
import json
# Define a list with type annotation
my_list: List[Set[int]] = []

# Add a set to the list
# my_set: Set[int] = {1, 2, 3}
# my_list.append(my_set)

# tuple inside list 
my_tuple = (4, 5, 6)
my_list.append((4, 5, 6))
# Print the list
print(json.dumps(my_list))