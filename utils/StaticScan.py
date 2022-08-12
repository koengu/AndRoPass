from os import walk
from os.path import join
from re import sub as find_and_replace
from utils.Constant import Constant


class StaticScan:
    """
    Check for Root Detection strings and replace the file
    """
    def __init__(self, apk_decompile_output_path: str) -> None:
        self.apk_decompile_output_path = apk_decompile_output_path

    def scanner(self) -> None:
        """
        Run static scanner to find patterns and replace
        Returns:
            (None)
        """
        self.smali_finder()

    def smali_finder(self) -> None:
        """
        Find all smali files in decompiled directory
        Returns:
            (None)
        """
        # Walk throgh decompiled directory and find smali files and pass to pattern_finder() function
        for root, dirs, files in walk(self.apk_decompile_output_path):
            for file_name in files:
                full_file_name = join(root, file_name)
                if full_file_name.endswith(".smali"):
                    self.pattern_finder(full_file_name)

    def pattern_finder(self, smali_file_name: str) -> None:
        """
        Find pattern in smali file and replace it
        Args:
            smali_file_name(str): smali file path to find pattern and replace
        Returns:
            (None)
        """
        file = open(smali_file_name, "r")
        file_content = file.read()
        file.close()

        for pattern in Constant.all:
            file_content = find_and_replace(pattern, self.pattern_to_junk(pattern), file_content)

        file = open(smali_file_name, 'w')
        file.write(file_content)
        file.close()

    @staticmethod
    def pattern_to_junk(pattern: str) -> str:
        """
        Manipulate pattern with junk one
        Args:
            pattern(str): pattern to manipulate

        Returns:
            (str): manipulated pattern

        """
        return "x" + pattern[1:]
