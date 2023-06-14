FROM python:3.12.0b1-slim 
COPY ./master.py /opt/
COPY ./server_socket_module/ /opt/server_socket_module
CMD python /opt/master.py --ip 0.0.0.0 --porta 8189
