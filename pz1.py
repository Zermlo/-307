import cv2
import tkinter as tk
from threading import Thread

buf = []
SZ = 20

stop_flag = False


def cb(evt, x, y, flags, param):
    if evt == cv2.EVENT_LBUTTONDOWN:
        buf.append((x - SZ, y - SZ, x + SZ, y + SZ))


def video_loop():
    global stop_flag, buf

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera error")
        return

    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", cb)

    while not stop_flag:
        ret, frame = cap.read()
        if not ret:
            break

        for (x1, y1, x2, y2) in buf:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow("Video", frame)

        key = cv2.waitKey(1) & 0xFF

        if key in (ord('c'), ord('C')):
            print("test1")
            buf.clear()

        if key in (ord('q'), ord('Q')):
            print("test1")
            stop_flag = True
            break

        if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
            stop_flag = True
            break

    cap.release()
    cv2.destroyAllWindows()


def start_video():
    Thread(target=video_loop, daemon=True).start()


def stop_all(root):
    global stop_flag
    stop_flag = True
    root.quit()
    root.destroy()
    cv2.destroyAllWindows()


def ui():
    root = tk.Tk()
    root.title("Control")

    tk.Button(root, text="Start", command=start_video).pack(pady=10)
    tk.Button(root, text="Quit", command=lambda: stop_all(root)).pack(pady=10)

    root.bind('q', lambda e: stop_all(root))
    root.mainloop()


if __name__ == "__main__":
    ui()