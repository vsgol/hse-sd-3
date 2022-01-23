# CLI

A bash-like command line emulator.

## Architecture overview

![Architecture](architecture.png)

The `Main App` reads user commands in an endless loop.

`Main App` object contains `Memory` field for keeping variables values. `Memory` is a key-value storage.

Then the string is parsed by a finite-state machine in `Formatter`, which substitutes variables with their values taken from `Memory`, skipping the substitution in single quotes

The string is passed to the `Parser`, which splits the string into tokens and passes the resulting sequence (syntax tree if we need to support brackets, for now it seems much easier to use a list of commands) to the `Command Factory`.

`Command Factory` creates a descendant of the `Command` class for each element of parsed sequence (or for each nodes of the syntax tree if we use one). Each `Command` object contains `execute` method for perfoming corresponding operation and takes required arguments (e.g. `Cat`'s `execute` method takes name of file and outputs provided file content)

The tree is passed to the `Executor`, which sequentially calls all nodes with the `execute` method using provided arguments, passing the output to the following nodes as their input 

The resulting output or error messages returns to the `Main App`, where it further output to the user.

