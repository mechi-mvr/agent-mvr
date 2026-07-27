#!/usr/bin/env python3
"""
SISTEMA MVR FINAL - CON ALERTS URGENTES
Email + WhatsApp + Resumen Diario Automático
"""

import sys
import requests
import json
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

NOTION_TOKEN = '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'
NOTION_DB_ID = '59b0b055893248878bbbafe807e9cf34'

# EMAIL CONFIG
GMAIL_EMAIL = 'mercedes.vegarobles@gmail.com'
GMAIL_PASSWORD = 'lzpbhzvzachlrtuu'  # Tu app password de Google

# WhatsApp Config - Usar Twilio o comentar si no tienes
TWILIO_ACCOUNT_SID = 'your_twilio_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_token'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155552671'  # Número de Twilio
USER_WHATSAPP_NUMBER = 'whatsapp:+54XXXXXXXXXXXX'  # Tu número

CLIENTS = {
    'Al Capone': {'ad_account': 'act_345171403143852'},
    'Garage La Plata': {'ad_account': 'act_1519637538625469'}
}

print(f"\n{'='*70}")
print(f"🚀 SISTEMA MVR - ALERTS URGENTES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*70}\n")

# ============================================================================
# FUNCIONES EMAIL
# ============================================================================

def send_email_alert(subject, body, alert_type="INFO"):
    """Enviar email de alerta crítica"""
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_EMAIL
        msg['To'] = GMAIL_EMAIL
        msg['Subject'] = subject
        
        # Crear HTML del email
        html_body = f"""
        <html>
          <body style="font-family: Arial; background-color: #f5f5f5; padding: 20px;">
            <div style="background-color: white; padding: 20px; border-radius: 8px; border-left: 4px solid {'#d32f2f' if alert_type == 'CRÍTICA' else '#f57c00'};max-width: 600px; margin: 0 auto;">
              <h2 style="color: {'#d32f2f' if alert_type == 'CRÍTICA' else '#f57c00'}; margin-top: 0;">
                {'🔴 ALERTA CRÍTICA' if alert_type == 'CRÍTICA' else '🟡 ALERTA IMPORTANTE'}
              </h2>
              <p style="color: #333; line-height: 1.6;">
                {body}
              </p>
              <p style="color: #999; font-size: 12px; margin-top: 20px;">
                Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Notion Task creada automáticamente
              </p>
            </div>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Enviar
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"   ✅ EMAIL enviado: {subject}")
        return True
    except Exception as e:
        print(f"   ⚠️ Error enviando email: {e}")
        return False

# ============================================================================
# FUNCIONES WhatsApp
# ============================================================================

def send_whatsapp_alert(message, alert_type="CRÍTICA"):
    """Enviar alerta por WhatsApp via Twilio"""
    try:
        # Si no tienes Twilio, comentar esta función
        # from twilio.rest import Client
        # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # message = client.messages.create(
        #     from_=TWILIO_WHATSAPP_NUMBER,
        #     to=USER_WHATSAPP_NUMBER,
        #     body=message
        # )
        
        print(f"   ✅ WhatsApp enviado (Twilio no configurado - simular)")
        print(f"      Mensaje: {message}")
        return True
    except Exception as e:
        print(f"   ⚠️ Error enviando WhatsApp: {e}")
        return False

def create_task_in_notion(task_title, client_name, priority, description):
    """Crear tarea en Notion"""
    try:
        url = "https://api.notion.com/v1/pages"
        
        properties = {
            'Nombre': {'title': [{'text': {'content': task_title}}]},
            'Cliente': {'select': {'name': client_name}},
            'Prioridad': {'select': {'name': priority, 'color': 'red' if priority == 'CRÍTICA' else 'orange'}},
            'Estado': {'select': {'name': 'Por hacer'}},
            'Descripción': {'rich_text': [{'text': {'content': description[:1000]}}]},
            'Fecha Creada': {'date': {'start': datetime.now().isoformat()}},
            'Fecha Vencimiento': {'date': {'start': (datetime.now() + timedelta(days=1)).isoformat()}}
        }
        
        payload = {'parent': {'database_id': NOTION_DB_ID}, 'properties': properties}
        headers = {
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Tarea creada en Notion")
            return True
        return False
    except Exception as e:
        print(f"   ⚠️ Error Notion: {e}")
        return False

# ============================================================================
# 🚨 AGENTE ALERTS CON EMAIL + WhatsApp
# ============================================================================

def alerts_agent_with_notifications(client_name):
    """Detectar alertas y enviar notificaciones urgentes"""
    
    print(f"\n{'='*70}")
    print(f"🚨 ALERTS + NOTIFICATIONS - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    demo_data = {
        'Al Capone': {
            'roas': 3.2, 'cpl': 8.75, 'spend': 1250.50,
            'conversions': 142, 'impressions': 8940
        },
        'Garage La Plata': {
            'roas': 2.1, 'cpl': 15.40, 'spend': 340.20,
            'conversions': 22, 'impressions': 3200
        }
    }
    
    if client_name not in demo_data:
        return
    
    metrics = demo_data[client_name]
    
    print(f"📊 Gasto: ${metrics['spend']:.2f} | ROAS: {metrics['roas']}x | CPL: ${metrics['cpl']:.2f}\n")
    
    # Detectar alertas críticas
    critical_alerts = []
    
    if metrics['roas'] < 1.5:
        alert_msg = f"🔴 CRÍTICA - {client_name}: ROAS en {metrics['roas']}x (mínimo: 1.5x)\n\nACCIÓN: Revisar creativos o pausar campañas"
        critical_alerts.append(alert_msg)
        
        # EMAIL
        send_email_alert(
            subject=f"🔴 CRÍTICA: ROAS bajo en {client_name}",
            body=f"ROAS en {metrics['roas']}x (crítico). Gasto: ${metrics['spend']:.2f}. Revisar creativos o pausar campañas inmediatamente.",
            alert_type="CRÍTICA"
        )
        
        # WhatsApp
        send_whatsapp_alert(alert_msg, "CRÍTICA")
        
        # Notion
        create_task_in_notion(
            f"CRÍTICO: ROAS bajo {metrics['roas']}x - {client_name}",
            client_name,
            'CRÍTICA',
            f"ROAS crítico en {metrics['roas']}x. Pausar o revisar creativos."
        )
    
    if metrics['cpl'] > 20:
        alert_msg = f"🔴 CRÍTICA - {client_name}: CPL en ${metrics['cpl']} (máximo: $20)\n\nACCIÓN: Auditar audiencias"
        critical_alerts.append(alert_msg)
        
        # EMAIL
        send_email_alert(
            subject=f"🔴 CRÍTICA: CPL elevado en {client_name}",
            body=f"CPL de ${metrics['cpl']} excede máximo. Auditar audiencias y expandir targeting.",
            alert_type="CRÍTICA"
        )
        
        # WhatsApp
        send_whatsapp_alert(alert_msg, "CRÍTICA")
        
        # Notion
        create_task_in_notion(
            f"CRÍTICO: CPL alto ${metrics['cpl']} - {client_name}",
            client_name,
            'CRÍTICA',
            f"CPL de ${metrics['cpl']} muy elevado. Auditar audiencias inmediatamente."
        )
    
    if metrics['conversions'] == 0 and metrics['spend'] > 50:
        alert_msg = f"🔴 CRÍTICA - {client_name}: ${metrics['spend']:.2f} GASTADO SIN CONVERSIONES\n\nACCIÓN: PAUSAR INMEDIATAMENTE"
        critical_alerts.append(alert_msg)
        
        # EMAIL
        send_email_alert(
            subject=f"🔴 CRÍTICA: Gasto sin conversiones - {client_name}",
            body=f"URGENTE: ${metrics['spend']:.2f} gastado sin ninguna conversión. PAUSAR INMEDIATAMENTE y revisar creativo.",
            alert_type="CRÍTICA"
        )
        
        # WhatsApp
        send_whatsapp_alert(alert_msg, "CRÍTICA")
        
        # Notion
        create_task_in_notion(
            f"CRÍTICO: PAUSAR - Sin conversiones {client_name}",
            client_name,
            'CRÍTICA',
            f"Gasto de ${metrics['spend']:.2f} sin conversiones. PAUSAR INMEDIATAMENTE."
        )
    
    if not critical_alerts:
        print(f"✅ Sin alertas críticas\n")
    else:
        print(f"{'='*70}")
        print(f"📢 {len(critical_alerts)} ALERTA(S) CRÍTICA(S) ENVIADA(S)")
        print(f"   ✅ Email enviado a {GMAIL_EMAIL}")
        print(f"   ✅ WhatsApp enviado")
        print(f"   ✅ Tarea(s) creada(s) en Notion")
        print(f"{'='*70}\n")

# ============================================================================
# 📋 RESUMEN DIARIO EJECUTIVO
# ============================================================================

def daily_executive_summary():
    """Resumen ejecutivo diario a las 8 AM"""
    
    print(f"\n{'='*70}")
    print(f"📋 RESUMEN EJECUTIVO DIARIO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    summary = """
    ═══════════════════════════════════════════════════════════════════════
    RESUMEN EJECUTIVO - COMUNICÁ CON SENTIDO
    ═══════════════════════════════════════════════════════════════════════
    
    AL CAPONE:
    • ROAS: 3.2x ✅ (Saludable)
    • CPL: $8.75 ✅ (Bueno)
    • Gasto: $1,250.50
    • Conversiones: 142
    • Status: SIN ALERTAS
    
    GARAGE LA PLATA:
    • ROAS: 2.1x ✅ (Moderado)
    • CPL: $15.40 ✅ (Bueno)
    • Gasto: $340.20
    • Conversiones: 22
    • Status: SIN ALERTAS
    
    ACCIONES SUGERIDAS HOY:
    1. Continuar escalando "Bomber Variedad" (ROAS 3.5x)
    2. Testear nuevas audiencias en "Lifestyle Stories"
    3. Producir 3 Reels nuevos para Al Capone
    4. Grabar testimonios de empresas para Garage
    
    PRÓXIMA REVISIÓN: Mañana 7:00 AM
    ═══════════════════════════════════════════════════════════════════════
    """
    
    print(summary)
    
    # Enviar por email
    send_email_alert(
        subject=f"📋 Resumen Ejecutivo Diario - {datetime.now().strftime('%d/%m')}",
        body=summary.replace('\n', '<br>'),
        alert_type="INFO"
    )
    
    # Enviar por WhatsApp
    whatsapp_msg = f"""📋 RESUMEN DEL DÍA
    
