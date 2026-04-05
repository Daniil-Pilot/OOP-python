class BankServer:
    def __init__(self):
        self.accounts = {
            '1001': {'pin': '1234', 'balance': 5000.0},
            '1002': {'pin': '5678', 'balance': 1500.0},
            '1003': {'pin': '9012', 'balance': 300.0}
        }

    def authenticate(self, card_number, pin):
        if card_number in self.accounts:
            return self.accounts[card_number]['pin'] == pin
        return False

    def get_balance(self, card_number):
        return self.accounts[card_number]['balance']

    def withdraw(self, card_number, amount):
        if amount > 0 and self.accounts[card_number]['balance'] >= amount:
            self.accounts[card_number]['balance'] -= amount
            return True
        return False


class CardReader:
    def read_card(self):
        return input("Введите номер карты: ")


class CashDispenser:
    def dispense(self, amount):
        print("Выдано наличных:", amount)


class CheckPrinter:
    def print_receipt(self, message):
        print("Чек:", message)


class ATM:
    def __init__(self, server, reader, dispenser, printer):
        self.server = server
        self.reader = reader
        self.dispenser = dispenser
        self.printer = printer

    def start(self):
        print("Банкомат запущен.")
        card = self.reader.read_card()
        pin = input("Введите PIN-код: ")

        if not self.server.authenticate(card, pin):
            print("Ошибка: неверный номер карты или PIN-код.")
            return

        print("Аутентификация успешна.")
        while True:
            print("1. Проверить баланс")
            print("2. Снять наличные")
            print("3. Выход")
            choice = input("Выберите операцию: ")

            if choice == '1':
                balance = self.server.get_balance(card)
                self.printer.print_receipt("Текущий баланс: " + str(balance))
            elif choice == '2':
                try:
                    amount = float(input("Введите сумму для снятия: "))
                    if self.server.withdraw(card, amount):
                        self.dispenser.dispense(amount)
                        balance = self.server.get_balance(card)
                        self.printer.print_receipt("Снято: " + str(amount) + ". Остаток: " + str(balance))
                    else:
                        print("Ошибка: недостаточно средств или неверная сумма.")
                except ValueError:
                    print("Ошибка: введите корректное число.")
            elif choice == '3':
                print("Завершение работы банкомата.")
                break
            else:
                print("Ошибка: неверный выбор.")


class Operator:
    def __init__(self, server):
        self.server = server

    def show_accounts(self):
        print("Список счетов:")
        for card, data in self.server.accounts.items():
            print("Карта:", card, "| PIN:", data['pin'], "| Баланс:", data['balance'])


def main():
    server = BankServer()
    atm = ATM(server, CardReader(), CashDispenser(), CheckPrinter())
    operator = Operator(server)

    while True:
        print("\nВыберите роль:")
        print("1. Клиент (Банкомат)")
        print("2. Оператор")
        print("3. Выход")
        role = input("Ваш выбор: ")

        if role == '1':
            atm.start()
        elif role == '2':
            operator.show_accounts()
        elif role == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()