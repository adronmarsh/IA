import os
from datetime import datetime
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def parse_date_from_filename(filename):
    date_str = filename[len('productosJD'):-len('.csv')]
    return datetime.strptime(date_str, '%Y%m%d%H%M%S')

def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def generate_data_and_graph(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.startswith('productosJD') and f.endswith('.csv')]
    
    if not csv_files:
        return "No se encontraron archivos CSV en la carpeta.", None

    dates = sorted(parse_date_from_filename(f) for f in csv_files)
    line_counts = [count_lines_in_file(os.path.join(folder_path, f)) for f in csv_files]

    # Crear gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(dates, line_counts, marker='o')
    plt.xlabel('Fecha')
    plt.ylabel('Número de líneas')
    plt.title('Número de líneas por archivo a lo largo del tiempo')
    plt.xticks(rotation=45)  # Rotar las etiquetas de las fechas para mejor lectura

    # Guardar gráfica como imagen base64
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    first_date = dates[0].strftime('%Y-%m-%d %H:%M:%S')
    last_date = dates[-1].strftime('%Y-%m-%d %H:%M:%S')
    total_files = len(csv_files)

    report = f"Fecha del primer CSV: {first_date}\nFecha del último CSV: {last_date}\nTotal de CSV: {total_files}"

    return report, graph_url

# Generar reporte y gráfica
folder_path = 'results'
report, graph_url = generate_data_and_graph(folder_path)

# Reemplazar saltos de línea para HTML
report_html = report.replace('\n', '<br>')

# Crear HTML
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Reporte de Archivos CSV</title>
        <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }}
        .container {{
            width: 80%;
            margin: auto;
            overflow: hidden;
        }}
        header {{
            background: #333;
            color: #fff;
            padding-top: 30px;
            min-height: 70px;
            border-bottom: #bbb 1px solid;
        }}
        header a {{
            color: #fff;
            text-decoration: none;
            text-transform: uppercase;
            font-size: 16px;
        }}
        header ul {{
            padding: 0;
            margin: 0;
            list-style: none;
            overflow: hidden;
        }}
        header li {{
            float: left;
            display: inline;
            padding: 0 20px 0 20px;
        }}
        header #branding {{
            float: left;
        }}
        header #branding h1 {{
            margin: 0;
        }}
        header nav {{
            float: right;
            margin-top: 10px;
        }}
        header .highlight, header .current a {{
            color: #e8491d;
            font-weight: bold;
        }}
        header a:hover {{
            color: #ffffff;
            font-weight: bold;
        }}
        .button {{
            display: inline-block;
            text-decoration: none;
            color: #fff;
            background: #333;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }}
        .button:hover {{
            background: #e8491d;
        }}
        #graph-container {{
            display: none;
            text-align: center;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div id="branding">
                <h1><span class="highlight">JD</span> Reporte de Prodcutos</h1>
            </div>
            <nav>
                <ul>
                    <li><a href="javascript:void(0)" onclick="toggleGraph()">Mostrar/Ocultar Gráfica</a></li>
                </ul>
            </nav>
        </div>
    </header>


    <div class="container">
        <h2>Reporte</h2>
        <p>{report_html}</p>
        <button class="button" onclick="toggleGraph()">Mostrar/Ocultar Gráfica</button>
        <div id="graph-container">
            <img src="data:image/png;base64,{graph_url}" alt="Gráfica de líneas">
        </div>
    </div>

    <script>
        function toggleGraph() {{
            var graphContainer = document.getElementById("graph-container");
            if (graphContainer.style.display === "none") {{
                graphContainer.style.display = "block";
            }} else {{
                graphContainer.style.display = "none";
            }}
        }}
    </script>
</body>
</html>
"""

# Guardar HTML en un archivo
with open("reporte.html", "w", encoding='utf-8') as html_file:
    html_file.write(html_content)