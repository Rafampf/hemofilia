from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.app import App
from kivy.config import Config
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.animation import Animation
from random import sample
from random import random
from random import randint
from kivy.clock import Clock
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget


Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '634')

sm = ScreenManager(transition=FadeTransition(duration=0.04))

Builder.load_file("my.kv")


def letras(palavra):
    l = ["Primeira", "Segunda", "Terceira", "Quarta", "Quinta",
         "Sexta", "Sétima", "Oitava", "Nona", "Décima"]
    x = randint(0, len(palavra) - 1)
    return str(l[x] + " letra: " + palavra[x])




def transformar(decimal):
    a = int(decimal * 1000)
    return a/1000


ultimo_score = 0

class Touch(Widget):
    def on_touch_down(self, touch):
        print(touch)

    def on_touch_move(self, touch):
        pass

    def on_touch_up(self, touch):
        pass

class ButtonL(ButtonBehavior, Image):
    pass


class CircularButtonE(ButtonBehavior, Label):
    pass


class CircularButtonC(ButtonBehavior, Label):
    pass


class Inicio(Screen):
    topicos = '''    -Sangue
    -Mecanismos
    -Vitamina K
    -Genética
    -Sintomas e Exames
    -Aspectos Sociais
    
    '''
    def sobeteclado(self, coisa):
        coisa.text = ""
        coisa.pos_hint = {"top": 0.6}
    def on_pre_enter(self, *args):
        Clock.schedule_interval(self.apagar, 3)
        self.ids.texto.text = "senha"
    def acender(self, *args):
        anim = Animation(opacity=1, duration=1.5)
        anim.start(self.ids.pedesenha)
    def apagar(self, *args):
        anim = Animation(opacity=0.2, duration= 1.5)
        anim.start(self.ids.pedesenha)
        Clock.schedule_once(self.acender, 1.5)
    def validar(self, coisa):
        coisa.pos_hint = {"top": 0.3}
        if self.ids.texto.text.lower() == "sesamo" or self.ids.texto.text.lower() == "sésamo":
            sm.current = 'm_lvl'

        self.ids.texto.text = ""
    pass


class Menu_level(Screen):
    l = ["", "Sangue", "Mecanismos", "Vitamina K", "Genética", "Sintomas e Exames", "Aspectos Sociais"]
    s = ["", "plaquetas"]

    def limpa1(self):
        try:
            self.ids.fltexto.remove_widget(self.ids.bttexto)
        except:
            pass

    def abrirmenu(self, qual):
        if qual.text == "Level Bonus":
            self.ids.txtlvl.text = "Level Bônus"
            self.ids.txtlvl.font_size = self.height/22
            self.ids.temalvl.text = ":)"
        else:
            self.ids.txtlvl.text = "Level " + qual.text
            if self.ids.txtlvl.text == "Level 1":
                self.ids.fltexto.add_widget(self.ids.bttexto)
            self.ids.temalvl.text = self.l[int(qual.text)]
        self.ids.tudo.add_widget(self.ids.menulevels)


    def validar(self):
        if self.ids.texto.text.lower() == "trombina" and self.ids.txtlvl.text == "Level 2":
            sm.current = 'rafa'
        elif self.ids.texto.text.lower() == "menadiona" and self.ids.txtlvl.text == "Level 3":
            sm.current = 'carlos'
        elif self.ids.texto.text.lower() == "cariotipo" and self.ids.txtlvl.text == "Level 4":
            sm.current = 'dago'
        elif self.ids.texto.text.lower() == "cariótipo" and self.ids.txtlvl.text == "Level 4":
            sm.current = 'dago'
        elif self.ids.texto.text.lower() == "ecografia" and self.ids.txtlvl.text == "Level 5":
            sm.current = 'alex'
        elif self.ids.texto.text.lower() == "convivio" and self.ids.txtlvl.text == "Level 6":
            sm.current = 'cortez'
        elif self.ids.texto.text.lower() == "convívio" and self.ids.txtlvl.text == "Level 6":
            sm.current = 'cortez'
        elif self.ids.texto.text.lower() == "obrigado" and self.ids.txtlvl.text == "Level Bônus":
            sm.current = 'game'
        self.ids.texto.text = ""


class Erro(Button):
    pass

class GameOver(Screen):
    us = NumericProperty(0)
    pont = "Pontuação: "
    def on_pre_enter(self, *args):
        self.us = ultimo_score
    pass

class Player(Image):
    source = "Hgame2.png"
    speed = NumericProperty(0)
    pass

