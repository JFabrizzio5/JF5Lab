"""Generación de etiquetas: Barcode (Code128/EAN13) + QR + plantilla PDF."""
from __future__ import annotations
import io
import secrets
import qrcode
from barcode import Code128, EAN13
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PIL import Image


def generate_barcode_png(code: str, kind: str = "CODE128") -> bytes:
    kind = kind.upper()
    buf = io.BytesIO()
    if kind == "EAN13":
        c = code.zfill(12)[:12]
        EAN13(c, writer=ImageWriter()).write(buf)
    else:
        Code128(code, writer=ImageWriter()).write(buf)
    return buf.getvalue()


def generate_qr_png(payload: str, size: int = 320) -> bytes:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_nfc_code() -> str:
    """UID virtual de 14 hex para pre-registrar tags NFC antes de escribir físicamente."""
    return secrets.token_hex(7).upper()


def render_label_pdf(labels: list[dict]) -> bytes:
    """labels: [{code, kind, name, subtitle}] → PDF A4 con grid 3x7 etiquetas."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4
    cols, rows = 3, 7
    margin_x, margin_y = 10 * mm, 10 * mm
    lw = (W - 2 * margin_x) / cols
    lh = (H - 2 * margin_y) / rows

    for i, lbl in enumerate(labels):
        idx = i % (cols * rows)
        if i > 0 and idx == 0:
            c.showPage()
        col = idx % cols
        row = idx // cols
        x = margin_x + col * lw
        y = H - margin_y - (row + 1) * lh

        c.setStrokeColorRGB(0.85, 0.85, 0.85)
        c.rect(x + 2, y + 2, lw - 4, lh - 4, stroke=1, fill=0)

        kind = (lbl.get("kind") or "QR").upper()
        code = lbl.get("code", "")
        payload = lbl.get("payload", code)

        if kind in ("QR", "NFC"):
            png = generate_qr_png(payload, size=200)
        else:
            png = generate_barcode_png(code, kind=kind)

        img = Image.open(io.BytesIO(png))
        img_ratio = img.width / img.height
        target_w = lw * 0.6
        target_h = target_w / img_ratio
        if target_h > lh * 0.55:
            target_h = lh * 0.55
            target_w = target_h * img_ratio
        img_buf = io.BytesIO()
        img.save(img_buf, format="PNG")
        img_buf.seek(0)
        from reportlab.lib.utils import ImageReader
        c.drawImage(ImageReader(img_buf), x + (lw - target_w) / 2, y + lh * 0.35, width=target_w, height=target_h)

        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + lw / 2, y + lh * 0.25, (lbl.get("name") or "")[:36])
        c.setFont("Helvetica", 6)
        c.drawCentredString(x + lw / 2, y + lh * 0.15, (lbl.get("subtitle") or "")[:48])
        c.setFont("Courier", 6)
        c.drawCentredString(x + lw / 2, y + lh * 0.08, code[:28])

    c.save()
    return buf.getvalue()
