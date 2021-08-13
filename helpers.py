#!/bin/python3
# helpers.py
import os
import json
import subprocess

from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


def checkFile(path):
    for x in sessionActions:
        if os.path.splitext(path)[1] == x["extension"]:
            return x

    linkObject = {
        "filename" : "",
        "extension": "",
        "command": "notlinked",
        "icon": "images/unlinked.png",
    }
    string = path
    string = string.split("/")
    string = string[len(string) - 1]  # e.g /home/bastian/main.py => string == main.py
    linkObject["extension"] = os.path.splitext(string)[1]
    linkObject["filename"] = string

    return linkObject

def loadJson(path):
    filepath = os.path.realpath(__file__)
    filepath = filepath.split("/")
    filepath.pop()
    filepath.append(path)
    path  = '/'.join(filepath)
    print("----------" , path)

    f = open(path)
    t = f.read()
    return json.loads(t)


def formatExtension(extension_raw):
    extensions = extension_raw.split(",")
    final = []
    for x in extensions:
        final.append(x.strip())
    return final


def formatName(string):
    string = string.split("/")
    string = os.path.splitext(string[len(string) - 1])[0]
    return string


def scan_workspaces(path, depth, extensions):
    results = []
    print(path, depth, extensions)
    if depth > 0:
        for x in os.listdir(path):
            if os.path.isdir(os.path.join(path, x)):
                for y in scan_workspaces(os.path.join(path, x), depth - 1, extensions):
                    results.append(y)
            else:
                if os.path.splitext(x)[1] in extensions:
                    results.append(os.path.join(path, x))
    else:
        for x in os.listdir(path):
            if os.path.splitext(x)[1] in extensions:
                results.append(os.path.join(path, x))
    return results


def notlinked(ws, linkObject):
    entries = []
    for action in sessionActions:
        entries.append(
            ExtensionResultItem(
                icon=action["icon"],
                name=linkObject['filename'] + " " + action["display_name"],
                description=ws,
                on_enter=ExtensionCustomAction(
                    {
                        "open_cmd": action["command"],
                        "opt": [ws, action],
                    },
                    keep_app_open=False,
                ),
            )
        )
    return entries


def execAction(cmd_path, opt):
    subprocess.Popen(
        cmd_path + " " + opt[0], shell=opt[1]["isCLI"], cwd=os.path.dirname(opt[0])
    )

print(os.path.realpath(__file__))
sessionActions = loadJson("/session-actions.json")