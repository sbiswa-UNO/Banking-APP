from logging import exception

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *
import os
from accounts import Account
import csv


class create_gui(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.user = ""
        self.data = []
        self.dataOnLogin = []

    def initUI(self) -> None:
        self.setWindowTitle("Project 1")
        self.setFixedSize(300, 240)
        self.SCREEN = "MAIN MENU"

        self.errorLabel = QLabel("")
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.errorLabel.setStyleSheet("color: red")

        self.mainMenu = QVBoxLayout()
        self.setMainMenu(self.mainMenu)



        self.setLayout(self.mainMenu)

    def setMainMenu(self, screen: QVBoxLayout) -> None:
        """Create Main Meny screen

        Args:
            screen (QWidget): QVBoxLayout that is being adjusted
        """

        #create layouts
        usernameLayout = QHBoxLayout()
        passwordLayout = QHBoxLayout()

        #create entry labels
        titleLabel = QLabel("Sudeep's Banking")
        titleLabel.setFixedHeight(25)
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        titleLabel.setFont(font)



        usernameLabel = QLabel("Username:")
        passwordLabel = QLabel("Password:")
        usernameLayout.addWidget(usernameLabel)
        passwordLayout.addWidget(passwordLabel)

        #create login entry box
        self.usernameEntry = QLineEdit()
        self.passwordEntry = QLineEdit()
        usernameLayout.addWidget(self.usernameEntry)
        passwordLayout.addWidget(self.passwordEntry)

        #create buttons
        loginButton = QPushButton("Login", self)
        signUpButton = QPushButton("Sign Up", self)

        #connect buttons
        loginButton.clicked.connect(lambda: self.login(screen))
        signUpButton.clicked.connect(lambda: self.changeLayout(screen, "SIGNUP"))

        #add layouts and widgets to screen
        screen.addWidget(titleLabel)
        screen.addLayout(usernameLayout)
        screen.addLayout(passwordLayout)
        screen.addWidget(loginButton)
        screen.addWidget(signUpButton)
        screen.addWidget(self.errorLabel)

    def setsignupScreen(self, screen):
        # create layouts
        usernameLayout = QHBoxLayout()
        passwordLayout = QHBoxLayout()

        # create entry labels
        titleLabel = QLabel("Sign Up")
        titleLabel.setFixedHeight(50)
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        titleLabel.setFont(font)
        usernameLabel = QLabel("Create Username:")
        passwordLabel = QLabel("Create Password:")
        usernameLayout.addWidget(usernameLabel)
        passwordLayout.addWidget(passwordLabel)

        # create login entry box
        self.usernameCEntry = QLineEdit()
        self.passwordCEntry = QLineEdit()
        usernameLayout.addWidget(self.usernameCEntry)
        passwordLayout.addWidget(self.passwordCEntry)

        # create buttons
        signUpButton = QPushButton("Sign Up", self)

        signUpButton.clicked.connect(lambda: self.signUp(screen))

        # add layouts and widgets to screen
        screen.addWidget(titleLabel)
        screen.addLayout(usernameLayout)
        screen.addLayout(passwordLayout)
        screen.addWidget(signUpButton)
        screen.addWidget(self.errorLabel)

    def setDashboardScreen(self, screen: QVBoxLayout) -> None:
        """
        Creates the dashboard screen

        Args:
            screen (QWidget): QVBoxLayout that is being adjusted
        """

        #get data
        output = []
        with (open(f'userData_{self.user}.txt', 'r') as file):
            lines = file.readlines()
            for line in lines:
                output = line.split()
                if len(output) > 1:
                    if output[0] == "user:":
                        self.data.append(output[1])
                    elif output[0] == "balance:":
                        self.data.append(float(output[1]))
                        break
        print(self.data)

        #comparison var to see if data was changed
        self.dataOnLogin = self.data

        #create bank account
        acc = Account(self.data[0], self.data[1])

        #create bal label
        self.balLabel = QLabel(f"Balance: {acc.get_balance()}")


        #create page title
        title = QLabel(f"Dashboard: {self.data[0]}")
        title.setFixedHeight(25)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        title.setFont(font)

        #create amount entry
        amountLayout = QHBoxLayout()
        amountLabel = QLabel("Amount:")
        amountEntry = QLineEdit()
        amountLayout.addWidget(amountLabel)
        amountLayout.addWidget(amountEntry)

        #create and connect buttons
        buttonLayout = QHBoxLayout()
        depositButton = QPushButton("Deposit", self)
        withdrawButton = QPushButton("Withdraw", self)
        depositButton.clicked.connect(lambda: self.deposit(acc, amountEntry.text()))
        withdrawButton.clicked.connect(lambda: self.withdraw(acc, amountEntry.text()))
        buttonLayout.addWidget(depositButton)
        buttonLayout.addWidget(withdrawButton)


        #add to screen
        screen.addWidget(title)
        screen.addWidget(self.balLabel)
        screen.addLayout(amountLayout)
        screen.addLayout(buttonLayout)
        screen.addWidget(self.errorLabel)

    def deposit(self, acc: Account, amountVal: str) -> None:
        """
        deposit the given val to account

        Args:
            acc (Account): Account object that is being deposited to
            amountVal (str): amount to deposit
        """
        try:
            amount = float(amountVal)
            if amount <= 0:
                raise Exception("Amount must be greater than 0")

            acc.deposit(float(amount))
            self.balLabel.setText(f"Balance: {acc.get_balance()}")
            self.data[1] = acc.get_balance()
            self.errorLabel.setText("")
        except ValueError:
            self.errorLabel.setText(f"Please input a valid value")
        except Exception as e:
            self.errorLabel.setText(f"{e}")



    def withdraw(self, acc: Account, amountVal: str):
        """
        withdraw the given val from account

        Args:
            acc (Account): Account object that is being withdrawn from
            amountVal (str): amount to withdraw
        """
        try:
            amount = float(amountVal)

            if amount <= 0:
                raise Exception("Amount must be greater than 0")
            elif amount >= acc.get_balance():
                raise Exception("Amount must be greater than or equal to balance")

            acc.withdraw(float(amount))
            self.balLabel.setText(f"Balance: {acc.get_balance()}")
            self.data[1] = acc.get_balance()
            self.errorLabel.setText("")
        except ValueError:
            self.errorLabel.setText("Please input a valid value")
        except Exception as e:
            self.errorLabel.setText(f"{e}")

    def saveData(self) -> None:
        """
        Saves user data
        """
        if len(self.data) >= 2:
            print("started save data")
            try:
                with open(f'userData_{self.data[0]}.txt', 'r+') as file:
                    lines = file.readlines()
                    lines[2] = f'balance: {self.data[1]}\n'
                    file.seek(0)
                    file.writelines(lines)
                    file.truncate()
                    file.close()
                print("finished save data")
            except Exception as e:
                print(f"Error saving data: {e}")

    def login(self, screen: QVBoxLayout) -> None:
        """
        Checks given login credentials and changes screen if logins are valid

        Args:
            screen (QWidget): QVBoxLayout/screen that is being adjusted
        """
        try:
            if self.usernameEntry.text() == "" or self.passwordEntry.text() == "":
                raise Exception("Please enter both username and password")

            output = []
            with open(f'users.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    output = line.split()
                if len(output) > 0:
                    if output[1] == self.usernameEntry.text() and output[3] == self.passwordEntry.text():
                        self.user = self.usernameEntry.text()
                        self.changeLayout(screen, "DASHBOARD")
                    else:
                        raise Exception("Username or password is incorrect.")
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            self.errorLabel.setText(f"{e}")

        else:
            file.close()

    def signUp(self, screen: QVBoxLayout) -> None:
        """
        if user gives valid account credentials, user is created using given credentials

        Args:
            screen (QWidget): QVBoxLayout/screen that is being adjusted
        """
        print("being called")
        try:
            if self.usernameCEntry.text() == "" or self.passwordCEntry.text() == "":
                raise Exception("Please enter both username and password")
            output = []
            current_directory = os.getcwd()

            userFileFound = False
            for file in os.listdir(current_directory):
                if file == "users.txt":
                    userFileFound = True
            if not userFileFound:
                with open(f'users.txt', 'w') as file:
                    file.write("users:")

            with open(f'users.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    output = line.split()
            if len(output) > 2:
                if output[1] == self.usernameCEntry.text():
                    raise Exception("Username already exists.")
            file.close()

            with open(f'users.txt', 'a') as file:
                file.write(f'user: {self.usernameCEntry.text()} pass: {self.passwordCEntry.text()}\n')
            file.close()


            userDataFound = False
            for osfile in os.listdir(current_directory):
                if osfile == f'userData_{self.usernameCEntry.text()}.txt':
                    userDataFound = True

            if not userDataFound:
                with open(f'userData_{self.usernameCEntry.text()}.txt', 'a') as file:
                    file.write(f'user: {self.usernameCEntry.text()}\n')
                    file.write(f'pass: {self.passwordCEntry.text()}\n')
                    file.write("balance: 0\n")
            file.close()

            self.user = self.usernameCEntry.text()
            self.changeLayout(screen, "DASHBOARD")
        except FileNotFoundError:
            print("File not found")
        except Exception  as e:
            print("There was a error logging in.\nUser may already exist.")
            self.errorLabel.setText(f'{e}')
        else:
            file.close()

    def changeLayout(self, screen: QVBoxLayout, layout: str) -> None:
        """
        Changes the screen that is being displayed to the user

        Args:
            screen (QWidget): QVBoxLayout/screen that is being adjusted
            layout (str): the screen being displayed to user
        """
        self.clearLayout(screen)
        if layout == "MAIN MENU":
            self.setMainMenu(self.mainMenu)
            self.errorLabel.setText("")
        elif layout == "SIGNUP":
            self.setsignupScreen(self.mainMenu)
            self.errorLabel.setText("")
        elif layout == "DASHBOARD":
            self.setDashboardScreen(self.mainMenu)
            self.errorLabel.setText("")

    def clearLayout(self, screen) -> None:
        """
        Clears everything from the layout except the error message label

        Args:
            screen (QWidget): QVBoxLayout/screen that is being adjusted
        """
        while screen.count():
            item = screen.takeAt(0)
            if not(item.widget() == self.errorLabel) and item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clearLayout(item.layout())
                item.layout().deleteLater()


