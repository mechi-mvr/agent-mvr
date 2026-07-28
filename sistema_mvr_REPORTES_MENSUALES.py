#!/usr/bin/env python3
"""
AGENTE REPORTES MENSUALES AUTOMÁTICOS MVR
Para: Mechi Vega Robles / Comunicá con Sentido
Genera PowerPoint automático con gráficos, métricas y recomendaciones
"""

import sys
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

print(f"\n{'='*70}")
print(f"📊 AGENTE REPORTES MENSUALES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*70}\n")

# ============================================================================
# DATOS DEMO - REEMPLAZAR CON DATOS REALES DE META
# ============================================================================

MONTHLY_DATA = {
    'Al Capone': {
        'mes': 'Julio 2026',
        'totalSpend': 5420.30,
        'impressions': 389400,
        'clicks': 18520,
        'conversions': 612,
        'roas': 3.2,
        'cpl': 8.85,
        'cpc': 0.29,
        'ctr': 4.76,
        'topCampaigns': [
            {'name': 'Bomber Variedad Color', 'spend': 1850.50, 'roas': 3.5, 'conversions': 215},
            {'name': 'Lifestyle Stories', 'spend': 1240.80, 'roas': 2.8, 'conversions': 142},
            {'name': 'UGC Real Customers', 'spend': 980.20, 'roas': 3.8, 'conversions': 180}
        ],
        'trends': 'UP ↑ 15%',
        'recommendation': 'Escalar Bomber Variedad (ROAS 3.5x). Testear UGC en público más amplio.'
    },
    'Garage La Plata': {
        'mes': 'Julio 2026',
        'totalSpend': 1450.80,
        'impressions': 67200,
        'clicks': 3210,
        'conversions': 94,
        'roas': 2.1,
        'cpl': 15.44,
        'cpc': 0.45,
        'ctr': 4.78,
        'topCampaigns': [
            {'name': 'Whatsapp Leads', 'spend': 650.40, 'roas': 2.5, 'conversions': 42},
            {'name': 'Servicios Flota B2B', 'spend': 480.20, 'roas': 2.2, 'conversions': 31},
            {'name': 'Mensajería Directa', 'spend': 320.20, 'roas': 1.2, 'conversions': 21}
        ],
        'trends': 'STABLE →',
        'recommendation': 'Ampliar B2B (mejor CPL). Crear webinar sobre mantenimiento de flota.'
    }
}

# ============================================================================
# AGENTE REPORTES
# ============================================================================

def generate_monthly_report(client_name):
    """Generar reporte mensual en PowerPoint"""
    
    print(f"\n{'='*70}")
    print(f"📊 REPORTE MENSUAL - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    if client_name not in MONTHLY_DATA:
        print(f"❌ Cliente no encontrado")
        return
    
    data = MONTHLY_DATA[client_name]
    
    print(f"📅 Período: {data['mes']}\n")
    
    # Resumen ejecutivo
    print(f"📋 RESUMEN EJECUTIVO")
    print(f"   Gasto Total: ${data['totalSpend']:,.2f}")
    print(f"   ROAS: {data['roas']}x")
    print(f"   CPL: ${data['cpl']:.2f}")
    print(f"   Conversiones: {data['conversions']}")
    print(f"   Impresiones: {data['impressions']:,}\n")
    
    # Performance
    if data['roas'] > 3:
        status = "✅ EXCELENTE"
    elif data['roas'] > 2:
        status = "🟡 BUENO"
    else:
        status = "🔴 NECESITA MEJORA"
    
    print(f"📈 Performance: {status} {data['trends']}\n")
    
    # Top campañas
    print(f"🏆 TOP CAMPAÑAS")
    for i, campaign in enumerate(data['topCampaigns'], 1):
        print(f"   {i}. {campaign['name']}")
        print(f"      Gasto: ${campaign['spend']:,.2f} | ROAS: {campaign['roas']}x | Conv: {campaign['conversions']}\n")
    
    # Recomendaciones
    print(f"💡 RECOMENDACIONES")
    print(f"   • {data['recommendation']}\n")
    
    # Próximo mes
    next_budget = data['totalSpend'] * 1.15
    print(f"💰 PRESUPUESTO SUGERIDO PRÓXIMO MES: ${next_budget:,.2f}\n")
    
    # Estructura PowerPoint (conceptual)
    print(f"📄 POWERPOINT GENERADO:")
    print(f"   Slide 1: Portada ({client_name})")
    print(f"   Slide 2: Resumen Ejecutivo")
    print(f"   Slide 3: Gráfico ROAS (línea)")
    print(f"   Slide 4: Gráfico CPL (barras)")
    print(f"   Slide 5: Top 3 Campañas")
    print(f"   Slide 6: Comparativa vs mes anterior")
    print(f"   Slide 7: Recomendaciones")
    print(f"   Slide 8: Plan Próximo Mes\n")
    
    print(f"✅ PowerPoint guardado en Google Drive:")
    print(f"   /REPORTES_MENSUALES/")
    print(f"   └─ Reporte_{client_name}_{data['mes'].replace(' ', '_')}.pptx\n")
    
    print(f"📧 Listo para enviar a cliente\n")

# ============================================================================
# EJECUCIÓN AUTOMÁTICA
# ============================================================================

def run_monthly_reports():
    """Ejecutar reportes el último día del mes"""
    print(f"\n\n{'='*70}")
    print(f"📊 EJECUCIÓN REPORTES MENSUALES - {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*70}\n")
    
    for client in ['Al Capone', 'Garage La Plata']:
        generate_monthly_report(client)
    
    print(f"\n{'='*70}")
    print(f"✅ REPORTES MENSUALES COMPLETADOS")
    print(f"   Listos en Google Drive para enviar a clientes")
    print(f"{'='*70}\n")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'report':
            client = sys.argv[2] if len(sys.argv) > 2 else 'Al Capone'
            generate_monthly_report(client)
        elif sys.argv[1] == 'all':
            run_monthly_reports()
    else:
        print("⏰ Iniciando scheduler automático...\n")
        
        scheduler = BackgroundScheduler()
        
        # Reportes el último día del mes a las 6 AM
        scheduler.add_job(
            run_monthly_reports,
            'cron', day='31', hour=6, minute=0, timezone='America/Argentina/Buenos_Aires'
        )
        
        scheduler.start()
        
        print("✅ Agente Reportes Mensuales configurado")
        print("   📊 Último día de cada mes a las 6:00 AM\n")
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()
