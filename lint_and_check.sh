black -l100 ansible_launcher 
black -l100 share/ansible_launcher/utils
mypy ansible_launcher share/ansible_launcher/utils
pylint ./ansible_launcher/*.* ./ansible_launcher/actions ./share/ansible_launcher/utils ./ansible_launcher/ui_framework

