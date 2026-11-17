import re
import tkinter as tk

layar_utama = tk.Tk()
layar_utama.title("Kalkulator")
layar_utama.geometry("350x500")
layar_utama.configure(bg="#369db4")

papan_hitung = ""      
baru_hitung = False    
OPERATOR = "+-x÷"


def tekan_tombol(nilai):
    global papan_hitung, baru_hitung
    nilai = str(nilai)

    if nilai in OPERATOR:
        if papan_hitung == "":
            
            if nilai != "-":
                return
        elif papan_hitung[-1] in OPERATOR:
            
            papan_hitung = papan_hitung[:-1]
            if papan_hitung == "" and nilai != "-":
                return
    elif baru_hitung:
        
        papan_hitung = ""

    baru_hitung = False
    papan_hitung += nilai
    string_tampilan.set(papan_hitung)


def persen():
    global papan_hitung, baru_hitung
    if papan_hitung and papan_hitung[-1] not in OPERATOR:
        papan_hitung += "÷100"
        baru_hitung = False
        string_tampilan.set(papan_hitung)


def ganti_tanda():
    """Balik tanda angka terakhir: 5 -> -5, 5+3 -> 5+(-3)."""
    global papan_hitung, baru_hitung
    cocok_kurung = re.search(r"\(-([\d,]+)\)$", papan_hitung)
    cocok_angka = re.search(r"([\d,]+)$", papan_hitung)
    if cocok_kurung:
        papan_hitung = papan_hitung[:cocok_kurung.start()] + cocok_kurung.group(1)
    elif cocok_angka:
        awal = papan_hitung[:cocok_angka.start()]
        angka = cocok_angka.group(1)
        if awal == "":
            papan_hitung = "-" + angka
        elif awal == "-":
            papan_hitung = angka
        else:
            papan_hitung = awal + "(-" + angka + ")"
    else:
        return
    baru_hitung = False
    string_tampilan.set(papan_hitung)


def hitung():
    global papan_hitung, baru_hitung
    if papan_hitung == "":
        return
    ekspresi = papan_hitung.replace("x", "*").replace("÷", "/").replace(",", ".")
    try:
        if not re.fullmatch(r"[0-9+\-*/(). ]+", ekspresi):
            raise ValueError("karakter tidak valid")
        hasil = eval(ekspresi, {"__builtins__": {}}, {})
        if isinstance(hasil, float):
            if hasil.is_integer():
                hasil = int(hasil)
            else:
                hasil = format(hasil, ".10g")
        papan_hitung = str(hasil).replace(".", ",")
        baru_hitung = True
        string_tampilan.set(papan_hitung)
    except Exception:
        string_tampilan.set("Error")
        papan_hitung = ""
        baru_hitung = False


def hapus_semua():
    global papan_hitung, baru_hitung
    papan_hitung = ""
    baru_hitung = False
    string_tampilan.set("")


string_tampilan = tk.StringVar()
layar = tk.Entry(
    layar_utama,
    textvariable=string_tampilan,
    font=("Helvetica", 36),
    bd=0,
    state="readonly",
    readonlybackground="#fafefa",
    fg="black",
    justify="right",
)
layar.pack(fill="both", ipadx=10, ipady=30, padx=10, pady=10)

frame_tombol = tk.Frame(layar_utama, bg="#f6fbf7")
frame_tombol.pack(fill="both", expand=True, padx=10, pady=10)

for i in range(5):
    frame_tombol.rowconfigure(i, weight=1)
for i in range(4):
    frame_tombol.columnconfigure(i, weight=1)

abu_terang = "#a5a5a5"
gelap = "#333333"
oranye = "#ff9f0a"

tombol_config = [
    ("C", 0, 0, abu_terang, "black", hapus_semua),
    ("+/-", 0, 1, abu_terang, "black", ganti_tanda),
    ("%", 0, 2, abu_terang, "black", persen),
    ("÷", 0, 3, oranye, "white", lambda: tekan_tombol("÷")),
    ("1", 1, 0, gelap, "white", lambda: tekan_tombol("1")),
    ("2", 1, 1, gelap, "white", lambda: tekan_tombol("2")),
    ("3", 1, 2, gelap, "white", lambda: tekan_tombol("3")),
    ("x", 1, 3, oranye, "white", lambda: tekan_tombol("x")),
    ("4", 2, 0, gelap, "white", lambda: tekan_tombol("4")),
    ("5", 2, 1, gelap, "white", lambda: tekan_tombol("5")),
    ("6", 2, 2, gelap, "white", lambda: tekan_tombol("6")),
    ("-", 2, 3, oranye, "white", lambda: tekan_tombol("-")),
    ("7", 3, 0, gelap, "white", lambda: tekan_tombol("7")),
    ("8", 3, 1, gelap, "white", lambda: tekan_tombol("8")),
    ("9", 3, 2, gelap, "white", lambda: tekan_tombol("9")),
    ("+", 3, 3, oranye, "white", lambda: tekan_tombol("+")),
    (",", 4, 2, gelap, "white", lambda: tekan_tombol(",")),
    ("=", 4, 3, oranye, "white", hitung),
]

for teks, r, c, bg_color, fg_color, aksi in tombol_config:
    btn = tk.Button(
        frame_tombol, text=teks, font=("Helvetica", 18, "bold"),
        bg=bg_color, fg=fg_color, bd=0, relief="flat", command=aksi,
    )
    btn.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)


btn_nol = tk.Button(
    frame_tombol, text="0", font=("Helvetica", 18, "bold"),
    bg=gelap, fg="white", bd=0, relief="flat",
    command=lambda: tekan_tombol("0"),
)
btn_nol.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

layar_utama.mainloop()