class Obstaculo(Image):
    source = "gordura.png"
    scored = False
    gameScreen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim = Animation(x= -self.width, duration=3)
        self.anim.bind(on_complete= self.vanish)
        self.anim.start(self)
        self.gameScreen = App.get_running_app().root.get_screen("game")

    def on_x(self, *args):
        if self.gameScreen:
            if self.x < self.gameScreen.ids.player.x and not self.scored:
                self.gameScreen.score += 0.5
                self.scored = True

    def vanish(self, *args):
        self.gameScreen.remove_widget(self)
        self.gameScreen.obstaculos.remove(self)


class Game(Screen):
    obstaculos = []
    score = NumericProperty(0)

    def on_enter(self, *args):
        Clock.schedule_interval(self.update,1/30)
        Clock.schedule_interval(self.putObstaculo, 1.4)

    def on_pre_enter(self, *args):
        self.ids.player.y = self.height/2
        self.ids.player.speed = 0
        self.score = 0

    def update(self, *args):
        global ultimo_score
        self.ids.player.speed += -self.height * 2 * 1/30
        self.ids.player.y += self.ids.player.speed * 1/30
        if self.ids.player.y > self.height or self.ids.player.y < 0:
            ultimo_score = self.score
            self.game0ver()
        elif self.playerCollided():
            ultimo_score = self.score
            self.game0ver()

    def putObstaculo(self, *args):
        gap = self.height*0.3
        position = (self.height-gap) * random()
        width = self.width*0.1
        obstaculoLow = Obstaculo(x = self.width, height=position, width= width)
        obstaculoHigh = Obstaculo(x=self.width, y=position + gap, height=self.height -position - gap, width= width)
        self.add_widget(obstaculoLow, 3)
        self.obstaculos.append(obstaculoLow)
        self.add_widget(obstaculoHigh, 3)
        self.obstaculos.append(obstaculoHigh)

    def game0ver(self):
        Clock.unschedule(self.update, 1/30)
        Clock.unschedule(self.putObstaculo, 1)
        App.get_running_app().root.current = "go"
        for ob in self.obstaculos:
            ob.anim.cancel(ob)
            self.remove_widget(ob)
        self.obstaculos = []

    def collided(self, wid1, wid2):
        if wid2.x <= wid1.x + wid1.width and \
            wid2.x + wid2.width >= wid1.x and \
            wid2.y <= wid1.y + wid1.height and \
            wid2.y + wid2.height >= wid1.y:
            return True
        return False

    def playerCollided(self):
        collided = False
        for obstacle in self.obstaculos:
            if self.collided(self.ids.player, obstacle):
                collided = True
                break
        return collided


    def on_touch_down(self, touch):
        self.ids.player.speed = self.height*0.7
    pass


class Victor(Screen):
    tempo = NumericProperty(15)
    l = l_inicial = [["O que são plaquetas?",
                      "Proteínas",
                      "Fragmentos\ncitoplasmáticos",
                      "Células\ncompletas",
                      "Anticorpos", 2],
                     ["Qual o formato das plaquetas?",
                      "Discoidal",
                      "Esférico",
                      "Discoidal\ne Esférico",
                      "Cuboidal", 3],
                     ["Qual o nome do sistema de\ncanais conectados à\nsuperfície das plaquetas?",
                      "Sistema canicular\naberto",
                      "Citoesqueleto\ntubular",
                      "Aquaporinas",
                      "Microtúbulos", 1],
                     ["A zona sol-gel das plaquetas\nconsiste em:",
                      "ribossomos e\nsistema contrábil",
                      "ribossomos e\n sistema tubular\ndenso",
                      "sistema tubular\ndenso e sistema\ncanicular aberto",
                      "sistema contrátil\ne citoesqueleto", 4],
                     ["Qual a região onde estão\nlocalizados os sistemas\nenzimáticos das plaquetas?",
                      "Zona\nperiférica",
                      "Sistema\nmembranar",
                      "Zona\nsol-gel",
                      "Zona de\norganelas", 2],
                     ["Em quantas zonas são\ndivididas as plaquetas?",
                      "Duas",
                      "Três",
                      "Quatro",
                      "Cinco", 3]]

    def fimtempo(self):
        self.perdeu = True
        self.ids.motivo.text = "Tempo Esgotado"
        self.ids.resposta.text = self.l[0][self.l[0][5]]
        self.ids.tudo.add_widget(self.ids.fim_tempo)
        Clock.unschedule(self.countdown, 1)


    def countdown(self,*args):
        if self.tempo > 0:
            self.tempo -= 1
        elif self.tempo <= 0 and not self.perdeu:
            self.fimtempo()




    def start(self):
        self.ids.marcacao.text = "1/2"
        self.score = 0
        self.perdeu = False
        self.tempo = 15
        self.ids.cronometro.opacity= 1
        Clock.schedule_interval(self.countdown, 1)
        self.ids.tudo.remove_widget(self.ids.fim_level)
        self.ids.tudo.remove_widget(self.ids.fim_tempo)
        self.l = sample(self.l_inicial, len(self.l_inicial))
        self.i = 0
        for button in self.ids.botoes.children:
            button.disabled = False
            self.i += 1
            button.text = self.l[0][self.i]
        self.ids.pergunta.text = self.l[0][0]

    def validar(self, botao):
        Clock.unschedule(self.countdown, 1)
        if botao.text == self.l[0][self.l[0][5]]:
            self.score += 1
            self.tempo = 15
            Clock.schedule_interval(self.countdown, 1)
            self.l.pop(0)
            self.i = 0
            for button in self.ids.botoes.children:
                self.i += 1
                button.text = self.l[0][self.i]
            self.ids.pergunta.text = self.l[0][0]
        else:
            self.ids.marcacao.text = "1/2"
            self.score = 0
            self.ids.motivo.text = "Resposta Incorreta"
            self.ids.resposta.text = self.l[0][self.l[0][5]]
            self.ids.tudo.add_widget(self.ids.fim_tempo)
        if self.score == 1:
            self.ids.marcacao.text = "2/2"
        elif self.score == 2:
            self.tempo = 10000
            self.ids.cronometro.opacity= 0
            self.ids.letra.text = letras("TROMBINA")
            self.ids.tudo.add_widget(self.ids.fim_level)
            for button in self.ids.botoes.children:
                button.disabled = True


