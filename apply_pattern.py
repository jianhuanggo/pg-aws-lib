import click
from logging import Logger as Log
from _common import _common as _common_
from _error_handling import _error_handling

@click.command()
@click.option('--pattern_template_filepath', required=True, type=str)
@click.option('--profile_name', required=True, type=str)
def apply_pattern(pattern_template_filepath: str,
                  profile_name: str = "default",
                  logger: Log = None):

    _common_.info_logger(f"pattern_template_filepath: {pattern_template_filepath}")
    _common_.info_logger(f"profile_name: {profile_name}")

    error_handle = _error_handling.ErrorHandlingSingleton(profile_name=profile_name, error_handler="subprocess")

    from _engine._subprocess import ShellRunner
    from _engine._command_protocol import execute_command_from_dag

    # from _engine import _process_flow
    # from _management._meta._inspect_module import load_module_from_path
    #
    # module_name = pattern_template_filepath.split("/")
    # filename = module_name[-1]
    #
    # template_obj = load_module_from_path(pattern_template_filepath,
    #                       filename)

    from _pattern_template._process_template import _process_template

    t_task = _process_template.process_template(profile_name=profile_name, template_name=pattern_template_filepath)
    shell_runner = ShellRunner(profile_name=profile_name)
    execute_command_from_dag(shell_runner, t_task.tasks)


if __name__ == '__main__':
    apply_pattern()

