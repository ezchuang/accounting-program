# 文字顏色模組
from colorama import Fore 
from colorama import Style

# 文字顏色(介面用)
class Color():
    def depiction(self):
        return Fore.YELLOW + self + Style.RESET_ALL
    def high_light(self):
        return Fore.YELLOW + Style.BRIGHT + self + Style.RESET_ALL
    def mode_select(self):
        return Fore.CYAN + Style.BRIGHT + self + Style.RESET_ALL
    def warning(self):
        return Fore.RED + Style.BRIGHT + self + Style.RESET_ALL
    def finished_msg(self):
        return Fore.GREEN + self + Style.RESET_ALL
    def finished_res(self):
        return Fore.BLUE + Style.BRIGHT + self + Style.RESET_ALL