class Rafa(Screen):
    l = l_inicial = ["Fibrina", "Fibrinogênio", "Fator IX", "Fator IXa", "Protrombina", "Trombina",
                     "Fator XI", "HMWK", "FT + FVII", "FX/FXa", "Trombina +\nFator XIII", "Fator XIIIa"]
    l_cor = [(1, 1, 0.251, 1), (1, 1, 0.251, 1), (0.69, 0.848, 0.902, 1), (0.69, 0.848, 0.902, 1),
             (0.933, 0.51, 0.933, 1), (0.933, 0.51, 0.933, 1), (0.957, 0.643, 0.376, 1), (0.957, 0.643, 0.376, 1),
             (0, 1, 0.498, 1), (0, 1, 0.498, 1), (0.98, 0.922, 0.843, 1), (0.98, 0.922, 0.843, 1)]
    def cor(self, quem):
        return self.l_cor[self.l_inicial.index(quem.text)]

    def start(self):
        self.cvirado = 0
        self.l = sample(self.l_inicial, len(self.l_inicial))
        for button in self.ids.memoria.children:
            button.text = "?"
            button.background_color = (1,1,1,1)
            button.font_size = button.height
            button.disabled = False
        self.ids.tudo.remove_widget(self.ids.tampa)
        self.ids.tudo.remove_widget(self.ids.fim_level)
        self.pares = 0

    def clear(self, *args):
        self.ids.txt1.text = self.ids.txt2.text = ""
        self.ids.txt1.color = self.ids.txt2.color = (1, 1, 1, 1)
        self.ids.tudo.remove_widget(self.ids.tampa)
        if self.pares == 6:
            self.ids.letra.text = letras("MENADIONA")
            self.ids.tudo.add_widget(self.ids.fim_level)


    def virar(self, botao, posicao):
        animC = Animation(color=(0, 0.7, 0, 1), duration= 0.5)
        animE = Animation(color=(0.7, 0, 0, 1), duration= 0.5)
        if botao.text == "?" and self.cvirado < 2:
            botao.font_size = int(botao.height/5.5)
            botao.text = self.l[posicao]
            botao.background_color = self.cor(botao)
            self.cvirado += 1
            if self.cvirado == 1:
                self.c1 = botao
                self.ids.txt1.text = self.c1.text
            elif self.cvirado == 2:
                self.c2 = botao
                self.ids.txt2.text = self.c2.text
                self.ids.tudo.add_widget(self.ids.tampa)
                if self.c1.background_color == botao.background_color:
                    self.pares += 1
                    animC.start(self.ids.txt1)
                    animC.start(self.ids.txt2)
                    self.cvirado = 0
                    self.c1.disabled = True
                    self.c2.disabled = True
                else:
                    animE.start(self.ids.txt1)
                    animE.start(self.ids.txt2)
                Clock.schedule_once(self.clear, 1)

        elif botao.text != "?" and self.cvirado != 1:
            self.c1.font_size = self.c2.font_size = botao.height
            self.c1.text = self.c2.text = "?"
            self.c1.background_color = self.c2.background_color = (1,1,1,1)
            self.cvirado -= 2


