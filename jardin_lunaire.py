"""Jardin lunaire - version Python du site.
© 2026 ᚛ᚏᚐᚉᚔᚅᚓ᚜ ᚛ᚚᚐᚄᚉᚐᚂ᚜ — Tous droits réservés.

Lancer :  python jardin_lunaire.py
Le bouton « Créer l'application Windows (.exe) » construit JardinLunaire.exe
(dossier dist/) avec PyInstaller. Les fichiers mp4 et mp3 placés à côté du
script ou de l'exe sont lus directement (son seul).
"""
import json, mimetypes, os, subprocess, sys, threading, urllib.request, urllib.error, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote, unquote, urlparse

mimetypes.add_type("application/manifest+json", ".webmanifest")
PORT = 8765  # port fixe : les notes et le plan restent enregistrés d'une session à l'autre
FROZEN = getattr(sys, "frozen", False)
ASSETS = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.dirname(sys.executable) if FROZEN else os.path.dirname(os.path.abspath(__file__))
EXT = (".mp4", ".m4a", ".mp3", ".ogg", ".wav")


def pistes():
    return [quote(f) for f in sorted(os.listdir(HOME)) if f.lower().endswith(EXT)]


def ecrire_playlist():
    """Écrit playlist.js à côté du site pour que index.html (double-clic) trouve aussi les sons."""
    try:
        with open(os.path.join(HOME, "playlist.js"), "w", encoding="utf-8") as fh:
            fh.write("window.MUSE=%s;" % json.dumps(pistes()))
    except OSError:
        pass


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        p = unquote(urlparse(self.path).path)
        if p == "/playlist.js":
            return self.envoyer(("window.MUSE=%s;" % json.dumps(pistes())).encode(), "text/javascript")
        nom = os.path.basename(p) or "index.html"
        f = os.path.join(HOME if nom.lower().endswith(EXT) or nom == "playlist.js" else ASSETS, nom)
        if not os.path.isfile(f):
            self.send_error(404)
            return
        taille = os.path.getsize(f)
        a, b, code = 0, taille - 1, 200
        r = self.headers.get("Range", "")
        if r.startswith("bytes="):
            d, _, e = r[6:].partition("-")
            a = int(d) if d else 0
            b = int(e) if e else taille - 1
            code = 206
        self.send_response(code)
        self.send_header("Content-Type", mimetypes.guess_type(f)[0] or "application/octet-stream")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(b - a + 1))
        if code == 206:
            self.send_header("Content-Range", "bytes %d-%d/%d" % (a, b, taille))
        self.end_headers()
        try:
            with open(f, "rb") as fh:
                fh.seek(a)
                restant = b - a + 1
                while restant > 0:
                    bloc = fh.read(min(65536, restant))
                    if not bloc:
                        break
                    self.wfile.write(bloc)
                    restant -= len(bloc)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_POST(self):
        """Relais vers l'API Pl@ntNet (évite les blocages du navigateur)."""
        u = urlparse(self.path)
        if not u.path.startswith("/api/"):
            self.send_error(404)
            return
        corps = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        url = "https://my-api.plantnet.org/v2/" + u.path[5:] + ("?" + u.query if u.query else "")
        req = urllib.request.Request(url, data=corps, headers={"Content-Type": self.headers.get("Content-Type", "")})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                code, data = r.status, r.read()
        except urllib.error.HTTPError as e:
            code, data = e.code, e.read()
        except Exception as e:
            code, data = 502, json.dumps({"message": str(e)}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def envoyer(self, data, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def demarrer_serveur():
    ecrire_playlist()
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        return  # déjà lancé
    threading.Thread(target=srv.serve_forever, daemon=True).start()


def ouvrir_site():
    demarrer_serveur()
    webbrowser.open("http://127.0.0.1:%d/" % PORT)


def creer_exe(log, fin):
    def travail():
        try:
            try:
                import PyInstaller  # noqa: F401
            except ImportError:
                log("Installation de PyInstaller…")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            sep = ";" if os.name == "nt" else ":"
            script = os.path.abspath(__file__)
            cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--windowed",
                   "--name", "JardinLunaire",
                   "--add-data", os.path.join(ASSETS, "index.html") + sep + ".",
                   "--add-data", os.path.join(ASSETS, "poster.jpg") + sep + ".",
                   "--add-data", os.path.join(ASSETS, "manifest.webmanifest") + sep + ".",
                   "--add-data", os.path.join(ASSETS, "sw.js") + sep + ".",
                   "--add-data", os.path.join(ASSETS, "icon-192.png") + sep + ".",
                   "--add-data", os.path.join(ASSETS, "icon-512.png") + sep + ".",
                   "--add-data", os.path.join(ASSETS, "icon-maskable-512.png") + sep + ".",
                   "--add-data", os.path.join(ASSETS, "apple-touch-icon.png") + sep + ".", script]
            log("Création de l'application, patientez quelques minutes…")
            proc = subprocess.Popen(cmd, cwd=HOME, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for ligne in proc.stdout:
                log(ligne.rstrip())
            proc.wait()
            if proc.returncode == 0:
                dist = os.path.join(HOME, "dist")
                log("Terminé : %s" % os.path.join(dist, "JardinLunaire.exe"))
                log("Placez vos mp4 et mp3 à côté de l'exe.")
                if os.name == "nt":
                    os.startfile(dist)
            else:
                log("Échec de la création (voir les messages ci-dessus).")
        except Exception as e:
            log("Erreur : %s" % e)
        finally:
            fin()
    threading.Thread(target=travail, daemon=True).start()


def fenetre():
    import tkinter as tk
    from tkinter import scrolledtext
    w = tk.Tk()
    w.title("Jardin lunaire")
    w.configure(bg="#123c40", padx=16, pady=16)
    tk.Label(w, text="Jardin lunaire", font=("Georgia", 22, "italic"), fg="#c9a45c", bg="#123c40").pack()
    tk.Label(w, text="© 2026 ᚛ᚏᚐᚉᚔᚅᚓ᚜ ᚛ᚚᚐᚄᚉᚐᚂ᚜ — Tous droits réservés", font=("Segoe UI Symbol", 9), fg="#c9a45c", bg="#123c40").pack(side="bottom", pady=(8, 0))
    tk.Button(w, text="Ouvrir le jardin lunaire", font=("Georgia", 13), bg="#e0654e", fg="white",
              command=ouvrir_site).pack(fill="x", pady=8)
    journal = scrolledtext.ScrolledText(w, height=10, width=70, bg="#0b2a2d", fg="#f3efe6")
    journal.pack()

    def log(t):
        w.after(0, lambda: (journal.insert("end", t + "\n"), journal.see("end")))

    bouton = tk.Button(w, text="Créer l'application Windows (.exe)", font=("Georgia", 12))
    bouton.pack(fill="x", pady=8)

    def lancer():
        bouton.config(state="disabled")
        creer_exe(log, lambda: w.after(0, lambda: bouton.config(state="normal")))

    if FROZEN:
        bouton.config(state="disabled", text="Application déjà installée")
    else:
        bouton.config(command=lancer)
    demarrer_serveur()
    if FROZEN:
        ouvrir_site()
    w.mainloop()


if __name__ == "__main__":
    fenetre()
