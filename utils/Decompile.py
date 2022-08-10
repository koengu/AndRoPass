from imp import IMP_HOOK
from multiprocessing.spawn import old_main_modules
from subprocess import PIPE, Popen
from os.path import join, isdir
from os import sep, mkdir
from typing import Tuple, List
from Exception import DecompileException
from utils.ColorPrint import ColorPrint as cp


class Decompile:
    def __init__(self, apk_file_path: str, apktool_bin_path: str, base_dir_path: str) -> None:
        self.apk_file_path = apk_file_path
        self.apktool_bin_path = apktool_bin_path
        self.base_dir_path = base_dir_path
        self.apk_decompile_output_path = ""

    def apk_tool_decompile(self) -> bool:
        """
        Decompile APK file

        Returns:
            (None)

        """
        if not isdir(join(self.base_dir_path, "tmp")):
            mkdir(join(self.base_dir_path, "tmp"))
        cp.pr("yellow", "[+] Decompiling {} - Try 1".format(self.apk_file_path.split(sep)[-1].split(".")[0]))
        self.apk_decompile_output_path = join(self.base_dir_path, "tmp",
                                              self.apk_file_path.split(sep)[-1].split(".")[0])

        apktool_cmd_try1 = [
            'java', '-jar', self.apktool_bin_path, 'd', self.apk_file_path,
            "-o", self.apk_decompile_output_path, '-f'
        ]
        stdout, stderr = self.call_os_command(apktool_cmd_try1)
        if not self.check_for_exception(stdout) or not self.check_for_exception(stderr):
            raise DecompileException()

    @staticmethod
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

    @staticmethod
    def check_for_exception(apktool_output: list) -> bool:
        """
        Check apk tool output for errors and exception
        Args:
            apktool_output (list): apktool output log

        Returns:
            (bool): error and exception existence in apktool output

        """
        # TODO check all apktool error
        for line in apktool_output:
            if line.split(":")[0] != "I":
                return False
        return True
