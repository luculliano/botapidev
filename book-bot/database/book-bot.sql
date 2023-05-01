create table if not exists users(
    users_id integer primary key autoincrement,
    tg_uid integer unique not null,
    cur_page integer,
    constraint positive_value1 check(0 < cur_page and cur_page <= 300)
);

create table if not exists bookmarks(
    bookmarks_id integer primary key autoincrement,
    page_number integer,
    users_id integer,
    constraint unique_user_page_number unique(page_number, users_id), /*уникальное правило*/
    constraint positive_value2 check(0 < page_number and page_number <= 300),
    foreign key (users_id) references users (users_id)
    on delete cascade  /*удаление пользователя удалит все с ним записи здесь*/
);

insert into users(tg_uid, cur_page) values (777, 1);
