class Parser:
    """
    Parse Apk file meta data.
    """

    def __init__(self, apktool_path):
        self.apktool_path = apktool_path

    def get_package_name(self) -> str:
        """
        Get APK file's package name
        Returns:
            (str): APK file's package name
        """
        return "com.hojat.simple"
