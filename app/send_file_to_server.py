import paramiko
import os

def send_file_to_server(local_file_path, remote_file_path, server_host, server_port, username, password):
    try:
        # Создаём объект SSHClient
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Разрешаем неизвестные ключи
        
        # Подключаемся к серверу
        ssh.connect(server_host, port=server_port, username=username, password=password)

        # Создаём объект SFTP для передачи файла
        sftp = ssh.open_sftp()

        # Отправляем файл
        sftp.put(local_file_path, remote_file_path)

        print(f"Файл {local_file_path} успешно отправлен на сервер {server_host} по пути {remote_file_path}")

        # Закрываем соединение SFTP и SSH
        sftp.close()
        ssh.close()

    except Exception as e:
        print(f"Ошибка при отправке файла на сервер: {e}")

# Пример использования:
local_file_path = "output/output_test.yml"
remote_file_path = "/root/output_yml/output.yml"
server_host = "77.105.166.9"
server_port = 22  # стандартный порт для SFTP
username = "root"
password = "gWLlnIr1hfbC"

# Отправляем файл
send_file_to_server(local_file_path, remote_file_path, server_host, server_port, username, password)
