import datetime
from Web.models import Habitacion, Reserva

def check_disponibilidad(habitacion, check_in, check_out):
    disp_list=[]
    reserva_list = Reserva.objects.filter(habitacion=habitacion)
    for reserva in reserva_list:
        if reserva.check_in > check_out or reserva.check_out < check_in:
            disp_list.append(True)
        else:
            disp_list.append(False)
    return all(disp_list)