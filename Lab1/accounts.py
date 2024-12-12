class Account:
    """
    Represents a bank account with basic operations like deposit, withdrawal, and balance inquiry.

    Attributes:
        __account_name (str): The name of the account holder.
        __account_balance (float): The current balance of the account.
    """
    def __init__(self, name: str, balance: float=0) -> None:
        """
        Initializes a new account with a name and an optional initial balance.

        Args:
            name (str): The name of the account holder.
            balance (float, optional): The initial account balance. Defaults to 0.
        """
        self.__account_name = name
        self.__account_balance = max(balance, 0)
        self.set_balance(balance)

    def deposit(self, amount: float) -> bool:
        """
        Deposits a specified amount into the account.

        Args:
            amount (float): The amount to deposit.

        Returns:
            bool: True if the deposit is successful, False otherwise.
        """
        if amount > 0:
            self.__account_balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """
        Withdraws a specified amount from the account.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            bool: True if the withdrawal is successful, False otherwise.
        """
        if 0 < amount <= self.__account_balance:
            self.__account_balance -= amount
            return True
        return False

    def get_balance(self) -> float:
        """
        Retrieves the current account balance.

        Returns:
            float: The account balance.
        """
        return self.__account_balance

    def get_name(self) -> str:
        """
        Retrieves the account holder's name.

        Returns:
            str: The account name.
        """
        return self.__account_name

    def set_balance(self, value: float) -> None:
        """
        Sets the account balance, ensuring it is not negative.

        Args:
            value (float): The new balance value.
        """
        self.__account_balance = max(value, 0)

    def set_name(self, value: str) -> None:
        """
        Sets the account holder's name.

        Args:
            value (str): The new account name.
        """
        self.__account_name = value

    def __str__(self) -> str:
        """
        Returns a string representation of the account.

        Returns:
            str: A string describing the account.
        """
        return f"Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}"

class SavingAccount(Account):
    """
    Represents a savings account with additional features like minimum balance and interest application.

    Attributes:
        MINIMUM (float): The minimum balance required for the savings account.
        RATE (float): The interest rate applied to the account balance.
    """
    MINIMUM = 100
    RATE = 0.02

    def __init__(self, name: str) -> None:
        """
        Initializes a new savings account with a name and default minimum balance.

        Args:
            name (str): The name of the account holder.
        """
        super().__init__(name, SavingAccount.MINIMUM)
        self.__deposit_count = 0

    def apply_interest(self) -> None:
        """
         Applies interest to the account balance if the deposit count threshold is reached.
        """
        if self.__deposit_count >= 5:
            self.set_balance(self.get_balance() * (1 + SavingAccount.RATE))
            self.__deposit_count = 0

    def deposit(self, amount: float) -> bool:
        """
        Deposits a specified amount into the account and applies interest if applicable.

        Args:
            amount (float): The amount to deposit.

        Returns:
            bool: True if the deposit is successful, False otherwise.
        """
        if amount > 0:
            self.__deposit_count += 1
            successful = super().deposit(amount)
            if self.__deposit_count >= 5:
                self.apply_interest()
            return successful
        return False

    def withdraw(self, amount: float) -> bool:
        """
        Withdraws a specified amount from the account, ensuring the minimum balance is maintained.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            bool: True if the withdrawal is successful, False otherwise.
        """
        if 0 < amount <= (self.get_balance() - SavingAccount.MINIMUM):
            return super().withdraw(amount)
        return False

    def set_balance(self, value: float) -> None:
        """
        Sets the account balance, ensuring it is not less than the minimum balance.

        Args:
            value (float): The new balance value.
        """
        super().set_balance(max(value, SavingAccount.MINIMUM))

    def __str__(self) -> str:
        """
        Returns a string representation of the savings account.

        Returns:
            str: A string describing the savings account.
        """
        return f"SAVINGS ACCOUNT: Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}"