
import random


class OCLMetamodel:
    """Defines valid OCL constructs."""
    def __init__(self):
        self.basic_operators = [">", "<", ">=", "<=", "=", "and", "or"]
        self.quantifiers = ["forall", "exists"]
        self.navigation = ["size()", "isEmpty()", "notEmpty()"]

    def random_operator(self, op_type: str) -> str:
        """Select a random operator based on the type."""
        if op_type == "basic":
            return random.choice(self.basic_operators)
        elif op_type == "quantifiers":
            return random.choice(self.quantifiers)
        elif op_type == "navigation":
            return random.choice(self.navigation)
        return ""
