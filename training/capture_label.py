
import cv2
import os
from datetime import datetime
import argparse

def ensure(path):
    os.makedirs(path, exist_ok=True)

def capture_to_folder(folder, device_index=0, show_preview=True):
    ensure(folder)
    cap = cv2.VideoCapture(device_index)
    if not cap.isOpened():
        print("ERROR: could not open webcam. Try changing device_index (0 -> 1).")
        return
    print("Webcam opened. Press SPACE to capture, 's' to toggle preview, 'q' to quit.")
    preview_names = show_preview
    saved = 0
    window_name = "capture (SPACE save, q quit)"
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: no frame from webcam. Exiting.")
            break
        display = frame.copy()
        if preview_names:
            fname = datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.putText(display, f"Preview: {fname}.jpg", (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.imshow(window_name, display)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):  # SPACE -> save
            fname = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            path = os.path.join(folder, fname)
            cv2.imwrite(path, frame)
            saved += 1
            print(f"Saved: {path}  (total: {saved})")
        elif key == ord("s"):
            preview_names = not preview_names
        elif key == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Done. Total saved:", saved)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture webcam frames into a labeled folder.")
    parser.add_argument("--out", required=True, help="Output folder, e.g. training/data/faces/joy")
    parser.add_argument("--device", type=int, default=0, help="Webcam device index (0 or 1 etc.)")
    args = parser.parse_args()
    capture_to_folder(args.out, device_index=args.device)
