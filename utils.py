def readFile(path: str) -> str:
    """
    Reads a file and returns its content as a string.
    Args:
        path (str): Path to the file.
    Returns:
        str: Content of the file.
    """
    with open(path, "r") as file:
        return file.read()

