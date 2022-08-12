from colorama import Fore, Style


class ColorPrint:
    """
    Prints colorful messages
    """

    @staticmethod
    def pr(color: str, input_text: str) -> None:
        """
        Print in colored style

        Args:
            color (str): color of print text
            input_text (str): print text

        Returns:
            (None)

        """
        if color == "red":
            try:
                print(Fore.RED + str(input_text))
                print(Style.RESET_ALL, end='')
            except:
                print(input_text)
        elif color == "yellow":
            try:
                print(Fore.YELLOW + str(input_text))
                print(Style.RESET_ALL, end='')
            except:
                print(input_text)
        elif color == "blue":
            try:
                print(Fore.BLUE + str(input_text))
                print(Style.RESET_ALL, end='')
            except:
                print(input_text)
        else:
            try:
                print(Fore.WHITE + str(input_text))
                print(Style.RESET_ALL, end='')
            except:
                print(input_text)
