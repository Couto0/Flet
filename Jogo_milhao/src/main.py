import flet as ft
import random
from base_config import apply_config, Config, create_sidebar
from perguntas import perguntas  # seu arquivo com as perguntas

# Mapear os níveis presentes em perguntas para prêmios (ajuste conforme desejar)
PRIZE_LADDER = {
    1: "R$ 100",
    2: "R$ 200",
    3: "R$ 500",
    4: "R$ 1.000",
    5: "R$ 5.000",
    6: "R$ 10.000",
    # se tiver mais níveis, adicione aqui
}


class MillionGame:
    def __init__(self, page: ft.Page):
        self.page = page
        self.config = Config()
        self.colors = apply_config(page, self.config)
        self.current_level = 1
        self.current_question = None
        self.used_questions = set()
        self.choice_buttons = []
        self.theme_button = None

        # UI containers
        self.question_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
        self.level_text = ft.Text("", size=14)
        self.prize_text = ft.Text("", size=14)
        self.message_text = ft.Text("", size=14)
        self.prize_column = ft.Column()
        self.main_column = ft.Column()

        # Build UI
        self.build_ui()

    def build_ui(self):
        self.page.title = "Jogo do Milhão"
        self.page.window_width = 900
        self.page.window_height = 600

        # Sidebar (criado em base_config)
        sidebar, self.theme_button = create_sidebar(self.restart_click, self.toggle_theme, self.config)

        # Pergunta e alternativas
        answers_container = ft.Column(spacing=8)

        # criar 4 botões de alternativa (placeholder)
        for i in range(4):
            btn = ft.ElevatedButton(
                text=f"Alternativa {i+1}",
                width=480,
                on_click=self.on_answer,
                bgcolor=None
            )
            self.choice_buttons.append(btn)
            answers_container.controls.append(btn)

        # Caixa de ações (próxima, reiniciar)
        next_button = ft.ElevatedButton("Próxima", on_click=self.next_click, disabled=True)
        self.next_button = next_button

        # Montar coluna principal
        self.main_column.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([self.level_text, ft.Spacer(), self.prize_text]),
                        ft.Divider(height=2),
                        self.question_text,
                        ft.Container(height=10),
                        answers_container,
                        ft.Container(height=10),
                        ft.Row([self.message_text, ft.Spacer(), next_button]),
                    ],
                    tight=True,
                    spacing=12
                ),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                width=520,
                expand=False,
                shadow=ft.BoxShadow(blur=5, color=ft.Colors.BLACK12),
            )
        ]

        # Ladder de prêmios (à direita)
        self.build_prize_column()

        # Layout da página
        layout = ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1),
                ft.Column([self.main_column], expand=True),
                ft.Container(width=12),
                ft.Column([self.prize_column], width=200),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20
        )

        self.page.add(layout)
        self.load_question()

    def build_prize_column(self):
        # Exibe o ladder de prêmios e destaca o nível atual
        items = []
        max_level = max(PRIZE_LADDER.keys())
        for lvl in sorted(PRIZE_LADDER.keys(), reverse=True):
            txt = ft.Text(f"Nível {lvl}: {PRIZE_LADDER[lvl]}", size=13)
            container = ft.Container(content=txt, padding=6)
            items.append(container)
        self.prize_column.controls = items

    def update_prize_highlight(self):
        # atualiza destaque na coluna de prêmios
        new_controls = []
        for idx, lvl in enumerate(sorted(PRIZE_LADDER.keys(), reverse=True)):
            display_lvl = lvl
            text = ft.Text(f"Nível {display_lvl}: {PRIZE_LADDER[display_lvl]}", size=13)
            if display_lvl == self.current_level:
                cont = ft.Container(content=text, padding=6, bgcolor=ft.Colors.YELLOW_100, border_radius=6)
            else:
                cont = ft.Container(content=text, padding=6)
            new_controls.append(cont)
        self.prize_column.controls = new_controls
        self.page.update()

    def pick_random_question_for_level(self, level):
        # Escolhe pergunta aleatória do nível sem repetir quando possível
        candidates = [ (i,q) for i,q in enumerate(perguntas) if q.get("nivel") == level and i not in self.used_questions ]
        if not candidates:
            # se esgotou, permitir repetir (pega qualquer do nivel)
            candidates = [ (i,q) for i,q in enumerate(perguntas) if q.get("nivel") == level ]
        if not candidates:
            return None, None
        idx, q = random.choice(candidates)
        return idx, q

    def load_question(self):
        # carregar pergunta para o current_level
        idx, q = self.pick_random_question_for_level(self.current_level)
        if q is None:
            # sem pergunta: fim do jogo (você venceu)
            self.question_text.value = "Parabéns — você venceu o jogo!"
            self.level_text.value = ""
            self.prize_text.value = f"Prêmio: {PRIZE_LADDER.get(self.current_level, '')}"
            for b in self.choice_buttons:
                b.disabled = True
                b.visible = False
            self.message_text.value = "Reinicie para jogar novamente."
            self.page.update()
            return

        self.current_question = (idx, q)
        self.used_questions.add(idx)
        # atualizar elementos de UI
        self.question_text.value = q["pergunta"]
        self.level_text.value = f"Nível {self.current_level}"
        self.prize_text.value = f"Prêmio: {PRIZE_LADDER.get(self.current_level, '')}"
        self.message_text.value = ""
        # embaralhar alternativas mantendo índice correto
        alternatives = q["alternativas"][:]
        correct_idx_original = q["correta"]
        paired = list(enumerate(alternatives))
        random.shuffle(paired)
        # encontrar nova posição da correta
        new_correct = None
        for new_i, (orig_i, alt) in enumerate(paired):
            if orig_i == correct_idx_original:
                new_correct = new_i
            self.choice_buttons[new_i].text = alt
            self.choice_buttons[new_i].bgcolor = None
            self.choice_buttons[new_i].disabled = False
            self.choice_buttons[new_i].data = {"is_correct": (orig_i == correct_idx_original)}
            self.choice_buttons[new_i].visible = True
        # esconder botões que não existem (caso alternativas <4)
        for i in range(len(paired), 4):
            self.choice_buttons[i].visible = False
        self.next_button.disabled = True
        self.update_prize_highlight()
        self.page.update()

    def on_answer(self, e: ft.ControlEvent):
        # clique em alternativa
        btn = e.control
        is_correct = btn.data.get("is_correct", False)
        # desabilitar todas alternativas
        for b in self.choice_buttons:
            b.disabled = True
        # mostrar resultado visual
        if is_correct:
            btn.bgcolor = ft.Colors.GREEN_200
            self.message_text.value = "Resposta correta! Clique em Próxima."
            # habilitar próxima
            self.next_button.disabled = False
        else:
            # marca o botão errado em vermelho e mostra a correta em verde
            btn.bgcolor = ft.Colors.RED_200
            # encontrar correta
            for b in self.choice_buttons:
                if b.data and b.data.get("is_correct"):
                    b.bgcolor = ft.Colors.GREEN_200
            self.message_text.value = "Resposta incorreta. Fim de jogo — você perdeu."
            self.next_button.disabled = True
            # no fim de jogo mantemos botões desabilitados
        self.page.update()

    def next_click(self, e):
        # avançar nível — se a última resposta foi correta
        # verifica se última seleção foi correta (usamos message_text)
        if "correta" in self.message_text.value or "Resposta correta" in self.message_text.value:
            # aumenta nível
            max_level = max(PRIZE_LADDER.keys())
            if self.current_level < max_level:
                self.current_level += 1
                self.load_question()
            else:
                # venceu
                self.question_text.value = "Parabéns — você venceu o jogo!"
                self.message_text.value = f"Você conquistou {PRIZE_LADDER.get(self.current_level, '')}"
                for b in self.choice_buttons:
                    b.visible = False
                self.page.update()
        else:
            # se message_text não indica acerto, nada acontece
            pass

    def restart_click(self, e):
        # reinicia o jogo
        self.current_level = 1
        self.used_questions = set()
        # restaurar botões
        for b in self.choice_buttons:
            b.disabled = False
            b.visible = True
            b.bgcolor = None
        self.next_button.disabled = True
        self.load_question()

    def toggle_theme(self, e):
        # alterna entre Light/Dark
        self.config.theme = "Dark" if self.config.theme == "Light" else "Light"
        self.colors = apply_config(self.page, self.config)
        # atualizar label do botão de tema
        if self.theme_button:
            self.theme_button.text = f"Tema: {self.config.theme}"
        self.page.update()


def main(page: ft.Page):
    game = MillionGame(page)


if __name__ == "__main__":
    ft.app(target=main)

