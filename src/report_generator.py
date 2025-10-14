"""
HTML dashboard generálás JSON riportból
"""
import json
from datetime import datetime
from jinja2 import Template
import os
import glob


def load_json_report(filepath):
    """JSON riport betöltése"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_dashboard(json_filepath, output_filepath=None):
    """
    Dashboard generálás Jinja2 sablonnal
    
    Args:
        json_filepath: pytest JSON riport fájl útvonala
        output_filepath: Kimeneti HTML fájl útvonala (opcionális, automatikus timestamp)
    """
    # JSON betöltése
    report_data = load_json_report(json_filepath)
    
    # Statisztikák kiszámítása
    summary = report_data.get('summary', {})
    tests = report_data.get('tests', [])
    
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    skipped = summary.get('skipped', 0)
    total = summary.get('total', 0)
    duration = summary.get('duration', 0)
    
    # Összes teszt futási idejének számítása
    total_test_duration = sum(
        test.get('call', {}).get('duration', 0) 
        for test in tests
    )
    
    # Sikeres arány számítás
    success_rate = (passed / total * 100) if total > 0 else 0
    
    # Teszt részletek feldolgozása
    test_details = []
    for test in tests:
        test_details.append({
            'name': test.get('nodeid', 'Unknown'),
            'outcome': test.get('outcome', 'unknown'),
            'duration': round(test.get('call', {}).get('duration', 0), 3),
            'error': test.get('call', {}).get('longrepr', '') if test.get('outcome') == 'failed' else ''
        })
    
    # Automatikus fájlnév időbélyeggel
    if output_filepath is None:
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = 'dashboard'
        os.makedirs(output_dir, exist_ok=True)
        output_filepath = f'{output_dir}/dashboard_{timestamp_str}.html'
    
    # HTML sablon
    html_template = """
    <!DOCTYPE html>
    <html lang="hu">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Test Dashboard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                min-height: 100vh;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                padding: 30px;
                background: #f8f9fa;
            }
            
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
            }
            
            .stat-card .number {
                font-size: 3em;
                font-weight: bold;
                margin: 10px 0;
            }
            
            .stat-card .label {
                color: #666;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .passed .number { color: #28a745; }
            .failed .number { color: #dc3545; }
            .skipped .number { color: #ffc107; }
            .total .number { color: #667eea; }
            .duration .number { font-size: 2em; }
            .success-rate .number { color: #17a2b8; }
            
            .tests-section {
                padding: 30px;
            }
            
            .tests-section h2 {
                color: #333;
                margin-bottom: 20px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            
            .test-item {
                background: #f8f9fa;
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 8px;
                border-left: 5px solid #ddd;
                transition: all 0.3s ease;
            }
            
            .test-item:hover {
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .test-item.passed {
                border-left-color: #28a745;
                background: #d4edda;
            }
            
            .test-item.failed {
                border-left-color: #dc3545;
                background: #f8d7da;
            }
            
            .test-item.skipped {
                border-left-color: #ffc107;
                background: #fff3cd;
            }
            
            .test-name {
                font-weight: bold;
                color: #333;
                margin-bottom: 5px;
            }
            
            .test-meta {
                font-size: 0.9em;
                color: #666;
            }
            
            .test-error {
                margin-top: 10px;
                padding: 10px;
                background: white;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 0.85em;
                color: #721c24;
                white-space: pre-wrap;
                max-height: 200px;
                overflow-y: auto;
            }
            
            .badge {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: bold;
                text-transform: uppercase;
            }
            
            .badge.passed { background: #28a745; color: white; }
            .badge.failed { background: #dc3545; color: white; }
            .badge.skipped { background: #ffc107; color: #333; }
            
            .footer {
                background: #333;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 0.9em;
            }
            
            .progress-bar {
                width: 100%;
                height: 30px;
                background: #e9ecef;
                border-radius: 15px;
                overflow: hidden;
                margin: 20px 0;
            }
            
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                transition: width 1s ease;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧪 API Test Dashboard</h1>
                <p>TMDB API Automatizált Tesztelés</p>
                <p style="font-size: 0.9em; margin-top: 10px;">Generálva: {{ timestamp }}</p>
            </div>
            
            <div class="stats">
                <div class="stat-card total">
                    <div class="label">Összes teszt</div>
                    <div class="number">{{ total }}</div>
                </div>
                <div class="stat-card passed">
                    <div class="label">Sikeres</div>
                    <div class="number">{{ passed }}</div>
                </div>
                <div class="stat-card failed">
                    <div class="label">Sikertelen</div>
                    <div class="number">{{ failed }}</div>
                </div>
                <div class="stat-card skipped">
                    <div class="label">Kihagyott</div>
                    <div class="number">{{ skipped }}</div>
                </div>
                <div class="stat-card duration">
                    <div class="label">Futási idő</div>
                    <div class="number">{{ duration }}s</div>
                </div>
                <div class="stat-card success-rate">
                    <div class="label">Sikerességi arány</div>
                    <div class="number">{{ success_rate }}%</div>
                </div>
            </div>
            
            <div style="padding: 0 30px;">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ success_rate }}%">
                        {{ success_rate }}% Sikeres
                    </div>
                </div>
            </div>
            
            <div class="tests-section">
                <h2>📋 Teszt Részletek</h2>
                {% for test in tests %}
                <div class="test-item {{ test.outcome }}">
                    <div class="test-name">
                        <span class="badge {{ test.outcome }}">{{ test.outcome }}</span>
                        {{ test.name }}
                    </div>
                    <div class="test-meta">
                        ⏱️ Futási idő: {{ test.duration }}s
                    </div>
                    {% if test.error %}
                    <div class="test-error">{{ test.error }}</div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            
            <div class="footer">
                <p>Automatizált API Tesztelés</p>
                <p>Python + pytest + TMDB API</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Sablon renderelése
    template = Template(html_template)
    html_output = template.render(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        total=total,
        passed=passed,
        failed=failed,
        skipped=skipped,
        duration=round(total_test_duration, 2),  # összes teszt futási ideje
        success_rate=round(success_rate, 1),
        tests=test_details
    )
    
    # HTML fájl mentése
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"✅ Dashboard sikeresen generálva: {output_filepath}")
    print(f"📊 Statisztika: {passed}/{total} sikeres teszt ({success_rate:.1f}%)")
    print(f"⏱️  Összes futási idő: {round(total_test_duration, 2)}s")


def find_latest_json_report(reports_dir='reports'):
    """
    Megtalálja a legutolsó JSON riport fájlt a megadott mappában
    
    Args:
        reports_dir: A reports mappa útvonala
    
    Returns:
        A legutolsó JSON fájl útvonala, vagy None ha nincs
    """
    import glob
    
    # Összes JSON fájl keresése
    json_files = glob.glob(f'{reports_dir}/report*.json')
    
    if not json_files:
        return None
    
    # Legutolsó fájl (módosítási idő alapján)
    latest_file = max(json_files, key=os.path.getmtime)
    return latest_file


if __name__ == "__main__":
    # Automatikus JSON fájl keresés
    json_file = find_latest_json_report('reports')
    
    if json_file:
        print(f"📄 Legutolsó JSON riport: {json_file}")
        generate_dashboard(
            json_filepath=json_file
            # output_filepath automatikusan generálódik időbélyeggel
        )
    else:
        print("⚠️ Nem található JSON riport a reports/ mappában!")
        print("   Futtasd először a teszteket: python run_tests.py")