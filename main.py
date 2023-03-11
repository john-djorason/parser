#!usr/bin/env python3

from parser.builder import LawlyBuilder
import datetime
import tkinter as tk


def start():

    def build():
        builder = LawlyBuilder()
        builder.build()

    root = tk.Tk()

    canvas1 = tk.Canvas(root, width=300, height=300)
    canvas1.pack()

    button1 = tk.Button(text='Start', command=build, bg='brown', fg='white')
    canvas1.create_window(150, 150, window=button1)

    root.mainloop()


def main():
    start()


if __name__ == '__main__':
    main()
