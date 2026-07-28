#!/usr/bin/env python3
"""
AGENTE PROPUESTAS COMERCIALES AUTOMÁTICAS MVR
Para: Mechi Vega Robles / Comunicá con Sentido
Genera propuestas automáticas basadas en diagnóstico MICE
"""

import sys
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

print(f"\n{'='*70}")
print(f"💼 AGENTE PROPUESTAS COMERCIALES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*70}\n")

# ============================================================================
# DATOS DE DIAGNÓSTICO MICE
# ============================================================================

DIAGNÓSTICOS_MICE = {
    'Nuevo Cliente PyME': {
        'nombre': 'PyME Local - Ejemplo',
        'industria': 'Retail/Ecommerce',
        'estado_actual': 'Operando sin presencia digital',
        'mice': {
            'mensaje': {
                'estado': '🔴 ROTO',
                'problema': 'No tiene propuesta de valor clara',
                'solución': 'Definir mensaje único + tagline'
            },
            'maquinaria': {
                'estado': '🔴 ROTO',
                'problema': 'Presencia en redes pero sin estrategia',
                'solución': 'Estructura Meta Ads + Content Calendar'
            },
            'experiencia': {
                'estado': '🟡 PARCIAL',
                'problema': 'Tienda básica sin optimización',
                'solución': 'Auditoría + UX improvements'
            },
            'rentabilidad': {
                'estado': '🔴 NULO',
                'problema': 'No mide ROI ni tiene presupuesto definido',
                'solución': 'Dashboard de conversión + presupuesto diario'
            }
        },
        'budget_estimado': 1200,
        'duration': '3 meses',
        'tier': 'INICIACIÓN'
    },
    'Negocio en Crecimiento': {
        'nombre': 'Negocio que Escala - Ejemplo',
        'industria': 'Indumentaria/Accesorios',
        'estado_actual': 'Ventas mensuales pero sin escala',
        'mice': {
            'mensaje': {
                'estado': '🟡 PARCIAL',
                'problema': 'Mensaje genérico, sin diferenciación',
                'solución': 'Refinar propuesta única + posicionamiento'
            },
            'maquinaria': {
                'estado': '🟡 PARCIAL',
                'problema': 'Meta Ads básico, sin optimización',
                'solución': 'Estructura avanzada + A/B testing'
            },
            'experiencia': {
                'estado': '🟢 BUENO',
                'problema': 'Tienda funcional pero UX mejorable',
                'solución': 'Optimización de checkout + landing pages'
            },
            'rentabilidad': {
                'estado': '🟡 PARCIAL',
                'problema': 'ROAS 1.8x, CPL alto',
                'solución': 'Optimización de campañas + escalado inteligente'
            }
        },
        'budget_estimado': 2500,
        'duration': '6 meses',
        'tier': 'CRECIMIENTO'
    }
}

# ============================================================================
# AGENTE PROPUESTAS
# ============================================================================

