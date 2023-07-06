import base64
import io

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def image_to_text(image):
    # Converte a imagem para escala de cinza
    image = image.convert('L')

    # Utiliza a biblioteca Tesseract OCR para extrair o texto da imagem
    text = pytesseract.image_to_string(image)

    return text


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Extrator de textos de imagens - feito em python | by: tondevpy'),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Arraste e solte ou selecione uma imagem:',
            html.Br(),
        ]),
        style={
            'width': '300px',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='output-text')
])


@app.callback(Output('output-text', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'))
def extract_text(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        image = Image.open(io.BytesIO(base64.b64decode(content_string)))
        text = image_to_text(image)
        return html.Div([
            html.H3(f'Arquivo: {filename}'),
            html.H4('Texto extraído:'),
            html.Pre(text),
            html.Img(src=contents, style={'max-width': '500px', 'margin-top': '10px'})
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
