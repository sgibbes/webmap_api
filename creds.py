# import sys, tty, termios
#
#
# 
# def getch():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(sys.stdin.fileno())
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch
#
#
# def get_paswd():
#     key = ""
#     # sys.stdout.write('Password:')
#     # var = input('enter something: ')
#     print('ArcGIS Online password:')
#     while True:
#         ch = getch()
#         if ch == '\r':
#             print('\n')
#             break
#         key += ch
#         sys.stdout.write('*')
#
#
#     # print
#     return key

# get_paswd()
