def add(num1: int, num2: int) -> int:
  return num1 + num2


class BankAccount:
  def __init__(self, balance: int) -> None:
    self.balance = balance

  def deposit(self, amount: int) -> None:
    self.balance += amount

  def withdraw(self, amount: int) -> None:
    if self.balance < amount:
      raise ValueError("Insufficient balance")
    self.balance -= amount

  def get_balance(self) -> int:
    return self.balance

  def collect_interest(self) -> None:
    self.balance *= 2
