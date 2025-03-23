from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QDialog, QFormLayout, QCheckBox, QListWidgetItem, QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont, QColor, QFontMetrics, QPixmap
import sys
import pickle
import smtplib
import random
import asyncio
from qasync import QEventLoop, asyncSlot
import socket

chat_data = {}  # Structure of the data = {"Personal_Chat": [{"Message": "", "Time": "", "Sender_email": "", "Reciever_email": ""}], "Group_Chat": [{"Message": "", "Time": "", "Sender_email": "", "Group_Name": ""}]}
email_id = ""

def get_ipv4_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        return f"Unable to get IP Address: {e}"
    
async def test():
    print("Test Started")
    for i in range(10):
        print(i+1)
        await asyncio.sleep(1)
    print("Test Ended")
    
def send_otp(email):
    otp = random.randint(100000, 999999)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("snapwave.social@gmail.com", "ldzv jwmh egas hxpq")
        subject = "Your OTP Code"
        body = f"Your OTP is {otp}"
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail("snapwave.social@gmail.com", email, message)
        server.quit()
        return otp
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Sign-Up")
        self.setGeometry(400, 200, 400, 450)
        self.setStyleSheet("background-color: white;")

        self.layout = QVBoxLayout()

        # Create back button
        self.back_button = QPushButton("← Back")
        self.back_button.setStyleSheet(
            "background-color: white; color: green; font-weight: bold; padding: 5px; border: 2px solid green; border-radius: 8px;"
        )
        self.back_button.setFixedWidth(80)
        self.back_button.clicked.connect(self.show_main_page)
        self.back_button.hide()

        # Add header
        self.header = QLabel("Welcome to MyApp")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
        self.layout.addWidget(self.header)

        # Add logo (optional)
        self.logo = QLabel()
        pixmap = QPixmap("Logo.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.logo.setText("Logo")
            self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setStyleSheet("padding: 10px; border: 2px solid green; border-radius: 8px;")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; border: 2px solid green; border-radius: 8px;")

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 10px; border: 2px solid green; border-radius: 8px;")

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.setStyleSheet("color: green;")
        self.show_password_checkbox.stateChanged.connect(self.show_password)

        # Create login and signup buttons as persistent widgets
        self.login_page_open_button = QPushButton("Login")
        self.login_page_open_button.setStyleSheet(
            "background-color: green; color: white; font-weight: bold; padding: 10px; border: none; border-radius: 8px;"
        )
        
        self.signup_page_open_button = QPushButton("Sign-Up")
        self.signup_page_open_button.setStyleSheet(
            "background-color: white; color: green; font-weight: bold; padding: 10px; border: 2px solid green; border-radius: 8px;"
        )

        self.layout.addWidget(self.login_page_open_button)
        self.layout.addWidget(self.signup_page_open_button)

        self.setLayout(self.layout)

        self.login_page_open_button.clicked.connect(self.login_page_open)
        self.signup_page_open_button.clicked.connect(self.signup_page_open)
        self.tasks = []

    def clear_layout(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.hide()

    def reset_inputs(self):
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()

    def show_password(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(0)
            self.confirm_password_input.setEchoMode(0)
        else:
            self.password_input.setEchoMode(2)
            self.confirm_password_input.setEchoMode(2)
    
    def show_main_page(self):
        self.clear_layout(self.layout)

        self.reset_inputs()
        self.back_button.hide()

        self.header.show()
        self.logo.show()
        self.login_page_open_button.show()
        self.signup_page_open_button.show()

    def login_page_open(self):
        self.clear_layout(self.layout)

        self.reset_inputs()
        self.back_button.show()
        self.back_button.raise_()

        self.layout.addWidget(self.back_button)
        self.email_input.show()
        self.password_input.show()
        self.show_password_checkbox.show()

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet(
            "background-color: green; color: white; font-weight: bold; padding: 10px; border: none; border-radius: 8px;"
        )
        
        self.forget_password_button = QPushButton("Forget Password")
        self.forget_password_button.setStyleSheet(
            "background-color: white; color: green; font-weight: bold; padding: 10px; border: 2px solid green; border-radius: 8px;"
        )

        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(QLabel("Password:"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.show_password_checkbox)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.forget_password_button)

        self.setLayout(self.layout)

        self.login_button.clicked.connect(self.login)
        self.forget_password_button.clicked.connect(self.forget_password)

    def signup_page_open(self):
        self.clear_layout(self.layout)

        self.reset_inputs()
        self.back_button.show()
        self.back_button.raise_()

        self.layout.addWidget(self.back_button)
        self.email_input.show()
        self.password_input.show()
        self.confirm_password_input.show()
        self.show_password_checkbox.show()

        self.sign_up_button = QPushButton("Sign-Up")
        self.sign_up_button.setStyleSheet(
            "background-color: green; color: white; font-weight: bold; padding: 10px; border: none; border-radius: 8px;"
        )

        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(QLabel("Password:"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(QLabel("Confirm Password:"))
        self.layout.addWidget(self.confirm_password_input)
        self.layout.addWidget(self.show_password_checkbox)
        self.layout.addWidget(self.sign_up_button)

        self.setLayout(self.layout)

        self.sign_up_button.clicked.connect(self.signup)

    def login(self):
        try:
            asyncio.run(self.login_connection())
        except Exception as e:
            print(e)

    def signup(self):
        asyncio.run(self.signup_connection())

    def forget_password(self):
        asyncio.run(self.forget_password_connection())

    async def login_connection(self):
        global chat_data, email_id
        reader, writer = await asyncio.open_connection(get_ipv4_address(), 8888)

        print("CLicked")

        id = 0

        writer.write(pickle.dumps(id))
        await writer.drain()
        print("Id sent")
        email = self.email_input.text()
        password = self.password_input.text()

        writer.write(pickle.dumps(["Login", email, password]))
        await writer.drain()
        print("Login request sent")

        try:
            success = pickle.loads(await reader.read(4096))
        except Exception as e:
            success = None
            print(e)

        if success == "Success":
            QMessageBox.information(self, "Success", "Login Successful!")
            self.accept()
            email_id = email
        else:
            QMessageBox.warning(self, "Error", "Invalid Email or Password")
        print("Closing connection")
        writer.close()
        await writer.wait_closed()

    async def signup_connection(self):
        global chat_data, email_id

        reader, writer = await asyncio.open_connection(get_ipv4_address(), 8888)

        id = 0

        writer.write(pickle.dumps(id))
        await writer.drain()
        print("Id sent")

        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        password_constraint = len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isupper() for char in password) and any(char.islower() for char in password)
        if not email or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        elif not password_constraint:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit")
            return
        if password == confirm_password:
            otp = send_otp(email)
            if not otp:
                QMessageBox.warning(self, "Error", "Invaild Email")
                return

            otp_input, ok = QInputDialog.getText(self, "OTP Verification", "Enter the OTP sent to your email:")
            if not ok or otp_input != str(otp):
                QMessageBox.warning(self, "Error", "Invalid OTP")
                return
            
            writer.write(pickle.dumps(["Sign_Up", email]))
            await writer.drain()

            existing_acc = pickle.loads(await reader.read(4096))

            if existing_acc == "Yes":
                QMessageBox.warning(self, "Error", "Account already exists")
            else:
                writer.write(pickle.dumps([email, password]))
                await writer.drain()

                acc_made = pickle.loads(await reader.read(4096))
                print(acc_made)
                QMessageBox.information(self, "Success", "Account created successfully!")
                self.accept()
                email_id = email
        else:
            QMessageBox.warning(self, "Error", "Passwords do not match")

        print("Closing connection")
        writer.close()
        await writer.wait_closed()
        
    async def forget_password_connection(self):
        global chat_data

        reader, writer = await asyncio.open_connection(get_ipv4_address(), 8888)

        id = 0

        writer.write(pickle.dumps(id))
        await writer.drain()

        email = self.email_input.text()
        
        writer.write(pickle.dumps(["Forget Password", email]))
        await writer.drain()
        print("Forget Password request sent")

        existing_acc = pickle.loads(await reader.read(4096))
        
        if existing_acc == "Yes":
            print("Email found")
            otp = send_otp(email)
            if not otp:
                QMessageBox.warning(self, "Error", "Invalid Email")
                return

            otp_input, ok = QInputDialog.getText(self, "OTP Verification", "Enter the OTP sent to your email:")
            if not ok or otp_input != str(otp):
                QMessageBox.warning(self, "Error", "Invalid OTP")
                return

            new_password, ok = QInputDialog.getText(self, "New Password", "Enter new password:")
            new_password_constraint = len(new_password) >= 8 and any(char.isdigit() for char in new_password) and any(char.isupper() for char in new_password) and any(char.islower() for char in new_password)
            
            if not new_password_constraint:
                QMessageBox.warning(self, "Error", "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit")
                return
            
            if ok and new_password_constraint:
                writer.write(pickle.dumps(["Forget Password", email, new_password]))
                await writer.drain()
                
                succ = pickle.loads(await reader.read(4096))
                print(succ)
                QMessageBox.information(self, "Success", "Password changed successfully!")
        else:
            QMessageBox.warning(self, "Error", "Email not found")

        print("Closing connection")
        writer.close()
        await writer.wait_closed()

class AddContactDialog(QDialog):
    def __init__(self):
        super().__init__()
        print("Initializing AddContactDialog")  # Debug log
        self.setWindowTitle("Add Contact")
        self.setGeometry(400, 200, 300, 200)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Contact Name")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.submit_button = QPushButton("Submit")

        layout.addRow("Name:", self.name_input)
        layout.addRow("Email:", self.email_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

class CreateGroupDialog(QDialog):
    def __init__(self, contacts):
        super().__init__()
        print("Initializing CreateGroupDialog with contacts:", contacts)  # Debug log
        self.setWindowTitle("Create Group")
        self.setGeometry(400, 200, 300, 300)

        layout = QVBoxLayout()

        self.group_name_input = QLineEdit()
        self.group_name_input.setPlaceholderText("Group Name")  
        self.submit_button = QPushButton("Create Group")

        self.contacts_checkboxes = []
        for contact in contacts:
            checkbox = QCheckBox(contact)
            self.contacts_checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        layout.addWidget(QLabel("Group Name:"))
        layout.addWidget(self.group_name_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

class WhatsAppGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        login_dialog = LoginDialog()
        if not login_dialog.exec_():
            sys.exit()
        print("Out of login dialog")  # Debug log
        

        # self.async_loop = None
        self.qtimer = None

        self.init_asyncio()
        self.setWindowTitle("My Social Media App")
        self.setGeometry(100, 100, 1000, 600)
        self.contacts = {}
        self.groups = {}

        # Main container
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Sidebar for contacts and groups
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(400)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)

        # Add contacts and groups buttons
        self.add_contact_button = QPushButton("Add Contact")
        self.add_group_button = QPushButton("Create Group")
        self.add_contact_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.add_group_button.setStyleSheet("padding: 10px; font-size: 16px;")

        self.sidebar_layout.addWidget(self.add_contact_button)
        self.sidebar_layout.addWidget(self.add_group_button)

        # Placeholder label
        self.placeholder_label_sidebar = QLabel("Add contacts or Create Groups")
        self.placeholder_label_sidebar.setFont(QFont("Arial", 16))
        self.placeholder_label_sidebar.setAlignment(Qt.AlignLeft)
        self.sidebar_layout.addWidget(self.placeholder_label_sidebar)



        # Chat Area
        self.chat_area = QWidget()
        self.chat_area_layout = QVBoxLayout()
        self.chat_area.setLayout(self.chat_area_layout)

        self.chat_header = QLabel()
        self.chat_header.setFont(QFont("Arial", 20))
        self.chat_header.setAlignment(Qt.AlignTop)
        self.chat_header.setFixedHeight(50)
        self.chat_header.hide()

        self.placeholder_label = QLabel("Select a contact or group to start chatting")
        self.placeholder_label.setFont(QFont("Arial", 16))
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.chat_area_layout.addWidget(self.placeholder_label)

        self.chat_area_layout.addWidget(self.chat_header)

        self.chat_display = QListWidget()
        self.chat_display_layout = QVBoxLayout()
        self.chat_display_layout.addWidget(self.chat_display)

        self.chat_display.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #cccccc;
            font-size: 14px;
            padding: 10px;
            border-radius: 5px;
""")
        self.chat_display.hide()

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.hide()

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("padding: 10px;")
        self.send_button.hide()

        chat_input_layout = QHBoxLayout()
        chat_input_layout.addWidget(self.message_input)
        chat_input_layout.addWidget(self.send_button)

        self.chat_area_layout.addWidget(self.chat_display)
        self.chat_area_layout.addLayout(chat_input_layout)

        # Add to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.chat_area)

        # Signal connections
        self.add_contact_button.clicked.connect(self.show_add_contact_dialog)
        self.add_group_button.clicked.connect(self.show_create_group_dialog)
        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)
        

        # Apply styling
        self.apply_styles()
        QTimer.singleShot(0, self.start_connection)

        # List of saved contacts and groups
        self.contacts_list = QListWidget()
        self.contacts_list.itemClicked.connect(self.open_chat)
        self.sidebar_layout.addWidget(self.contacts_list)

        self.update_placeholder_visibility()

    def init_asyncio(self):
        try:
            print("Initializing asyncio event loop...")  # Debug log
            # Create and set the event loop
            self.async_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.async_loop)
            print("Asyncio event loop initialized.")  # Debug log

            # Set up QTimer to periodically process asyncio events
            self.qtimer = QTimer()
            self.qtimer.timeout.connect(self.process_asyncio_events)
            self.qtimer.start(10)  # Process asyncio events every 10ms
        except Exception as e:
            print(f"Error initializing asyncio: {e}")

    def process_asyncio_events(self):
        try:
            # Run a single iteration of the event loop without stopping it
            tasks = asyncio.all_tasks(loop=self.async_loop)
            if tasks:
                self.async_loop.run_until_complete(asyncio.gather(*tasks))
        except Exception as e:
            print(f"Error processing asyncio events: {e}")

    def update_placeholder_visibility(self):
        print("Updating placeholder visibility")
        if not self.contacts and not self.groups:
            self.placeholder_label_sidebar.show()
        else:
            self.placeholder_label_sidebar.hide()

    def open_chat(self, item):
        global chat_data
        self.chat_display.clear()
        print(f"Opening chat with item: {item.text()}")  # Debug log
        self.placeholder_label.hide()
        self.chat_display.show()
        self.message_input.show()
        self.send_button.show()
        self.chat_header.show()

        name = item.text()
        if name in self.groups.keys():
            # Group logic
            print(f"Opening group chat for: {name}")  # Debug log
            self.chat_header.setText(f"Group: {name}")
            self.chat_header.mousePressEvent = lambda event: self.show_group_members(name)
        else:
            # Individual contact logic
            print(f"Opening individual chat for: {name}")  # Debug log
            self.chat_header.setText(f"Chatting with {name}")
            self.chat_header.mousePressEvent = None
        
        if name in self.contacts.keys():
            for i in chat_data["Personal_Chat"]:
                if i["Sender_email"] == email_id and i["Reciever_email"] == self.contacts[name]:
                    msg = QListWidgetItem(f"You: {i['Message']} \n{i['Time']}")
                    msg.setTextAlignment(Qt.AlignRight)
                    self.chat_display.addItem(msg)
                elif i["Sender_email"] == self.contacts[name] and i["Reciever_email"] == email_id:
                    msg = QListWidgetItem(f"{name}: {i['Message']} \n{i['Time']}")
                    msg.setTextAlignment(Qt.AlignLeft)
                    self.chat_display.addItem(msg)
        elif name in self.groups.keys():
            for i in chat_data["Group_Chat"]:
                if i["Sender_email"] == email_id and i["Group_Name"] == name:
                    msg = QListWidgetItem(f"You: {i['Message']} \n{i['Time']}")
                    msg.setTextAlignment(Qt.AlignRight)
                    self.chat_display.addItem(msg)
                elif i["Group_Name"] == name:
                    msg = QListWidgetItem(f"{name}: {i['Message']} \n{i['Time']}")
                    msg.setTextAlignment(Qt.AlignLeft)
                    self.chat_display.addItem(msg)
        else:
            print(f"Invalid contact or group selected: {name}")  # Debug log

    def show_add_contact_dialog(self):
        print("Showing Add Contact Dialog")  # Debug log
        self.dialog = AddContactDialog()
        self.dialog.submit_button.clicked.connect(self.add_contact)
        self.dialog.exec_()

    def add_contact(self):
        asyncio.create_task(self.add_contact_connection())

    # @asyncSlot()
    async def add_contact_connection(self):
        self.reader_contact, self.writer_contact = await asyncio.open_connection(get_ipv4_address(), 8888)

        # Sending an ID to the server
        id = 2
        self.writer_contact.write(pickle.dumps(id))
        await self.writer_contact.drain()
        print("Id sent")  # Debug log
        name = self.dialog.name_input.text()
        email = self.dialog.email_input.text()
        if name and email:
            self.writer_contact.write(pickle.dumps(["Add Contact", email]))
            await self.writer_contact.drain()
            print(f"Email sent {email}")  # Debug log
            User_exists = pickle.loads(await self.reader_contact.read(4096))
            if User_exists == "Yes" and email != email_id and name not in self.contacts.keys() and email not in self.contacts.values():
                print(f"Adding contact - Name: {name}, Email: {email}")  # Debug log
                self.contacts[name] = email
                self.contacts_list.addItem(name)
                self.update_placeholder_visibility()
                self.dialog.close()
            elif email == email_id:
                QMessageBox.warning(self, "Error", "You cannot add yourself as a contact")
                print(f"Email already exists")  # Debug log
            elif name in self.contacts.keys() or email in self.contacts.values():
                QMessageBox.warning(self, "Error", "Contact already exists")
                print(f"Email already exists")  # Debug log
            else:
                print("User does not exist")  # Debug log
                QTimer.singleShot(0, lambda: QMessageBox.warning(self, "Error", "User does not exist"))
            
            self.writer_contact.close()
            await self.writer_contact.wait_closed()

        else:
            QTimer.singleShot(0, lambda: QMessageBox.warning(self, "Error", "Please fill in both fields"))
            print("Invalid input for adding contact")  # Debug log


    def show_create_group_dialog(self):
        print("Showing Create Group Dialog")  # Debug log
        self.group_dialog = CreateGroupDialog(self.contacts)
        self.group_dialog.submit_button.clicked.connect(self.add_group)
        self.group_dialog.exec_()

    def add_group(self):
        group_name = self.group_dialog.group_name_input.text()
        selected_contacts = [cb.text() for cb in self.group_dialog.contacts_checkboxes if cb.isChecked()]
        if group_name and selected_contacts:
            print(f"Creating group - Name: {group_name}, Members: {selected_contacts}")  # Debug log
            self.groups.append(group_name)
            item = QListWidgetItem(group_name)
            item.setBackground(QColor("#FFDDC1"))
            self.contacts_list.addItem(item)
            self.update_placeholder_visibility()
            self.group_dialog.close()
            details = {"Personal_Details": {"name": group_name, "members": selected_contacts},
                       "Chat_details": {"Chat": {
                            "message": [], 
                            "sender": [],
                            "time": []
                          }}}
            with open(f"Groups/{group_name}.pkl", "wb") as file:
                pickle.dump(details, file)
        else:
            print("Invalid input for creating group")  # Debug log

    def show_group_members(self, group_name):
        print(f"Showing members for group: {group_name}")  # Debug log
        group_members = [cb.text() for cb in self.group_dialog.contacts_checkboxes if cb.isChecked()]

        dialog = QDialog()
        dialog.setWindowTitle(f"Members of {group_name}")
        dialog.setGeometry(400, 200, 300, 300)
        
        main_widget = QWidget()

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        members = QWidget()
        members_layout = QVBoxLayout()
        members.setLayout(members_layout)
        members_layout.addWidget(QLabel(f"Members of {group_name}:"))
        members_layout.setAlignment(Qt.AlignTop)
        for no, member in enumerate(group_members):
            print(f"Member: {member}")  # Debug log
            members_layout.addWidget(QLabel(f"{no+1}: {member}"))

        button_widget = QWidget()
        buttonlayout = QVBoxLayout()
        button_widget.setLayout(buttonlayout)
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        buttonlayout.addWidget(close_button)
        buttonlayout.setAlignment(Qt.AlignBottom)

        main_layout.addWidget(members)
        main_layout.addWidget(button_widget)

        dialog.setLayout(main_layout)

        dialog.exec_()

    def send_message(self):
        global chat_data
        message = self.message_input.text()
        if message:
            print(f"Sending message: {message}")  # Debug log
            time_sent = QTime.currentTime().toString("hh:mm AP")

            filtered_message = self.message_filter(message)

            message_item = QLabel(f"{filtered_message} \n{time_sent}")

            msg = QListWidgetItem(message_item.text())
            msg.setTextAlignment(Qt.AlignRight)

            self.chat_display.addItem(msg)
            self.message_input.clear()
            if self.chat_header.text().startswith("Group:"):
                group_name = self.chat_header.text().split(":")[1].strip()
                chat_data["Group_Chat"].append({"Message": filtered_message, "Time": time_sent, "Sender_email": email_id, "Group_Name": group_name})
            else:
                chat_data["Personal_Chat"].append({"Message": filtered_message, "Time": time_sent, "Sender_email": email_id, "Reciever_email": self.contacts[self.chat_header.text().split(" ")[-1].strip()]})

        else:
            print("Empty message, not sent")  # Debug log

    def receive_message(self, message):
        print(f"Receiving message: {message}")  # Debug log
        time_received = QTime.currentTime().toString("hh:mm AP")
        message_item = QLabel(f"{message} \n{time_received}")
        msg = QListWidgetItem(message_item.text())
        msg.setTextAlignment(Qt.AlignLeft)
        self.chat_display.addItem(msg)

        self.chat_area.setStyleSheet("""
            QListWidget::item {
                border: none;
                padding: 5px;
                background-color: #128C7E;
                color: white;
                border: 2px solid #064C48;
                border-radius: 10px;
                display: inline-block;
                padding: 10px;
            }
            QListWidget::item:hover {
                background-color: #128C7E;
            }
            QListWidget::item:selected {
                background-color: #128C7E;
            }
""")
        
    def message_filter(self, message):
        display_width = (self.chat_display.width()) - (self.chat_display.width())/2
        
        text_width = QFontMetrics(QLabel(message).font()).boundingRect(QLabel(message).text()).width()
        print(f"Display width: {display_width}")  # Debug log
        print(f"Message length: {text_width}")  # Debug log
        output = ""
        line_len = ""
        msg_words = message.split()
        if text_width > display_width:
            for _ in range(int((text_width//display_width) + 1)):
                for words in msg_words:
                    if QFontMetrics(QLabel(line_len).font()).boundingRect(QLabel(line_len).text()).width() < display_width:
                        line_len += words + " "
                    else:
                        output += line_len + "\n"
                        line_len = words + " "
        
        else:
            output = message

            
            print(f"Filtered message: {message}")  # Debug log
        return output

    def start_connection(self):
        asyncio.ensure_future(self.connect_to_server())
        asyncio.create_task(self.send_and_recieve_mesage())  # Run test in the background

    async def connect_to_server(self):
        global chat_data, email_id
        try:
            self.reader, self.writer = await asyncio.open_connection(get_ipv4_address(), 8888)

            # Sending an ID to the server
            id = 1
            self.writer.write(pickle.dumps(id))
            await self.writer.drain()

            # Sending email ID to the server
            self.writer.write(pickle.dumps(email_id))
            await self.writer.drain()

            # Receiving confirmation and chat data
            conn = pickle.loads(await self.reader.read(4096))
            print("Server connection confirmed:", conn)
            data = pickle.loads(await self.reader.read(4096))
            chat_data = data
            print("Chat data received:", data)
            self.writer.write(pickle.dumps("Contacts Turn"))
            self.contacts = pickle.loads(await self.reader.read(4096))
            print("Contacts received:", self.contacts)
            for contact in self.contacts.keys():
                self.contacts_list.addItem(contact)
        except Exception as e:
            print(f"Failed to connect: {e}")

    async def send_and_recieve_mesage(self):
        global chat_data
        # Continuously send and receive data in the background
        print("Data Transfer Started")
        while True:
            if True:
                try:
                    self.writer.write(pickle.dumps(chat_data))
                    await self.writer.drain()
                    print(f"Data Sent:")
                    data = pickle.loads(await self.reader.read(4096))
                    print("Received:")
                    if data != chat_data:
                        if data["Personal_Chat"][-1]["Reciever_email"] == email_id:
                            for name, email in self.contacts.items():
                                if email == data["Personal_Chat"][-1]["Sender_email"]:
                                    sender_name = name
                                    break
                            msg = QListWidgetItem(f"{sender_name}: {data['Personal_Chat'][-1]['Message']} \n{data['Personal_Chat'][-1]['Time']}")
                            msg.setTextAlignment(Qt.AlignLeft)
                            self.chat_display.addItem(msg)
                        chat_data = data
                        
                except Exception as e:
                    print("Error in test:", e)
            await asyncio.sleep(1)  # Avoid tight loop to reduce resource usage
    
    def closeEvent(self, event):
        msgBox = QMessageBox()
        msgBox.setText("Are you sure you want to exit?")
        msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        if msgBox.exec_() == QMessageBox.Yes:
            self.writer.write(pickle.dumps(["Exit",self.contacts]))
            # self.writer.drain()
            event.accept()
            print("Exited")
            self.writer.close()
            sys.exit()        
            super().closeEvent(event)
        else:
            event.ignore()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }

            QListWidget {
                background-color: #ffffff;
                border: none;
                font-size: 16px;
                padding: 5px;
            }

            QListWidget::item {
                padding: 10px;
                margin: 5px;
            }

            QListWidget::item:selected {
                background-color: #128C7E;
                color: white;
                border-radius: 5px;
            }

            QPushButton {
                background-color: #128C7E;
                color: white;
                border: none;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #075E54;
            }

            QTextEdit, QLineEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                font-size: 14px;
                padding: 5px;
            }

            QTextEdit {
                padding: 10px;
                border-radius: 5px;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    gui = WhatsAppGUI()
    gui.show()
    print("Starting asyncio event loop...")  # Debug log    
    with loop:  # Run the asyncio event loop
        loop.run_forever()
    if not app.exec_():
        loop.close()
        sys.exit()
        print(chat_data)


