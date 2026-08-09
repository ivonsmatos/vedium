# -*- coding: utf-8 -*-
"""
Vedium — Geração de Certificado PDF com QR Code de Verificação

Endpoint: vedium_core.certificate_pdf.generate_pdf(code)

Gera um PDF do certificado usando WeasyPrint (HTML→PDF) com:
- Layout premium do certificado
- QR code de verificação embutido (via qrcode + base64)
- Hash de verificação único

Dependências (requirements.txt):
    weasyprint>=61.0
    qrcode[pil]>=7.4
    Pillow>=10.0

Uso no frontend (botão "Baixar PDF"):
    window.location.href = '/api/method/vedium_core.certificate_pdf.generate_pdf?code=' + code;
"""

import base64
import io
import os
import tempfile

import frappe
from frappe import _


def _qr_base64(url: str) -> str:
    """Gera QR code como PNG em base64 para embutir no HTML."""
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1a1a2e", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        # Fallback: usa quickchart.io se qrcode não estiver instalado
        return ""


def _get_certificate_data(code: str) -> dict | None:
    """Busca dados do certificado pelo código de verificação."""
    try:
        # SÓ por verification_code (segredo). Antes havia fallback por `name`
        # (PK), que permitia enumerar titular+curso sem conhecer o código. QA
        # 2026-08-09.
        return frappe.db.get_value(
            "LMS Certificate",
            {"verification_code": code},
            ["name", "member", "course", "issue_date"],
            as_dict=True,
        )
    except Exception:
        return None


@frappe.whitelist(allow_guest=True)
def generate_pdf(code: str):
    """
    Gera e retorna o PDF do certificado identificado pelo código de verificação.
    Chamado via GET pelo browser — devolve o binário do PDF.
    """
    if not code or len(code) > 100:
        frappe.throw(_("Código inválido"), frappe.ValidationError)

    cert = _get_certificate_data(code.strip())
    if not cert:
        frappe.throw(_("Certificado não encontrado"), frappe.DoesNotExistError)

    # Dados complementares
    student_name = frappe.db.get_value("User", cert.member, "full_name") or cert.member
    course_title = frappe.db.get_value("LMS Course", cert.course, "title") or cert.course
    issue_date_fmt = (
        cert.issue_date.strftime("%d de %B de %Y")
        if cert.issue_date else "—"
    )

    verify_url = f"https://vediums.com/certificado?code={code}"
    qr_b64 = _qr_base64(verify_url)
    qr_src = (
        f"data:image/png;base64,{qr_b64}"
        if qr_b64
        else f"https://quickchart.io/qr?size=200&margin=1&text={frappe.utils.quote(verify_url)}"
    )

    html = _render_certificate_html(
        student_name=student_name,
        course_title=course_title,
        issue_date=issue_date_fmt,
        code=code,
        verify_url=verify_url,
        qr_src=qr_src,
    )

    try:
        from weasyprint import HTML as WP_HTML
        pdf_bytes = WP_HTML(string=html, base_url="https://vediums.com").write_pdf()
    except ImportError:
        frappe.throw(
            _("Geração de PDF não disponível neste momento. "
              "Instale: pip install weasyprint"),
            frappe.ValidationError,
        )

    # Entrega o PDF diretamente ao browser
    filename = f"certificado-vedium-{code[:12]}.pdf"
    frappe.response.update({
        "type": "binary",
        "filename": filename,
        "filecontent": pdf_bytes,
        "content-type": "application/pdf",
    })


