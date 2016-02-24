import datastore

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'admin':
        return '1234'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)



@app.route('/api/v1.0/comentarios', methods = ['POST'])
@auth.login_required
def create_comentario():
    if not request.json:
        abort(400)
    id_usuario = request.json['id_usuario']
	fecha = request.json['fecha']
	texto = request.json['texto']
	id_pub = request.json['id_pub']
    id_contestacion = addComentario(id_usuario, fecha, texto, id_pub)
    return jsonify( { 'id_contestacion': id_contestacion) } ), 201
	
@app.route('/api/v1.0/comentarios', methods = ['GET'])
@auth.login_required
def get_comentarios():
	id_pub = request.args.get('id_pub','')
	if id_pub == '':
		abort(400)		
    return jsonify( { 'comentarios': getComentarios(id_pub) } )
	
@app.route('/api/v1.0/contesaciones/<int:id>', methods = ['GET'])
@auth.login_required
def get_contestacion(id):
	contesatcion = getContestacion(id);
    if len(contesatcion) == 0:
        abort(404)
    return jsonify( { 'contesatcion': contesatcion } )
	
@app.route('/api/v1.0/dashboard', methods = ['GET'])
@auth.login_required
def get_publicaciones():
	id_user = request.args.get('id_user','')
	if id_user == '':
		abort(400)		
    return jsonify( { 'dashboard': getDashboard(id_user) } )

@app.route('/api/v1.0/publicaciones', methods = ['GET'])
@auth.login_required
def get_publicaciones():
	id_user = request.args.get('id_user','')
	if id_user == '':
		abort(400)		
    return jsonify( { 'publicaciones': getPublicaciones(id_user) } )

@app.route('/api/v1.0/publicaciones/<int:id_pub>/like/?id_user=455', methods = ['POST'])
@auth.login_required
def like(id_pub):
	id_user = request.args.get('id_user','')
    if id_user == '':
		abort(400)	
    addLike(id_pub, id_user)
    return jsonify( { 'result': True } )

@app.route('/api/v1.0/publicaciones/<int:id_pub>/like/?id_user=455', methods = ['DELETE'])
@auth.login_required
def dislike(id_pub):
	id_user = request.args.get('id_user','')
    if id_user == '':
		abort(400)	
    removeLike(id_pub, id_user)
    return jsonify( { 'result': True } )

@app.route('/api/v1.0/publicaciones/audios', methods = ['POST'])
@auth.login_required
def create_audio():
    if not request.json:
        abort(400)
    id_usuario = request.json['id_usuario']
	fecha = request.json['fecha']
	url = request.json['url']
	desc = request.json['desc']
    id_pub = addAudio(id_usuario, fecha, url, desc)
    return jsonify( { 'id_pub': id_pub } ), 201
	
@app.route('/api/v1.0/publicaciones/audios/<int:id_pub>', methods = ['GET'])
@auth.login_required
def get_audio(id_pub):
	audio = getAudio(id_pub);
    if len(audio) == 0:
        abort(404)
    return jsonify( { 'audio': audio } )
	
@app.route('/api/v1.0/publicaciones/enlaces', methods = ['POST'])
@auth.login_required
def create_enlace():
    if not request.json:
        abort(400)
    id_usuario = request.json['id_usuario']
	fecha = request.json['fecha']
	url = request.json['url']
	desc = request.json['desc']
    id_pub = addEnlace(id_usuario, fecha, url, desc)
    return jsonify( { 'id_pub': id_pub } ), 201
	
@app.route('/api/v1.0/publicaciones/enlaces/<int:id_pub>', methods = ['GET'])
@auth.login_required
def get_enlace(id_pub):
	enlace = getEnlace(id_pub);
    if len(enlace) == 0:
        abort(404)
    return jsonify( { 'enlace': enlace } )
	
@app.route('/api/v1.0/publicaciones/fotos', methods = ['POST'])
@auth.login_required
def create_foto():
    if not request.json:
        abort(400)
    id_usuario = request.json['id_usuario']
	fecha = request.json['fecha']
	url = request.json['url']
	desc = request.json['desc']
    id_pub = addFoto(id_usuario, fecha, url, desc)
    return jsonify( { 'id_pub': id_pub } ), 201
	
@app.route('/api/v1.0/publicaciones/fotos/<int:id_pub>', methods = ['GET'])
@auth.login_required
def get_foto(id_pub):
	foto = getFoto(id_pub);
    if len(foto) == 0:
        abort(404)
    return jsonify( { 'foto': foto } )
		
