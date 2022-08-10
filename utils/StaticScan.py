from os import walk
from os.path import join
from re import sub as re_find_and_replace, findall
from utils.Constant import Constant
from utils.ColorPrint import ColorPrint as cp
from hashlib import md5

class StaticScan:
    def __init__(self, apk_decompile_output_path: str):
        self.apk_decompile_output_path = apk_decompile_output_path

    def start_scanner(self):
        self.smali_finder()

    def smali_finder(self):
        for root, dirs, files in walk(self.apk_decompile_output_path):
            for file_name in files:
                full_file_name = join(root, file_name)
                if full_file_name.endswith(".smali"):
                    self.pattern_finder(full_file_name)

    def pattern_finder(self, smali_file_name: str):
        file = open(smali_file_name, "r")
        file_content = file.read()
        file.close()
        for pattern in Constant.all:
            file_content = re_find_and_replace(pattern, self.pattern_to_junk(pattern), file_content)
        file = open(smali_file_name, 'w')
        file.write(file_content)
        file.close()

    def pattern_to_junk(self, pattern: str):
        return "x" + pattern[1:]
