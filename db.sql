create table if not exists users
(
	id serial not null
		constraint users_pk
			primary key,
	user_name text,
	email text,
	password text,
	confirmed boolean default false
);


create unique index if not exists users_email_uindex
	on users (email);

create unique index if not exists users_user_name_uindex
	on users (user_name);

create table if not exists posts
(
	id serial not null
		constraint posts_pk
			primary key,
	submission_time timestamp not null,
	story text,
	user_id integer
		constraint posts_users_id_fk
			references users
				on update cascade on delete cascade,
	title text
);


create table if not exists files
(
	id serial not null
		constraint pictures_pk
			primary key,
	post_id integer not null
		constraint pictures_posts_id_fk
			references posts
				on update cascade on delete cascade,
	user_id integer not null
		constraint pictures_users_id_fk
			references users
				on update cascade on delete cascade,
	category text,
	filename text not null
);


