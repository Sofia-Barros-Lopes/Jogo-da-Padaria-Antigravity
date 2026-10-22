import urllib.request
import os

base_url = 'https://padariaaromaetrigo.netlify.app/'
assets_dir = r'C:\Users\aluno\.gemini\antigravity\scratch\aroma_e_trigo_game\assets'
os.makedirs(assets_dir, exist_ok=True)

files = [
    'img/logo_aroma_e_trigo.png',
    'img/padariaFrente.jpg',
    'img/croissantQueijo.jpg',
    'img/coxinhaFrango.jpg',
    'img/enroladinhoPresuntoQueijo.jpg',
    'img/empadaPalmito.jpg',
    'img/paoQueijo.jpg',
    'img/esfihaAbertaCarne.jpg',
    'img/kibeRecheado.jpg',
    'img/folhadoFrango.png',
    'img/quicheAlho.png',
    'img/donoutRecheado.jpg',
    'img/sonhoCreme.jpg',
    'img/carolinaDoceLeite.jpg',
    'img/croissantNutella.jpg',
    'img/pudim.png',
    'img/eclairChocolate.jpg'
]

headers = {'User-Agent': 'Mozilla/5.0'}

for f in files:
    filename = os.path.basename(f)
    dest = os.path.join(assets_dir, filename)
    url = base_url + f
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response, open(dest, 'wb') as out_file:
            out_file.write(response.read())
        print(f'Downloaded {filename}: {os.path.getsize(dest)} bytes')
    except Exception as e:
        print(f'Error downloading {f}: {e}')

print('Asset download finished.')
