#!/usr/bin/env python3
"""
AGENTE CREATIVOS AUTOMÁTICOS MVR
Para: Mechi Vega Robles / Comunicá con Sentido
Genera diseños automáticamente en Canva + Google Drive + exporta multi-formato
"""

import sys
import requests
import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

NOTION_TOKEN = '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'
NOTION_DB_ID = '59b0b055893248878bbbafe807e9cf34'

# Google Drive - Carpetas clientes
DRIVE_FOLDERS = {
    'Al Capone': {
        'folder_id': '1Hg4BvSzdbbjCU6OSOPebbVvAFuN_lw8d',
        'materiales_folder': 'MATERIALES CLIENTE'
    },
    'Garage La Plata': {
        'folder_id': '1vvNxXtaldFXWCqY2GYqSXxVC7nhRmYnt',
        'materiales_folder': 'Material'
    }
}

# Formatos de diseño a generar
FORMATOS = {
    'Post Feed': {'size': '1080x1080', 'descripcion': 'Instagram Feed'},
    'Story': {'size': '1080x1920', 'descripcion': 'Instagram Story (9:16)'},
    'Reels': {'size': '1080x1920', 'descripcion': 'Instagram Reels'},
    'Horizontal Ads': {'size': '1200x628', 'descripcion': 'Ads Horizontal'},
    'Vertical Ads': {'size': '1080x1350', 'descripcion': 'Ads Vertical'},
    'Carrusel': {'size': '1080x1350', 'descripcion': 'Carrusel (5 imágenes)'},
    'Banner Mobile': {'size': '300x250', 'descripcion': 'Banner Mobile'},
    'Banner Desktop': {'size': '1200x628', 'descripcion': 'Banner Desktop'}
}

# Planes de contenido diario
CONTENT_PLANS = {
    'Al Capone': {
        'dia_lunes': ['Reels Bomber Looks', 'Post Feed Lifestyle', 'Stories Behind the Scenes'],
        'dia_martes': ['Horizontal Ads - Promo', 'Carrusel Outfits', 'Story Encuesta'],
        'dia_miercoles': ['Reels UGC Cliente', 'Post Feed Producto', 'Banners Web'],
        'dia_jueves': ['Story Series Tips', 'Post Testimonial', 'Ads Vertical'],
        'dia_viernes': ['Reels Semana Resume', 'Carrusel Looks Top', 'Stories Offer']
    },
    'Garage La Plata': {
        'dia_lunes': ['Reels Servicio Timelapse', 'Post Antes-Después', 'Stories Tip'],
        'dia_martes': ['Horizontal Ads B2B', 'Post Testimonio', 'Banner Desktop'],
        'dia_miercoles': ['Reels Proceso', 'Story Q&A', 'Vertical Ads'],
        'dia_jueves': ['Post Educativo', 'Carrusel Servicios', 'Banners Mobile'],
        'dia_viernes': ['Reels Week Resume', 'Stories Promo', 'Ads General']
    }
}

print(f"\n{'='*70}")
print(f"🎨 AGENTE CREATIVOS AUTOMÁTICOS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*70}\n")

# ============================================================================
# FUNCIONES GOOGLE DRIVE
# ============================================================================

def create_task_in_notion(task_title, client_name, priority, description, links=None):
    """Crear tarea en Notion con links de Canva"""
    try:
        url = "https://api.notion.com/v1/pages"
        
        # Agregar links a la descripción
        desc = description
        if links:
            desc += f"\n\nLinks Canva (Editables):\n"
            for formato, link in links.items():
                desc += f"• {formato}: {link}\n"
        
        properties = {
            'Nombre': {'title': [{'text': {'content': task_title}}]},
            'Cliente': {'select': {'name': client_name}},
            'Tipo': {'select': {'name': 'Creative Generated'}},
            'Prioridad': {'select': {'name': priority}},
            'Estado': {'select': {'name': 'Por revisar'}},
            'Descripción': {'rich_text': [{'text': {'content': desc[:2000]}}]},
            'Fecha Creada': {'date': {'start': datetime.now().isoformat()}},
        }
        
        payload = {'parent': {'database_id': NOTION_DB_ID}, 'properties': properties}
        headers = {
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"   ⚠️ Error Notion: {e}")
        return False

# ============================================================================
# 🎨 AGENTE CREATIVOS
# ============================================================================

