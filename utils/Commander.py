from subprocess import PIPE, Popen


def call_os_command(cmd_list: list) -> tuple:
    """
    Args:
        cmd_list (list): Commands list to run in OS call

    Returns:
        (tuple): OS call output split by new lines

    """
    process = Popen(cmd_list,
                    stdout=PIPE,
                    stderr=PIPE)
    stdout, stderr = process.communicate()
    return str(stdout).split("\\n"), str(stderr).split("\\n")
