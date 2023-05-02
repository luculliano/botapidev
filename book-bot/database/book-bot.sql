create table book(
    book_id integer primary key autoincrement,
    book_name text,
    author_name text
);

create table book_pages(
    book_pages_id integer primary key autoincrement,
    page_number integer,
    page_text text,
    book_id integer,
    constraint unique_book_page_number unique (book_id, page_number)
    foreign key (book_id) references book (book_id)
);

create table if not exists bookmarks(
    bookmarks_id integer primary key autoincrement,
    page_number integer,
    users_id integer,
    constraint unique_user_page_number unique(page_number, users_id), /*уникальное правило*/
    foreign key (users_id) references users (users_id)
    on delete cascade  /*удаление пользователя удалит все с ним записи здесь*/
);

create table if not exists users(
    users_id integer primary key autoincrement,
    tg_uid integer unique not null,
    book_pages_id integer,
    foreign key (book_pages_id) references book_pages (book_pages_id)
);

insert into book(book_name, author_name) values ("Ham on Rye", "Charles Bukowski");
