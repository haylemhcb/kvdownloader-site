import subprocess
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

class DownloadApp(App):
    def build(self):
        self.title = 'Download Site'  # Establecer el título de la ventana
        self.window_size = (320, 240)  # Establecer el tamaño de la ventana

        self.layout = BoxLayout(orientation='vertical')

        self.url_input = TextInput(hint_text='Ingrese la URL del sitio', multiline=False)
        self.domain_input = TextInput(hint_text='Ingrese el dominio (ejemplo.com)', multiline=False)
        self.progress_label = Label(text='Progreso de la descarga:')
        self.start_button = Button(text='Iniciar descarga')
        self.start_button.bind(on_press=self.start_download)

        self.layout.add_widget(self.url_input)
        self.layout.add_widget(self.domain_input)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.progress_label)

        return self.layout

    def on_start(self):
        # Establecer el tamaño de la ventana al iniciar la aplicación
        self.root_window.size = self.window_size

    def start_download(self, instance):
        url = self.url_input.text
        domain = self.domain_input.text

        if url and domain:
            self.progress_label.text = 'Descargando...'
            # Iniciar el hilo de descarga
            threading.Thread(target=self.download_site, args=(url, domain)).start()

    def download_site(self, url, domain):
        command = [
            'wget',
            '--mirror',
            '--convert-links',
            '--adjust-extension',
            '--page-requisites',
            '--no-parent',
            f'--domains={domain}',
            url
        ]

        # Start the subprocess, redirect stderr to stdout
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Leer la salida del proceso
        for line in iter(process.stdout.readline, ''):
            # Actualizar la interfaz en el hilo principal
            Clock.schedule_once(lambda dt, text=line.strip(): self.update_progress(text))

        process.stdout.close()  # Cerrar stdout
        process.wait()  # Esperar a que el proceso termine
        Clock.schedule_once(lambda dt: self.update_progress('Descarga completada.'))

    def update_progress(self, text):
        self.progress_label.text += '\n' + text

if __name__ == '__main__':
    DownloadApp().run()
