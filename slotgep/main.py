import pygame
import random
import sys

# Inicializálás
pygame.init()

# Szimbólumok és esélyek
szotar = {1: "barack", 2: "jackpot", 3: "cseresznye", 4: "szilva", 5: "csengő"}
szimbolumok = [1, 2, 3, 4, 5]
eselyek = [0.3, 0.05, 0.25, 0.35, 0.05]

# Játék ablak beállításai
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Slot Machine Game")

# Színek
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Betűtípus
font = pygame.font.Font(None, 36)

def generate_slot_row():
    return random.choices(szimbolumok, eselyek, k=3)

def evaluate_row(row, tet):
    nyeremeny = 0
    if row.count(1) == 3:
        nyeremeny = tet * 2.0
    elif row.count(2) == 3:
        nyeremeny = tet * 100.0
    elif row.count(3) == 3:
        nyeremeny = tet * 15.0
    elif row.count(4) == 3:
        nyeremeny = tet * 5.0
    elif row.count(5) == 3:
        nyeremeny = tet * 10.0
    elif row.count(5) < 3 and row.count(5) > 0:
        nyeremeny = tet * row.count(5)
    return nyeremeny

def evaluate_diagonal(sor_1, sor_2, sor_3, tet):
    nyeremeny = 0
    if sor_1[0] == sor_2[1] == sor_3[2]:
        nyeremeny += evaluate_row([sor_1[0]], tet)
    if sor_1[2] == sor_2[1] == sor_3[0]:
        nyeremeny += evaluate_row([sor_1[2]], tet)
    return nyeremeny

def display_message(message, color, y_offset=0):
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))
    screen.blit(text, text_rect)

def main():
    while True:
        try:
            balance = int(input("Add meg az egyenleged $-ban: "))
            if balance < 0:
                print("Kérlek, adj meg egy pozitív számot!")
                continue
            break
        except ValueError:
            print("Kérlek, adj meg egy érvényes számot!")

    tet = 0
    playing = True

    while playing:
        # Tisztítsd a képernyőt minden körben
        screen.fill(BLACK)

        # Játék állapot kiírása
        display_message(f"Egyenleg: ${balance}", WHITE, -50)
        display_message(f"Tét: ${tet}", WHITE, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if tet > 0:
                        # Tisztítsd a képernyőt a játékos sorok megjelenítése előtt
                        screen.fill(BLACK)

                        sor_1 = generate_slot_row()
                        sor_2 = generate_slot_row()
                        sor_3 = generate_slot_row()

                        nyeremeny = 0
                        nyeremeny += evaluate_row(sor_1, tet)
                        nyeremeny += evaluate_row(sor_2, tet)
                        nyeremeny += evaluate_row(sor_3, tet)
                        nyeremeny += evaluate_diagonal(sor_1, sor_2, sor_3, tet)

                        balance += nyeremeny

                        # Sorok kiírása
                        display_message(f"Sor 1: {szotar[sor_1[0]]}, {szotar[sor_1[1]]}, {szotar[sor_1[2]]}", GREEN, 50)
                        display_message(f"Sor 2: {szotar[sor_2[0]]}, {szotar[sor_2[1]]}, {szotar[sor_2[2]]}", GREEN, 80)
                        display_message(f"Sor 3: {szotar[sor_3[0]]}, {szotar[sor_3[1]]}, {szotar[sor_3[2]]}", GREEN, 110)

                        if nyeremeny > 0:
                            display_message(f"Nyertél ${nyeremeny}!", GREEN, 140)
                        else:
                            display_message("Nem nyertél semmit.", WHITE, 140)

                        pygame.display.flip()
                        pygame.time.wait(2000)

                if event.key == pygame.K_UP:
                    if balance > 0:
                        tet = min(balance, tet + 1)
                if event.key == pygame.K_DOWN:
                    tet = max(0, tet - 1)

        pygame.display.flip()

        if balance <= 0:
            display_message("Elfogyott az egyenleged!", WHITE, 200)
            pygame.display.flip()
            pygame.time.wait(2)
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Hiba történt: {e}")
        pygame.quit()
