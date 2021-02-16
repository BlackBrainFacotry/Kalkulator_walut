import sys
import requests
import requests.exceptions
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import os


def pobierz_dane():

    waluty_xml = requests.get(r"http://www.nbp.pl/kursy/xml/LastA.xml")

    waluty_xml.encoding = "ISO-8859-2"

    waluty_soup = BeautifulSoup(waluty_xml.text, "html.parser")

    data_publikacji = waluty_soup.data_publikacji.string

    dane_walut = {}
    for pozycja in waluty_soup.find_all("pozycja"):
        kod = pozycja.kod_waluty.string
        nazwa = pozycja.nazwa_waluty.string

        przelicznik = int(pozycja.przelicznik.string)

        kurs = float(pozycja.kurs_sredni.string.replace(",", "."))
        dane_walut[kod] = {"nazwa": nazwa, "przelicznik": przelicznik, "kurs": kurs}

    return data_publikacji, dane_walut


def Okno_kody():
    """funkcja tworzaca okno pokazujace oznaczenia """
    window = tk.Tk()
    window.title("Kody walutowe")
    window.configure(bg="#262626")
    window.geometry("400x600")
    label_kody = tk.Label(window, bg="#262626", font=("Helvetica", 10), fg="white")
    label_kody.pack()
    lista_kodow_okno.clear()
    funkcja_kody()
    label_kody.configure(text="\n".join(lista_kodow_okno))


lista_kodow_okno = []


def funkcja_kody():
    """Funkcja parsujaca format na kody"""

    for k in waluty:
        lista_kodow_okno.append("    {}     {}".format(k, waluty[k]["nazwa"]))
    return lista_kodow_okno


lista_kodow = [
    "AUD",
    "BGN",
    "BRL",
    "CAD",
    "CHF",
    "CLP",
    "CNY",
    "CZK",
    "DKK",
    "EUR",
    "GBP",
    "HKD",
    "HRK",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "ISK",
    "JPY",
    "KRW",
    "MXN",
    "MYR",
    "NOK",
    "NZD",
    "PHP",
    "RON",
    "RUB",
    "SEK",
    "SGD",
    "THB",
    "TRY",
    "UAH",
    "USD",
    "XDR",
    "ZAR",
]


def Okno_kursy():
    """fukncja tworzaca okno kody"""
    window_kursy = tk.Tk()
    window_kursy.title("Kursy walut")
    window_kursy.configure(bg="#262626")
    window_kursy.geometry("450x600")
    label_kursy = tk.Label(
        window_kursy, bg="#262626", font=("Helvetica", 10), fg="white"
    )
    label_kursy.pack()
    """lista_kursow_okno2 = funkcja_kursy()"""
    label_kursy.configure(text="\n".join(funkcja_kursy()))


"""lista_kursow_okno = []"""


def funkcja_kursy():
    """Funkcja formatujaca na kursy"""
    lista_kursow_okno=[]
    lista_kursow_okno.clear()
    print(
        "    Kursy średnie walut obcych w złotówkach wedługo NBP.\n"
        "    Data publikacji: {}\n".format(data)
    )

    for k in waluty:
        lista_kursow_okno.append(
            "    {}{:>10} {:35}{:>11}".format(
                k, waluty[k]["przelicznik"], waluty[k]["nazwa"], waluty[k]["kurs"]
            )
        )
    return lista_kursow_okno

def funkcja_data():
    """uzupełnienie daty"""
    lbl_data.configure(text="Data publikacji danych: {}\n".format(data))


def przelicz_na_pln(kod, kwota, tekst=True):

    kurs = waluty[kod]["kurs"]
    przelicznik = waluty[kod]["przelicznik"]
    wynik = (kwota * kurs) / przelicznik
    if tekst:
        print("\t{:.2f} {} --> {:.2f} PLN".format(kwota, kod, wynik))
    return wynik


def przelicz_z_pln(kod, kwota, tekst=True):

    kurs = waluty[kod]["kurs"]
    przelicznik = waluty[kod]["przelicznik"]
    wynik = (przelicznik * kwota) / kurs
    if tekst:
        print("\t{:.2f} PLN --> {:.2f} {}".format(kwota, wynik, kod))
    return wynik


def przelicz_obce(kod1, kod2, kwota, tekst=True):

    # kod1 --> PLN --> kod2:
    wynik = przelicz_z_pln(kod2, przelicz_na_pln(kod1, kwota, tekst=False), tekst=False)
    if tekst:
        print("\t{:.2f} {} --> {:.2f} {}".format(kwota, kod1, wynik, kod2))
    return wynik


def przycisk():
    try:
        kod_AAA = n.get()
        kod_BBB = nn.get()
        kwota_konwertowana = float(kwota_AAA.get())
        przeliczony_wynik = przelicz_obce(kod_AAA, kod_BBB, kwota_konwertowana, True)
        wynik_label.configure(
            text="    {:.2f} {} == {:.2f} {}".format(
                kwota_konwertowana, kod_AAA, przeliczony_wynik, kod_BBB
            ),
            fg="white",
        )
    except Exception as X:
        wynik_label.configure(text="Wprowadz poprawne wartości!", fg="red")


if __name__ == "__main__":
    while True:

        pobrano = False

        # Pobranie aktualnych danych:
        try:
            data, waluty = pobierz_dane()

        # Przechwycenie wszystkich wyjątków związanych z 'requests':
        except requests.exceptions.RequestException:
            wynik_label.configure(text="Error 404!", fg="red")

        # Jeśli brak wyjątków z 'requests':
        else:
            pobrano = True

            break

    root = tk.Tk()
    canvas = tk.Canvas(root, height=400, width=500, bg="#262626")
    canvas.pack()
    lbl = tk.Label(
        canvas, text="KALKULATOR WALUT", fg="red", font=("Helvetica", 28), bg="#262626"
    )
    lbl.place(x=250, y=60, anchor="center")

    lbl_data = tk.Label(canvas, fg="white", font=("Helvetica", 10), bg="#262626")
    funkcja_data()
    lbl_data.place(x=250, y=110, anchor="center")

    n = tk.StringVar()
    walA_choosen = ttk.Combobox(canvas, width=15, textvariable=n)
    # combo box z sktorami walut AAA
    walA_choosen["values"] = lista_kodow
    walA_choosen.place(x=100, y=150)

    nn = tk.StringVar()
    walB_choosen = ttk.Combobox(canvas, width=15, textvariable=nn)
    # combo box z sktorami walut AAA
    walB_choosen["values"] = lista_kodow
    walB_choosen.place(x=295, y=150)

    kwota_AAA = tk.StringVar()
    kwota_AAA_Entered = ttk.Entry(canvas, width=18, textvariable=kwota_AAA)
    kwota_AAA_Entered.place(x=100, y=200)

    button = tk.Button(canvas, text="PRZELICZ", width=15, command=przycisk)
    button.place(x=295, y=200)

    wynik_label = tk.Label(
        canvas, text="", fg="white", font=("Helvetica", 15), bg="#262626"
    )
    wynik_label.place(x=250, y=270, anchor="center")

    button_kody = tk.Button(canvas, width=20, text="KODY", command=Okno_kody)
    button_kody.place(x=250, y=330, anchor="center")

    button_kody = tk.Button(canvas, width=20, text="KURSY", command=Okno_kursy)
    button_kody.place(x=250, y=360, anchor="center")

    root.mainloop()
