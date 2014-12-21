#! /usr/bin/env python

from gi.repository import AppIndicator3 as AppIndicator
from gi.repository import Gtk
from subprocess import Popen


SUPPORTED_MANAGERS = {
    'Gala': 'gala',
    'Openbox': 'openbox'
}


class Application(object):

    def __init__(self, managers):
        self._managers = managers
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

    def _create_menu(self):
        menu = Gtk.Menu()
        for label, command in self._managers.items():
            menu.append(self._create_wm_item(label, command))
        menu.append(self._create_quit_item())
        menu.show()
        return menu

    def _create_quit_item(self):
        item = Gtk.MenuItem()
        item.set_label('Quit')
        item.connect('activate', self.quit)
        item.show()
        return item

    def _create_wm_item(self, label, command):
        item = Gtk.MenuItem()
        item.set_label(label)
        item.connect('activate', self.switch, command)
        item.show()
        return item

    def quit(self, widget):
        Gtk.main_quit()

    def switch(self, widget, name):
        Popen([name, '--replace'])

    def run(self):
        self._ind = self._create_indicator()
        Gtk.main()


if __name__ == '__main__':
    app = Application(SUPPORTED_MANAGERS)
    app.run()