class Carlos(Screen):
    l = l_inicial = [["Quantidades ingeridas de\nvitamina K acima de 45mg/dia\ntornam-se tóxicas", False],
                     ["Óleos vegetais são ricos\nem vitaminas K", True],
                     ["A hipovitaminose k diminui os\nníveis de protrombina e outros\nfatores de coagulação", True],
                     ["O excesso de vitamina K\npode anular o efeito de\nalguns anticoagulantes", True],
                     ["Fatores de coagulação II, VII, X e XII\nno fígado são dependentes\nde vitamina K", False],
                     ["Menadiona (vitamina K3) é o tipo\nde vitamina k mais predominante\nem alimentos de origem"
                      " vegetal", False],
                     ["Filoquinona (vitamina K1) é absorvida\nno intestino delgado e transportada\n"
                      "pelas vias linfáticas", True],
                     ["O ciclo da vitamina K ocorre\nsomente no fígado", False],
                     ["O resultado líquido do ciclo é\na conversão da epoxi-vitamina\nK em hidroquinona", True]]
    def tirarampa(self, *args):
        try:
            self.ids.tudo.remove_widget(self.ids.tampa)
        except:
            pass
    def prox_frase(self, seconds=0):
        if self.l[0][1]:
            self.ultima_resposta = True
        else:
            self.ultima_resposta = False
        self.ids.frase.text = self.l[0][0]
        self.l.remove(self.l[0])
    def renovar(self):
        Clock.schedule_once(self.tirarampa, 1.1)
        Animation.cancel_all(self.ids.tempo)
        animFim = Animation(size_hint=(1.99, 0.065),background_color=(0.25,1,0.25,1), duration=1)
        if 3 > self.score > 0:
            animFim.start(self.ids.tempo)
            Clock.schedule_once(self.time, 1.5)
            Clock.schedule_once(self.prox_frase, 1)
        if self.score == 1:
            self.cont= (0.66, 0.065)
        elif self.score == 2:
            self.cont= (1.34, 0.065)
        else:
            self.cont= (1.99, 0.065)
            self.ids.letra.text = letras("CARIOTIPO")
            self.ids.tudo.add_widget(self.ids.fim_level)
        animCont= Animation(size_hint= self.cont)
        animCont.start(self.ids.contador)
        print(self.cont)
    def perdeu(self, seconds=0):
        if self.ids.tempo.size_hint == [0.04, 0.065]:
            self.ids.motivo.text = "Tempo Esgotado"
            self.ids.tudo.add_widget(self.ids.fim_tempo)
            self.score = 0
            if self.l[0][1]:
                self.ids.resposta.text = "Verdadeiro"
            elif not self.l[0][1]:
                self.ids.resposta.text = "Falso"
    def time(self, seconds=0):
        anim = Animation(size_hint=(0.04, 0.065),background_color=(1,0,0,1), duration=10)
        anim.start(self.ids.tempo)
        Clock.schedule_once(self.perdeu, 10.1)
    def start(self):
        self.tirarampa()
        self.ultima_resposta = ""
        self.score = 0
        self.ids.contador.size_hint = (0.04, 0.065)
        self.ids.tempo.size_hint = (1.99, 0.065)
        self.ids.tempo.background_color = 0.25,1,0.25,1
        self.l = sample(self.l_inicial, len(self.l_inicial))
        self.prox_frase()
        Clock.schedule_once(self.time, 2)
    def checar(self, resposta):
        self.ids.tudo.add_widget(self.ids.tampa)
        if resposta == self.ultima_resposta:
            self.score += 1
            self.renovar()
        else:
            if self.ultima_resposta:
                self.ids.resposta.text = "Verdadeiro"
            elif not self.ultima_resposta:
                self.ids.resposta.text = "Falso"
            Animation.cancel_all(self.ids.tempo)
            self.ids.motivo.text = "Resposta Incorreta"
            self.ids.tudo.add_widget(self.ids.fim_tempo)
            self.score = 0
    pass


