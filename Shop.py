from datetime import datetime, timedelta
from operator import invert


# Родительский класс
class Product:
    def __init__(self, name: str, price: float, quantity: int):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(price, (int, float)) or price < 0:
            raise TypeError("Price must be a non-negative number")
        if not isinstance(quantity, int) or quantity < 0:
            raise TypeError("Quantity must be a non-negative integer")
        self.name = name
        self.price = price
        self.quantity = quantity

    def is_available(self, requested_quantity: int) -> bool:
        if not isinstance(requested_quantity, int) or requested_quantity <= 0:
            raise ValueError("Requested quantity must be a positive integer")
        return self.quantity >= requested_quantity

    def reduce_quantity(self, requested_quantity: int) -> None:
        if self.is_available(requested_quantity):
            self.quantity -= requested_quantity
        else:
            raise ValueError(f"Not enough {self.name} in stock.")

# Продукты питания
class FoodProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, proteins: float, fats: float, carbohydrates: float, calories: int):
        super().__init__(name, price, quantity)
        if not all(isinstance(nutrient, (int, float)) and nutrient >= 0 for nutrient in [proteins, fats, carbohydrates]):
            raise TypeError("Proteins, fats, and carbs must be non-negative numbers")
        if not isinstance(calories, int) or calories < 0:
            raise TypeError("Calories must be a non-negative integer")
        self.proteins = proteins
        self.fats = fats
        self.carbohydrates = carbohydrates
        self.calories = calories

# Скоропортящиеся товары
class PerishableProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, creation_date: datetime, expiration_period: int):
        super().__init__(name, price, quantity)
        if not isinstance(creation_date, datetime):
            raise TypeError("Creation date must be a datetime object")
        if not isinstance(expiration_period, int) or expiration_period < 0:
            raise TypeError("Expiration period must be a non-negative integer")
        self.creation_date = creation_date
        self.expiration_period = expiration_period

    def is_expired(self) -> bool:
        expiration_date = self.creation_date + timedelta(days=self.expiration_period)
        return expiration_date < datetime.now()

    def expires_in_less_than_24_hours(self) -> bool:
        expiration_date = self.creation_date + timedelta(days=self.expiration_period)
        return expiration_date <= datetime.now() + timedelta(hours=24)

# Витамины
class Vitamin(Product):
    def __init__(self, name: str, price: float, quantity: int, prescription_required: bool):
        super().__init__(name, price, quantity)
        if not isinstance(prescription_required, bool):
            raise TypeError("Prescription required must be a boolean value")
        self.prescription_required = prescription_required

# Корзина пользователя
class Cart:
    def __init__(self):
        self.items = []
        self.total_proteins = 0.0
        self.total_fats = 0.0
        self.total_carbohydrates = 0.0
        self.total_calories = 0.0
        self.total_price = 0.0

    def add_item(self, product: Product, quantity: int):
        if not isinstance(product, Product):
            raise TypeError("Item must be a Product instance")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

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
            self.total_carbohydrates += product.carbohydrates * quantity
            self.total_calories += product.calories * quantity

    def check_PFC_limits(self, max_proteins: float, max_fats: float, max_carbohydrates: float, max_calories: int):
        if not all(isinstance(limit, (int, float)) and limit >= 0 for limit in [max_proteins, max_fats, max_carbohydrates]):
            raise ValueError("BJU limits must be non-negative numbers")
        if not isinstance(max_calories, int) or max_calories < 0:
            raise ValueError("Calorie limit must be a non-negative integer")

        if (self.total_proteins > max_proteins or
                self.total_fats > max_fats or
                self.total_carbohydrates > max_carbohydrates or
                self.total_calories > max_calories):
            raise ValueError("Exceeded PFC or calorie limits.")

    def calculate_total(self) -> float:
        return self.total_price

# Управление складом
class InventoryManager:
    def __init__(self, products: list[Product]):
        if not all(isinstance(product, Product) for product in products):
            raise TypeError("All items in products list must be instances of Product")
        self.products = products

    def generate_restock_list(self) -> list[Product]:
        return [product for product in self.products if product.quantity == 0]

    def generate_disposal_list(self) -> list[Product]:
        return [product for product in self.products if isinstance(product, PerishableProduct) and product.is_expired()]


# watermelon = FoodProduct("Watermelon", 100, 100, 100, 100, 100, 100)
# vitamin = Vitamin('C', 200, 200, True)
# eggs = PerishableProduct('Eggs', 50, 50, datetime(2024, 9, 18), 50)
# cart = Cart()
# cart.add_item(eggs, 20)
# cart.add_item(vitamin, 100)
# cart.add_item(watermelon, 10)
# cart.check_PFC_limits(100, 100, 100, 1000)
# print("total", cart.calculate_total())
# inventory = InventoryManager([watermelon, vitamin, eggs])
# print("Restock list:", [item.name for item in inventory.generate_restock_list()])
# print("Disposal list:", [item.name for item in inventory.generate_disposal_list()])