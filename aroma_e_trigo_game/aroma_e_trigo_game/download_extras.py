import urllib.request
import os

assets_dir = r'C:\Users\aluno\.gemini\antigravity\scratch\aroma_e_trigo_game\assets'

extra_urls = {
    'cafeEspresso.jpg': 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?auto=format&fit=crop&w=400&q=80',
    'cappuccino.jpg': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?auto=format&fit=crop&w=400&q=80',
    'paoFrances.jpg': 'https://images.unsplash.com/photo-1586444248902-2f64eddc13df?auto=format&fit=crop&w=400&q=80',
    'boloChocolate.jpg': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=400&q=80',
    'sucoLaranja.jpg': 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=400&q=80'
}

headers = {'User-Agent': 'Mozilla/5.0'}

for name, url in extra_urls.items():
    dest = os.path.join(assets_dir, name)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response, open(dest, 'wb') as out_file:
            out_file.write(response.read())
        print(f'Downloaded {name}: {os.path.getsize(dest)} bytes')
    except Exception as e:
        print(f'Error downloading {name}: {e}')

print('Extra assets ready.')
