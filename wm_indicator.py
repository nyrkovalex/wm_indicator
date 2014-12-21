#! /usr/bin/env python

from gi.repository import AppIndicator3 as AppIndicator
from gi.repository import Gtk
from subprocess import Popen, PIPE, STDOUT

import os


def is_exec_available(cmd):
    for path in os.environ['PATH'].split(os.pathsep):
        path = path.strip('"')
        exec_path = os.path.join(path, cmd)
        if os.path.isfile(exec_path) and os.access(exec_path, os.X_OK):
            return True
    return False



class WindowManager(object):

    def __init__(self, name, command):
        self.name = name
        self.command = command
        self.available = is_exec_available(command)
        self._process = None

    def is_running(self):
        ps = Popen(['ps', '-e'], stdout=PIPE)
        for line in ps.stdout:
            if line.find(self.name) >= 0:
                return True
        return False

    def replace(self):
        self._process = Popen([self.command, '--replace'], stdout=PIPE, stderr=STDOUT)


SUPPORTED_MANAGERS = [
    WindowManager('Gala', 'gala'),
    WindowManager('Openbox', 'openbox'),
    WindowManager('Compiz', 'compiz'),
    WindowManager('Mutter', 'mutter'),
]


class Application(object):

    def __init__(self, managers):
        self._managers = managers
        self._wm_items = self._create_wm_items(managers)
        self._ind = self._create_indicator()
        Gtk.init()

    def _create_indicator(self):
        indicator = AppIndicator.Indicator.new(
            'wm_indicator',
            'wm_indicator',
            AppIndicator.IndicatorCategory.OTHER
        )
        indicator.set_menu(self._create_menu())
        indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        return indicator

    def _create_wm_items(self, managers):
        items = []
        group = None
        for wm in managers:
            if not wm.available:
                print wm.name + ' is not available'
                continue
            item = self._create_single_wm_item(wm, group)
            group = item
            items.append(item)
        return items

    def _create_menu(self):
        menu = Gtk.Menu()
        for wm_item in self._wm_items:
            menu.append(wm_item)
        menu.append(self._create_separator_item())
        menu.append(self._create_quit_item())
        menu.show()
        return menu

    def _create_quit_item(self):
        item = Gtk.MenuItem()
        item.set_label('Quit')
        item.connect('activate', self.quit)
        item.show()
        return item

    def _create_separator_item(self):
        separator = Gtk.SeparatorMenuItem()
        separator.show()
        return separator

    def _create_single_wm_item(self, wm, group):
        item = Gtk.RadioMenuItem(group=group, label=wm.name)
        item.wm = wm
        item.set_active(wm.is_running())
        item.connect('toggled', self.switch)
        item.show()
        return item

    def quit(self, widget):
        Gtk.main_quit()

    def switch(self, widget):
        if not widget.get_active():
            return
        widget.wm.replace()

    def run(self):
        Gtk.main()


if __name__ == '__main__':
    app = Application(SUPPORTED_MANAGERS)
    app.run()


