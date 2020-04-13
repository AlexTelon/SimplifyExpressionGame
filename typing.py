from pygametextinput import pygame_textinput
import pygame as pg
import expressions

# def get_next_example():
#     import random
#     with open('typing.py') as f:
#         lines = f.read().splitlines()
#         candidates = [line.strip() for line in lines]
#         # remove empty lines
#         candidates = [line for line in candidates if any(line)]
#         return random.choice(candidates)

def get_next_example():
    return expressions.generate_expression() 

def verify():
    # return expressions.expressions_are_logically_same(example_text, user_input.input_string)
    return expressions.expression_in_simplest_form(example_text, user_input.input_string)

def create_user_input_box():
    return pygame_textinput.TextInput(antialias=True, font_family='Consolas', text_color=WHITE, cursor_color=WHITE, font_size=20)

if __name__ == '__main__':
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    pg.init()

    user_input = create_user_input_box()

    screen = pg.display.set_mode((1200, 250))
    clock = pg.time.Clock()

    problem_description_font = pg.font.SysFont("Consolas", 20)

    example_text = get_next_example()
    error_reason = ""

    score = 0
    attempts = 0
    while True:
        screen.fill(BLACK)

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                exit()

        keys = pg.key.get_pressed()

        if keys[pg.K_KP_ENTER] and user_input.input_string != "":
            if user_input.input_string == "quit":
                exit()

            attempts += 1
            if verify():
                score += 1
                example_text = get_next_example()
                error_reason = ""
            else:
                error_reason = expressions._error_reason

            # Always reset user input after enter.
            user_input = create_user_input_box()

        else:
            user_input.update(events)
            screen.blit(user_input.get_surface(), (10, 10))


        label = problem_description_font.render(example_text, 1, WHITE)
        screen.blit(label, (10, 100))
        
        score_label = problem_description_font.render(f"{score=}/{attempts}", 1, WHITE)
        screen.blit(score_label, (10, 150))

        if error_reason:
            error_reason_label = problem_description_font.render(f"{error_reason}", 1, WHITE)
            screen.blit(error_reason_label, (10, 170))


        pg.display.update()
        clock.tick(30)