import pygame
import random
import sys
import time

pygame.init()

WIDTH, HEIGHT = 890, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Amplitude Pair Match")

# Fonts
font = pygame.font.SysFont("Arial", 26)
big_font = pygame.font.SysFont("Arial", 50)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CARD_COLOR = (173, 216, 230)
MATCHED_COLOR = (144, 238, 144)
SELECTED_COLOR = (255, 255, 102)

# Card dimensions
CARD_WIDTH, CARD_HEIGHT = 100, 150
PADDING = 10

# Levels
levels = [
    (4, 2, 5),
    (16, 8, 20),
    (24, 12,30)
]

# Quantum ket pairs
valid_pairs = [
    ("1", "0"),
    ("0", "1"),
    ("-1", "0"),
    ("0", "-1"),
    ("1/√2", "1/√2"),
    ("-1/√2", "1/√2"),
    ("1/√2", "-1/√2"),
    ("-1/√2", "-1/√2"),
    ("√3/2", "1/2"),
    ("1/2", "√3/2"),
    ("-√3/2", "1/2"),
    ("-1/2", "√3/2"),
    ("√3/2", "-1/2"),
    ("1/2", "-√3/2"),
    ("-√3/2", "-1/2"),
    ("-1/2", "-√3/2"),
    ('3/5','4/5'),
    ('4/5','3/5'),
    ('-3/5','4/5'),
    ('4/5','-3/5'),
]

class Card:
    def __init__(self, x, y, value):
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.value = value
        self.matched = False
        self.selected = False

    def draw(self):
        color = MATCHED_COLOR if self.matched else (SELECTED_COLOR if self.selected else CARD_COLOR)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text = font.render(self.value, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) and not self.matched

def generate_cards(pair_count):
    selected_pairs = random.sample(valid_pairs, pair_count)
    flat_values = [v for pair in selected_pairs for v in pair]
    random.shuffle(flat_values)
    return flat_values

def is_valid_match(val1, val2):
    return (val1, val2) in valid_pairs or (val2, val1) in valid_pairs

def game_loop(total_cards, pair_count, time_limit):
    clock = pygame.time.Clock()
    cards = []
    cols = int(WIDTH / (CARD_WIDTH + PADDING))
    rows = (total_cards + cols - 1) // cols
    card_values = generate_cards(pair_count)

    for i in range(total_cards):
        x = PADDING + (i % cols) * (CARD_WIDTH + PADDING)
        y = PADDING + (i // cols) * (CARD_HEIGHT + PADDING)
        cards.append(Card(x, y, card_values[i]))

    selected = []
    matches_found = 0
    start_time = time.time()

    running = True
    while running:
        screen.fill(WHITE)

        elapsed_time = time.time() - start_time
        time_left = max(0, int(time_limit - elapsed_time))

        # Timer Display
        timer_text = font.render(f"Time Left: {time_left} sec", True, BLACK)
        screen.blit(timer_text, (20, HEIGHT - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for card in cards:
                    if card.is_clicked(pos):
                        if len(selected) < 2 and card not in selected:
                            card.selected = True
                            selected.append(card)

                if len(selected) == 2:
                    pygame.time.wait(300)
                    if is_valid_match(selected[0].value, selected[1].value):
                        selected[0].matched = True
                        selected[1].matched = True
                        matches_found += 1
                    selected[0].selected = False
                    selected[1].selected = False
                    selected = []

        for card in cards:
            card.draw()

        if matches_found == pair_count:
            win_text = big_font.render("Level Cleared!", True, BLACK)
            screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(1500)
            return True

        if elapsed_time >= time_limit:
            lose_text = big_font.render("Time's Up!", True, BLACK)
            screen.blit(lose_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return False

        pygame.display.flip()
        clock.tick(60)

def main():
    for total_cards, pair_count, time_limit in levels:
        result = game_loop(total_cards, pair_count, time_limit)
        if not result:
            break

    pygame.quit()

if __name__ == "__main__":
    main()
