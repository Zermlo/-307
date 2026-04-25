import cv2
import tkinter as tk
from threading import Thread
import sys

buf = []
SZ = 20
stop_flag = False


def cb(evt, a, b, flg, prm):
    global buf

    if evt == cv2.EVENT_LBUTTONDOWN:
        buf.append((a - SZ, b - SZ, a + SZ, b + SZ))


def core(src):
    global buf, stop_flag

    stream = cv2.VideoCapture(src)

    if not stream.isOpened():
        print("Ошибка открытия видео")
        return

    cv2.namedWindow("X")
    cv2.setMouseCallback("X", cb)

    while True:
        if stop_flag:
            break

        ok, img = stream.read()
        if not ok:
            break

        for (p, q, r, s) in buf:
            cv2.rectangle(img, (p, q), (r, s), (0, 255, 0), 2)

        cv2.imshow("X", img)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('c') or k == ord('C'):
            buf.clear()

        if k == ord('q') or k == ord('Q'):
            stop_flag = True
            break

        if cv2.getWindowProperty("X", cv2.WND_PROP_VISIBLE) <= 0:
            stop_flag = True
            break

    stream.release()
    cv2.destroyAllWindows()


def run():
    core(0)


def quit_all(root):
    global stop_flag
    stop_flag = True
    root.destroy()
    cv2.destroyAllWindows()
    sys.exit(0)


def ui():
    root = tk.Tk()
    root.title("Panel")

    b1 = tk.Button(root, text="Start", command=lambda: Thread(target=run, daemon=True).start())
    b1.pack(pady=10)

    b2 = tk.Button(root, text="Quit", command=lambda: quit_all(root))
    b2.pack(pady=10)

    root.bind('q', lambda e: quit_all(root))
    root.focus_set()

    root.mainloop()


if __name__ == "__main__":
    ui()