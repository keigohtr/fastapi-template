"""
Utilities.
"""
import uuid


def random_resource_id() -> str:
    """Generate random ID.
    Returns:
        id (str): ID.
    """
    return str(uuid.uuid4())
