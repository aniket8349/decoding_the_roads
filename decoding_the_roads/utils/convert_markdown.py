import markdown

def convert_markdown_fields(data: dict) -> dict:
    """
    Recursively converts Markdown-formatted text fields in a dictionary to HTML.
    
    Args:
        data (dict): The dictionary containing Markdown text.

    Returns:
        dict: The updated dictionary with Markdown fields converted to HTML.
    """
    for key, value in data.items():
        if isinstance(value, dict):  # Ensure we process only nested dictionaries
            if "description" in value:
                value["description"] = markdown.markdown(value["description"])
            if "explination" in value:
                value["explination"] = markdown.markdown(value["explination"])
    return data