def _render_certificate_html(
    student_name: str,
    course_title: str,
    issue_date: str,
    code: str,
    verify_url: str,
    qr_src: str,
) -> str:
    """Renderiza o HTML premium do certificado para conversão em PDF."""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Kumbh+Sans:wght@300;400;700&family=Playfair+Display:wght@400;700&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 297mm; height: 210mm; font-family: 'Kumbh Sans', sans-serif; }}
  .cert {{
    width: 297mm; height: 210mm;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    position: relative; overflow: hidden; padding: 20mm 24mm;
  }}
  /* Bordas decorativas */
  .cert::before {{
    content: ''; position: absolute; inset: 8mm;
    border: 2px solid rgba(212,175,55,.4); border-radius: 4px;
    pointer-events: none;
  }}
  .cert::after {{
    content: ''; position: absolute; inset: 10mm;
    border: 1px solid rgba(212,175,55,.15); border-radius: 3px;
    pointer-events: none;
  }}
  /* Ornamentos de canto */
  .corner {{ position: absolute; width: 18mm; height: 18mm; }}
  .corner.tl {{ top: 12mm; left: 12mm; border-top: 3px solid #D4AF37; border-left: 3px solid #D4AF37; }}
  .corner.tr {{ top: 12mm; right: 12mm; border-top: 3px solid #D4AF37; border-right: 3px solid #D4AF37; }}
  .corner.bl {{ bottom: 12mm; left: 12mm; border-bottom: 3px solid #D4AF37; border-left: 3px solid #D4AF37; }}
  .corner.br {{ bottom: 12mm; right: 12mm; border-bottom: 3px solid #D4AF37; border-right: 3px solid #D4AF37; }}
  /* Conteúdo */
  .logo-area {{ display: flex; align-items: center; gap: 8px; margin-bottom: 4mm; }}
  .logo-text {{
    font-family: 'Playfair Display', serif; font-size: 24pt; font-weight: 700;
    color: #D4AF37; letter-spacing: 3px; text-transform: uppercase;
  }}
  .issuer {{ color: rgba(255,255,255,.5); font-size: 8pt; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 6mm; }}
  .divider {{ width: 60mm; height: 1px; background: linear-gradient(90deg, transparent, #D4AF37, transparent);
    margin: 3mm auto; }}
  .cert-title {{ color: rgba(255,255,255,.7); font-size: 10pt; letter-spacing: 3px;
    text-transform: uppercase; margin-bottom: 5mm; }}
  .student-name {{
    font-family: 'Playfair Display', serif; font-size: 32pt; color: #fff;
    font-weight: 700; text-align: center; margin-bottom: 3mm;
    text-shadow: 0 2px 20px rgba(212,175,55,.3);
  }}
  .completed-text {{ color: rgba(255,255,255,.6); font-size: 9pt; margin-bottom: 3mm; letter-spacing: 1px; }}
  .course-name {{
    font-size: 16pt; color: #D4AF37; font-weight: 700; text-align: center;
    margin-bottom: 6mm; letter-spacing: 1px;
  }}
  .meta-row {{ display: flex; gap: 20mm; align-items: flex-start; margin-top: 2mm; }}
  .meta-block {{ text-align: center; }}
  .meta-label {{ color: rgba(255,255,255,.4); font-size: 7pt; text-transform: uppercase;
    letter-spacing: 1px; margin-bottom: 1mm; }}
  .meta-value {{ color: rgba(255,255,255,.85); font-size: 9pt; font-weight: 600; }}
  .code-value {{ color: #D4AF37; font-size: 8pt; font-family: monospace; letter-spacing: 1.5px; }}
  /* QR code */
  .qr-block {{ position: absolute; bottom: 16mm; right: 20mm; text-align: center; }}
  .qr-block img {{ width: 22mm; height: 22mm; border: 2px solid rgba(212,175,55,.3);
    border-radius: 4px; padding: 2px; background: #fff; }}
  .qr-label {{ color: rgba(255,255,255,.3); font-size: 6pt; margin-top: 1mm;
    text-transform: uppercase; letter-spacing: 1px; }}
  /* Assinatura */
  .signature-block {{ position: absolute; bottom: 16mm; left: 24mm; text-align: center; }}
  .signature-line {{ width: 44mm; height: 1px; background: rgba(255,255,255,.2); margin-bottom: 2mm; }}
  .signature-name {{ color: rgba(255,255,255,.7); font-size: 8pt; font-weight: 600; }}
  .signature-role {{ color: rgba(255,255,255,.3); font-size: 7pt; }}
</style>
</head>
<body>
<div class="cert">
  <!-- Cantos decorativos -->
  <div class="corner tl"></div>
  <div class="corner tr"></div>
  <div class="corner bl"></div>
  <div class="corner br"></div>

  <!-- Logo -->
  <div class="logo-area">
    <span class="logo-text">VEDIUM</span>
  </div>
  <p class="issuer">Global Education &amp; Technology</p>

  <div class="divider"></div>
  <p class="cert-title">Certificado de Conclusão</p>
  <div class="divider"></div>

  <!-- Nome do aluno -->
  <p class="student-name">{frappe.utils.escape_html(student_name)}</p>
  <p class="completed-text">concluiu com êxito o curso</p>
  <p class="course-name">{frappe.utils.escape_html(course_title)}</p>

  <!-- Metadados -->
  <div class="meta-row">
    <div class="meta-block">
      <p class="meta-label">Data de Emissão</p>
      <p class="meta-value">{issue_date}</p>
    </div>
    <div class="meta-block">
      <p class="meta-label">Código de Verificação</p>
      <p class="code-value">{frappe.utils.escape_html(code[:20])}</p>
    </div>
    <div class="meta-block">
      <p class="meta-label">Verificar em</p>
      <p class="meta-value" style="font-size:7pt;color:rgba(255,255,255,.5)">vediums.com/certificado</p>
    </div>
  </div>

  <!-- QR Code -->
  <div class="qr-block">
    <img src="{qr_src}" alt="QR Code de verificação" width="88" height="88">
    <p class="qr-label">Verificar autenticidade</p>
  </div>

  <!-- Assinatura -->
  <div class="signature-block">
    <div class="signature-line"></div>
    <p class="signature-name">Vedium Global Education</p>
    <p class="signature-role">Direção Pedagógica</p>
  </div>
</div>
</body>
</html>"""
