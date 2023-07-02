import socket
def socket_rect_int(c:socket):
    """Int via socket sempre será um inteiro de oito bytes com sinal"""
    recv_int =  c.recv(8)
    return int.from_bytes(recv_int, 'little')

def socket_recv_str(c:socket, dencoder:str='ascii'):
    """String via socket sempre será uma string menor que 4096 bytes. Por padrão o encoder é ascii"""
    try:
        tam_str = socket_rect_int(c)
        msg = c.recv(tam_str)
        return msg.decode(dencoder)
    except Exception as e:
            raise e

def socket_send_int(c:socket, num:int):
    """Envia inteiro via socket"""
    c.send(int.to_bytes(num, 8, 'little'))
    
def socket_send_str(c:socket, string:str, encoder:str='ascii'):
    """Envia string via socket"""
    encoded_string = string.encode(encoder)
    len_string = len(encoded_string)
    socket_send_int(c, len_string)
    c.send(encoded_string)