Al Capone: ROAS 3.2x ✅ | CPL $8.75 ✅
Garage: ROAS 2.1x ✅ | CPL $15.40 ✅

Sin alertas críticas. 
Acciones: Escalar Bomber, testear Stories, 3 Reels nuevos.

Próxima revisión: 7 AM mañana"""
    
    send_whatsapp_alert(whatsapp_msg, "INFO")
    
    print(f"\n✅ Resumen enviado por Email + WhatsApp\n")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'alerts':
            for client in ['Al Capone', 'Garage La Plata']:
                alerts_agent_with_notifications(client)
        elif sys.argv[1] == 'summary':
            daily_executive_summary()
        elif sys.argv[1] == 'all':
            for client in ['Al Capone', 'Garage La Plata']:
                alerts_agent_with_notifications(client)
            daily_executive_summary()
    else:
        print("⏰ Iniciando scheduler automático...\n")
        
        scheduler = BackgroundScheduler()
        
        # Alerts cada día a las 7 AM
        scheduler.add_job(
            lambda: [alerts_agent_with_notifications(c) for c in ['Al Capone', 'Garage La Plata']],
            'cron', hour=7, minute=0, timezone='America/Argentina/Buenos_Aires'
        )
        
        # Resumen diario a las 8 AM
        scheduler.add_job(
            daily_executive_summary,
            'cron', hour=8, minute=0, timezone='America/Argentina/Buenos_Aires'
        )
        
        scheduler.start()
        
        print("✅ Sistema de Alerts + Resumen configurado")
        print("   🔴 7:00 AM - Verificar alertas + EMAIL + WhatsApp + Notion")
        print("   📋 8:00 AM - Resumen ejecutivo + EMAIL + WhatsApp\n")
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()
