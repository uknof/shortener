drop table if exists urls;
create table urls (
  short string primary key,
  dest string not null
);
drop table if exists hits;
create table hits (
  short string,
  hits4 integer default 0,
  hits6 integer default 0
);
