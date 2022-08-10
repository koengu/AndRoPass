from os.path import abspath, dirname
from utils.Decompile import Decompile
from utils.File import File
from utils.ColorPrint import ColorPrint as cp
from utils.RequirementCheck import RequirementCheck
from argparse import ArgumentParser
from sys import exit
from utils.Exception import DecompileException

DES = """
 █████╗ ███╗  ██╗██████╗ ██████╗  █████╗ ██████╗  █████╗  ██████╗ ██████╗
██╔══██╗████╗ ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
███████║██╔██╗██║██║  ██║██████╔╝██║  ██║██████╔╝███████║╚█████╗ ╚█████╗ 
██╔══██║██║╚████║██║  ██║██╔══██╗██║  ██║██╔═══╝ ██╔══██║ ╚═══██╗ ╚═══██╗
██║  ██║██║ ╚███║██████╔╝██║  ██║╚█████╔╝██║     ██║  ██║██████╔╝██████╔╝
╚═╝  ╚═╝╚═╝  ╚══╝╚═════╝ ╚═╝  ╚═╝ ╚════╝ ╚═╝     ╚═╝  ╚═╝╚═════╝ ╚═════╝ 
https://github.com/koengu/AndRoPass                 
"""

BASE_DIR = dirname(abspath(__file__))


def main():
    cp.pr('blue', DES)
    my_parser = ArgumentParser(
        prog='AndRoPass', description='Android Root Detection Bypass')
    my_parser.add_argument('--apk', '-a',
                           type=str,
                           required=True,
                           help='APK full path')
    apk_path = my_parser.parse_args().apk
    apk_file = File(apk_path, BASE_DIR)
    if not apk_file.apk_exist():
        cp.pr("red", "[-] Apk File Not Fount")
        return False

    req_status = RequirementCheck(BASE_DIR)
    if not req_status.check_all():
        for error in req_status.errors:
            cp.pr("red", "[-] {error}".format(error=error))
        exit(0)

    req_status.check_apktool()
    decompiler = Decompile(apk_file.apk_path, req_status.apktool_bin_path, BASE_DIR)

    try:
        decompiler.apk_tool_decompile()
    except DecompileException:
        # TODO handle Decompile Exception
        print("Error")
        pass


if __name__ == "__main__":
    main()
