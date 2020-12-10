## GENERAL
--------------------------------------------------------------------------------------
esc                                     Go back
^f/PgUp                                 Page up
^b/PgDn                                 Page down
arrow up, arrow down                    Scroll up/down
:blog                                   Check out the recent Ansible blog entries
:bullhorn                               Catch up on the latest bullhorn issues
:d <plugin> :doc <plugin>               Show a plugin doc
:f, :filter <re>                        Filter page lines using a regex
:h, :help                               This page
:l, :log                                Review current log file
:o, :open                               Open current page in the editor
:o, :open {{ some_key }}                Open file path in a key's value
:q, :quit                               Quit the application
:q!, :quit!, ^c                         Force quit while a playbook is running
:redhat                                 See the latest from Red Hat
:rr, :rerun                             Rerun the playbook
:s <file>, :save <file>                 Save current plays as an artifact
:st, :stream                            Watch playbook results realtime
:w <file>, :write <file>                Write current page to a new file
:w! <file>, :write! <file>              Write current page to an existing or new file
:w>> <file> :write>> <file>             Append current page to an existing file
:w!>> <file> :write!>> <file>           Append current page to an existing or new file

## MENUS
--------------------------------------------------------------------------------------
[0-9]                                   Go to menu item
:<number>                               Go to menu item
:{{ n|filter }}                         Template the menu item

## TASKS
--------------------------------------------------------------------------------------
[0-9]                                   Goto task number
:<number>                               Goto task number
+, -                                    Next/Previous task
_, :_                                   Toggle hidden keys
:{{ key|filter }}                       Template the key's value
:d, :doc                                Show the doc for the current task's module
:j, :json                               Switch to json serializtion
:y, :yaml                               Switch to yaml serialization

## LINE INPUT
--------------------------------------------------------------------------------------
esc                                     Exit line input
^A                                      Beginning of line
^E                                      End of line
insert                                  Enable/disable insert mode
arrow up, arrow down                    Previous/next command in history