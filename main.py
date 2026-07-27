import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# CONFIG
META_TOKEN = os.getenv('META_TOKEN')
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DB_ID = os.getenv('NOTION_DB_ID')
EMAIL = os.getenv('EMAIL_TO')

CLIENTS = {
    'Al Capone': {'ad_account': 'act_345171403143852'},
    'Garage La Plata': {'ad_account': 'act_1519637538625469'}
}

def get_meta_insights(ad_account_id):
    """Traer datos de Meta Ads"""
    try:
        url = f"https://graph.instagram.com/v18.0/{ad_account_id}/insights"
        params = {
            'fields': 'spend,impressions,clicks,conversions,purchase_value',
            'access_token': META_TOKEN,
            'time_range': json.dumps({
                'since': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'until': datetime.now().strftime('%Y-%m-%d')
            })
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                metrics = data['data'][0]
                return {
                    'spend': float(metrics.get('spend', 0)),
                    'impressions': int(metrics.get('impressions', 0)),
                    'clicks': int(metrics.get('clicks', 0)),
                    'conversions': int(metrics.get('conversions', 0)),
                    'purchase_value': float(metrics.get('purchase_value', 0))
                }
        return None
    except Exception as e:
        print(f"Error fetching Meta insights: {e}")
        return None

def calculate_metrics(metrics):
    """Calcular ROAS, CPL"""
    if not metrics:
        return None
    
    roas = metrics['purchase_value'] / metrics['spend'] if metrics['spend'] > 0 else 0
    cpl = metrics['spend'] / metrics['conversions'] if metrics['conversions'] > 0 else 0
    
    return {
        **metrics,
        'roas': round(roas, 2),
        'cpl': round(cpl, 2)
    }

def detect_alerts(metrics):
    """Detectar alertas"""
    alerts = []
    
    if metrics['roas'] < 1.5 and metrics['roas'] > 0:
        alerts.append('🔴 ROAS bajo: ' + str(metrics['roas']))
    
    if metrics['cpl'] > 20 and metrics['cpl'] > 0:
        alerts.append('🔴 CPL alto: $' + str(metrics['cpl']))
    
    if metrics['conversions'] == 0 and metrics['spend'] > 50:
        alerts.append('🔴 Gasto sin conversiones')
    
    return alerts

def save_to_notion(client_name, metrics):
    """Guardar métricas en Notion"""
    try:
        url = f"https://api.notion.com/v1/pages"
        
        data = {
            'parent': {'database_id': NOTION_DB_ID},
            'properties': {
                'Cliente': {'title': [{'text': {'content': client_name}}]},
                'ROAS': {'number': metrics['roas']},
                'CPL': {'number': metrics['cpl']},
                'Gasto': {'number': metrics['spend']},
                'Conversiones': {'number': metrics['conversions']},
                'Fecha': {'date': {'start': datetime.now().isoformat()}}
            }
        }
        
        headers = {
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        
        response = requests.post(url, json=data, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"Error saving to Notion: {e}")
        return False

def send_alerts(client_name, alerts):
    """Enviar alertas por email (usa SendGrid o Mailgun)"""
    if not alerts:
        return
    
    print(f"🚨 ALERTAS PARA {client_name}:")
    for alert in alerts:
        print(f"  {alert}")

def run_agent():
    """Ejecutar agent principal"""
    print(f"\n{'='*60}")
    print(f"🚀 ALERTS AGENT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    for client_name, config in CLIENTS.items():
        print(f"\n📊 Analizando {client_name}...")
        
        # Traer datos
        insights = get_meta_insights(config['ad_account'])
        if not insights:
            print(f"  ⚠️ No hay datos")
            continue
        
        # Calcular métricas
        metrics = calculate_metrics(insights)
        
        # Detectar alertas
        alerts = detect_alerts(metrics)
        
        # Guardar en Notion
        save_to_notion(client_name, metrics)
        
        # Enviar alertas
        send_alerts(client_name, alerts)
        
        print(f"  ✅ ROAS: {metrics['roas']}x | CPL: ${metrics['cpl']}")

if __name__ == '__main__':
    run_agent()
