drop table if exists urls;
create table urls (
  id integer primary key autoincrement,
  short string,
  dest string not null,
  hits integer default 0
);
