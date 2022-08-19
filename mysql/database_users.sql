use myremotedb;

CREATE TABLE users(
  user_id INT NOT NULL,
  user_name VARCHAR(50) NOT NULL,
  creation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id)
);

INSERT into users(user_id, user_name)
values(1, "Tomer"),(2, "Julia"),(3, "David");