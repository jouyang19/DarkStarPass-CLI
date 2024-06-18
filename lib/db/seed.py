from db.init import CONN, CURSOR
from db.user import User
from db.password import Password

def seed_database():
    u1 = User.create("Guest1", "Pass1")
    u2 = User.create("Guest2", "Pass2")
    u3 = User.create("Guest3", "Pass3")
    p1 = Password.create("Acc1","Username1", "Pass1", u1.id)
    p2 = Password.create("Acc2","Username2", "Pass2", u1.id)
    p3 = Password.create("Acc3","Username3", "Pass3", u1.id)
    p4 = Password.create("Acc4","Username4", "Pass4", u3.id)
    p5 = Password.create("Acc5","Username5", "Pass5", u2.id)
    p6 = Password.create("Acc6","Username6", "Pass6", u2.id)
    
    
    
    