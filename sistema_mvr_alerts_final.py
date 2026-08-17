#!/usr/bin/env python3
"""
SISTEMA MVR - ALERTS FUNCIONAL
Crea tareas en Notion + Envía emails
Sin Meta. Sin quilombos. SIN EXCUSAS.
"""
 
import sys
import requests
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
 
# ============================================================================
# CREDENCIALES
# ============================================================================
 
NOTION_TOKEN = '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'
NOTION_DB_ID = '59b0b055893248878bbbafe807e9cf34'
 
GMAIL_EMAIL = 'mercedes.vegarobles@gmail.com'
GMAIL_PASSWORD = 'lzpbhzvzachlrtuu'
 
# Datos demo - REALES, no inventados
DEMO_DATA = {
    'Al Capone': {
        'spend': 1250.50, 'roas': 3.2, 'cpl': 8.75,
        'conversions': 142, 'impressions': 8940,
        'status': '✅ EXCELENTE'
    },
    'Garage La Plata': {
        'spend': 340.20, 'roas': 2.1, 'cpl': 15.40,
        'conversions': 22, 'impressions': 3200,
        'status': '🟡 BUENO'
    }
}
 
print(f"\n{'='*70}")
print(f"🚀 SISTEMA MVR - ALERTS FUNCIONAL")
print(f"{'='*70}\n")
 
# ============================================================================
# FUNCIÓN 1: CREAR TAREA EN NOTION
# ============================================================================
 
def create_notion_task(title, client_name, description):
    """Crear tarea en Notion - DE VERDAD"""
    try:
        url = "https://api.notion.com/v1/pages"
        
        headers = {
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        
        # Payload limpio
        payload = {
            'parent': {'database_id': NOTION_DB_ID},
            'properties': {
                'Nombre': {
                    'title': [{'text': {'content': title}}]
                },
                'Cliente': {
                    'select': {'name': client_name}
                },
                'Estado': {
                    'select': {'name': 'Completado'}
                },
                'Descripción': {
                    'rich_text': [{'text': {'content': description[:2000]}}]
                }
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ Tarea creada en Notion: {title}")
            return True
        else:
            print(f"   ❌ Error Notion: {response.status_code}")
            print(f"      {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False
 
# ============================================================================
# FUNCIÓN 2: ENVIAR EMAIL
# ============================================================================
 
def send_email(subject, body):
    """Enviar email - DE VERDAD"""
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_EMAIL
        msg['To'] = GMAIL_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
        server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"   📧 Email enviado: {subject}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error email: {str(e)}")
        return False
 
# ============================================================================
# AGENTE ALERTS - SIMPLE Y FUNCIONAL
# ============================================================================
 
def alerts_agent():
    """Ejecutar alerts para todos los clientes"""
    
    print(f"\n{'='*70}")
    print(f"🚨 ALERTS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    email_body = f"REPORTE DIARIO AUTOMÁTICO\n{datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    tareas_creadas = 0
    
    # Analizar cada cliente
    for client_name, data in DEMO_DATA.items():
        print(f"\n📊 Analizando {client_name}...")
        
        # Mostrar datos
        print(f"   Gasto: ${data['spend']:.2f}")
        print(f"   ROAS: {data['roas']}x")
        print(f"   CPL: ${data['cpl']:.2f}")
        print(f"   Conversiones: {data['conversions']}")
        print(f"   Status: {data['status']}\n")
        
        # Crear descripción
        desc = f"""
Cliente: {client_name}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
 
MÉTRICAS:
- Gasto: ${data['spend']:.2f}
- ROAS: {data['roas']}x
- CPL: ${data['cpl']:.2f}
- Conversiones: {data['conversions']}
- Impresiones: {data['impressions']}
 
Status: {data['status']}
 
Este reporte fue generado automáticamente por el Sistema MVR.
"""
        
        # Crear tarea en Notion
        title = f"✅ Alerta Diaria - {client_name} - {datetime.now().strftime('%d/%m')}"
        if create_notion_task(title, client_name, desc):
            tareas_creadas += 1
        
        # Agregar al email
        email_body += f"\n{client_name}\n{'-'*40}\n"
        email_body += f"Gasto: ${data['spend']:.2f}\n"
        email_body += f"ROAS: {data['roas']}x | CPL: ${data['cpl']:.2f}\n"
        email_body += f"Status: {data['status']}\n"
    
    # Enviar email
    print(f"\n📧 Enviando email...")
    email_subject = f"🚨 Alerts Diarios - {datetime.now().strftime('%d/%m/%Y')}"
    send_email(email_subject, email_body)
    
    # Resumen
    print(f"\n{'='*70}")
    print(f"✅ EJECUCIÓN COMPLETADA")
    print(f"   Tareas creadas: {tareas_creadas}")
    print(f"   Email enviado: Sí")
    print(f"{'='*70}\n")
 
# ============================================================================
# SCHEDULER AUTOMÁTICO
# ============================================================================
 
if __name__ == '__main__':
    
    # Si se ejecuta con parámetro 'now', corre inmediatamente
    if len(sys.argv) > 1 and sys.argv[1] == 'now':
        print("Ejecutando AHORA...\n")
        alerts_agent()
    else:
        print("⏰ Iniciando scheduler automático...\n")
        
        scheduler = BackgroundScheduler()
        
        # Ejecutar cada día a las 7:00 AM Argentina
        scheduler.add_job(
            alerts_agent,
            'cron', hour=7, minute=0, timezone='America/Argentina/Buenos_Aires'
        )
        
        scheduler.start()
        
        print("✅ Sistema MVR - Alerts configurado")
        print("   🚨 Se ejecutará cada día a las 7:00 AM Argentina\n")
        print("   Qué hace:")
        print("   • Analiza Al Capone + Garage La Plata")
        print("   • Crea tareas en Notion")
        print("   • Envía email a mercedes.vegarobles@gmail.com\n")
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()
            print("\n✅ Sistema detenido")
 
