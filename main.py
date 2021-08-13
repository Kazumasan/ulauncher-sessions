import os
import subprocess
import json

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk 

from helpers import *

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import ItemEnterEvent, KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


class DemoExtension(Extension):
    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        extensions_raw = extension.preferences["file_extensions"]
        extension_depth = extension.preferences["extension_depth"]
        workspaces_root = os.path.expanduser(extension.preferences["root"])
        workspaces = scan_workspaces(
            workspaces_root, int(extension_depth), formatExtension(extensions_raw)
        )
        print("----> Found: ", workspaces)
        
        #filter workspaces by query
        query = event.get_argument()
        print(query)
        if(query != "" and query != None):
            query = query.strip().lower()
            filtered = []
            for ws in workspaces:
                if query in ws.lower():
                    filtered.append(ws)
        else:
            filtered = workspaces


        entries = []
        for fl in filtered:
            action = checkFile(fl)
            entries.append(
                ExtensionResultItem(
                    icon=action["icon"],
                    name=formatName(fl),
                    description=fl,
                    on_enter=ExtensionCustomAction(
                        {
                            "open_cmd": action["command"],
                            "opt": [fl, action],
                        },
                        keep_app_open=True,
                    ),
                )
            )  # append Items here
        return RenderResultListAction(entries)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        cmd_path = data["open_cmd"]
        opt = data["opt"]

        if cmd_path == "notlinked":
            return RenderResultListAction(notlinked(opt[0], opt[1]))
        else:
            execAction(cmd_path, opt)


if __name__ == "__main__":
    DemoExtension().run()