class Dago(Screen):
    def restart(self):
        self.ids.tudo.clear_widgets()
        self.ids.tudo.add_widget(self.ids.branco)
        self.ids.tudo.add_widget(self.ids.imgdago1)
        self.ids.imgdago1.pos_hint = {"right": 0.92 + 0.038, "y": 0.774 - 0.42}
        self.ids.imgdago1.size_hint = (0.92, 0.42)
        self.ids.imgdago1.opacity = 1
        self.ids.tudo.add_widget(self.ids.FLcariotipo)
        self.ids.erroaqui1.clear_widgets()
        self.ids.tudo.add_widget(self.ids.imgdago2)
        self.ids.imgdago2.pos_hint = {"center_x": 0.6, "y": 0.42}
        self.ids.imgdago2.size_hint = (0.92 * 0.8, 0.42 * 0.8)
        self.ids.imgdago2.opacity = 0
        self.ids.tudo.add_widget(self.ids.imgdago3)
        self.ids.imgdago3.size_hint= (0.92/4, 0.6/4)
        self.ids.imgdago3.pos_hint= {"center_x": 0.5, "center_y": 0.55}
        self.ids.imgdago3.opacity= 0
        self.ids.tudo.add_widget(self.ids.base)
        self.ids.tudo.add_widget(self.ids.lbl1)
        self.ids.tudo.add_widget(self.ids.lbl2)
        self.ids.tudo.add_widget(self.ids.barra)
        self.ids.tudo.add_widget(self.ids.topo)

    def _clear1(self, duration):
        animDap= Animation(opacity=0, duration=0.5)
        animAp= Animation(opacity=1, size_hint=(0.92, 0.4), pos_hint={"y": 0.37, "center_x": 0.5}, duration= 0.5)
        animAp.start(self.ids.imgdago2)
        animDap.start(self.ids.imgdago1)
    def _start2(self, duration):
        self.ids.tudo.add_widget(self.ids.FLcromossomo)
        self.ids.erroaqui2.clear_widgets()
    def _clear2(self, duration):
        animDap= Animation(opacity=0, duration=0.6)
        animAp= Animation(opacity=1, size_hint=(0.92, 0.6), pos_hint={"center_y": 0.55, "center_x": 0.5}, duration= 0.8)
        animAp.start(self.ids.imgdago3)
        animDap.start(self.ids.imgdago2)
    def _start3(self, duration):
        self.ids.tudo.add_widget(self.ids.FLxq28)
        self.ids.erroaqui3.clear_widgets()

    def zoom(self, nmr):
        if nmr == 1:
            self.ids.tudo.remove_widget(self.ids.FLcariotipo)
            anim = Animation(size_hint=(0.92*5, 0.42*5))
            anim.start(self.ids.imgdago1)
            Clock.schedule_once(self._clear1, 0.8)
            Clock.schedule_once(self._start2, 1.4)
        elif nmr == 2:
            self.ids.tudo.remove_widget(self.ids.FLcromossomo)
            anim = Animation(size_hint=(0.92*20, 0.42*20))
            anim.start(self.ids.imgdago2)
            Clock.schedule_once(self._clear2, 0.9)
            Clock.schedule_once(self._start3, 1.9)
        elif nmr == 3:
            self.ids.letra.text = letras("ECOGRAFIA")
            self.ids.tudo.add_widget(self.ids.fim_level)

    def erro(self, botao):
        if botao.text == "1":
            self.ids.erroaqui1.add_widget(Erro(pos_hint=botao.pos_hint))
        elif botao.text == "2":
            self.ids.erroaqui2.add_widget(Erro(pos_hint=botao.pos_hint))
        elif botao.text == "3":
            self.ids.erroaqui3.add_widget(Erro(pos_hint=botao.pos_hint))


    pass


class Alex(Screen):

    cedilha = "ç"
    l = l_inicial = [["sangramento dentro de uma articulação", "hermatrose"],
                     ["principal exame para detectar hemofilia", "coagulograma"],
                     ["acúmulo de sangue fora dos vasos\n(geralmente pós trauma)", "hematoma"]]

    def perdeu(self, *args):
        self.ids.resposta.text = self.l[0][1]
        self.ids.tudo.add_widget(self.ids.fim_tempo)


    def start(self):
        self.l = sample(self.l_inicial, len(self.l_inicial))
        self.ids.letraqui.clear_widgets()
        self.ids.imagemforca.source = "img0.png"
        self.ids.tudo.remove_widget(self.ids.fim_level)
        self.ids.tudo.remove_widget(self.ids.fim_tempo)
        self.erros = self.acertos = i = 0
        self.ids.dica.text = self.l[0][0]
        for button in self.ids.teclado.children:
            button.disabled = False
        for l in self.l[0][1]:
            self.ids.letraqui.add_widget(Label(text="__",
                                                   font_size= self.height/40,
                                                   pos_hint={"x": i / len(self.l[0][1]), "top": 0.4},
                                                   size_hint=(1 / len(self.l[0][1]), 0.7), color=(1, 0, 0, 1)))
            i += 1
    def apertar(self, tecla):
        certo = False
        i = -1
        for l in self.l[0][1]:
            i += 1
            if tecla.text == l:
                self.ids.letraqui.add_widget(Label(text=tecla.text,
                                                   font_size= self.height/40,
                                                   pos_hint={"x": i / len(self.l[0][1]), "top": 0.41},
                                                   size_hint=(1 / len(self.l[0][1]), 0.7), color=(1, 0, 0, 1)))
                self.acertos += 1
                certo = True
        tecla.disabled = True
        if not certo:
            self.erros += 1
            self.ids.imagemforca.source = "img" + str(self.erros) + ".png"
            if self.ids.imagemforca.source == "img6.png":
                for button in self.ids.teclado.children:
                    button.disabled = True
                Clock.schedule_once(self.perdeu, 1)
        elif self.acertos == len(self.l[0][1]):
            self.ids.letra.text = letras("CONVIVIO")
            self.ids.tudo.add_widget(self.ids.fim_level)


