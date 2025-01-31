
from Modules.CNC_Logic import driver_conection, give_info, close_conection
import gclib

g = gclib.py()
g = driver_conection('192.168.1.100')
give_info(g)


def mmtocounts(mm):
    counts = round(mm/3e-5)
    return counts

def degtocounts(deg):
    return round(deg/8.05556e-5)

deg = 10

c = g.GCommand
c('SP , , 150000')
print(c('RP'))
c(f'PR , , {degtocounts(deg)}')
c('BG C')
g.GMotionComplete('C')

close_conection(g)


