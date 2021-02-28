# ![icon](./images/icon2.png) Sessions  
## Launch Session files like any other Programm

![gif](./demo.gif)

This plugin is should make it easy if you use vim Sessions or any other session file.

in Preferences just point it to a higher directory than all of your code.

*Recommended folder strucure should look like this*

``` sh

 ~/Code/Project-A/SessionA.code-workspace
    .../Project-B/SessionB.code-workspace
    .../Project-C/SessionC.code-workspace
```

Note: although not Tested it should follow symlink meaning you can link your session files to a central place. Like:


``` sh
 ~/Sessions/Project-A/SessionALink.code-workspace   (link)
        .../Project-B/SessionBLink.code-workspace   (link)
        .../Project-C/SessionCLink.code-workspace   (link)
```

## Search Root

Where to start looking for your session files e.g `~/Code`

## File extensions

A comma-seperated-list of file extensions you want to include e.g `.code-workspace, .vim-sessions`

## Search depth

File Searching is kinda Curde so don't go too deep.

``` sh
Depth of 1 means ~/Code(1)

Depth of 2 means ~/Code(1)/Project-A(2)/

... and so on

```

## Session Actions

Session actions are json objects that define what you want to do with the selected files 

default is for VSCode and Neovim (remove it if you dont need it)
``` JS

[
    {
        "extension": ".vim-session",        //file extension this action applys to
        "command" : "konsole -e nvim -S",   //command / application
        "isCLI" : true,                     //if the executable is a terminal app or not e.g vim / neovim
                                            //but can also help if it doesn't work otherwise
        "display_name" : "Open in Neovim",  //actually obsolete but well its there i guess ?
        "icon" : "images/nvim.png"          //poins to the icon you want to display next to it.
    },
    {
        "extension": ".code-workspace",
        "command" : "code",
        "isCLI" : false,
        "display_name" : "Open in VSCode",
        "icon" : "images/vscode.png"
    }
]
```

**Located** @ `~/.local/share/ulauncher/extensions/Sessions/`

## Unlinked files

if you have added a file extension to the list that doesnt have an actions set up e.g `.eclipse`
it will ask you wich actions you want to try on it. 

idea behind that is that for example vim sessions are vimscript that doesnt have to end with .vim (*file content is more important*) so if i setup a .vim action it will treat all other .vim files as "Session" wich is unwanted but in case you know that this file actually hase the session as its content and perhaps the file extensions is incorrect fore some reason this will provide a neat way to remedy that. It will then try to open that file with that action.