class Cortez(Screen):
    def start(self):
        self.ids.tudo.remove_widget(self.ids.fim_level)
        self.ids.npessoas.text = "0"
        self.ids.feedback.text = ""
        self.ids.term.background_color= (0.09, 0.86, 0.89, 1)
        self.ids.term.size_hint = ( 1, 0.15)
        self.ids.bolaterm.background_color = (0.09, 0.86, 0.89, 1)
    def _fbcerto (self, duration):
        self.ids.feedback.text = "parabens"
        self.ids.letra.text = letras("OBRIGADO")
        self.ids.tudo.add_widget(self.ids.fim_level)
    def _fbmenor (self, duration):
        self.ids.feedback.text = "mais"
    def _fbmaior (self, duration):
        self.ids.feedback.text = "menos"
    def soma(self, numero):
        self.ids.npessoas.text = str(int(self.ids.npessoas.text) + numero)
    def confirmar(self):
        animfb= Animation(opacity=0, duration=0.5) + Animation(opacity=1,duration=0.5)
        if 749 < int(self.ids.npessoas.text) < 851:
            a = 1
            Clock.schedule_once(self._fbcerto, 0.5)
        elif int(self.ids.npessoas.text) < 750:
            a = int(self.ids.npessoas.text)/750
            Clock.schedule_once(self._fbmenor, 0.5)
        elif int(self.ids.npessoas.text) > 850:
            a = 1 - (int(self.ids.npessoas.text)/850 - 1)
            Clock.schedule_once(self._fbmaior, 0.5)
        else:
            a = 1
        if a < 0.15:
            a = 0.15
        anim = Animation(size_hint=(1, transformar(a)))
        anim.start(self.ids.term)
        if a == 1:
            b = 1, 0.1, 0.1, 1
        elif transformar(a) < 0.2:
            b = 0.09, 0.86, 0.89, 1
        elif transformar(a) < 0.4:
            b = 0.18, 0.09, 0.96, 1
        elif transformar(a) < 0.6:
            b = 0.62, 0.09, 0.96, 1
        elif transformar(a) < 0.8:
            b = 0.96, 0.09, 0.86, 1
        elif transformar(a) < 1:
            b = 0.96, 0.42, 0.09, 1
        else:
            b = 1, 1, 1, 1
        anim2 = Animation(background_color=b)
        anim2.start(self.ids.term)
        anim2.start(self.ids.bolaterm)
        animfb.start(self.ids.feedback)


class Teoria(Screen):
    pass


