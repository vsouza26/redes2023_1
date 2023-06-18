FROM python:3.12.0b1-slim 
COPY ./minion.py /opt/
COPY ./minion_socket_module/ /opt/minion_socket_module
CMD python /opt/minion.py --ip  network_sim_master-1 --porta 8189
