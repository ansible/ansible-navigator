.. _using_ansible_navigator:

*******************************
Understanding ansible-navigator
*******************************

``ansible-navigator`` has two main operational modes:

Command mode
  Provides a standard CLI experience to ``ansible-navigator``

Interactive mode
  Provides a textual user interface for ``ansible-navigator`` that can work with IDEs to provide a richer visual exploration of your Ansible content.

.. contents::
   :local:


Exploring ansible-navigator command mode
=========================================

``ansible-navigator`` provides CLI commands similar to what is available in Ansible. You can use these commands directly to explore collections and inventories, run playbooks, and view plugin documentation.

Use ``ansible-navigator --help`` to see the available command options, or see :ref:`ansible_navigator_cli` for details.

``ansible-navigator`` includes a set of options that allow you to:

* Set the execution environment and container image.
* Set interactive mode to work with an IDE or your default web browser.
* Configure logging details.

Many of the subcommands for ``ansible-navigator`` run familiar ``ansible-*`` commands in passthrough mode and support all the ``ansible-*`` subcommands and parameters.

+-----------------------------------+-------------------------------+
| ``ansible-navigator`` command     | ``ansible-*`` command         |
+===================================+===============================+
| ``ansible-navigator collections`` | ``ansible-galaxy collection`` |
+-----------------------------------+-------------------------------+
| ``ansible-navigator config``      | ``ansible-config``            |
+-----------------------------------+-------------------------------+
| ``ansible-navigator explore``     | ``ansible-playbook``          |
+-----------------------------------+-------------------------------+
| ``ansible-navigator inventory``   | ``ansible-inventory``         |
+-----------------------------------+-------------------------------+



Exploring ansible-navigator interactive mode
=============================================


``ansible-navigator`` provides a textual user interface that can be used with an IDE for a more interactive experience.

To launch the interactive mode:

.. code-block:: bash

  ansible-navigator

By default, this uses ``vim`` as the default IDE. You can use ``ansible-navigator --ide`` to select another IDE, such as ``pycharm`` or ``vscode``.

Alternately, you can use ``ansible-navigator --web`` to launch interactive mode within your default browser.

Interactive mode provides a welcome screen with the available options.

.. code-block:: text

  0│## Welcome
  1│--------------------------------------------------------------------------------------
  2│
  3│Some things you can try from here:
  4│- `:config`                                 Explore the current Ansible configuration
  5│- `:collections`                            Explore installed collections
  6│- `:doc <plugin>`                           Show a plugin doc
  7│- `:explore <playbook> -i <inventory>`      Run a playbook with explore
  8│- `:help`                                   Show the main help page
  9│- `:inventory <inventory>`                  Explore an inventory
  10│- `:log`                                    Review the application log
  11│- `:open`                                   Open current page in the IDE
  12│- `:quit`                                   Quit the application
  13│- `:sample_form`                            Prototype curses form rendered
  14│
  15│happy automating,
  16│
  17│-ansible-navigator

``ansible-navigator`` in interactive mode gives similar options to command mode, but includes a rich set of exploration options you can view by typing the help option. The following subset of options shows the interactive options that help you explore content, run, and troubleshoot your playbooks:

.. code-block:: text

  ## MENUS
  27│--------------------------------------------------------------------------------------
  28│[0-9]                                   Go to menu item
  29│:<number>                               Go to menu item
  30│:{{ n|filter }}                         Template the menu item
  31│
  32│## TASKS
  33│--------------------------------------------------------------------------------------
  34│[0-9]                                   Go to task number
  35│:<number>                               Go to task number
  36│+, -                                    Next/Previous task
  37│_, :_                                   Toggle hidden keys
  38│:{{ key|filter }}                       Template the key's value
  39│:d, :doc                                Show the doc for the current task's module
  40│:j, :json                               Switch to JSON serialization
  41│:y, :yaml                               Switch to YAML serialization
