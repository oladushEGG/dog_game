import pygame as pg
import random
pg.init()

SCR_W = 900
SCR_H = 550
BTN_W = 150
BTN_H = 60
ICO_S = 80
PADD = 10

DOG_W = 300
DOG_H = 455

MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 130

FOOD_SIZE = 200
TOY_SIZE = 100

font = pg.font.Font(None, 40)
font_mini = pg.font.Font(None, 15)

def load_images(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))
    return image

def text_render(text):
    return font.render(str(text), True, (0,0,0))

class Button:
    def __init__(self, text, x, y, width = BTN_W, height = BTN_H, text_font = font, func = None):
        self.func = func
        self.idle_img = load_images("images/button.png", width, height)
        self.pressed_img = load_images("images/button_clicked.png", width, height)
        self.image = self.idle_img
        self.rect = self.image.get_rect()
        self.rect.topright = (x, y)
        self.is_pressed = False
        self.text_font = text_font
        self.text = text_font.render(str(text), True, (0, 0, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_img
            else:
                self.image = self.idle_img

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.func()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False

class Item:
    def __init__(self, name, price, file, is_bought=False, is_put_on=False):
        self.name = name
        self.price = price
        self.is_bought = is_bought
        self.is_put_on = is_put_on

        self.image = load_images(file, DOG_W // 1.7, DOG_H // 1.7)
        self.full_img = load_images(file, DOG_W, DOG_H)

class ClothesMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_images("images/menu/menu_page.png", SCR_W, SCR_H)

        self.bottom_label_off = load_images("images/menu/bottom_label_off.png", SCR_W, SCR_H)
        self.bottom_label_on = load_images("images/menu/bottom_label_on.png", SCR_W, SCR_H)
        self.top_label_off = load_images("images/menu/top_label_off.png", SCR_W, SCR_H)
        self.top_label_on = load_images("images/menu/top_label_on.png", SCR_W, SCR_H)

        self.items = [Item("Синяя футболка", 10, "images/items/blue t-shirt.png"),
                      Item("Ботинки", 50, "images/items/boots.png"),
                      Item("Шляпа", 50, "images/items/hat.png")]

        self.current_item = 0
        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCR_W // 2, SCR_H // 2)

        self.next_btn = Button("Вперёд", SCR_W - MENU_NAV_XPAD*1.3, SCR_H - MENU_NAV_YPAD,
                                width=int(BTN_W // 1.2), height=int(BTN_H // 1.2), func=self.to_next)
        self.back_btn = Button("Назад", MENU_NAV_XPAD + BTN_W, SCR_H - MENU_NAV_YPAD,
                                width=int(BTN_W // 1.2), height=int(BTN_H // 1.2), func=self.to_previous)
        self.wear_btn = Button("Надеть", MENU_NAV_XPAD + BTN_W, SCR_H - MENU_NAV_YPAD - BTN_H,
                                width=int(BTN_W // 1.2), height=int(BTN_H // 1.2), func=self.wear)
        self.buy_btn = Button("Купить", SCR_W//2 + (BTN_W//2 - 10), SCR_H - MENU_NAV_YPAD - BTN_H,
                                width=int(BTN_W // 1.2), height=int(BTN_H // 1.2), func=self.buy)
        
        self.buttons_m = [self.next_btn, self.back_btn, self.wear_btn, self.buy_btn]

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCR_W // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCR_W // 2, 120)

        self.use_text = text_render("Надето")
        self.use_text_rect = self.use_text.get_rect()
        self.use_text_rect.midleft = (SCR_W // 1.39, 130)

        self.buy_text = text_render("Куплено")
        self.buy_text_rect = self.buy_text.get_rect()
        self.buy_text_rect.midleft = (SCR_W // 1.39, 200)
        
    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCR_W // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCR_W // 2, 120)

    def to_previous(self):
        if self.current_item != len(self.items) + 1:
            self.current_item -= 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCR_W // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCR_W // 2, 120)

    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True

    def wear(self):
        self.items[self.current_item].is_put_on = not self.items[self.current_item].is_put_on and self.items[self.current_item].is_bought

    def update(self):
        for btn in self.buttons_m:
                btn.update()

    def is_clicked(self, event):
        for btn in self.buttons_m:
                btn.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))
        screen.blit(self.items[self.current_item].image, self.item_rect)

        if self.items[self.current_item].is_put_on:
                screen.blit(self.top_label_on, (0, 0))
                screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.top_label_off, (0, 0))
            if self.items[self.current_item].is_bought:
                screen.blit(self.bottom_label_on, (0, 0))
            else:
                screen.blit(self.bottom_label_off, (0, 0))
        
        for btn in self.buttons_m:
                btn.draw(screen)
                
        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.use_text, self.use_text_rect)
        screen.blit(self.buy_text, self.buy_text_rect)

class Food:
    def __init__(self, name, price, file, satiety, medicine_pwr = 0):
        self.name = name
        self.price = price
        self.satiety = satiety
        self.medicine_pwr = medicine_pwr
        self.image = load_images(file, FOOD_SIZE, FOOD_SIZE)

class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_images("images/menu/menu_page.png", SCR_W, SCR_H)

        self.bottom_label_off = load_images("images/menu/bottom_label_off.png", SCR_W, SCR_H)
        self.bottom_label_on = load_images("images/menu/bottom_label_on.png", SCR_W, SCR_H)
        self.top_label_off = load_images("images/menu/top_label_off.png", SCR_W, SCR_H)
        self.top_label_on = load_images("images/menu/top_label_on.png", SCR_W, SCR_H)

        self.items = [Food("Мясо", 30, "images/food/meat.png", 10),
                      Food("Корм", 40, "images/food/dog_food.png", 15),
                      Food("Элитный корм", 100, "images/food/dog_food_elite.png", 25, medicine_pwr=2),
                      Food("Лекарство", 200, "images/food/medicine.png", 0, medicine_pwr=10)]

        self.current_item = 0
        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCR_W // 2, SCR_H // 2)

        self.next_btn = Button("Вперёд", SCR_W - MENU_NAV_XPAD*1.3, SCR_H - MENU_NAV_YPAD,
                                width=int(BTN_W // 1.2), height=int(BTN_H // 1.2), func=self.to_next)
        self.back_btn = Button("Назад", MENU_NAV_XPAD + BTN_W, SCR_H - MENU_NAV_YPAD,
                                width=int(BTN_W // 1.2), height=int(BTN_H // 1.2), func=self.to_previous)
        self.buy_btn = Button("Съесть", SCR_W//2 + (BTN_W//2 - 10), SCR_H - MENU_NAV_YPAD - BTN_H,
                                width=int(BTN_W // 1.2), height=int(BTN_H // 1.2), func=self.buy)
        
        self.buttons_m = [self.next_btn, self.back_btn, self.buy_btn]

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCR_W // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCR_W // 2, 120)
        
    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCR_W // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCR_W // 2, 120)

    def to_previous(self):
        if self.current_item != len(self.items) + 1:
            self.current_item -= 1

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCR_W // 2, 180)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCR_W // 2, 120)

    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.game.satiety += self.items[self.current_item].satiety
            self.game.health += self.items[self.current_item].medicine_pwr
            if self.game.satiety > 100:
                self.game.satiety = 100
            if self.game.health > 100:
                self.game.health = 100

    def update(self):
        for btn in self.buttons_m:
                btn.update()

    def is_clicked(self, event):
        for btn in self.buttons_m:
                btn.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))
        screen.blit(self.items[self.current_item].image, self.item_rect)

        self.next_btn.draw(screen)
        self.back_btn.draw(screen)
        self.buy_btn.draw(screen)

        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)

class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.toy_0 = load_images("images/toys/ball.png", TOY_SIZE, TOY_SIZE)
        self.toy_1 = load_images("images/toys/blue bone.png", TOY_SIZE, TOY_SIZE)
        self.toy_2 = load_images("images/toys/red bone.png", TOY_SIZE, TOY_SIZE)
        self.toys_img = [self.toy_0, self.toy_1, self.toy_2]
        self.image = self.toys_img[random.randint(0, 2)]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCR_W)
        
        
    def update(self):
        self.rect.y += 1


class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_images("images/dog.png", DOG_W // 2, DOG_H // 2)
        self.rect = self.image.get_rect()
        
    def update(self):
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_a]:
            if self.rect.left >= 90:
                self.rect.x -= 1
            else:
                self.rect.x = 89
        if self.keys[pg.K_d]:
            if self.rect.right <= 810:
                self.rect.x += 1
            else:
                self.rect.x = 670

class MiniGame:
    def __init__(self, game):
        self.game = game
        self.background = load_images("images/game_background.png", SCR_W, SCR_H)

        self.dog = Dog()
        self.toys_group = pg.sprite.Group() 
        self.gm = Game()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5

    def new_game(self):
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5
        self.dog.rect.x = 375
        self.happiness_added = False

    def update(self):
        self.dog.update()
        self.toys_group.update()
        if random.randint(0, 500) == 0:
            self.toys_group.add(Toy())
        hits = pg.sprite.spritecollide(self.dog, self.toys_group, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)
        
        if pg.time.get_ticks() - self.start_time > self.interval and not self.happiness_added:
            self.game.happiness += int(self.score // 2)
            if self.game.happiness > 100:
                self.game.happiness = 100
            self.happiness_added = True 
            self.game.mode = "Main"

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(text_render(self.score), (MENU_NAV_XPAD + 20, 80))
        screen.blit(self.dog.image, (self.dog.rect.x, 300))
        for toy in self.toys_group:
            screen.blit(toy.image, (toy.rect.x, toy.rect.y))


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCR_W, SCR_H), pg.RESIZABLE)
        pg.display.set_caption("Виртуальный питомец")

        self.happiness = 100
        self.satiety = 100
        self.health = 100
        self.money = 0
        self.coins_per_click = 1
        self.coins_per_second = 1

        self.background = load_images("images/background.png", SCR_W, SCR_H)
        self.happiness_img = load_images("images/happiness.png", ICO_S, ICO_S)
        self.satiety_img = load_images("images/satiety.png", ICO_S, ICO_S)
        self.health_img = load_images("images/health.png", ICO_S, ICO_S)
        self.money_img = load_images("images/money.png", ICO_S, ICO_S)
        self.dog_img = load_images("images/dog.png", DOG_W, DOG_H)

        button_x = SCR_W - PADD
        self.eat_btn = Button("Еда", button_x, PADD + ICO_S, func=self.food_menu_on)
        self.cloth_btn = Button("Одежда", button_x, PADD + ICO_S*2, func=self.clothes_menu_on)
        self.game_btn = Button("Игры", button_x, PADD + ICO_S*3, func=self.game_on)

        self.upgrade_btn = Button("Улучшить", SCR_W - PADD, 0, width=BTN_W//2, height=BTN_H//3, text_font=font_mini, func=self.increase_money)
        self.buttons = [self.eat_btn, self.cloth_btn, self.game_btn, self.upgrade_btn]

        self.clothes_menu = ClothesMenu(self)
        self.food_menu = FoodMenu(self)
        self.mini_game = MiniGame(self)
        
        self.costs_of_upgrade = {100: False, 1000: False, 5000: False, 10000: False}

        self.mode = "Main"


        self.INCREACE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREACE_COINS, 1000)
        self.DECREASE = pg.USEREVENT + 2
        pg.time.set_timer(self.DECREASE, 1000)
        

        self.run()

    def clothes_menu_on(self):
        self.mode = "Clothes menu"

    def food_menu_on(self):
        self.mode = "Food menu"

    def game_on(self):
        self.mode = "Mini game"
        self.mini_game.new_game()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def increase_money(self):
        for cost, is_upgraded in self.costs_of_upgrade.items():
            if not is_upgraded and self.money >= cost:
                self.coins_per_second += 2
                self.coins_per_click += 1
                self.money -= cost
                self.costs_of_upgrade[cost] = True

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = "Main"

            for btn in self.buttons:
                btn.is_clicked(event)
            
            if event.type == self.INCREACE_COINS:
                self.money += self.coins_per_second

            if event.type == self.DECREASE:
                chance = random.randint(1, 10)
                if chance <= 5:
                    self.satiety -= 1
                elif 5 < chance <= 9:
                    self.happiness -= 1
                else:
                    self.health -= 1

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money += self.coins_per_second

            if self.mode == "Clothes menu":
                self.clothes_menu.is_clicked(event)
            if self.mode == "Food menu":
                self.food_menu.is_clicked(event)
                



    def update(self):
        for btn in self.buttons:
            btn.update()
        self.clothes_menu.update()
        self.food_menu.update()
        self.mini_game.update()
        

    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.happiness_img, (PADD, PADD))
        self.screen.blit(self.satiety_img, (PADD, ICO_S + PADD))
        self.screen.blit(self.health_img, (PADD, ICO_S*2 + PADD))
        self.screen.blit(self.money_img, (SCR_W - (ICO_S + PADD), PADD))
        self.screen.blit(self.dog_img, (SCR_W/2 - DOG_W/2, SCR_H/2 - DOG_H/2))
        self.screen.blit(text_render(self.happiness), (PADD + ICO_S, self.happiness_img.get_rect().centerx))
        self.screen.blit(text_render(self.satiety), (PADD + ICO_S, ICO_S + self.satiety_img.get_rect().centerx))
        self.screen.blit(text_render(self.health), (PADD + ICO_S, ICO_S*2 + self.health_img.get_rect().centerx))
        self.screen.blit(text_render(self.money), (SCR_W - (PADD*2 + ICO_S + 23), self.money_img.get_rect().centerx))
        for btn in self.buttons:
                btn.draw(self.screen)
        for item in self.clothes_menu.items:
            if item.is_put_on:
                self.screen.blit(item.full_img, (SCR_W // 2 - DOG_W // 2, 50))
        if self.mode == "Clothes menu":
            self.clothes_menu.draw(self.screen)
        if self.mode == "Food menu":
            self.food_menu.draw(self.screen)
        if self.mode == "Mini game":
            self.mini_game.draw(self.screen)
        pg.display.flip()


if __name__ == "__main__":
    Game()
