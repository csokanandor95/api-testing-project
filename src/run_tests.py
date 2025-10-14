"""
Automatizált API tesztfuttatás és riportálás
"""
import subprocess
import os
import sys
from datetime import datetime
from report_generator import generate_dashboard

def print_header():
    """Fejléc kiírása"""
    print("\n" + "="*60)
    print("🧪 API TESZTELÉSI KERETRENDSZER")
    print("TMDB API Automatizált Tesztelés")
    print("="*60 + "\n")

def run_tests_with_reports():
    """
    Tesztek futtatása és riportok generálása
    
    Lépések:
    1. pytest futtatás JSON és HTML riporttal
    2. Egyedi dashboard generálás
    3. Eredmények összegzése
    """
    
    print_header()
    
    # Mappák létrehozása (projekt gyökérben)
    os.makedirs('../reports', exist_ok=True)
    os.makedirs('../dashboard', exist_ok=True)
    
    # Időbélyeg a riportokhoz
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Fájlnevek (relatív útvonal a projekt gyökérhez)
    json_report = f'../reports/report_{timestamp}.json'
    html_report = f'../reports/report_{timestamp}.html'
    
    print(f"📅 Futtatás időpontja: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 JSON riport: {json_report}")
    print(f"📁 HTML riport: {html_report}")
    print("\n" + "-"*60 + "\n")
    
    # ========== PYTEST FUTTATÁS ==========
    print("🚀 Tesztek futtatása...\n")
    
    result = subprocess.run([
        'pytest',
        'test_cases.py',
        '-v',
        '--json-report',
        f'--json-report-file={json_report}',
        '--html=' + html_report,
        '--self-contained-html'
    ], capture_output=False)
    
    print("\n" + "-"*60 + "\n")
    
    # ========== EREDMÉNY ELLENŐRZÉS ==========
    if not os.path.exists(json_report):
        print("❌ HIBA: JSON riport nem jött létre!")
        print("   Ellenőrizd, hogy a pytest-json-report telepítve van.")
        return 1
    
    # ========== DASHBOARD GENERÁLÁS ==========
    print("📊 Egyedi dashboard generálása...\n")
    
    try:
        generate_dashboard(
            json_filepath=json_report,
            output_filepath=None  # Automatikus időbélyeges név, de ../dashboard/ mappába
        )
    except Exception as e:
        print(f"❌ HIBA a dashboard generálás során: {e}")
        return 1
    
    # ========== ÖSSZEGZÉS ==========
    print("\n" + "="*60)
    print("📋 TESZTFUTÁS BEFEJEZVE")
    print("="*60)
    
    if result.returncode == 0:
        print("\n✅ Minden teszt sikeresen lefutott.")
    else:
        print("\n⚠️  Néhány teszt elbukott vagy hibaüzenet történt.")
    
    print("\n📄 Generált riportok:")
    print(f"   • pytest HTML: {html_report}")
    print(f"   • Egyedi dashboard: dashboard/dashboard_{timestamp}.html")
    print(f"   • JSON adat: {json_report}")
    
    print("\nA részletes tesztriportok a böngészőben megtekinthetőek.")
    print("="*60 + "\n")
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests_with_reports()
    sys.exit(exit_code)