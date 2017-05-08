drop table if exists users;
create table users(
id integer identity(1,1),
username text not null,
password text not null,
nickname text not null,
sex text,
birthday text,
email text,
phone_number text not null,
head_img text,
);