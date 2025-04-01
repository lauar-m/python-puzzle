import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

background = pygame.image.load("assets/images/initial_background.png")
background = pygame.transform.scale(background, (1280, 720))

font = pygame.font.Font(None, 50)

button_text = "Novo Jogo"
cor_texto = (255, 255, 255)
cor_botao = (0, 128, 255)
botao_x, botao_y, botao_largura, botao_altura = 900, 550, 200, 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (
                botao_x <= event.pos[0] <= botao_x + botao_largura and
                botao_y <= event.pos[1] <= botao_y + botao_altura
            ):
                print("botao clicado!!!")

    screen.blit(background, (0, 0))

    pygame.draw.rect(screen, cor_botao, (botao_x, botao_y, botao_largura, botao_altura), border_radius=10)

    texto_renderizado = font.render(button_text, True, cor_texto)
    texto_rect = texto_renderizado.get_rect(center=(botao_x+botao_largura//2, botao_y+botao_altura//2))

    screen.blit(texto_renderizado, texto_rect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()
