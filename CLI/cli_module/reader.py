class Reader:
    """Responsible for reading user input"""

    def get_line(self):
        """Reads user input

            Returns:
                A string for user input
        """
        user_input = ''
        while not len(user_input):
            user_input = input('>>> ')
        return user_input
