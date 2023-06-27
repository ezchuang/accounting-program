# 文字顏色模組
from colorama import Fore 
from colorama import Style

# 文字顏色(介面用)
class Color():
    def depiction(self, msg):
        return Fore.YELLOW + msg + Style.RESET_ALL
    def high_light(self, msg):
        return Fore.YELLOW + Style.BRIGHT + msg + Style.RESET_ALL
    def mode_select(self, msg):
        return Fore.CYAN + Style.BRIGHT + msg + Style.RESET_ALL
    def warning(self, msg):
        return Fore.RED + Style.BRIGHT + msg + Style.RESET_ALL
    def finished_msg(self, msg):
        return Fore.GREEN + msg + Style.RESET_ALL
    def finished_res(self, msg):
        return Fore.BLUE + Style.BRIGHT + msg + Style.RESET_ALL
