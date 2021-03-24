.. _installing_ansible_navigator:

******************************
Installing ansible-navigator
******************************


.. contents::
   :local:

Installing ansible-navigator in a virtual environment
======================================================

If you are installing ``ansible-navigator`` on Red Hat Enterprise Linux version 8 or Centos8, you first need to install ``python3``:

.. code-block:: bash

   sudo dnf install python3
   sudo dnf install gcc python3-devel

To install ``ansible-navigator`` in a virtual environment:

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/ansible/ansible-navigator.git


2. Create a demo directory:

.. code-block:: bash

  mkdir ansible-navigator_demo
  cd ansible-navigator_demo

3. Create the virtual environment and activate it:

.. code-block:: bash

   python3 -m venv venv
   source venv/bin/activate

4. Install the required packages:

.. code-block:: bash

   pip install -U setuptools
   pip install -U ansible

5. Install ``ansible-navigator``

.. code-block:: bash

   pip install ../ansible-navigator

6. Optionally, run the command to verify your installation.

.. code-block:: bash

  ansible-navigator --help
