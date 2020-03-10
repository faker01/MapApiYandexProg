import pygame as pg

pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(*event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    return True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        self.txt_surface = FONT.render(self.text, True, self.color)
        return False

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*event.pos):
                return True
        return False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)


class TextDialog:
    def __init__(self, x, y, w, h, text):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.font = pg.font.Font(None, 16)
        self.txt_surface = self.font.render(text, True, self.color)

    def set_text(self, text):
        self.txt_surface = self.font.render(text, True, self.color)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)


class MailAddressUI:

    def __init__(self, x, y, w, h):
        self.state = False
        self.text = ''
        self.w, self.h = w, h
        self.button = pg.Rect(x, y, int(w / 6), h)
        self.rect = pg.Rect(x + int(w / 5), y, int(w / 5 * 4), h)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.button.collidepoint(*event.pos):
                return True
        return False

    def set_text(self, text):
        self.state = bool(self.state and text)
        self.text = text

    def draw(self, screen):
        color = (COLOR_ACTIVE if self.state else COLOR_INACTIVE)
        w, h = self.button.size
        x, y = self.button.x, self.button.y
        size = int(h / 3 * 2)

        slider = pg.Surface((size, size))
        pg.draw.rect(slider, color, pg.Rect(0, 0, size, size))
        screen.blit(slider, (x - size + int((h + size) / 2) + (w + 2 * (size - int((h + size) / 2)) - size) * self.state, y - size + int((h + size) / 2)))
        pg.draw.rect(screen, color, self.button, 2)
        pg.draw.rect(screen, color, self.rect, 2)

        iw, ih = int(self.w / 12), size
        ix, iy = x + self.w - iw - 5, y - ih + int((h + ih) / 2)

        pg.draw.rect(screen, COLOR_INACTIVE, (ix, iy, iw, ih))
        pg.draw.lines(screen, (250, 250, 250), False, (
            (ix, iy), (ix + int(iw / 2), iy + int(ih / 3 * 2)), (ix + iw, iy)
        ), 3)
        pg.draw.line(screen, (250, 250, 250), (ix, iy + ih), (ix + int(iw / 8 * 3), iy + int(ih / 2)), 3)
        pg.draw.line(screen, (250, 250, 250), (ix + int(iw / 8 * 5) + 1, iy + int(ih / 2) + 1), (ix + iw, iy + ih), 3)

        if self.state:
            txt_surface = FONT.render(self.text, True, COLOR_ACTIVE)
            screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def change_state(self):
        self.state = int(not self.state)
