class Writer:
    """Responsible for writing output"""

    def print_outputs(self, stdout, stderr):
        """Writes output

            Args:
                stdout: A str for output
                stderr: A str for errors
        """
        if stdout != '':
            print(f'stdout: {stdout}')
        if stderr != '':
            print(f'stderr: {stderr}')
