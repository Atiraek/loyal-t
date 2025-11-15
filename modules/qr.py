import random, qrcode
from io import BytesIO
from PIL import Image
import pyzbar.pyzbar as pyzbar

def generate_unique_code(conn):
    while True:
        code = str(random.randint(100000, 999999))
        exists = conn.execute("SELECT 1 FROM customers WHERE identifier=?", (code,)).fetchone()
        if not exists:
            return code

def make_qr(code):
    img = qrcode.make(code)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def decode_qr(uploaded_image):
    image = Image.open(uploaded_image)
    decoded = pyzbar.decode(image)
    if decoded:
        return decoded[0].data.decode("utf-8")
    return None
