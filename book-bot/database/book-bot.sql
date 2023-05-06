create table if not exists book(
    book_id integer primary key autoincrement,
    book_name text,
    author_name text
);

create table if not exists book_pages(
    book_pages_id integer primary key autoincrement,
    page_number integer,
    page_text text,
    book_id integer,
    constraint unique_book_page_number unique (book_id, page_number),
    foreign key (book_id) references book (book_id)
);

create table if not exists bookmarks(
    bookmarks_id integer primary key autoincrement,
    book_pages_id integer not null,
    users_id integer,
    constraint unique_user_page_number unique(book_pages_id, users_id), /*уникальное правило*/
    foreign key (users_id) references users (users_id) on delete cascade,
    foreign key (book_pages_id) references book_pages (book_pages_id)
    on delete cascade  /*удаление пользователя удалит все с ним записи здесь*/
);

create table if not exists users(
    users_id integer primary key autoincrement,
    tg_uid integer unique not null,
    book_pages_id integer not null,  /*not null ибо constraint check с условием нельзя в sqlite*/
    foreign key (book_pages_id) references book_pages (book_pages_id)
);

insert into book(book_name, author_name) values
  ("Ham on Rye", "Charles Bukowski");

alter table book add column page_amount integer;

update book set page_amount =
  (select COUNT(page_number) from book_pages WHERE book_id = 1)
  where book_id = 1;
