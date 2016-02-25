DROP TABLE if EXISTS usuarios;
DROP TABLE if EXISTS publicaciones;
DROP TABLE if EXISTS videos;
DROP TABLE if EXISTS fotos;
DROP TABLE if EXISTS audios;
DROP TABLE if EXISTS enlaces;
DROP TABLE if EXISTS textos;
DROP TABLE if EXISTS likes;
DROP TABLE if EXISTS seguidores;
DROP TABLE if EXISTS contestaciones;
DROP TABLE if EXISTS comentarios;
DROP TABLE if EXISTS respuestas;

CREATE TABLE usuarios(
	id integer primary key autoincrement,
	usuario text UNIQUE,
	nombre text,
	email text UNIQUE,
	desc text,
	pw text,
	num_seguidores integer,
	num_seguidos int
);

CREATE TABLE publicaciones(
	id integer primary key autoincrement,
	id_usuario integer,
	fecha date,
	tipo integer,
	num_likes integer,
	num_comentarios integer,
	num_compartido integer, 
	FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE videos(
	id integer primary key autoincrement,
	id_pub integer,
	url text,
	desc text,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id)
);

CREATE TABLE fotos(
	id integer primary key autoincrement,
	id_pub integer,
	url text,
	desc text,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id)
);

CREATE TABLE audios(
	id integer primary key autoincrement,
	id_pub integer,
	url text,
	desc text,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id)
);

CREATE TABLE enlaces(
	id integer primary key autoincrement,
	id_pub integer,
	url text,
	desc text,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id)
);

CREATE TABLE textos(
	id integer primary key autoincrement,
	id_pub integer,
	texto text,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id)
);

CREATE TABLE likes(
	id_pub integer,
	id_usuario integer,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id),
	FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE seguidores(
	id_usuario integer,
	id_seguidor integer,
	FOREIGN KEY(id_usuario) REFERENCES usuarios(id),
	FOREIGN KEY(id_seguidor) REFERENCES usuarios(id)
);

CREATE TABLE contestaciones(
	id integer primary key autoincrement,
	id_usuario integer,
	fecha date,
	texto text,
	FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE comentarios(
	id_contestacion integer,
	id_pub integer,
	num_respuestas integer,
	FOREIGN KEY(id_contestacion) REFERENCES contestaciones(id),
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id)
);

CREATE TABLE respuestas(
	id_contestacion integer,
	id_comentario integer,
	FOREIGN KEY(id_contestacion) REFERENCES contestaciones(id),
	FOREIGN KEY(id_comentario) REFERENCES comentarios(id)
);