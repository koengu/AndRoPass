from subprocess import PIPE, Popen
from os import listdir
from os.path import join, isdir


class RequirementCheck:

    def __init__(self, base_dir_name : str) -> None:
        self.java_version = None
        self.errors = []
        self.base_dir_name = base_dir_name
        self.apktool_path = join(self.base_dir_name, "utils", "files", "apktool")
        self.apktool_bin_list = []
        self.apktool_bin_path = str()

    def check_all(self) -> bool:
        """
        Check all AndroPass requirements to run

            Returns:
                Bool of requirements check

        """
        if not self.check_java_installed():
            self.errors.append(
                "Java is not installed, install Java and try again.")
        if not self.check_apktool():
            self.errors.append(
                "ApkTool is not in utils/files/apktool directory. \n    Download last Version and place it in "
                "utils/files/apktool directory and try again.\n    "
                "https://bitbucket.org/iBotPeaches/apktool/downloads/")
        if self.errors:
            return False
        else:
            return True

    def check_apktool(self) -> bool:
        """
        Check apktool is installed
            Returns:
                Bool of apktool installed

        """
        if not isdir(self.apktool_path):
            return False
        else:
            for apktool_bin in listdir(self.apktool_path):
                if apktool_bin.endswith(".jar"):
                    self.apktool_bin_list.append(apktool_bin)
            if not self.apktool_bin_list:
                return False
            else:
                self.apktool_bin_list.sort()
                self.apktool_bin_path = join(
                    self.apktool_path, self.apktool_bin_list[-1])
                return True

    def check_java_installed(self):
        """
         Check apktool is installed

            Returns:
                Bool of apktool installed

        """
        try:
            process = Popen(['java', '-version'],
                            stdout=PIPE,
                            stderr=PIPE)
            stdout, stderr = process.communicate()
        except FileNotFoundError as e:
            return print(e)
        try:
            self.java_version = str(stderr).split(
                r"\r\n")[0].split("version")[1].split(r"\n")[0]
            return True
        except IndexError as e:
            return False
        except TypeError as e:
            return False

    def get_java_version(self):
        """
        Returns installed java version
            Returns:
                Str of java version

        """
        try:
            return self.java_version
        except NameError as e:
            return None
