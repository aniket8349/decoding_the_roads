from ..utils.sql_utils import fetch_query_results, execute_query;
from ..config.db_config import db_config
from .logger import setup_logger
logger = setup_logger(__name__)  

def sqlquery_to_json(query_result=None, x="x", y="y", row1_num=None, row2_num=None):
    """ 
    Function to convert the SQL query result to a JSON object
    
    args: 
        query_result: List of tuples
        x: str
        y: str
        row1_num: int
        row2_num: int
    
    returns:
        result_dict: Dict
    """
    try:
        result_dict = {x: [], y: []}
        # Your code for executing the SQL query and converting the result to JSON
        if query_result  is None:
            raise ValueError("query_result cannot be None")
        if row1_num is None or row2_num is None:
            raise ValueError("row1_num and row2_num cannot be None")

        for row in query_result:
            result_dict[x].append(row[row1_num])
            result_dict[y].append(row[row2_num])

        return result_dict
    except Exception as e:
        # Handle any exceptions that occur during the execution of the SQL query
        logger.error(f"An error occurred: {str(e)}")

# Call the function
# sqlquery_to_json()

if __name__ == "__main__":
    query = "SELECT * FROM accident_data LIMIT 4;"
    query_result = fetch_query_results(db_config, query)
    print(query_result)
    result =  sqlquery_to_json(query_result=query_result, x="country", y="accidents", row1_num=1, row2_num=2)
    print(result)