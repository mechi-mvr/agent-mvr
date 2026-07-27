#!/usr/bin/env python3
"""
SISTEMA COMPLETO MVR - TASK AUTOMATION
Para: Mechi Vega Robles / Comunicá con Sentido
Ejecuta agentes, guarda resultados Y CREA TAREAS automáticamente en Notion
"""

import sys
import requests
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

NOTION_TOKEN = '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'
NOTION_DB_ID = '59b0b055893248878bbbafe807e9cf34'

CLIENTS = {
    'Al Capone': {'ad_account': 'act_345171403143852'},
    'Garage La Plata': {'ad_account': 'act_1519637538625469'}
}

print(f"\n{'='*70}")
print(f"🚀 SISTEMA MVR - TASK AUTOMATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*70}\n")

# ============================================================================
# FUNCIONES NOTION
# ============================================================================

def create_task_in_notion(task_title, client_name, priority, description, task_type):
    """Crear una tarea en Notion con propiedades automáticas"""
    try:
        url = "https://api.notion.com/v1/pages"
        
        # Determinar color de prioridad
        priority_colors = {
            'CRÍTICA': 'red',
            'ALTA': 'orange',
            'MEDIA': 'yellow',
            'BAJA': 'green'
        }
        
        properties = {
            'Nombre': {'title': [{'text': {'content': task_title}}]},
            'Cliente': {'select': {'name': client_name}},
            'Tipo': {'select': {'name': task_type}},
            'Prioridad': {'select': {'name': priority, 'color': priority_colors.get(priority, 'gray')}},
            'Estado': {'select': {'name': 'Por hacer'}},
            'Descripción': {'rich_text': [{'text': {'content': description[:1000]}}]},
            'Fecha Creada': {'date': {'start': datetime.now().isoformat()}},
            'Fecha Vencimiento': {'date': {'start': (datetime.now() + timedelta(days=1 if priority == 'CRÍTICA' else 3)).isoformat()}}
        }
        
        payload = {
            'parent': {'database_id': NOTION_DB_ID},
            'properties': properties
        }
        
        headers = {
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"      ✅ TAREA CREADA EN NOTION")
            return True
        else:
            print(f"      ⚠️ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"      ⚠️ Error: {e}")
        return False

# ============================================================================
# 🚨 AGENTE 1: ALERTS CON TASK AUTOMATION
# ============================================================================

def alerts_agent(client_name):
    """Detectar alertas y crear tareas automáticamente"""
    
    print(f"\n{'='*70}")
    print(f"🚨 ALERTS - {client_name.upper()}")
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
        print(f"❌ Cliente no encontrado")
        return
    
    metrics = demo_data[client_name]
    
    print(f"📊 Gasto: ${metrics['spend']:.2f} | ROAS: {metrics['roas']}x | CPL: ${metrics['cpl']:.2f}")
    print(f"   Conversiones: {metrics['conversions']} | Impresiones: {metrics['impressions']:,}\n")
    
    # Detectar alertas y crear tareas
    alerts_created = 0
    
    if metrics['roas'] < 1.5:
        print(f"   🔴 ALERTA: ROAS bajo ({metrics['roas']}x)")
        task_title = f"URGENTE: ROAS bajo en {client_name} - {metrics['roas']}x"
        description = f"ROAS crítico en {metrics['roas']}x (objetivo: 1.5x+). Revisar creativos, audiencias o pausar campañas de bajo rendimiento."
        create_task_in_notion(task_title, client_name, 'CRÍTICA', description, 'Ads Optimization')
        alerts_created += 1
    
    if metrics['cpl'] > 20:
        print(f"   🔴 ALERTA: CPL elevado (${metrics['cpl']})")
        task_title = f"URGENTE: CPL elevado en {client_name} - ${metrics['cpl']}"
        description = f"CPL de ${metrics['cpl']} excede el máximo de $20. Auditar audiencias, expandir targeting o revisar landing page."
        create_task_in_notion(task_title, client_name, 'CRÍTICA', description, 'Ads Optimization')
        alerts_created += 1
    
    if metrics['impressions'] < 1000:
        print(f"   🟡 ALERTA: Pocas impresiones ({metrics['impressions']})")
        task_title = f"Aumentar presupuesto - {client_name} (bajo alcance)"
        description = f"Solo {metrics['impressions']} impresiones en últimos 7 días. Considerar aumentar presupuesto diario o revisar segmentación."
        create_task_in_notion(task_title, client_name, 'MEDIA', description, 'Budget Planning')
        alerts_created += 1
    
    if metrics['conversions'] == 0 and metrics['spend'] > 50:
        print(f"   🔴 ALERTA: Gasto sin conversiones!")
        task_title = f"CRÍTICO: ${metrics['spend']} gastado sin conversiones - {client_name}"
        description = f"Gasto de ${metrics['spend']:.2f} sin ninguna conversión. PAUSAR INMEDIATAMENTE. Revisar creativo, landing page, y checkout."
        create_task_in_notion(task_title, client_name, 'CRÍTICA', description, 'Emergency Action')
        alerts_created += 1
    
    if alerts_created == 0:
        print(f"   ✅ Sin alertas - Métrica saludable\n")
    else:
        print(f"\n   📋 {alerts_created} tarea(s) creada(s) en Notion\n")

# ============================================================================
# 📊 AGENTE 2: REPORTS
# ============================================================================

def reports_agent(client_name):
    """Generar reporte y crear tareas de seguimiento"""
    
    print(f"\n{'='*70}")
    print(f"📊 REPORT - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    demo = {
        'Al Capone': {
            'totalSpend': 5420.30, 'impressions': 389400,
            'conversions': 612, 'avgROAS': 3.2, 'avgCPL': 8.85
        },
        'Garage La Plata': {
            'totalSpend': 1450.80, 'impressions': 67200,
            'conversions': 94, 'avgROAS': 2.1, 'avgCPL': 15.44
        }
    }
    
    if client_name not in demo:
        print(f"❌ Cliente no encontrado")
        return
    
    data = demo[client_name]
    
    print(f"💰 Gasto: ${data['totalSpend']:,.2f}")
    print(f"📈 ROAS: {data['avgROAS']}x | CPL: ${data['avgCPL']:.2f}")
    print(f"✅ Conversiones: {data['conversions']}\n")
    
    # Crear tarea de reporte mensual
    task_title = f"Reporte Mensual - {client_name} ({datetime.now().strftime('%B')})"
    description = f"""Reporte mensual completado:
    - Gasto Total: ${data['totalSpend']:,.2f}
    - ROAS: {data['avgROAS']}x
    - CPL: ${data['avgCPL']:.2f}
    - Conversiones: {data['conversions']}
    
    Acciones sugeridas: Revisar creativos top, escalar presupuesto en mejores performers."""
    
    create_task_in_notion(task_title, client_name, 'MEDIA', description, 'Reporting')
    print(f"   📋 Tarea de reporte creada en Notion\n")

# ============================================================================
# 🔍 AGENTE 3: RESEARCH CON TASK AUTOMATION
# ============================================================================

def research_agent(client_name):
    """Tendencias e insights - Crear tareas de acción"""
    
    insights = {
        'Al Capone': {
            'opportunities': [
                'Crear Reels mostrando looks en movimiento',
                'Colaborar con micro-influencers (10k-50k)',
                'Producir contenido UGC de clientes reales'
            ]
        },
        'Garage La Plata': {
            'opportunities': [
                'Grabar videos timelapse de reparaciones',
                'Conseguir testimonios de empresas con flota',
                'Grabar webinar sobre plan de mantenimiento'
            ]
        }
    }
    
    if client_name not in insights:
        print(f"❌ Cliente no encontrado")
        return
    
    data = insights[client_name]
    
    print(f"\n{'='*70}")
    print(f"🔍 RESEARCH - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    print(f"💡 Oportunidades detectadas:\n")
    for i, opp in enumerate(data['opportunities'], 1):
        print(f"   {i}. {opp}")
        
        # Crear tarea para cada oportunidad
        task_title = f"Acción: {opp} - {client_name}"
        description = f"Oportunidad de crecimiento identificada: {opp}\n\nEstimado de impacto: ALTO\nComplexidad: MEDIA\nVencimiento: 14 días"
        create_task_in_notion(task_title, client_name, 'ALTA', description, 'Content Action')
    
    print(f"\n   📋 {len(data['opportunities'])} tarea(s) de acción creada(s)\n")

# ============================================================================
# 📝 AGENTE 4: CONTENT
# ============================================================================

def content_agent(client_name):
    """Plan de contenidos - Crear tareas por pillar"""
    
    plans = {
        'Al Capone': {
            'PRODUCTO': ['Reels: Bomber looks', 'Carousel: outfits'],
            'LIFESTYLE': ['UGC clientes', 'Stories styling'],
            'COMUNIDAD': ['Encuestas', 'Featured UGC']
        },
        'Garage La Plata': {
            'SERVICIO': ['Timelapse reparación', 'Antes/Después'],
            'B2B': ['Testimonio empresa', 'Webinar'],
            'EDUCACIÓN': ['Tips auto', 'Q&A']
        }
    }
    
    if client_name not in plans:
        print(f"❌ Cliente no encontrado")
        return
    
    data = plans[client_name]
    
    print(f"\n{'='*70}")
    print(f"📝 CONTENT PLAN - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    tasks_created = 0
    for pillar, ideas in data.items():
        print(f"📌 {pillar}:")
        for idea in ideas:
            print(f"   • {idea}")
            
            # Crear tarea para cada idea
            task_title = f"Contenido: {idea} - {pillar}"
            description = f"Crear contenido: {idea}\n\nPillar: {pillar}\nCliente: {client_name}\nProioridad: Publicar esta semana"
            create_task_in_notion(task_title, client_name, 'MEDIA', description, 'Content Creation')
            tasks_created += 1
        print()
    
    print(f"   📋 {tasks_created} tarea(s) de contenido creada(s)\n")

# ============================================================================
# 🏪 AGENTE 5: AUDIT
# ============================================================================

def audit_agent(client_name="Al Capone"):
    """Auditoría - Crear tareas de mejora"""
    
    print(f"\n{'='*70}")
    print(f"🏪 AUDIT - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    issues = [
        {'name': 'Optimizar velocidad mobile', 'priority': 'ALTA'},
        {'name': 'Mejorar descripción de productos', 'priority': 'MEDIA'},
        {'name': 'Revisar checkout en mobile', 'priority': 'ALTA'}
    ]
    
    print(f"Problemas encontrados:\n")
    for issue in issues:
        print(f"   • {issue['name']}")
        
        # Crear tarea por cada problema
        task_title = f"Auditoría: {issue['name']} - {client_name}"
        description = f"Problema identificado en auditoría: {issue['name']}\n\nImpacto: Conversión\nAcción: Revisar y optimizar"
        create_task_in_notion(task_title, client_name, issue['priority'], description, 'Technical Issue')
    
    print(f"\n   📋 {len(issues)} tarea(s) de mejora creada(s)\n")

# ============================================================================
# EJECUCIÓN AUTOMÁTICA
# ============================================================================

def run_daily_report():
    """Ejecutar agentes, guardar y crear tareas"""
    print(f"\n\n{'='*70}")
    print(f"⏰ EJECUCIÓN AUTOMÁTICA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    print(f"🔄 Ejecutando agentes y creando tareas automáticamente...\n")
    
    # Al Capone
    alerts_agent('Al Capone')
    reports_agent('Al Capone')
    research_agent('Al Capone')
    content_agent('Al Capone')
    audit_agent('Al Capone')
    
    # Garage
    alerts_agent('Garage La Plata')
    reports_agent('Garage La Plata')
    research_agent('Garage La Plata')
    content_agent('Garage La Plata')
    
    print(f"\n{'='*70}")
    print(f"✅ REPORTE COMPLETADO - TAREAS CREADAS EN NOTION")
    print(f"{'='*70}\n")
    print(f"📋 Próximo ciclo: Mañana 7:00 AM\n")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        agent = sys.argv[1].lower()
        client = sys.argv[2] if len(sys.argv) > 2 else 'Al Capone'
        
        if agent == 'alerts':
            alerts_agent(client)
        elif agent == 'reports':
            reports_agent(client)
        elif agent == 'research':
            research_agent(client)
        elif agent == 'content':
            content_agent(client)
        elif agent == 'audit':
            audit_agent(client)
        elif agent == 'all':
            run_daily_report()
    else:
        print("⏰ Iniciando scheduler automático...")
        print("   Próxima ejecución: Mañana 7:00 AM\n")
        
        scheduler = BackgroundScheduler()
        scheduler.add_job(run_daily_report, 'cron', hour=7, minute=0, timezone='America/Argentina/Buenos_Aires')
        scheduler.start()
        
        print("✅ Sistema listo - Creando tareas automáticamente cada día...\n")
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()
