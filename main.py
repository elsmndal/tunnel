import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.config import Config

# Set dark mode background color
Config.set('graphics', 'background_color', '1f1f1f')

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(orientation='vertical', **kwargs)

        self.title_label = Label(text='Kaizo Tunnel', font_size=30, color=[1, 1, 1, 1])
        self.ip_address_input = TextInput(hint_text='IP Address', multiline=False)
        self.port_number_input = TextInput(hint_text='Port Number', multiline=False)
        self.connect_button = Button(text='Connect', on_press=self.on_connect_button_press)
        self.status_label = Label(text='', color=[1, 0, 0, 1])

        self.add_widget(self.title_label)
        self.add_widget(self.ip_address_input)
        self.add_widget(self.port_number_input)
        self.add_widget(self.connect_button)
        self.add_widget(self.status_label)

    def on_connect_button_press(self, instance):
        ip_address = self.ip_address_input.text
        port_number = int(self.port_number_input.text)

        threading.Thread(target=self.handle_client, args=(ip_address, port_number)).start()

    def handle_client(self, ip_address, port_number):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip_address, port_number))
            self.status_label.text = 'Connected'
            self.status_label.color = [0, 1, 0, 1]  # Set color to green for success
            data = b'Test Data'
            client_socket.send(data)
            response = client_socket.recv(1024)
            self.status_label.text = f'Received: {response.decode()}'
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'
            self.status_label.color = [1, 0, 0, 1]  # Set color to red for error
        finally:
            client_socket.close()

class MainApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    MainApp().run()
