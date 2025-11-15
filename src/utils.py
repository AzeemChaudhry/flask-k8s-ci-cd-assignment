# Small utility functions used by the Flask app and unit tests.
# Keep this file minimal — it's intentionally simple so tests are easy.
def add(a, b):
    """
    Add two numbers and return the result.

    This function is intentionally trivial:
    - Good candidate for a unit test (deterministic)
    - Keeps our CI fast
    """
    return a + b
