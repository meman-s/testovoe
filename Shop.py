from datetime import datetime, timedelta


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def is_available(self, requested_quantity):
        return self.quantity >= requested_quantity

    def reduce_quantity(self, requested_quantity):
        if self.is_available(requested_quantity):
            self.quantity -= requested_quantity
        else:
            raise ValueError(f"Not enough {self.name} in stock.")


class FoodProduct(Product):
    def __init__(self, name, price, quantity, proteins, fats, carbohydrates, calories):
        super().__init__(name, price, quantity)
        self.proteins = proteins
        self.fats = fats
        self.carbs = carbohydrates
        self.calories = calories


class PerishableProduct(Product):
    def __init__(self, name, price, quantity, creation_date, expiration_period):
        super().__init__(name, price, quantity)
        self.creation_date = creation_date
        self.expiration_period = expiration_period

    def is_expired(self):
        expiration_date = self.creation_date + timedelta(days=self.expiration_period)
        return expiration_date < datetime.now()

    def expires_in_less_than_24_hours(self):
        expiration_date = self.creation_date + timedelta(days=self.expiration_period)
        return expiration_date <= datetime.now() + timedelta(hours=24)


class Vitamin(Product):
    def __init__(self, name, price, quantity, prescription_required):
        super().__init__(name, price, quantity)
        self.prescription_required = prescription_required


class Cart:
    def __init__(self):
        self.items = []
        self.total_proteins = 0
        self.total_fats = 0
        self.total_carbs = 0
        self.total_calories = 0
        self.total_price = 0

    def add_item(self, product, quantity):
        if not product.is_available(quantity):
            raise ValueError(f"{product.name} is out of stock.")
        if isinstance(product, PerishableProduct) and product.expires_in_less_than_24_hours():
            raise ValueError(f"{product.name} will expire in less than 24 hours.")
        if isinstance(product, Vitamin) and product.prescription_required:
            raise ValueError(f"{product.name} requires a prescription.")

        product.reduce_quantity(quantity)
        self.items.append((product, quantity))
        self.total_price += product.price * quantity

        if isinstance(product, FoodProduct):
            self.total_proteins += product.proteins * quantity
            self.total_fats += product.fats * quantity
            self.total_carbs += product.carbs * quantity
            self.total_calories += product.calories * quantity

    def check_PFC_limits(self, max_proteins, max_fats, max_carbs, max_calories):
        if (self.total_proteins > max_proteins or
                self.total_fats > max_fats or
                self.total_carbs > max_carbs or
                self.total_calories > max_calories):
            raise ValueError("Exceeded PFC or calorie limits.")

    def calculate_total(self):
        return self.total_price


class InventoryManager:
    def __init__(self, products):
        self.products = products

    def generate_restock_list(self):
        return [product for product in self.products if product.quantity == 0]

    def generate_disposal_list(self):
        return [product for product in self.products if isinstance(product, PerishableProduct) and product.is_expired()]
