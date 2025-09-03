import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, render_template
import pandas as pd
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    graph = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            df = pd.read_excel(file)

            if df.shape[1] >= 2:
                x = df.iloc[:, 0]
                y = df.iloc[:, 1]

                plt.figure()
                plt.plot(x, y, marker='o')
                plt.title("Graph from Excel")
                plt.xlabel(df.columns[0])
                plt.ylabel(df.columns[1])

                # Save to BytesIO
                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                graph = base64.b64encode(img.getvalue()).decode()

                plt.close()

    return render_template('index.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
