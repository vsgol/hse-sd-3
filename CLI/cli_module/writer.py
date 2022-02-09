class Writer:
    """Responsible for writing output"""

    def print_outputs(self, stdout, stderr):
        """Writes output

            Args:
                stdout: A str for output
                stderr: A str for errors
        """
        print(f'stdout: {stdout}\nstderr:{stderr}')
