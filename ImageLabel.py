import tkinter as tk
from itertools import count, cycle
from PIL import Image, ImageTk

class ImageLabel(tk.Label):
    
    # Um label que exibe imagens e as reproduz se forem gifs, :im:, uma instância de imagem PIL ou um nome de arquivo de string
    
    def load(self, im):
        # É responsável por carregar uma imagem para exibição. Ele recebe como parâmetro um objeto im, que pode ser uma instância de imagem PIL (PIL.Image) ou o nome de um arquivo de imagem em formato de string.
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        # É responsável por descarregar a imagem atualmente exibida, configurando o rótulo ImageLabel com uma imagem vazia e definindo o atributo frames como None.
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        # Configura o rótulo ImageLabel com o próximo frame da lista frames e agendia a chamada para o próximo frame após o tempo definido em delay.
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)
