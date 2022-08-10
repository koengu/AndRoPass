from os import walk
from os.path import join
from re import sub as re_find_and_replace
from utils.Constant import Constant
from utils.ColorPrint import ColorPrint as cp


class StaticScan:
    def __init__(self, apk_decompile_output_path: str):
        self.apk_decompile_output_path = apk_decompile_output_path

    def scanner(self):
        pass

    def smali_finder(self):
        for root, dirs, files in walk(self.apk_decompile_output_path):
            for file_name in files:
                full_file_name = join(root, file_name)
                if full_file_name.endswith(".smali"):
                    self.pattern_finder(full_file_name)

    @staticmethod
    def pattern_finder(self, smali_file_name: str):
        with open(smali_file_name, "r") as smali_file:
            for pattern in Constant.known_root_apps_packages:
                re_find_and_replace(pattern, self.pattern_to_junk(pattern), smali_file.read())

    @staticmethod
    def pattern_to_junk(self, pattern: str):
        return "x" + pattern[1:]