class Menu_teoria(Screen):
    dic = {
        "Aspectos Sociais": '''       Embora a hemofilia seja uma doença sem cura, com o tratamento adequado e o autocuidado, a maioria das pessoas pode manter um estilo de vida ativo e produtivo. Esse tratamento é feito com a reposição intravenosa do concentrado do fator deficiente dependendo da variedade da hemofilia( tipo A usa-se o fator VIII e B o fator IX). Essa reposição é disponibilizada pelo SUS, geralmente em centros especializados, ou  pode ser feita em casa, e o HEMOPE disponibiliza esse curso para aplicação dos fatores coagulantes.
        É bastante comum o relato de crianças e adolescentes hemofílicos queixando-se de existir uma sensação  de exclusão dos demais. Pois, algumas atividades bastante comuns nessa idade como jogar futebol, basquete e qualquer brincadeira que exige muito contato físico, são desaconselhadas. Muitos deles relataram não revelar para os amigos que são hemofílicos com medo de haver uma exclusão maior ainda, muito também por conta da desinformação sobre a doença. Esse cenário pode causar uma maior tendência a desenvolver sintomas de doenças psicológicas como a depressão.
        Por conta disso é fundamental acompanhamento psicológico desses indivíduos, até porque também foi recorrente entre os entrevistados a desmotivação no tratamento da hemofilia, pois já que é uma doença que não tem cura, mas sim atenua-se as complicações, eles não vêem perspectiva no tratamento e não querem passar pelo desconforto das infusões dos fatores coagulantes frequentes. Por isso é fundamental um bom acompanhamento médico para instruir os pais e os jovens sobre a importância do tratamento regular para amenizar os desconfortos provocados pela doença, para que se sintam seguros em aplicar os fatores de coagulação em casa e para que os pacientes possam conciliar a doença sem que afete drasticamente o convívio social.
        
        ''',
        "Mecanismos": '''A coagulação sanguínea consiste na conversão de uma proteína solúvel do plasma, o fibrinogênio, em um polímero insolúvel, a fibrina, por ação de uma enzima denominada trombina. A fibrina forma uma rede de fibras elásticas que consolida o tampão plaquetário e o transforma em tampão hemostático. A coagulação é uma série de reações químicas entre várias proteínas que convertem pró-enzimas em enzimas. Essas pró-enzimas e enzimas são denominadas fatores de coagulação. A ativação destes fatores é iniciada pelo endotélio ativado e finalizado na superfície das plaquetas ativadas e tem como produto a formação de trombina que promoverá modificações na molécula de fibrinogênio, liberando monômeros de fibrina na circulação. Esses monômeros vão unir suas terminações e formar um polímero solúvel (fibrina S) que, sob a ação do fator XIIIa (fator XIII ativado pela trombina) e íons cálcio, produz a base de fibras que mantêm o agregado de plaquetas previamente formado. No modelo de cascata de ativação, cada fator da coagulação leva a ativação de outro fator até a eventual formação da trombina. Esses fatores são numerados de I ao XIII, com seus respectivos sinônimos. O número correspondente para cada fator foi designado considerando a ordem de sua descoberta. Ainda sobre o modelo cascata da coagulação, ele pode ser dividido em duas vias: a via intrínseca na qual todos os componentes estão presentes no sangue e na via extrínseca na qual é necessária a presença da proteína da membrana celular subendotelial, o fator tecidual (TF). Apesar das duas vias serem diferentes, existem processos comuns da coagulação (via final comum), que é são a ativação do fator X sendo convertido em Xa, a conversão de trombina a partir da protrombina pela ação do fator Xa, formação de fibrina estimulada pela trombina e estabilização da fibrina pelo fator XIIIa. A coagulação, pela via intrínseca, é desencadeada quando o fator XII é ativado pelo contato com o colágeno endotelial. Além do fator XII, estão envolvidos neste processo o fator XI, a pré-calicreína e o cininogênio de alto peso molecular (HMWK = high molecular weight kinogen). Nesse sentido, tanto o fator XI quanto a pré-calicreína necessitam da HMWK para efetuar a adsorção à superfície em que está ligado o fator XIIa. Do resultado desses processos ocorre a ativação do fator XI, que transforma o fator IX em IXa. O fator IXa e o fator VIIa associam-se à superfície de fosfolipídio através de uma "ponte" de cálcio estimulando a conversão de fator X para Xa. De maneira mais simplificada, na via extrínseca, a cascata é desencadeada quando os tecidos lesados liberam o fator tecidual (tromboplastina tecidual), que forma um complexo com o fator VII, mediado por íons cálcio. Este complexo age sobre o fator X estimulando sua conversão em Xa. Explicado tudo isso, as duas vias encontram um caminho comum em que ocorre a conversão de protrombina em trombina que, por sua vez, estimula a transformação de fibrinogênio em fibrina.
        
        ''',
        "Vitamina K": '''       Uma importante coenzima envolvida no processo de coagulação sanguínea é a vitamina K, ela é encontrada em quatro formas: Filoquinona (vitamina K1) que é a forma predominante, presente principalmente em óleos vegetais e hortaliças; Menaquinona (vitamina K2), presente em produtos animais e alimentos fermentados; Menadiona (vitamina K3) que é um composto sintético; Dihidrofiloquinona (dK), formada durante a hidrogenação comercial de óleos vegetais.
        A vitamina K atua como cofator para a carboxilação de resíduos específicos de ácido glutâmico para formar o ácido gama carboxiglutâmico (Gla), aminoácido presente nos fatores de coagulação (fatores II, VII, IX e X). A carboxilação capacita as proteínas de coagulação a se ligarem ao cálcio, permitindo assim a interação com os fosfolipídios das membranas de plaquetas e células endoteliais, o que, por sua vez, possibilita o processo de coagulação sanguínea normal.
        Em essência, o ciclo de vitamina K, pode ser considerado uma via de recuperação da vitamina, presente em quantidades nanomolares no fígado e em outros tecidos.
        Ao alcançar o fígado, a filoquinona é reduzida a hidronaftoquinona (KH2), que é o cofator ativo para a carboxilase . O fígado tem um papel exclusivo na transformação metabólica que leva à excreção da vitamina K do organismo. A deficiência de vitamina K diminui os níveis de protrombina e outros fatores de coagulação dependentes de vitamina K, causando coagulação defeituosa e, potencialmente, sangramento. É importante entender também que a  vitamina K1 (filoquinona) não é tóxica quando consumida via oral, mesmo em grandes quantidades. Entretanto, a menadiona (precursor sintético de vitamina K solúvel em água) pode causar toxicidade e não deve ser utilizada para tratar a deficiência de vitamina K.
        
        ''',
        "Sintomas e Exames": '''        As manifestações clínicas da hemofilia são bastantes e ocorrem em diferentes intensidades, desde pequenos hematomas até sangramentos espontâneos e sem causa aparente. 
        Dessa forma, o indivíduo pode ter sua hemofilia classificada em leve, moderada ou grave, a depender da quantidade de fator VIII ou IX presente no sangue.
        A leve apresenta sintomas mais brandos e sua manifestação é mais perceptível em cirurgias e cortes, casos em que a cicatrização é mais demorada.
        A moderada já é mais evidente, uma vez que hematomas já são mais frequentes e demoram mais a cicatrizar, além de relato de sangramentos articulares na criança e, por consequência, falta de mobilidade. Nos casos graves, sangramentos espontâneos são semanais e acompanham outras manifestações.
        Para realização do diagnóstico, é considerada a história clínica do paciente e são feitos exames como coagulograma, no qual é examinado o tempo de tromblopastina parcial ativada (TTPa), que podem ser complementados com a dosagem do fator VIII ou IX
        Por fim, deve-se considerar também o período gestacional de mães portadoras do gene da hemofilia, nesses casos, é importante determinar o sexo do feto o mais cedo possível, para que haja um tratamento adequado em caso de suspeita da doença. Para identificar o sexo, podem ser feitos exames de amniocentese ou de identificação de DNA livre.
        
        ''',
        "Sangue": '''As plaquetas, foco desse estudo, são elementos figurados do sangue, assim como as hemácias e os leucócitos. Diferentemente dos demais elementos, as plaquetas não são células, elas são fragmentos citoplasmáticos anucleados que apresentam forma discóide quando circulam no sangue e esférica ao desempenhar sua função na hemostasia. Originam-se da fragmentação dos pseudópodes dos megacariócitos, num processo denominado trombopoiese . Pode-se dividir a estrutura das plaquetas em 4 zonas. A primeira é denominada zona periférica, abrange membrana plasmática trilaminar externa e interna, além  de um sistema de canais conectado à superfície chamado de sistema canicular aberto. A segunda se denomina zona sol-gel, composta pelo citoesqueleto(fornece a sustentação) e sistema contrátil. A terceira é chamada zona de organelas e apresenta os grânulos alfa, grânulos densos e componentes celulares. A última zona se chama sistema membranar, na qual se situam o sistema tubular denso, que concentra cálcio, importante para desencadear os eventos contráteis, e os sistemas enzimáticos, envolvidos na síntese de prostaglandinas.
        
        ''',
        "Genetica": '''A hemofilia é caracterizada como uma coagulopatia hereditária, recessiva e ligada ao cromossomo X em que há uma deficiência de fatores da coagulação sanguínea responsáveis pela via intrínseca. Seguindo esse contexto, o homem é hemizigoto para a doença e é nele que a grande maioria dos casos ocorre, pois na mulher é preciso que os 2 genes mutantes estejam presentes para expressar a doença. Existem 2 tipos da doença: o tipo A (80% dos casos) é decorrente da deficiência do fator VIII da coagulação, enquanto que no tipo B (20% dos casos) a deficiência é do fator IX. Apesar das causas da doença serem majoritariamente genéticas, a destruição dos fatores por aloanticorpos ou o câncer podem originar formas alternativas dela. No tipo A há uma mutação do gene F8(composto por 26 éxons e 25 íntrons), localizado na posição Xq28, sendo que em 50% dos casos graves ocorre uma inversão do íntron 22. Já no tipo B, há mutações do gene F9, localizado na posição Xq27(composto por 8 éxons), de forma que 90% dessas mutações são do tipo pontual. Em uma última análise, a hemofilia pode ser causada por mutações de novo nesses genes, que caracterizam casos esporádicos e não hereditários.
        
        '''

    }
    def clicar(self, qual):
        self.teoria = App.get_running_app().root.get_screen("teoria")
        self.teoria.ids.titulo.text = qual.text
        self.teoria.ids.texto.text = self.dic[qual.text]

    pass






sm.add_widget(Inicio(name='inicio'))
sm.add_widget(Menu_level(name='m_lvl'))
sm.add_widget(Teoria(name='teoria'))
sm.add_widget(Menu_teoria(name='m_teo'))
sm.add_widget(Victor(name='vic'))
sm.add_widget(Rafa(name='rafa'))
sm.add_widget(Carlos(name='carlos'))
sm.add_widget(Dago(name='dago'))
sm.add_widget(Alex(name='alex'))
sm.add_widget(Cortez(name='cortez'))
sm.add_widget(Game(name='game'))
sm.add_widget(GameOver(name='go'))


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()





