# CLI

A bash-like command line emulator.

## Architecture overview

![Architecture](architecture.png)

The `Main App` reads user commands in an endless loop. 

Then the string is parsed by a finite-state machine in `Formatter`, which substitutes variables with their values, skipping the substitution in single quotes

The string is passed to the `Parser`, which splits the string into tokens and passes the resulting syntax tree to the `Command Factory`.

`Command Factory` creates a descendant of the `Command` class in the nodes of the syntax tree.

The tree is passed to the `Executor`, which sequentially calls all nodes with the `execute` method, passing the output to the following nodes

The resulting output with error messages is returned to the `Main App`, where it is further output to the user.

