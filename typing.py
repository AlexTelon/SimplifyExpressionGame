from pygametextinput import pygame_textinput
import pygame as pg

BLACK = (0, 0, 0)
def get_next_example():
    import random
    with open('typing.py') as f:
        lines = f.read().splitlines()
        return random.choice(lines).strip()

if __name__ == '__main__':
    pg.init()
    WHITE = (255, 255, 255)

    textinput = pygame_textinput.TextInput(antialias=True, font_family='Consolas', text_color=WHITE, cursor_color=WHITE)

    screen = pg.display.set_mode((1000, 200))
    clock = pg.time.Clock()

    problem_description_font = pg.font.SysFont("Consolas", 30)

    example_text = get_next_example()


    while True:
        screen.fill(BLACK)

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                exit()

        keys = pg.key.get_pressed()

        if keys[pg.K_KP_ENTER]:
            if textinput.input_string == example_text:
                textinput.input_string = ""
                example_text = get_next_example()
            if textinput.input_string == "quit":
                exit()
        else:
            textinput.update(events)
            screen.blit(textinput.get_surface(), (10, 10))


        label = problem_description_font.render(example_text, 1, WHITE)
        screen.blit(label, (10, 100))


        pg.display.update()
        clock.tick(30)