import flet as ft

class Piece:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0

def main(page: ft.Page):

    def place(card, slot):
        """place card to the slot"""
        card.top = slot.top
        card.left = slot.left

    def bounce_back(game, card):
        """return card to its original position"""
        card.top = game.start_top
        card.left = game.start_left
        page.update()

    def move_on_top(card, controls):
        """moves draggable card to the top of the stack"""
        controls.remove(card)
        controls.append(card)
        page.update()

    def start_drag(e: ft.DragStartEvent):
        move_on_top(e.control, controls)
        piece.start_top = e.control.top
        piece.start_left = e.control.left

    def drag(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def drop(e: ft.DragEndEvent):
        for slot in slots:
            if (
                abs(e.control.top - slot.top) < 20
                and abs(e.control.left - slot.left) < 20
            ):
                place(e.control, slot)
                e.control.update()
                return

        bounce_back(piece, e.control)
        e.control.update()

    slots = []
    for i in range(3):
        for j in range(3):
            slot = ft.Container(
                width=70,
                height=100,
                left= j * 100,
                top=i * 120,
                border=ft.border.all(1)
            )
            slots.append(slot)

    cards = []
    for i in range(9):
        card = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=5,
            on_pan_start=start_drag,
            on_pan_update=drag,
            on_pan_end=drop,
            left=400,
            top=i * 55,
            content=ft.Container(bgcolor=ft.Colors.GREEN, width=70, height=100),
        )
        cards.append(card)

    controls = slots + cards

    piece = Piece()

    page.add(ft.Stack(controls=controls, width=1000, height=500))

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
