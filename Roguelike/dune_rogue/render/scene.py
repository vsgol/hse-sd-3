from abc import ABC


class Scene(ABC):
    """Abstract class for scenes (e.g. level, menus)"""
    def render(self):
        """Now supposed to return tuple of text and colors"""
        raise NotImplementedError('render function is not implemented')

    def process_input(self, action):
        """Processes user action in current scene
        :param action: committed action
        :return: new state
        """
        raise NotImplementedError('process_input function is not implemented')
