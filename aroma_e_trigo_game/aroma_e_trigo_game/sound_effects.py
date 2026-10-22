"""
Efeitos Sonoros Otimizados - Padaria Aroma & Trigo
Utiliza fila única em thread dedicada em segundo plano (Zero lag e sem criar threads por frame)
"""
import sys
import queue
import threading

SOUND_ENABLED = True
_sound_queue = queue.Queue(maxsize=3)

def is_windows():
    return sys.platform.startswith("win")

def _sound_worker():
    while True:
        try:
            tones = _sound_queue.get(timeout=1.0)
            if tones is None:
                break
            if SOUND_ENABLED and is_windows():
                try:
                    import winsound
                    for freq, dur in tones:
                        winsound.Beep(int(freq), int(dur))
                except Exception:
                    pass
            _sound_queue.task_done()
        except queue.Empty:
            continue
        except Exception:
            pass

# Inicia thread única persistente
_worker = threading.Thread(target=_sound_worker, daemon=True)
_worker.start()

def _queue_tones(tone_list):
    if not SOUND_ENABLED or not is_windows():
        return
    try:
        # Descarta se a fila estiver cheia para evitar acúmulo de latência
        _sound_queue.put_nowait(tone_list)
    except queue.Full:
        pass

def play_pickup():
    """Som ao pegar um item ou adicionar ao carrinho"""
    _queue_tones([(880, 50), (1318, 70)])

def play_remove():
    """Som ao remover um item do carrinho"""
    _queue_tones([(659, 50), (440, 60)])

def play_step():
    """Passo silencioso para evitar travamento de áudio"""
    pass

def play_checkout():
    """Som do caixa registradora ao finalizar a compra"""
    _queue_tones([(587, 60), (784, 60), (1174, 120), (1568, 160)])

def play_victory():
    """Fanfarra de missão cumprida"""
    _queue_tones([(523, 80), (659, 80), (784, 100), (1046, 220)])

def play_interact():
    """Som ao abrir vitrine ou conversar"""
    _queue_tones([(700, 40), (950, 50)])

def toggle_sound():
    global SOUND_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED
    # Se desativou, limpa a fila
    while not _sound_queue.empty():
        try:
            _sound_queue.get_nowait()
            _sound_queue.task_done()
        except Exception:
            break
    return SOUND_ENABLED
