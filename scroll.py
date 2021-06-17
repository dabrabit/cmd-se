import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("500x400")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
auxFrame = tk.Frame(canvas)
canvas.create_window((0, 0), window=auxFrame, anchor='nw')
for thing in range(100):
    tk.Button(auxFrame, text=f'Boton {thing}').grid(row=thing, column=0, pady=10, padx=10)

root.mainloop()
