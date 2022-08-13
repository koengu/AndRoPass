from os.path import join, isdir, exists
from os import sep, mkdir, remove
from shutil import rmtree
from .Exception import DecompileException, RecompileException
from utils.ColorPrint import ColorPrint as cp
from .Commander import call_os_command


class Compile:
    """
    Performs Decompile and Recompile of APK file
    """

    def __init__(self, apk_file_path: str, apktool_bin_path: str, base_dir_path: str) -> None:
        self.apk_file_path = apk_file_path
        self.apktool_bin_path = apktool_bin_path
        self.base_dir_path = base_dir_path
        self.apk_decompile_output_path = join(self.base_dir_path, "tmp",
                                              self.apk_file_path.split(sep)[-1].split(".")[0])
        self.apk_name = self.apk_file_path.split(sep)[-1].split(".")[0]
        self.apk_recompile_file_path = self.apk_decompile_output_path + '_bypass.apk'
        self.apktool_decompile_command_set = {
            "Apk Decompile Including Resources":
                [
                    'java', '-jar', self.apktool_bin_path, 'd', self.apk_file_path,
                    "-o", self.apk_decompile_output_path, '-f'
                ],
            "Apk Decompile Excluding Resources":
                [
                    'java', '-jar', self.apktool_bin_path, 'd', '-r',  self.apk_file_path,
                    "-o", self.apk_decompile_output_path, '-f'
                ],
        }

        self.apktool_recompile_command_set = {
            "Apk Recompile":
                [
                    'java', '-jar', self.apktool_bin_path, 'b', self.apk_decompile_output_path,
                    "-o", self.apk_recompile_file_path, '-f'
                ]
        }

    def apk_tool_decompile(self) -> bool:
        """
        Decompile APK file

        Returns:
            (None)

        """

        # Create tmp dir if not exists
        if not isdir(join(self.base_dir_path, "tmp")):
            mkdir(join(self.base_dir_path, "tmp"))

        # Check apk decompile dir existence
        if exists(self.apk_decompile_output_path):
            cp.pr("red", f"{self.apk_decompile_output_path} exists, delete and continue? [Y/n]: ")
            user_input = input()
            if user_input.lower() == "n":
                return True
            else:
                self.remove_apk_decompile_dir()

        # Loop in apktool de-compile command set
        for apktool_command in self.apktool_decompile_command_set:
            cp.pr("yellow", f"[+] Decompiling `{self.apk_name}` - {apktool_command}")

            stdout, stderr = call_os_command(self.apktool_decompile_command_set[apktool_command])
            if not self.check_for_exception(stdout) or not self.check_for_exception(stderr):
                self.remove_apk_decompile_dir()
            else:
                return True
            raise DecompileException('[-] Unable to Decompile Apk')

    def apk_tool_recompile(self) -> bool:
        """
        Recompile APK file

        Returns:
            (None)
        """
        # Loop in apktool re-compile command set
        for apktool_command in self.apktool_recompile_command_set:
            cp.pr("yellow", f"[+] Recompiling `{self.apk_name}` - {apktool_command}")

            stdout, stderr = call_os_command(self.apktool_recompile_command_set[apktool_command])
            if not self.check_for_exception(stdout) or not self.check_for_exception(stderr):
                print(stderr)
                print(stdout)
                raise RecompileException(f"[-] Error in Recompiling -  {apktool_command}")
            else:
                return True

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
            if ":" in line:
                if line.split(":")[0][-1] != "I":
                    return False
        return True

    def remove_apk_decompile_dir(self):
        """
        Remove apk decompiled directory
        Returns:
            (None)
        """
        try:
            rmtree(self.apk_decompile_output_path)
        except PermissionError:
            raise DecompileException("Permission denied, run with higher privilege or delete manually.")