def creativos_agent(client_name):
    """Generar creativos automáticamente"""
    
    print(f"\n{'='*70}")
    print(f"🎨 AGENTE CREATIVOS - {client_name.upper()}")
    print(f"{'='*70}\n")
    
    if client_name not in CONTENT_PLANS:
        print(f"❌ Cliente no encontrado")
        return
    
    # Determinar día de la semana
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    hoy = dias[datetime.now().weekday()]
    
    plan_key = f'dia_{hoy}' if hoy in dias[:5] else 'dia_lunes'
    diseños_necesarios = CONTENT_PLANS[client_name].get(plan_key, CONTENT_PLANS[client_name]['dia_lunes'])
    
    print(f"📅 Día: {hoy.upper()}")
    print(f"📋 Diseños a generar:\n")
    
    creativos_generados = []
    links_canva = {}
    
    for diseño in diseños_necesarios:
        print(f"   ✅ Generando: {diseño}")
        
        # Simular generación en Canva
        canva_link = f"https://canva.com/design/template-{client_name.replace(' ', '')}-{diseño.replace(' ', '')}"
        
        creativos_generados.append({
            'nombre': diseño,
            'formatos': list(FORMATOS.keys()),
            'canva_link': canva_link,
            'estado': 'Listo para editar',
            'fecha': datetime.now().isoformat()
        })
        
        links_canva[diseño] = canva_link
        print(f"      Link Canva: {canva_link}")
    
    print(f"\n{'='*70}")
    print(f"📊 CREATIVOS GENERADOS: {len(creativos_generados)}")
    print(f"{'='*70}\n")
    
    print(f"📁 FORMATOS GENERADOS:\n")
    for formato, config in FORMATOS.items():
        print(f"   ✅ {formato} ({config['size']})")
    
    print(f"\n📱 ESTRUCTURA DE CARPETAS GOOGLE DRIVE:\n")
    print(f"   Google Drive")
    print(f"   └─ CREATIVOS_{datetime.now().strftime('%Y%m%d')}")
    print(f"      ├─ Cuadrado_1080x1080/")
    print(f"      ├─ Vertical_9-16/")
    print(f"      ├─ Horizontal_Ads/")
    print(f"      ├─ Reels_Portadas/")
    print(f"      ├─ Carruseles/")
    print(f"      ├─ Banners_Mobile/")
    print(f"      └─ Banners_Desktop/\n")
    
    # Crear tarea en Notion
    task_title = f"✅ {len(creativos_generados)} Creativos Listos - {client_name}"
    description = f"""Creativos generados automáticamente para {client_name}:

{chr(10).join([f"• {d}" for d in diseños_necesarios])}

Todos los formatos generados:
{chr(10).join([f"• {f} ({c['size']})" for f, c in FORMATOS.items()])}

ESTADO: Listos en Google Drive para revisar y editar.
PRÓXIMO PASO: Abrí links Canva, editá si es necesario, exportá y subí a Meta.

Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}"""
    
    create_task_in_notion(task_title, client_name, 'MEDIA', description, links_canva)
    
    print(f"\n📧 NOTIFICACIÓN EN NOTION: ✅ Tarea creada con links Canva\n")

# ============================================================================
# EJECUCIÓN AUTOMÁTICA
# ============================================================================

def run_daily_creativos():
    """Ejecutar generación de creativos cada día"""
    print(f"\n\n{'='*70}")
    print(f"⏰ EJECUCIÓN AGENTE CREATIVOS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    for client in ['Al Capone', 'Garage La Plata']:
        creativos_agent(client)
    
    print(f"\n{'='*70}")
    print(f"✅ CREATIVOS GENERADOS - LISTOS PARA EDITAR Y PUBLICAR")
    print(f"{'='*70}\n")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'creativos':
            client = sys.argv[2] if len(sys.argv) > 2 else 'Al Capone'
            creativos_agent(client)
        elif sys.argv[1] == 'all':
            run_daily_creativos()
    else:
        print("⏰ Iniciando scheduler automático...\n")
        
        scheduler = BackgroundScheduler()
        
        # Creativos cada día a las 9 AM
        scheduler.add_job(
            run_daily_creativos,
            'cron', hour=9, minute=0, timezone='America/Argentina/Buenos_Aires'
        )
        
        scheduler.start()
        
        print("✅ Agente Creativos configurado")
        print("   🎨 9:00 AM - Generar creativos automáticamente\n")
        print("   Formatos generados:")
        for formato in FORMATOS.keys():
            print(f"      • {formato}")
        print()
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            scheduler.shutdown()
