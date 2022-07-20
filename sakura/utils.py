# * colors
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# * For Logs Success
def prGreen(args):
    print('{0}{1}{2}{3}'.format(color.BOLD, color.GREEN, args, color.END))


# * For Logs Error
def prRed(args):
    print('{0}{1}{2}{3}'.format(color.BOLD, color.RED, args, color.END))


# * For Logs Warnings
def prBlue(args):
    print('{0}{1}{2}{3}'.format(color.BOLD, color.BLUE, args, color.END))


# * For INFO
def prBold(args):
    print('{0}{1}{2}'.format(color.BOLD, args, color.END))


# *  Bot Command Not Found Error
def prYellow(args):
    """
    Bot Command Not Found Error
    """
    print('{0}{1}{2}{3}'.format(color.BOLD, color.YELLOW, args, color.END))


# * For Guild or Member Leave
def prPurple(args):
    print('{0}{1}{2}{3}'.format(color.BOLD, color.PURPLE, args, color.END))


# * For Guild or Member Join
def prCyan(args):
    print('{0}{1}{2}{3}'.format(color.BOLD, color.CYAN, args, color.END))
