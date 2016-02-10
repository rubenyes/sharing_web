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
	id int primary key autoincrement,
	usuario text,
	nombre text,
	email text,
	desc text,
	pass text
);

CREATE TABLE publicaciones(
	id int primary key autoincrement,
	id_usuario int,
	fecha date,
	tipo int,
	FOREIGN KEY(id_usuario) REFERENCES usuarios(id),
);

CREATE TABLE videos(
	id int primary key autoincrement,
	id_pub int,
	url text,
	desc text,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id),
);

CREATE TABLE fotos(
	id int primary key autoincrement,
	id_pub int,
	url text,
	desc text,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id),
);

CREATE TABLE audios(
	id int primary key autoincrement,
	id_pub int,
	url text,
	desc text,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id),
);

CREATE TABLE enlaces(
	id int primary key autoincrement,
	id_pub int,
	url text,
	desc text,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id),
);

CREATE TABLE textos(
	id int primary key autoincrement,
	id_pub int,
	texto text,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id),
);

CREATE TABLE likes(
	id_pub int,
	id_usuario int,
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id),
	FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE seguidores(
	id_usuario int,
	id_seguidor int,
	FOREIGN KEY(id_usuario) REFERENCES usuarios(id),
	FOREIGN KEY(id_seguidor) REFERENCES usuarios(id)
);

CREATE TABLE contestaciones(
	id int primary key autoincrement,
	id_usuario int,
	fecha date,
	texto text,
	FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE comentarios(
	id_contestacion int,
	id_pub int,
	FOREIGN KEY(id_contestacion) REFERENCES contestaciones(id),
	FOREIGN KEY(id_pub) REFERENCES publicaciones(id)
);

CREATE TABLE respuestas(
	id_contestacion int,
	id_comentario int,
	FOREIGN KEY(id_contestacion) REFERENCES contestaciones(id),
	FOREIGN KEY(id_comentario) REFERENCES comentarios(id)
);