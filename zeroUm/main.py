import customtkinter
import tkinter
import musica
import webbrowser
from PIL import Image

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("800x600")
root.title("Zero Um - Recomendador de Músicas")
root.resizable(False, False)
root.iconbitmap("images/zeroum_icon.ico")

imgYoutube = Image.open("images/youtube_logo_icon.png")
imgBtn = customtkinter.CTkImage(light_image=imgYoutube, dark_image=imgYoutube, size=(65, 15))
logo = Image.open("images/zeroum_logo.png")
imgLogo = customtkinter.CTkImage(light_image=logo, dark_image=logo, size=(150, 46))

def abrirLink(url):
    webbrowser.open_new_tab(url)


def procMusica():
    dfProcMusicas = musica.procurarMusica(str(etrMusica.get()))
    lstLista.delete(0, "end")

    if dfProcMusicas.shape[0] == 0:
        frmLst.pack_forget()
        frmBottom.pack_forget()
        lblErro.pack(pady=10, padx=10)
    else:
        lblErro.pack_forget()
        frmLst.pack(pady=10, padx=10, fill="both", expand=True)
        frmBottom.pack(pady=10, padx=10, fill="both", expand=True)
        cont = 0
        for i, item in dfProcMusicas.iterrows():
            cont += 1
            lstLista.insert(cont, str(i) + ". " + item['track_name'] + " - por " + item['artists'])


def crtMsgBox(index):
    msc = musica.procurarMusicaIndice(index)

    global msgbox
    msgbox = customtkinter.CTkToplevel(master=jnlRec)
    msgbox.geometry("400x360")
    msgbox.resizable(False, False)
    msgbox.title("Atributos da música " + msc['track_name'])
    msgbox.grab_set()

    frmAtr1 = customtkinter.CTkFrame(master=msgbox)
    frmAtr1.pack(side="top", pady=5, padx=5, fill="both")
    frmAtr2 = customtkinter.CTkFrame(master=msgbox)
    frmAtr2.pack(side="left", pady=5, padx=5, fill="both", expand=True)

    customtkinter.CTkLabel(master=frmAtr1, text="Música: " + msc['track_name'], font=("Arial", 15)).pack(anchor="w", padx=10)
    customtkinter.CTkLabel(master=frmAtr1, text="Artista: " + msc['artists'], font=("Arial", 15)).pack(anchor="w", padx=10)
    customtkinter.CTkLabel(master=frmAtr1, text="Àlbum: " + msc['album_name'], font=("Arial", 15)).pack(anchor="w", padx=10)
    customtkinter.CTkLabel(master=frmAtr1, text="Gênero: " + msc['track_genre'], font=("Arial", 15)).pack(anchor="w", padx=10)

    customtkinter.CTkLabel(master=frmAtr2, text="Popularidade: " + str(msc['popularity']), font=("Arial", 12)).pack(anchor="w", padx=10)
    customtkinter.CTkLabel(master=frmAtr2, text="Acústica: " + str(msc['acousticness']), font=("Arial", 12)).pack(anchor="w", padx=10)
    customtkinter.CTkLabel(master=frmAtr2, text="Dançabilidade: " + str(msc['danceability']), font=("Arial", 12)).pack(anchor="w", padx=10)
    customtkinter.CTkLabel(master=frmAtr2, text="Energia: " + str(msc['energy']), font=("Arial", 12)).pack(anchor="w", padx=10)
    customtkinter.CTkLabel(master=frmAtr2, text="Instrumentalidade: " + str(msc['instrumentalness']), font=("Arial", 12)).pack(anchor="w", padx=10)
    customtkinter.CTkLabel(master=frmAtr2, text="Vivacidade: " + str(msc['liveness']), font=("Arial", 12)).pack(anchor="w", padx=10)
    customtkinter.CTkLabel(master=frmAtr2, text="Fala: " + str(msc['speechiness']), font=("Arial", 12)).pack(anchor="w", padx=10)
    customtkinter.CTkLabel(master=frmAtr2, text="Valência: " + str(msc['valence']), font=("Arial", 12)).pack(anchor="w", padx=10)


