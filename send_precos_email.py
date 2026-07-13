"""
Send PRECOS_MERCADO.pdf to Moniquinha via SMTP.

Usage:
  1. Set environment variables (or edit the CONFIG section below):
     - SMTP_HOST   (ex: smtp.gmail.com, smtp-mail.outlook.com, smtp.office365.com)
     - SMTP_PORT   (587 for STARTTLS, 465 for SSL)
     - SMTP_USER   (the sending email address)
     - SMTP_PASS   (app password — NOT your normal login password for Gmail/Outlook)
     - SMTP_FROM   (optional, defaults to SMTP_USER)
     - MAIL_TO     (optional, defaults to moniquinhashine@hotmail.com)

  2. Run:
       python send_precos_email.py

Notes:
  - Gmail: enable 2FA then create an "App Password" at https://myaccount.google.com/apppasswords
  - Outlook/Hotmail: use https://account.live.com/proofs/AppPassword
  - The PDF is attached from the same folder as this script.
"""

from __future__ import annotations
import os
import sys
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

# ---------- CONFIG ----------
SMTP_HOST = os.getenv("SMTP_HOST", "")          # ex: "smtp.gmail.com"
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))  # 587 STARTTLS or 465 SSL
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
MAIL_TO   = os.getenv("MAIL_TO", "moniquinhashine@hotmail.com")

PDF_PATH = Path(__file__).parent / "PRECOS_MERCADO.pdf"

SUBJECT = "Tabela de Preços de Mercado — Avaliação para Moniquinha's Shine"

BODY = """Olá Moniquinha! 💛

Em anexo segue o documento com a pesquisa de preços de mercado para os serviços da Moniquinha's Shine,
para as zonas de Óbidos e Caldas da Rainha.

O documento inclui:
  • Tabela com os 12 serviços (mínimo, típico, máximo) e respetivas unidades
  • Sugestão de posicionamento de preços
  • Parâmetros alternativos de cobrança (por hora, m², peça, visita, projeto…)
  • Fatores que influenciam o preço
  • Fontes para verificação manual

⚠️ Importante: os valores são estimativas baseadas em ranges públicos do mercado português.
Recomendamos confirmar com 2–3 orçamentos reais (Zaask, Fixando) antes de fixar a tabela final.

Beijinhos,
Equipa Moniquinha's Shine ✨
"""


def main() -> int:
    # Validate config
    missing = [k for k, v in {
        "SMTP_HOST": SMTP_HOST,
        "SMTP_USER": SMTP_USER,
        "SMTP_PASS": SMTP_PASS,
    }.items() if not v]
    if missing:
        print(f"ERROR: missing env vars: {', '.join(missing)}", file=sys.stderr)
        print("Set them and re-run. See file header for details.", file=sys.stderr)
        return 1

    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}", file=sys.stderr)
        return 1

    msg = EmailMessage()
    msg["From"] = SMTP_FROM
    msg["To"] = MAIL_TO
    msg["Subject"] = SUBJECT
    msg.set_content(BODY)

    with PDF_PATH.open("rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=PDF_PATH.name,
        )

    print(f"Connecting to {SMTP_HOST}:{SMTP_PORT} as {SMTP_USER}...")
    context = ssl.create_default_context()
    try:
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=30) as s:
                s.login(SMTP_USER, SMTP_PASS)
                s.send_message(msg)
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as s:
                s.ehlo()
                s.starttls(context=context)
                s.ehlo()
                s.login(SMTP_USER, SMTP_PASS)
                s.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        print(f"AUTH FAILED: {e}", file=sys.stderr)
        print("Tip: Gmail/Outlook require an App Password, not your normal password.", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"SEND FAILED: {e}", file=sys.stderr)
        return 3

    print(f"✅ Sent {PDF_PATH.name} to {MAIL_TO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
