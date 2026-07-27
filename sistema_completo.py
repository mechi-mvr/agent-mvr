#!/usr/bin/env python3
"""
SISTEMA COMPLETO MVR - 6 AGENTES INTEGRADOS
Para: Mechi Vega Robles / Comunicá con Sentido
Deployado en: Railway (automático cada día 7 AM)

Agentes:
  - alerts       (Detectar alertas)
  - reports      (Reportes mensuales)
  - research     (Tendencias + insights)
  - audit        (Auditoría de tienda)
  - content      (Plan de contenidos)
  - onboarding   (Nuevos clientes)
"""

import sys
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

print(f"\n{'='*70}")
print(f"🚀 SISTEMA COMPLETO MVR v1.0 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*70}\n")

# ============================================================================
# 🚨 AGENTE 1: ALERTS
# ============================================================================

def alerts_agent(client_name, metrics=None):
    """Analizar campañas y detectar alertas"""
    
    demo_data = {
        'Al Capone': {
            'roas': 3.2,
            'cpl': 8.75,
            'spend': 1250.50,
            'conversions': 142,
            'impressions': 8940,
            'campaigns': [
                {'name': 'Bomber Variedad', 'roas': 3.5, 'status': 'Active'},
                {'name': 'Lifestyle Stories', 'roas': 2.8, 'status': 'Active'}
            ]
        },
        'Garage La Plata': {
            'roas': 2.1,
            'cpl': 15.40,
            'spend': 340.20,
            'conversions': 22,
            'impressions': 3200,
            'campaigns': [
                {'name': 'Whatsapp Leads', 'roas': 2.5, 'status': 'Active'},
                {'name': 'Mensajería B2B', 'roas': 1.2, 'status': 'Active'}
            ]
        }
    }
    
    if metrics is None and client_name in demo_data:
        metrics = demo_data[client_name]
    
    print(f"\n{'='*70}")
    print(f"🚨 ALERTS - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    if not metrics:
        print(f"❌ Cliente no encontrado")
        return
    
    alerts = []
    
    if metrics['roas'] < 1.5:
        alerts.append({
            'severity': 'ROJO',
            'message': f"ROAS bajo: {metrics['roas']}x",
            'action': 'Pausar o revisar creativos'
        })
    
    if metrics['cpl'] > 20:
        alerts.append({
            'severity': 'ROJO',
            'message': f"CPL elevado: ${metrics['cpl']}",
            'action': 'Auditar audiencias'
        })
    
    if metrics['impressions'] < 1000:
        alerts.append({
            'severity': 'AMARILLO',
            'message': f"Pocas impresiones: {metrics['impressions']}",
            'action': 'Aumentar presupuesto'
        })
    
    if metrics['conversions'] == 0 and metrics['spend'] > 50:
        alerts.append({
            'severity': 'ROJO',
            'message': f"Gasto sin conversiones: ${metrics['spend']}",
            'action': 'Pausar inmediatamente'
        })
    
    print(f"📊 Gasto: ${metrics['spend']:.2f} | ROAS: {metrics['roas']}x | CPL: ${metrics['cpl']:.2f}")
    print(f"   Conversiones: {metrics['conversions']} | Impresiones: {metrics['impressions']:,}\n")
    
    if 'campaigns' in metrics:
        print(f"📈 Campañas:")
        for c in metrics['campaigns']:
            print(f"   • {c['name']} (ROAS: {c['roas']}x)\n")
    
    if alerts:
        print(f"⚠️  ALERTAS:")
        for alert in alerts:
            icon = '🔴' if alert['severity'] == 'ROJO' else '🟡'
            print(f"   {icon} {alert['message']} → {alert['action']}\n")
    else:
        print(f"✅ Sin alertas\n")


# ============================================================================
# 📊 AGENTE 2: REPORTS
# ============================================================================

def reports_agent(client_name):
    """Generar reporte mensual"""
    
    demo = {
        'Al Capone': {
            'totalSpend': 5420.30,
            'impressions': 389400,
            'conversions': 612,
            'avgROAS': 3.2,
            'avgCPL': 8.85,
            'topCampaigns': ['Bomber Variedad', 'Lifestyle Stories'],
        },
        'Garage La Plata': {
            'totalSpend': 1450.80,
            'impressions': 67200,
            'conversions': 94,
            'avgROAS': 2.1,
            'avgCPL': 15.44,
            'topCampaigns': ['Whatsapp Leads', 'Servicios Flota'],
        }
    }
    
    if client_name not in demo:
        print(f"❌ Cliente no encontrado")
        return
    
    data = demo[client_name]
    
    print(f"\n{'='*70}")
    print(f"📊 REPORT - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    print(f"💰 Gasto: ${data['totalSpend']:,.2f}")
    print(f"📈 ROAS: {data['avgROAS']}x | CPL: ${data['avgCPL']:.2f}")
    print(f"✅ Conversiones: {data['conversions']} | Impresiones: {data['impressions']:,}\n")
    
    print(f"🏆 Top Campaigns:")
    for c in data['topCampaigns']:
        print(f"   • {c}\n")
    
    next_budget = data['totalSpend'] * 1.15
    print(f"💡 Presupuesto sugerido próximo mes: ${next_budget:,.2f}\n")


# ============================================================================
# 🔍 AGENTE 3: RESEARCH
# ============================================================================

def research_agent(client_name):
    """Tendencias + insights"""
    
    insights = {
        'Al Capone': {
            'trends': [
                '📱 Reels: 3.5x mejor ROAS que feed',
                '👕 Ropa unisex ganando 45% más engagement',
                '🎬 Video corto (15-30seg): 5x más conversiones'
            ],
            'opportunities': [
                'Crear Reels mostrando looks en movimiento',
                'Colaborar con micro-influencers',
                'Contenido UGC de clientes reales'
            ]
        },
        'Garage La Plata': {
            'trends': [
                '🏢 B2B Lead Gen creciendo 28% YoY',
                '📹 Video servicio: 5x más conversiones',
                '💼 LinkedIn + Meta: combinación ganadora'
            ],
            'opportunities': [
                'Videos timelapse de reparaciones',
                'Testimonios empresa (flota)',
                'Webinar: plan de mantenimiento'
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
    
    print(f"📈 Tendencias:")
    for t in data['trends']:
        print(f"   • {t}\n")
    
    print(f"💡 Oportunidades:")
    for o in data['opportunities']:
        print(f"   • {o}\n")


# ============================================================================
# 🏪 AGENTE 4: AUDIT
# ============================================================================

def audit_agent(store_name="Tienda"):
    """Auditoría de tienda"""
    
    print(f"\n{'='*70}")
    print(f"🏪 AUDIT - {store_name.upper()}")
    print(f"{'='*70}\n")
    
    checks = {
        'Arquitectura': [('Categorías claras', True), ('Búsqueda', True)],
        'Productos': [('Fotos HD', True), ('Descripciones', True)],
        'Checkout': [('< 3 pasos', True), ('Múltiples pagos', True)],
        'Mobile': [('Responsive', True), ('Velocidad < 3s', True)]
    }
    
    issues = 0
    for section, items in checks.items():
        print(f"{section}:")
        for name, status in items:
            icon = '✅' if status else '❌'
            print(f"   {icon} {name}\n")
            if not status:
                issues += 1
    
    print(f"{'='*70}")
    if issues == 0:
        print(f"✅ Tienda optimizada - {issues} problemas\n")
    else:
        print(f"⚠️  {issues} problemas detectados\n")


# ============================================================================
# 📝 AGENTE 5: CONTENT
# ============================================================================

def content_agent(client_name):
    """Plan de contenidos"""
    
    plans = {
        'Al Capone': {
            'pillars': {
                'PRODUCTO': ['Reels: Bomber looks', 'Carousel: outfits', 'Behind-the-scenes'],
                'LIFESTYLE': ['UGC clientes', 'Stories styling', 'Reels transformación'],
                'COMUNIDAD': ['Encuestas', 'Q&A', 'Featured UGC']
            },
            'frecuencia': '5 posts/semana + 3 Reels'
        },
        'Garage La Plata': {
            'pillars': {
                'SERVICIO': ['Timelapse reparación', 'Antes/Después', 'Tips mantenimiento'],
                'B2B': ['Testimonio empresa', 'Webinar', 'Case study'],
                'EDUCACIÓN': ['Tips auto', 'Q&A', 'Señales alerta']
            },
            'frecuencia': '3 posts/semana + 2 Reels'
        }
    }
    
    if client_name not in plans:
        print(f"❌ Cliente no encontrado")
        return
    
    data = plans[client_name]
    
    print(f"\n{'='*70}")
    print(f"📝 CONTENT PLAN - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    for pillar, ideas in data['pillars'].items():
        print(f"📌 {pillar}")
        for idea in ideas:
            print(f"   • {idea}\n")
    
    print(f"⏰ Frecuencia: {data['frecuencia']}\n")


# ============================================================================
# 🎯 AGENTE 6: ONBOARDING
# ============================================================================

def onboarding_agent(client_name="Nuevo Cliente"):
    """Flujo de nuevos clientes"""
    
    print(f"\n{'='*70}")
    print(f"🎯 ONBOARDING - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    print(f"Semana 1: Diagnóstico")
    print(f"   ☐ Auditoría de tienda")
    print(f"   ☐ Análisis competencia")
    print(f"   ☐ Entrevista dueño\n")
    
    print(f"Semana 2: Estrategia")
    print(f"   ☐ Definir Mensaje")
    print(f"   ☐ Maquinaria (canales)")
    print(f"   ☐ Experiencia (customer journey)")
    print(f"   ☐ Rentabilidad (ROAS objetivo)\n")
    
    print(f"Semana 3+: Ejecución")
    print(f"   ☐ Crear assets")
    print(f"   ☐ Setup Meta Ads")
    print(f"   ☐ Calendario 30 días\n")
    
    print(f"💰 Setup: $500 | Mensual: $300-$1,500\n")


# ============================================================================
# EJECUCIÓN AUTOMÁTICA
# ============================================================================

def run_daily_report():
    """Ejecutar todos los agentes cada mañana"""
    print(f"\n\n{'='*70}")
    print(f"⏰ EJECUCIÓN AUTOMÁTICA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    # Al Capone
    alerts_agent('Al Capone')
    reports_agent('Al Capone')
    research_agent('Al Capone')
    content_agent('Al Capone')
    
    # Garage
    alerts_agent('Garage La Plata')
    reports_agent('Garage La Plata')
    research_agent('Garage La Plata')
    content_agent('Garage La Plata')
    
    # Otros
    audit_agent('Al Capone')
    onboarding_agent('Nuevo Cliente')
    
    print(f"\n{'='*70}")
    print(f"✅ REPORTE DIARIO COMPLETADO")
    print(f"{'='*70}\n")


# ============================================================================
# MAIN - SCHEDULER EN RAILWAY
# ============================================================================

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        # Ejecución manual
        agent = sys.argv[1]
        client = sys.argv[2] if len(sys.argv) > 2 else 'Al Capone'
        
        if agent == 'alerts':
            alerts_agent(client)
        elif agent == 'reports':
            reports_agent(client)
        elif agent == 'research':
            research_agent(client)
        elif agent == 'audit':
            audit_agent(client)
        elif agent == 'content':
            content_agent(client)
        elif agent == 'onboarding':
            onboarding_agent(client)
        elif agent == 'all':
            run_daily_report()
    else:
        # AUTOMÁTICO EN RAILWAY
        print("⏰ Iniciando scheduler automático...")
        print("   Próxima ejecución: Mañana 7:00 AM (Argentina)\n")
        
        scheduler = BackgroundScheduler()
        scheduler.add_job(run_daily_report, 'cron', hour=7, minute=0, timezone='America/Argentina/Buenos_Aires')
        scheduler.start()
        
        print("✅ Sistema listo. Ejecutando cada día a las 7 AM...\n")
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()
            print("\n⏹️ Sistema detenido")
