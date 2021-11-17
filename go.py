from .runner.api import CommandRunner

runner = CommandRunner(executable_cmd="ls")
output, error, _ = runner.run()

print(output, error)