import json



def test_fetch_query_results():

    query_result = [
        [1,"usa",222,2022],
        [1,"usa",222,2022],
        [1,"usa",222,2022]
        ]

    # convert the query result to a json object
    columns = ["id", "country", "accidents", "year"]
    rows = json.dumps(query_result)
    data = [dict(zip(columns, row)) for row in rows]

    return data



if __name__ == "__main__":
    test_fetch_query_results()
