import os
import subprocess
import json

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
        
        # Filter by query if inserted but Names not pathes....
        query = event.get_argument()
        if query:
            query = query.strip().lower()
            for ws in workspaces:
                name = ws.lower()
                if query not in name:
                    workspaces.pop(ws)

        entries = []
        
        for ws in workspaces:
            action = checkFile(ws)
            print("-----------", action)
            entries.append(
                ExtensionResultItem(
                    icon=action["icon"],
                    name=formatName(ws),
                    description=ws,
                    on_enter=ExtensionCustomAction(
                        {
                            "open_cmd": action["command"],
                            "opt": [ws, action],
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

        print("-----" , data)

        if cmd_path == "notlinked":
            print("\n --- calling notlinked --- \n")
            return RenderResultListAction(notlinked(opt[0], opt[1]))
        else:
            execAction(cmd_path, opt)






if __name__ == "__main__":
    DemoExtension().run()
