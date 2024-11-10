import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QComboBox, QLabel, 
                             QMessageBox, QFrame)
from PySide6.QtCore import Qt
import serial
import serial.tools.list_ports
import time

class ArduinoGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.arduino = None
        self.is_connected = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Controle Arduino')
        self.setFixedSize(400, 300)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Frame de conexão
        connection_frame = QFrame()
        connection_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        connection_layout = QHBoxLayout(connection_frame)

        # Combobox para portas
        self.port_combo = QComboBox()
        self.update_ports()
        
        # Botões
        refresh_button = QPushButton('Atualizar Portas')
        refresh_button.clicked.connect(self.update_ports)
        self.connect_button = QPushButton('Conectar')
        self.connect_button.clicked.connect(self.toggle_connection)

        # Adiciona widgets ao frame de conexão
        connection_layout.addWidget(QLabel('Porta:'))
        connection_layout.addWidget(self.port_combo)
        connection_layout.addWidget(refresh_button)
        connection_layout.addWidget(self.connect_button)

        # Frame de LEDs
        led_frame = QFrame()
        led_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        led_layout = QHBoxLayout(led_frame)

        # Botões LED
        self.led_buttons = []
        for letter in ['A', 'B', 'C']:
            button = QPushButton(f'LED {letter}')
            button.clicked.connect(lambda checked, l=letter.lower(): self.send_command(l))
            led_layout.addWidget(button)
            self.led_buttons.append(button)

        # Status
        self.status_label = QLabel('Desconectado')
        self.status_label.setAlignment(Qt.AlignCenter)

        # Adiciona frames ao layout principal
        layout.addWidget(connection_frame)
        layout.addWidget(led_frame)
        layout.addWidget(self.status_label)

    def update_ports(self):
        """Atualiza a lista de portas COM disponíveis"""
        self.port_combo.clear()
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo.addItems(ports)

    def toggle_connection(self):
        """Alterna entre conectar e desconectar do Arduino"""
        if not self.is_connected:
            self.connect_arduino()
        else:
            self.disconnect_arduino()

    def connect_arduino(self):
        """Estabelece conexão com o Arduino"""
        try:
            port = self.port_combo.currentText()
            self.arduino = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Aguarda inicialização
            self.is_connected = True
            self.connect_button.setText('Desconectar')
            self.status_label.setText(f'Conectado à porta {port}')
            QMessageBox.information(self, 'Sucesso', 'Arduino conectado com sucesso!')
        except serial.SerialException as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao conectar: {str(e)}')

    def disconnect_arduino(self):
        """Desconecta do Arduino"""
        if self.arduino:
            self.arduino.close()
        self.is_connected = False
        self.connect_button.setText('Conectar')
        self.status_label.setText('Desconectado')

    def send_command(self, command):
        """Envia comando para o Arduino"""
        if not self.is_connected:
            QMessageBox.warning(self, 'Aviso', 'Arduino não está conectado!')
            return

        try:
            self.arduino.write(command.encode())
            time.sleep(0.1)  # Pequeno delay para resposta
            if self.arduino.in_waiting:
                response = self.arduino.readline().decode().strip()
                self.status_label.setText(f'Resposta: {response}')
        except serial.SerialException as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao enviar comando: {str(e)}')
            self.disconnect_arduino()

    def closeEvent(self, event):
        """Manipula o evento de fechamento da janela"""
        if self.is_connected:
            self.disconnect_arduino()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ArduinoGUI()
    gui.show()
    sys.exit(app.exec())