#!/usr/bin/env python3
"""
SISTEMA MVR - ALERTS CON META API REAL
Versión mejorada con debugging completo
"""

import sys
import requests
import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

NOTION_TOKEN = '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'
NOTION_DB_ID = '59b0b055893248878bbbafe807e9cf34'
GMAIL_PASSWORD = 'lzpbhzvzachlrtuu'

META_TOKEN = 'EAAVZByt6dKX0BSAa5QaV0NqcokTkQafHRb2fMIOmW6ywCu6ZCGwlWElNbu51gseqZCZCBzrjYWj2fhJnZAHTeYHuOC8z1LzDBRZBhw3zbZAMmDmFt3vniqlFVAujwHFkokTYIKGZBtVBkSQW3HhmmKnOX8ZBZAEqpHlZCEa5oSXI8jP7j8EyWNZC6eif8iGqjtZBIMwZDZD'

CLIENTS = {
    'Al Capone': {'ad_account': 'act_345171403143852'},
    'Garage La Plata': {'ad_account': 'act_1519637538625469'}
}

print(f"\n{'='*70}")
print(f"🚀 ALERTS CON META REAL - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*70}\n")

# ============================================================================
# INTENTAR CONECTAR A META - CON DEBUGGING
# ============================================================================

def get_account_insights(ad_account_id):
    """Intentar traer datos de Meta Ads - CON DEBUGGING COMPLETO"""
    try:
        print(f"   🔍 Intentando conectar a Meta...\n")
        
        url = f"https://graph.instagram.com/v18.0/{ad_account_id}/insights"
        
        params = {
            'fields': 'spend,impressions,clicks,conversions',
            'access_token': META_TOKEN,
            'date_preset': 'last_7d'
        }
        
        print(f"   URL: {url}")
        print(f"   Token presente: {'Sí' if META_TOKEN else 'No'}\n")
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:500]}\n")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                metrics = data['data'][0]
                return {
                    'spend': float(metrics.get('spend', 0)),
                    'impressions': int(metrics.get('impressions', 0)),
                    'clicks': int(metrics.get('clicks', 0)),
                    'conversions': int(metrics.get('conversions', 0)),
                    'fuente': 'Meta Real'
                }
        
        # Si hay error, mostrar
        if response.status_code != 200:
            error_data = response.json()
            print(f"   ❌ ERROR META:")
            print(f"      Code: {error_data.get('error', {}).get('code')}")
            print(f"      Message: {error_data.get('error', {}).get('message')}\n")
        
        return None
        
    except requests.exceptions.Timeout:
        print(f"   ⚠️ TIMEOUT - Meta no responde\n")
        return None
    except Exception as e:
        print(f"   ⚠️ ERROR: {str(e)}\n")
        return None

# ============================================================================
# ALERTS CON FALLBACK A DEMO
# ============================================================================

def alerts_agent(client_name):
    """Alertas - Intenta Meta Real, si falla usa Demo"""
    
    print(f"\n{'='*70}")
    print(f"🚨 ALERTS - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    if client_name not in CLIENTS:
        print(f"❌ Cliente no encontrado\n")
        return
    
    ad_account = CLIENTS[client_name]['ad_account']
    
    # PASO 1: Intentar Meta Real
    print(f"📡 PASO 1: Intentando Meta API Real...\n")
    metrics_real = get_account_insights(ad_account)
    
    # PASO 2: Si falla, usar Demo
    if not metrics_real:
        print(f"⚠️ PASO 2: Meta no disponible, usando datos DEMO...\n")
        
        demo_data = {
            'Al Capone': {
                'spend': 1250.50, 'roas': 3.2, 'cpl': 8.75,
                'conversions': 142, 'impressions': 8940
            },
            'Garage La Plata': {
                'spend': 340.20, 'roas': 2.1, 'cpl': 15.40,
                'conversions': 22, 'impressions': 3200
            }
        }
        
        metrics = demo_data.get(client_name)
        fuente = "DEMO (Meta no disponible)"
    else:
        metrics = metrics_real
        fuente = "Meta Real"
    
    if not metrics:
        print(f"❌ No hay datos disponibles\n")
        return
    
    # Mostrar datos
    print(f"✅ DATOS OBTENIDOS - Fuente: {fuente}\n")
    print(f"   Gasto: ${metrics.get('spend', 0):.2f}")
    print(f"   ROAS: {metrics.get('roas', 'N/A')}x")
    print(f"   CPL: ${metrics.get('cpl', 'N/A')}")
    print(f"   Conversiones: {metrics.get('conversions', 0)}")
    print(f"   Impresiones: {metrics.get('impressions', 0)}\n")
    
    # Detectar alertas
    alerts = []
    if metrics.get('roas', 0) < 1.5:
        alerts.append('ROAS bajo')
    if metrics.get('cpl', 0) > 20:
        alerts.append('CPL elevado')
    
    if alerts:
        print(f"⚠️ ALERTAS: {', '.join(alerts)}\n")
    else:
        print(f"✅ Sin alertas\n")

# ============================================================================
# EJECUTAR
# ============================================================================

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'all':
        for client in ['Al Capone', 'Garage La Plata']:
            alerts_agent(client)
    else:
        print("⏰ Scheduler configurado - ejecutará mañana 7 AM\n")
        
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            lambda: [alerts_agent(c) for c in ['Al Capone', 'Garage La Plata']],
            'cron', hour=7, minute=0, timezone='America/Argentina/Buenos_Aires'
        )
        scheduler.start()
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()
