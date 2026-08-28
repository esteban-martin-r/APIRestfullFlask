from models import db, Juego

def insertar_juego(nombre, descripcion, precio):
    nuevo_juego = Juego(nombre=nombre, descripcion=descripcion, precio=precio)
    db.session.add(nuevo_juego)
    db.session.commit()
    return nuevo_juego

def obtener_juegos():
    return Juego.query.all()

def eliminar_juego(id):
    juego = Juego.query.get(id)
    if juego:
        db.session.delete(juego)
        db.session.commit()
        return True
    return False

def actualizar_juego(id, nombre, descripcion, precio):
    juego = Juego.query.get(id)
    if juego:
        juego.nombre = nombre
        juego.descripcion = descripcion
        juego.precio = precio
        db.session.commit()
        return True
    return False

def obtener_juego_por_id(id):
    return Juego.query.get(id)

        
        