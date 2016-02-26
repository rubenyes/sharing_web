from flask import Flask , g
import sqlite3

from flask import Flask
app = Flask(__name__)

db_location = 'var/sharing.db'

tipoVideo = 1
tipoFoto = 2
tipoAudio = 3
tipoEnlace = 4
tipoTexto = 5

def get_db():
	db = getattr (g, 'db', None)
	if db is None:
		db = sqlite3.connect(db_location)
		g.db = db
	return db

@app.teardown_appcontext
def close_db_connection(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode ='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


def addComentario(id_usuario, fecha, texto, id_pub):
	db = get_db()
	c = db.cursor()
	c.execute('INSERT INTO contestaciones VALUES (?, ?, ?, ?)', (None, id_usuario, fecha, texto))
	id_contestacion = c.lastrowid
	c.execute('INSERT INTO comentarios VALUES (?, ?, ?)', (id_contestacion, id_pub, 0))
	c.execute('UPDATE publicaciones SET num_comentarios=num_comentarios+1 WHERE id=?', (id_pub,))
	db.commit()
	return id_contestacion
		
def getComentarios(id_pub):
	db = get_db()
	results = db.cursor().execute('SELECT * FROM comentarios INNER JOIN contestaciones ON contestaciones.id=comentarios.id_contestacion WHERE comentarios.id_pub=?', (id_pub,)).fetchall()
	return results	

def getContestacion(id):
	db = get_db()
	result = db.cursor().execute('SELECT * FROM contestaciones WHERE id=?', (id,)).fetchone()
	return result

def getPublicaciones(id_user):
	db = get_db()
	results = db.cursor().execute('SELECT * FROM publicaciones WHERE id_usuario=?', (id_user,)).fetchall()
	return results
	
def getDashboard(id_user):
	db = get_db()
	seguidos = getSeguidos(id_user)
	publicaciones = []
	for user in seguidos:
		results = db.cursor().execute('SELECT * FROM publicaciones WHERE id_usuario=?', (user[0],)).fetchall() #la pos 0 corresponde al id del usuario
		print results
		publicaciones.extend(results)
	publicaciones.sort(key=lambda x: x[2], reverse=True) #la pos 2 corresponde a la fecha de la publicacion
	#publicaciones_ordenadas = sorted(publicaciones.keys(), key=lambda x: x[2])
	return publicaciones
	
def addLike(id_pub, id_user):
	db = get_db()
	db.cursor().execute('UPDATE publicaciones SET num_likes=num_likes+1 WHERE publicaciones.id=?', (id_pub,))
	db.cursor().execute('INSERT INTO likes VALUES (?, ?)', (id_pub, id_user))
	db.commit()
	
def removeLike(id_pub, id_user):
	db = get_db()
	db.cursor().execute('UPDATE publicaciones SET num_likes=num_likes-1 WHERE publicaciones.id=?', (id_pub,))
	db.cursor().execute('DELETE FROM likes WHERE id_pub=? AND id_usuario=?', (id_pub, id_user))
	db.commit()
	
def addAudio(id_usuario, fecha, url, desc):
	db = get_db()
	c = db.cursor()
	c.execute('INSERT INTO publicaciones VALUES (?, ?, ?, ?, ?, ?, ?)', (None, id_usuario, fecha, tipoAudio, 0, 0, 0))
	id_pub = c.lastrowid
	c.execute('INSERT INTO audios VALUES (?, ?, ?, ?)', (None, id_pub, url, desc))
	db.commit()
	return id_pub
		
def getAudio(id_pub):
	db = get_db()
	result = db.cursor().execute('SELECT * FROM publicaciones INNER JOIN audios ON audios.id_pub=? WHERE publicaciones.id=?', (id_pub, id_pub)).fetchone()
	return result
		
def addEnlace(id_usuario, fecha, url, desc):
	db = get_db()
	c = db.cursor()
	c.execute('INSERT INTO publicaciones VALUES (?, ?, ?, ?, ?, ?, ?)', (None, id_usuario, fecha, tipoEnlace, 0, 0, 0))
	id_pub = c.lastrowid
	c.execute('INSERT INTO enlaces VALUES (?, ?, ?, ?)', (None, id_pub, url, desc))
	db.commit()
	return id_pub
		
def getEnlace(id_pub):
	db = get_db()
	result = db.cursor().execute('SELECT * FROM publicaciones INNER JOIN enlaces ON enlaces.id_pub=? WHERE publicaciones.id=?', (id_pub, id_pub)).fetchone()
	return result
		
def addFoto(id_usuario, fecha, url, desc):
	db = get_db()
	c = db.cursor()
	c.execute('INSERT INTO publicaciones VALUES (?, ?, ?, ?, ?, ?, ?)', (None, id_usuario, fecha, tipoFoto, 0, 0, 0))
	id_pub = c.lastrowid
	c.execute('INSERT INTO fotos VALUES (?, ?, ?, ?)', (None, id_pub, url, desc))
	db.commit()
	return id_pub
		
def getFoto(id_pub):
	db = get_db()
	result = db.cursor().execute('SELECT * FROM publicaciones INNER JOIN fotos ON fotos.id_pub=? WHERE publicaciones.id=?', (id_pub, id_pub)).fetchone()
	return result
		
def addTexto(id_usuario, fecha, texto):
	db = get_db()
	c = db.cursor()
	c.execute('INSERT INTO publicaciones VALUES (?, ?, ?, ?, ?, ?, ?)', (None, id_usuario, fecha, tipoTexto, 0, 0, 0))
	id_pub = c.lastrowid
	c.execute('INSERT INTO textos VALUES (?, ?, ?)', (None, id_pub, texto))
	db.commit()
	return id_pub
		
def getTexto(id_pub):
	db = get_db()
	result = db.cursor().execute('SELECT * FROM publicaciones INNER JOIN textos ON textos.id_pub=? WHERE publicaciones.id=?', (id_pub, id_pub)).fetchone()
	return result
		
def addVideo(id_usuario, fecha, url, desc):
	db = get_db()
	c = db.cursor()
	c.execute('INSERT INTO publicaciones VALUES (?, ?, ?, ?, ?, ?, ?)', (None, id_usuario, fecha, tipoVideo, 0, 0, 0))
	id_pub = c.lastrowid
	c.execute('INSERT INTO videos VALUES (?, ?, ?, ?)', (None, id_pub, url, desc))
	db.commit()
	return id_pub
		
def getVideo(id_pub):
	db = get_db()
	result = db.cursor().execute('SELECT * FROM publicaciones INNER JOIN videos ON videos.id_pub=? WHERE publicaciones.id=?', (id_pub, id_pub)).fetchone()
	return result

def addRespuesta(id_usuario, fecha, texto, id_comentario):
	db = get_db()
	c = db.cursor()
	c.execute('INSERT INTO contestaciones VALUES (?, ?, ?, ?)', (None, id_usuario, fecha, texto))
	id_contestacion = c.lastrowid
	c.execute('INSERT INTO respuestas VALUES (?, ?)', (id_contestacion, id_comentario))
	c.execute('UPDATE comentarios SET num_respuestas=num_respuestas+1 WHERE id_contestacion=?', (id_comentario,))
	db.commit()
	return id_contestacion
		
def getRespuestas(id_comentario):
	db = get_db()
	results = db.cursor().execute('SELECT * FROM respuestas INNER JOIN contestaciones ON contestaciones.id=respuestas.id_contestacion WHERE respuestas.id_comentario=?', (id_comentario,)).fetchall()
	return results	

def getSeguidores(id_user):
	db = get_db()
	results = db.cursor().execute('SELECT id_seguidor FROM seguidores WHERE seguidores.id_usuario=?', (id_user,)).fetchall()
	return results	
	
def getSeguidos(id_user):
	db = get_db()
	results = db.cursor().execute('SELECT id_usuario FROM seguidores WHERE seguidores.id_seguidor=?', (id_user,)).fetchall()
	return results	

def addSeguidor(id_user, id_user_seguidor):
	db = get_db()
	db.cursor().execute('UPDATE usuarios SET num_seguidores=num_seguidores+1 WHERE id=?', (id_user,))
	db.cursor().execute('UPDATE usuarios SET num_seguidos=num_seguidos+1 WHERE id=?', (id_user_seguidor,))
	db.cursor().execute('INSERT INTO seguidores VALUES (?, ?)', (id_user, id_user_seguidor))
	db.commit()

def removeSeguidor(id_user, id_user_seguidor):
	db = get_db()
	db.cursor().execute('UPDATE usuarios SET num_seguidores=num_seguidores-1 WHERE id=?', (id_user,))
	db.cursor().execute('UPDATE usuarios SET num_seguidos=num_seguidos-1 WHERE id=?', (id_user_seguidor,))
	db.cursor().execute('DELETE FROM seguidores WHERE id_usuario=? AND id_seguidor=?', (id_user, id_user_seguidor))
	db.commit()
	
def addUsuario(usuario, nombre, email, desc, pw):
	db = get_db()
	c = db.cursor()
	c.execute('INSERT INTO usuarios VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (None, usuario, nombre, email, desc, pw, 0, 0))
	db.commit()
	return c.lastrowid
	
def getUsuario(id_user):
	db = get_db()
	result = db.cursor().execute('SELECT * FROM usuarios WHERE id=?', (id_user,)).fetchone()
	return result
	
def updateUsuario(id_user, usuario, nombre, email, desc, pw):
	db = get_db()
	db.cursor().execute('UPDATE usuarios SET usuario=?, nombre=?, email=?, desc=?, pw=? WHERE id=?', (usuario, nombre, email, desc, pw, id_user))
	db.commit()
	
def deleteUsuario(id_user):
	db = get_db()
	db.cursor().execute('DELETE FROM usuarios WHERE id=?', (id_user,))
	db.commit()
	
	