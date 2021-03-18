black -l100 ansible_navigator
black -l100 share/ansible_navigator/utils
mypy ansible_navigator share/ansible_navigator/utils
pylint ./ansible_navigator/*.* ./ansible_navigator/actions ./share/ansible_navigator/utils ./ansible_navigator/ui_framework

