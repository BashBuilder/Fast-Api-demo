import pytest

from app.calculations import BankAccount, add


@pytest.fixture
def bank_account():
  return BankAccount(100)


@pytest.mark.parametrize("num1, num2, expected", [(1, 2, 3), (5, 5, 10)])
def test_add(num1: int, num2: int, expected: int):
  assert add(num1, num2) == expected


def test_bank_set_initial_amount(bank_account: BankAccount):
  assert bank_account.get_balance() == 100


def test_withdraw(bank_account: BankAccount):
  bank_account.withdraw(50)
  assert bank_account.get_balance() == 50


def test_deposit(bank_account: BankAccount):
  bank_account.deposit(50)
  assert bank_account.get_balance() == 150


def test_collect_interest(bank_account: BankAccount):
  bank_account.collect_interest()
  assert bank_account.get_balance() == 200


def test_insufficient_balance(bank_account: BankAccount):
  with pytest.raises(ValueError):
    bank_account.withdraw(200)
