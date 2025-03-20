def save_data(fileName: str, data: bytes) -> None:
    with open(fileName, 'wb') as file:
        file.write(data)

def load_data(fileName: str) -> bytes:
    with open(fileName, 'rb') as file:
        return file.read()
