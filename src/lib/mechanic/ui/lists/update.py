from vanilla import CheckBoxListCell

from mechanic.update import Update
from mechanic.storage import Storage
from mechanic.ui.lists.extension import ExtensionList
from mechanic.ui.formatters.version import VersionFormatter


class UpdateList(ExtensionList):
    """Return an ExtensionList for updates window."""

    class ConnectionError(Exception): pass

    columns = [{"title": "Install",
                "key": "install",
                "width": 40,
                "editable": True,
                "cell": CheckBoxListCell()},
               {"title": "Extension",
                "key": "name",
                "width": 300,
                "editable": False},
               {"title": "Version",
                "key": "remote_version",
                "width": 60,
                "editable": False,
                "formatter": VersionFormatter.alloc().init()}]

    def __init__(self, posSize, **kwargs):
        self.is_refreshing = False
        self.refresh_callback = kwargs.get('refreshCallback')
        if self.refresh_callback:
            del kwargs['refreshCallback']
        super(UpdateList, self).__init__(posSize, [], **kwargs)

    def refresh(self, force=False):
        try:
            self.is_refreshing = True
            self.enable(False)
            self.set(Update.all(force))
            if self.refresh_callback:
                self.refresh_callback()
        except Update.ConnectionError:
            raise UpdateList.ConnectionError
        finally:
            self.enable(True)
            self.is_refreshing = False

    def _wrapItem(self, extension):
        item = super(UpdateList, self)._wrapItem(extension)
        item['remote_version'] = extension.remote.version
        return item

    @property
    def selected(self):
        return [row['self'] for row in self.get() if row['install']]
