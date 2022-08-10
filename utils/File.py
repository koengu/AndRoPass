from os.path import exists, join


class File:
    def __init__(self, apk_path : str, base_dir_name : str) -> None:
        self.apk_path = apk_path
        self.apktool_path = str()
        self.base_dir_name = base_dir_name

    def apk_exist(self) -> bool:
        """
        check APK file existence

        Returns:
            (bool): existence of APK file

        """
        if exists(self.apk_path):
            return True
        else:
            if exists(join(self.base_dir_name, self.apk_path)):
                return True
        return False