def escMusica():
    esc = lstLista.get(lstLista.curselection())
    escSplit = esc.split(". ")
    iMscEsc = int(escSplit[0])
    dfMscEsc = musica.procurarMusicaIndice(iMscEsc)

    global jnlRec
    jnlRec = customtkinter.CTkToplevel(master=root)
    jnlRec.geometry("800x470")
    jnlRec.resizable(True, False)
    jnlRec.title("Músicas recomedadas com base em " + dfMscEsc['track_name'])
    jnlRec.grab_set()

    frmMscEsc = customtkinter.CTkFrame(master=jnlRec)
    frmMscEsc.pack(pady=5, padx=10, fill="both")

    lblMsc1 = customtkinter.CTkLabel(master=frmMscEsc, text=dfMscEsc['track_name'], font=("Arial", 15))
    lblMsc1.pack(side="left", pady=5, padx=10)
    lblMsc2 = customtkinter.CTkLabel(master=frmMscEsc, text=dfMscEsc['artists'], font=("Arial", 10))
    lblMsc2.pack(side="left", padx=10)
    linkEsc = musica.youtubeSearchVideo(dfMscEsc['track_name'] + " " + dfMscEsc['artists'])['url']
    btAtr = customtkinter.CTkButton(master=frmMscEsc, text="...", command=lambda: crtMsgBox(iMscEsc))
    btAtr.pack(side="right", pady=5, padx=10)
    btYt = customtkinter.CTkButton(master=frmMscEsc, text="", image=imgBtn, command=lambda: abrirLink(linkEsc))
    btYt.pack(side="right", pady=5, padx=2)

    titulo2 = "Músicas recomendadas de " + dfMscEsc['track_genre'] + " baseado em " + dfMscEsc['track_name']
    lblTitulo2 = customtkinter.CTkLabel(master=jnlRec, text=titulo2, font=("Arial", 13))
    lblTitulo2.pack(pady=5, padx=10, fill="both")

    frmRec = customtkinter.CTkFrame(master=jnlRec)
    frmRec.pack(pady=5, padx=10, fill="both")

    pop = 0
    if isChecked.get() == True:
        pop = 60
    elif isChecked.get() == False:
        pop = 0

    for i in musica.recomedarMusicas(iMscEsc, pop):
        mscRec = musica.procurarMusicaIndice(i)
        frmRecEsc = customtkinter.CTkFrame(master=frmRec)
        frmRecEsc.pack(pady=2, padx=2, fill="both")
        lblRec = customtkinter.CTkLabel(master=frmRecEsc, text=mscRec['track_name'], font=("Arial", 15))
        lblRec.pack(side="left", padx=10)
        lblRecArt = customtkinter.CTkLabel(master=frmRecEsc, text=mscRec['artists'], font=("Arial", 10))
        lblRecArt.pack(side="left", padx=10)
        btAtrEsc = customtkinter.CTkButton(master=frmRecEsc, text="...", command=lambda ind=i: crtMsgBox(ind))
        btAtrEsc.pack(side="right", pady=2, padx=10)
        link = musica.youtubeSearchVideo(mscRec['track_name'] + " " + mscRec['artists'])['url']
        btYtEsc = customtkinter.CTkButton(master=frmRecEsc, text="", image=imgBtn, command=lambda url=link: abrirLink(url))
        btYtEsc.pack(side="right", pady=2, padx=2)


lblTitulo = customtkinter.CTkLabel(master=root, text="", image=imgLogo)
lblTitulo.pack(pady=20, padx=10, fill="both")

frmInput = customtkinter.CTkFrame(master=root)
frmInput.pack(pady=10, padx=10, fill="both")

etrMusica = customtkinter.CTkEntry(master=frmInput, placeholder_text="Digite o nome da música")
etrMusica.pack(pady=10, padx=10, fill="both")

btProc = customtkinter.CTkButton(master=frmInput, text="Procurar", command=procMusica)
btProc.pack(pady=15, padx=10)

lblErro = customtkinter.CTkLabel(master=root, text="Música não encontrada!", font=("Arial", 12))
lblErro.pack_forget()

frmLst = customtkinter.CTkFrame(master=root)
frmLst.pack_forget()

lstLista = tkinter.Listbox(master=frmLst, font=("Arial", 10), bg="#212121", selectbackground="#1A1A1A", fg="white")
lstLista.config(selectmode="single", borderwidth=0, highlightthickness=0, justify="left", activestyle="none")
lstLista.pack(side="left", pady=20, padx=10, fill="both", expand=True)

scrollbar = tkinter.Scrollbar(master=frmLst)
scrollbar.pack(side="right", fill="both")

lstLista.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lstLista.yview)

frmBottom = customtkinter.CTkFrame(master=root)
frmBottom.pack_forget()

isChecked = tkinter.BooleanVar()
checkbox = customtkinter.CTkCheckBox(master=frmBottom, text="Recomendar somente as mais populares", variable=isChecked, onvalue=True, offvalue=False)
checkbox.select()
checkbox.pack(pady=15, padx=10)

btEsc = customtkinter.CTkButton(master=frmBottom, text="Escolher", command=escMusica)
btEsc.pack(pady=15, padx=10)

root.mainloop()