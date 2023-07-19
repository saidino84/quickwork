import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification

my_w = ttk.Window(themename="lumen")
my_w.geometry("300x200")  # width and height

toast = ToastNotification(
    title="This is the title of Notification ",
    message="Welcom to plus2net.com to learn Python ",
    position=(400, 250, "ne"),
    bootstyle=DANGER
)
# toast.show_toast()
b1 = ttk.Button(
    my_w, text="Open Toast", command=lambda: toast.show_toast(), bootstyle=SUCCESS
)
b1.grid(row=1, column=1, padx=10, pady=30)
b2 = ttk.Button(
    my_w, text="Close Toast", command=lambda: toast.hide_toast(), bootstyle=DANGER
)
b2.grid(row=1, column=2, padx=10, pady=30)
my_w.mainloop()