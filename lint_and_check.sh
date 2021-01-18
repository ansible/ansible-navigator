black -l100 winston 
black -l100 share/winston/utils
mypy winston share/winston/utils
pylint ./winston/*.* ./winston/actions ./share/winston/utils ./winston/ui_framework

