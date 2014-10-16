drop table if exists urls;
create table urls (
  short string primary key,
  custom string,
  dest string not null,
  createdby string not null,
  createdon string not null
);
drop table if exists hits;
create table hits (
  short string,
  hitdate string,
  hits4 integer default 0,
  hits6 integer default 0
);
drop table if exists users;
create table users (
  username string,
  password string,
  registered_on string,
  last_login string,
  logins integer default 0
);
