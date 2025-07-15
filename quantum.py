import pygame
import cirq

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Cirq Viewer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (70, 130, 180)

# Font
font = pygame.font.SysFont('Courier New', 24)
font_big = pygame.font.SysFont('Arial', 32)

# Create Cirq Circuit
qubit_names = ["cakeA_Base", "cakeB_Base", "Frosting"]
qubits = [cirq.NamedQubit(name) for name in qubit_names]
circuit = cirq.Circuit(
    cirq.H(qubits[0]),
    cirq.CNOT(qubits[0], qubits[1]),
    cirq.X(qubits[2]),
    cirq.measure(*qubits)
)

# Get circuit diagram as text
circuit_diagram = str(circuit)

# Function to render text block
def render_text_block(text, x, y, line_height=30):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        rendered_line = font.render(line, True, BLACK)
        screen.blit(rendered_line, (x, y + i * line_height))

# Button rectangle
button_rect = pygame.Rect(350, 200, 200, 60)

# Screen state
current_screen = "main_menu"

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_screen == "main_menu":
                if button_rect.collidepoint(event.pos):
                    current_screen = "view_circuit"
            elif current_screen == "view_circuit":
                # Click anywhere to go back
                current_screen = "main_menu"

    if current_screen == "main_menu":
        # Draw button
        pygame.draw.rect(screen, BLUE, button_rect)
        text = font_big.render("View Circuit", True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    elif current_screen == "view_circuit":
        # Draw circuit diagram
        render_text_block(circuit_diagram, 50, 50)
        render_text_block("Cake A \n Base Flavor--|0>=Chocolate,|1>= Orange", 50, 200)
        render_text_block("Cake B \n Base Flavor--|0>=Mango,|1>= Apple", 50, 260)
        render_text_block("Frosting \n Flavor--|0>=Vanela,|1>= Strawberry", 50, 320)
        tip_text = font.render("Click anywhere to return.", True, (100, 100, 100))
        screen.blit(tip_text, (50, HEIGHT-40))

    pygame.display.update()

pygame.quit()
