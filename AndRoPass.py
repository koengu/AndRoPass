from os.path import abspath, dirname
from utils.Decompile import Decompile
from utils.File import File
from utils.ColorPrint import ColorPrint as cp
from utils.RequirementCheck import RequirementCheck
from argparse import ArgumentParser
from sys import exit
from utils.Exception import DecompileException, RecompileException
from utils.StaticScan import StaticScan

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


def argument_catcher():
    my_parser = ArgumentParser(
        prog='AndRoPass', description='Android Root Detection Bypass')
    my_parser.add_argument('--apk', '-a',
                           type=str,
                           required=True,
                           help='APK full path')
    return my_parser.parse_args().apk


def main():
    cp.pr('blue', DES)
    apk_file_path = argument_catcher()
    apk_file = File(apk_file_path, BASE_DIR)
    if not apk_file.apk_exist():
        cp.pr("red", "[-] Apk File Not Fount")
        return False

    # Requirement Check Process
    req_status = RequirementCheck(BASE_DIR)
    if not req_status.check_all():
        for error in req_status.errors:
            cp.pr("red", "[-] {error}".format(error=error))
        exit(0)

    # Decompile Process
    decompiler = Decompile(apk_file.apk_path, req_status.apktool_bin_path, BASE_DIR)
    try:
        decompiler.apk_tool_decompile()
    except DecompileException as e:
        cp.pr("red", str(e))
        exit(0)

    # Static Scan Process
    try:
        static_scanner = StaticScan(decompiler.apk_decompile_output_path)
        static_scanner.scanner()
    except Exception as e:
        cp.pr('red', "[-] Unknown error in static scanner.")

    # reCompile Process
    try:
        decompiler.apk_tool_recompile()
    except RecompileException as e:
        cp.pr('red', e)

    # Sign Process


if __name__ == "__main__":
    main()
