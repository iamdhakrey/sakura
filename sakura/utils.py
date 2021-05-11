
#* colors
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

#* For Success
def prGreen(args):
    print('{0}{1}{2}{3}'.format(color.BOLD,color.GREEN,args,color.END))

#* For Error
def prRed(args):
    print('{0}{1}{2}{3}'.format(color.BOLD,color.RED,args,color.END))

#* For Warning
def prYellow(args):
    print('{0}{1}{2}{3}'.format(color.BOLD,color.YELLOW,args,color.END))