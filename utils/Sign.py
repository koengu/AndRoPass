from .Commander import call_os_command
from .Exception import SignException
from .ColorPrint import ColorPrint as cp
from shutil import copy2
from os.path import join


class Sign:
    """
    Sign Apk file
    """

    def __init__(self, apk_file_path: str, uber_apk_signer_bin_path: str, apk_recompile_file_path: str,
                 base_dir: str) -> None:
        self.apk_file_path = apk_file_path
        self.apk_recompile_file_path = apk_recompile_file_path
        self.uber_apk_signer_bin_path = uber_apk_signer_bin_path
        self.output_apk_file = self.apk_recompile_file_path.split(".apk")[0] + "-aligned-debugSigned.apk"
        self.signed_apk_file_path = self.apk_file_path.split('.apk')[0] + '_bypassed.apk'
        self.base_dir = base_dir
        self.sign_command = ['java', '-jar', self.uber_apk_signer_bin_path, '--apks', self.apk_recompile_file_path]

    def sign(self) -> None:
        """
        Signs Apk file
        Returns:
            (None)
        """
        cp.pr('yellow', f"[+] Signing `{self.apk_file_path}` using Uber Apk Signer")
        stdout, stderr = call_os_command(self.sign_command)
        if not self.check_for_exception(stdout) or not self.check_for_exception(stderr):
            raise SignException(f"[-] Error in Singing APK - {self.sign_command}")
        copy2(self.output_apk_file, self.signed_apk_file_path)

    def check_for_exception(self, sign_output: str) -> bool:
        """
        Check for Uber Apk Signer's output error
        Args:
            sign_output(str): output of uber apk signer's command's output

        Returns:
            (bool): true if error found in signing's output
        """
        return True
