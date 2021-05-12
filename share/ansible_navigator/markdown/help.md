## GENERAL
----------------------------------------------------------------------------------------------------
esc                                                   Go back
^f/PgUp                                               Page up
^b/PgDn                                               Page down
arrow up, arrow down                                  Scroll up/down
:collections                                          Explore installed collections
:config                                               Explore the current Ansible configuration
:eed, :ee-details -eei <image>                        Explore execution environment details
:d, :doc <plugin>                                     Show a plugin doc
:r, :run <playbook> -i <inventory>                    Run a playbook in interactive mode
:f, :filter <re>                                      Filter page lines using a regex
:h, :help                                             This page
:i -i <inventory>, :inventory -i <inventory>          Explore the current or alternate inventory
:l, :log                                              Review current log file
:load  <file>                                         Load a playbook artifact
:o, :open                                             Open current page in the editor
:o, :open {{ some_key }}                              Open file path in a key's value
:q, :quit                                             Quit the application
:q!, :quit!, ^c                                       Force quit while a playbook is running
:rr, :rerun                                           Rerun the playbook
:s, :save <file>                                      Save current plays as an artifact
:st, :stdout                                          Watch playbook results real time
:w, :write <file>                                     Write current page to a new file
:w!, :write! <file>                                   Write current page to an existing or new file
:w>>, :write>> <file>                                 Append current page to an existing file
:w!>>, :write!>> <file>                               Append current page to an existing or new file

## MENUS
--------------------------------------------------------------------------------------
[0-9]                                   Go to menu item
:<number>                               Go to menu item
:{{ n|filter }}                         Template the menu item

## TASKS
--------------------------------------------------------------------------------------
[0-9]                                   Go to task number
:<number>                               Go to task number
+, -                                    Next/Previous task
_, :_                                   Toggle hidden keys
:{{ key|filter }}                       Template the key's value
:d, :doc                                Show the doc for the current task's module
:j, :json                               Switch to JSON serialization
:y, :yaml                               Switch to YAML serialization

## LINE INPUT
--------------------------------------------------------------------------------------
esc                                     Exit line input
^A                                      Beginning of line
^E                                      End of line
insert                                  Enable/disable insert mode
arrow up, arrow down                    Previous/next command in history
