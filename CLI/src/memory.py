class Memory:
    """Responsible for storing environment variables

        Attributes:
            data: A dict storing environment variables
    """
    def __init__(self):
        self.data = {}

    def get_value(self, key):
        """Gets value for key

            Args:
                key: A str for variable name
            Returns:
                A string value for variable if exists. Otherwise returns ''
        """
        return self.data.get(name, '')

    def set_value(self, key, value):
        """Sets value for key

            Args:
                key: A str for variable name
                value: A str for new value of variable
        """
        self.data[name] = value

    def get_env(self):
        """Gets all variables values

            Returns:
                A dict with all variables
        """
        return self.data