@app.route('/api/v1.0/publicaciones/textos', methods = ['POST'])
@auth.login_required
def create_texto():
    if not request.json:
        abort(400)
    id_usuario = request.json['id_usuario']
	fecha = request.json['fecha']
	texto = request.json['url']
    id_pub = addTexto(id_usuario, fecha, texto)
    return jsonify( { 'id_pub': id_pub } ), 201
	
@app.route('/api/v1.0/publicaciones/textos/<int:id_pub>', methods = ['GET'])
@auth.login_required
def get_texto(id_pub):
	texto = getTexto(id_pub);
    if len(texto) == 0:
        abort(404)
    return jsonify( { 'texto': texto } )
		
@app.route('/api/v1.0/publicaciones/videos', methods = ['POST'])
@auth.login_required
def create_video():
    if not request.json:
        abort(400)
    id_usuario = request.json['id_usuario']
	fecha = request.json['fecha']
	url = request.json['url']
	desc = request.json['desc']
    id_pub = addVideo(id_usuario, fecha, url, desc)
    return jsonify( { 'id_pub': id_pub } ), 201
	
@app.route('/api/v1.0/publicaciones/videos/<int:id_pub>', methods = ['GET'])
@auth.login_required
def get_video(id_pub):
	video = getVideo(id_pub);
    if len(video) == 0:
        abort(404)
    return jsonify( { 'video': video } )
	
@app.route('/api/v1.0/respuestas', methods = ['POST'])
@auth.login_required
def create_respuesta():
    if not request.json:
        abort(400)
    id_usuario = request.json['id_usuario']
	fecha = request.json['fecha']
	texto = request.json['texto']
	id_comentario = request.json['id_comentario']
    id_contestacion = addRespuesta(id_usuario, fecha, texto, id_comentario)
    return jsonify( { 'id_contestacion': id_contestacion) } ), 201
	
@app.route('/api/v1.0/respuestas', methods = ['GET'])
@auth.login_required
def get_respuestas():
	id_comentario = request.args.get('id_comentario','')
	if id_comentario == '':
		abort(400)		
    return jsonify( { 'respuestas': getRespuestas(id_comentario) } )
	
@app.route('/api/v1.0/usuarios/<int:id_user>/seguidores', methods = ['GET'])
@auth.login_required
def get_seguidores(id_user):
	seguidores = getSeguidores(id_user);
    if len(seguidores) == 0:
        abort(404)
    return jsonify( { 'seguidores': seguidores } )

@app.route('/api/v1.0/usuarios/<int:id_user>/seguidos', methods = ['GET'])
@auth.login_required
def get_seguidos(id_user):
	seguidos = getSeguidos(id_user);
    if len(seguidos) == 0:
        abort(404)
    return jsonify( { 'seguidos': seguidos } )
	
@app.route('/api/v1.0/usuarios', methods = ['POST'])
@auth.login_required
def create_usuario():
    if not request.json:
        abort(400)
    usuario = request.json['usuario']
	nombre = request.json['nombre']
	email = request.json['email']
	desc = request.json['desc']
	pw = request.json['pw']
    id_usuario = addUsuario(usuario, nombre, email, desc, pw)
    return jsonify( { 'id_usuario': id_usuario } ), 201

@app.route('/api/v1.0/usuarios/<int:id_user>', methods = ['GET'])
@auth.login_required
def get_usuario(id_user):
	usuario = getUsuario(id_user);
    if len(usuario) == 0:
        abort(404)
    return jsonify( { 'usuario': usuario } )

@app.route('/api/v1.0/usuarios/<int:id_user>', methods = ['PUT'])
@auth.login_required
def update_usuario(id_user):
    usuario = getUsuario(id_user)
    if len(usuario) == 0:
        abort(404)
    if not request.json:
        abort(400)
    usuario = request.json['usuario']
	nombre = request.json['nombre']
	email = request.json['email']
	desc = request.json['desc']
	pw = request.json['pw']
    updateUsuario(id_user, usuario, nombre, email, desc, pw)
    return jsonify( { 'result': True } )
    
@app.route('/api/v1.0/usuarios/<int:id_user>', methods = ['DELETE'])
@auth.login_required
def delete_usuario(id_user):
    usuario = getUsuario(id_user)
    if len(usuario) == 0:
        abort(404)
    deleteUsuario(id_user)
    return jsonify( { 'result': True } )
    
	
if __name__ == '__main__':
    app.run(debug = True)