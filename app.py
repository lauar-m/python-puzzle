import flet as ft

class Piece:
    def __init__(self, original_top, original_left):
        self.start_top = 0
        self.start_left = 0
        self.original_top = original_top
        self.original_left = original_left

def main(page: ft.Page):

    def place(card, slot):
        """place card to the slot"""
        card.top = slot.top
        card.left = slot.left

    def return_to_original_position(card, piece):
        """return card to its original position outside the board"""
        card.top = piece.original_top
        card.left = piece.original_left
        page.update()

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
        piece = pieces[e.control]
        piece.start_top = e.control.top
        piece.start_left = e.control.left

    def drag(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def drop(e: ft.DragEndEvent):
        found_slot = False
        for slot in slots:
            if (
                abs(e.control.top - slot.top) < 20
                and abs(e.control.left - slot.left) < 20
            ):
                place(e.control, slot)
                e.control.update()
                found_slot = True
                return

        if not found_slot:
            return_to_original_position(e.control, pieces[e.control])

    slots = []
    for i in range(3):
        for j in range(3):
            slot = ft.Container(
                width=70,
                height=70,
                left= j * 72,
                top=i * 72,
                border=ft.border.all(1)
            )
            slots.append(slot)

    cards = []
    pieces = {}
    for i in range(9):
        original_left = 400
        original_top = i * 55
        card = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=5,
            on_pan_start=start_drag,
            on_pan_update=drag,
            on_pan_end=drop,
            left=original_left,
            top=original_top,
            content=ft.Container(bgcolor=ft.Colors.GREEN, width=70, height=70),
        )
        cards.append(card)
        pieces[card] = Piece(original_top, original_left)

    controls = slots + cards

    page.add(ft.Stack(controls=controls, width=1500, height=600))

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
