"""Builds static/upi-qr.png from the exact UPI payload the app encodes.

Same string the Android app feeds to ZXing, so the code the site shows and the
code inside the app scan to the same thing.
"""
import os
import qrcode

PAYLOAD = ("upi://pay?pa=romflasher@naviaxis&pn=Rom%20Flasher&cu=INR"
           "&tn=Donation%20to%20Rom%20Flasher")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "static", "upi-qr.png")


def main():
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=3,
    )
    qr.add_data(PAYLOAD)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(OUT)
    print("[OK] %s  %dx%d  %d bytes"
          % (OUT, img.size[0], img.size[1], os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
