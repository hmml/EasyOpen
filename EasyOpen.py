import os
import sublime
import sublime_plugin


class EasyOpenCommand(sublime_plugin.TextCommand):

    __path = ''
    __currentList = []

    def run(self, edit):
        settings = sublime.load_settings('EasyOpen.sublime-settings')
        startPath = settings.get('start_directory', u'~')
        self.__path = os.path.abspath(os.path.expanduser(startPath))
        self.newViewFromPath(self.__path)

    def newViewFromPath(self, path):
        self.__currentList = os.listdir(path)
        self.showQuickPanel(self.__currentList, self.onSelected)

    def showQuickPanel(self, elements, onSelection):
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(elements, onSelection), 10)

    def onSelected(self, index):
        if index == -1:
            pass
        else:
            selectedFilePath = os.path.join(
                self.__path, self.__currentList[index])
            if os.path.isfile(selectedFilePath):
                self.view.window().open_file(selectedFilePath)
            elif os.path.isdir(selectedFilePath):
                self.__path = selectedFilePath
                for name in os.listdir(self.__path):
                    self.__currentList = os.listdir(self.__path)
                self.showQuickPanel(self.__currentList, self.onSelected)
            else:
                print('EasyOpen, warning: not a file nor a directory (%s)...' % selectedFilePath)