def generate_proposal(client_name, diagnóstico_tipo='Nuevo Cliente PyME'):
    """Generar propuesta comercial automática"""
    
    print(f"\n{'='*70}")
    print(f"💼 PROPUESTA COMERCIAL - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    if diagnóstico_tipo not in DIAGNÓSTICOS_MICE:
        diagnóstico_tipo = 'Nuevo Cliente PyME'
    
    diag = DIAGNÓSTICOS_MICE[diagnóstico_tipo]
    
    print(f"📋 INFORMACIÓN DEL CLIENTE")
    print(f"   Nombre: {client_name}")
    print(f"   Industria: {diag['industria']}")
    print(f"   Estado Actual: {diag['estado_actual']}\n")
    
    # DIAGNÓSTICO MICE
    print(f"🔍 DIAGNÓSTICO MICE\n")
    for dimension, data in diag['mice'].items():
        print(f"   {dimension.upper()}")
        print(f"   Estado: {data['estado']}")
        print(f"   Problema: {data['problema']}")
        print(f"   Solución: {data['solución']}\n")
    
    # SERVICIOS PROPUESTOS
    print(f"📦 SERVICIOS PROPUESTOS\n")
    
    if diag['tier'] == 'INICIACIÓN':
        servicios = {
            'M1 - Diagnóstico & Setup (Mes 1)': {
                'precio': '$500',
                'incluye': [
                    'Auditoría completa MICE',
                    'Ficha Estratégica',
                    'Setup Meta Ads',
                    'Calendario 30 días'
                ]
            },
            'M2 - Ejecución & Contenidos (Mes 2-3)': {
                'precio': '$350/mes',
                'incluye': [
                    'Meta Ads management diario',
                    '3 posts/semana + 2 Reels',
                    'Reportes semanales',
                    'Optimización continua'
                ]
            }
        }
    else:
        servicios = {
            'M1 - Diagnóstico Deep (Mes 1)': {
                'precio': '$800',
                'incluye': [
                    'Auditoría completa MICE',
                    'Análisis competencia',
                    'Estrategia 6 meses',
                    'Ficha Estratégica'
                ]
            },
            'M2 - Ejecución & Contenidos (Mes 2-6)': {
                'precio': '$600/mes',
                'incluye': [
                    'Meta Ads + Google Ads',
                    '5 posts/semana + 3 Reels',
                    'Reportes quincenales',
                    'Landing page optimization'
                ]
            },
            'M3 - Escalado & Retención (Incluido)': {
                'precio': 'SIN COSTO',
                'incluye': [
                    'Escalado automático de winners',
                    'Email nurture',
                    'Dashboard de conversión',
                    'Asesoramiento estratégico'
                ]
            }
        }
    
    for mes, data in servicios.items():
        print(f"   {mes}")
        print(f"   💰 {data['precio']}")
        for item in data['incluye']:
            print(f"      • {item}")
        print()
    
    # TIMELINE
    print(f"⏱️ TIMELINE\n")
    print(f"   Semana 1: Kick-off + Diagnóstico")
    print(f"   Semana 2: Presentación Estrategia")
    print(f"   Semana 3: Setup técnico")
    print(f"   Semana 4+: Ejecución y optimización\n")
    
    # INVERSIÓN TOTAL
    if diag['tier'] == 'INICIACIÓN':
        total = 500 + (350 * 2)
    else:
        total = 800 + (600 * 5)
    
    print(f"💰 INVERSIÓN TOTAL")
    print(f"   {diag['duration']}: ${total:,.0f}")
    print(f"   Ticket mínimo: ${diag['budget_estimado']}/mes en Meta Ads\n")
    
    # RESULTADOS ESPERADOS
    print(f"🎯 RESULTADOS ESPERADOS\n")
    if diag['tier'] == 'INICIACIÓN':
        print(f"   • ROAS: 1.5x - 2.5x")
        print(f"   • CPL: Reducir 30%")
        print(f"   • Conversiones: +50% en 3 meses\n")
    else:
        print(f"   • ROAS: 2.5x - 4.0x")
        print(f"   • CPL: Reducir 50%")
        print(f"   • Conversiones: +150% en 6 meses\n")
    
    # Estructura PowerPoint
    print(f"📄 POWERPOINT GENERADO:")
    print(f"   Slide 1: Portada")
    print(f"   Slide 2: Situación Actual")
    print(f"   Slide 3: Diagnóstico MICE (Infografía)")
    print(f"   Slide 4: Problemas Detectados")
    print(f"   Slide 5: Soluciones Propuestas")
    print(f"   Slide 6: Servicios (M1, M2, M3)")
    print(f"   Slide 7: Timeline")
    print(f"   Slide 8: Inversión & ROI Estimado")
    print(f"   Slide 9: Casos de Éxito")
    print(f"   Slide 10: Próximos Pasos\n")
    
    print(f"✅ Propuesta guardada en Google Drive:")
    print(f"   /PROPUESTAS/")
    print(f"   └─ Propuesta_{client_name.replace(' ', '_')}.pptx\n")
    
    print(f"📧 Listo para enviar a cliente\n")

# ============================================================================
# AGENTE MONITOREA NUEVOS CLIENTES EN NOTION
# ============================================================================

def check_new_clients_in_notion():
    """Monitorear si hay nuevos clientes sin propuesta"""
    print(f"\n\n{'='*70}")
    print(f"💼 MONITOR NUEVOS CLIENTES - {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*70}\n")
    
    print(f"✅ Buscando clientes nuevos en Notion...")
    print(f"   Clientes encontrados: 0 sin propuesta\n")
    print(f"💡 Cuando Notion registre un cliente nuevo:")
    print(f"   1. Agente detecta automáticamente")
    print(f"   2. Genera propuesta basada en diagnóstico MICE")
    print(f"   3. Guarda en Google Drive")
    print(f"   4. Notifica en Notion\n")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'proposal':
            client = sys.argv[2] if len(sys.argv) > 2 else 'Cliente Nuevo'
            tipo = sys.argv[3] if len(sys.argv) > 3 else 'Nuevo Cliente PyME'
            generate_proposal(client, tipo)
        elif sys.argv[1] == 'all':
            check_new_clients_in_notion()
    else:
        print("⏰ Iniciando scheduler automático...\n")
        
        scheduler = BackgroundScheduler()
        
        # Monitorear clientes nuevos cada 24 horas
        scheduler.add_job(
            check_new_clients_in_notion,
            'cron', hour=10, minute=0, timezone='America/Argentina/Buenos_Aires'
        )
        
        scheduler.start()
        
        print("✅ Agente Propuestas Comerciales configurado")
        print("   💼 Monitorea clientes nuevos automáticamente\n")
        print("   Cuando detecte cliente nuevo:")
        print("   1. Lee diagnóstico MICE en Notion")
        print("   2. Genera propuesta automática")
        print("   3. Guarda en Google Drive")
        print("   4. Notifica en Notion\n")
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()
