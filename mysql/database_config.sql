use myremotedb;

CREATE TABLE config(
  id INT NOT NULL,
  api_gateway_url VARCHAR(50) NOT NULL,
  browser_name VARCHAR(40) NOT NULL,
  user_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);

INSERT into config (id, api_gateway_url, browser_name, user_name)
values (1, "http://127.0.0.1:5001/users/get_user_data", "Chrome", "Assaf");
INSERT into config (id, api_gateway_url, browser_name, user_name)
values (2, "http://127.0.0.1:5001/users/get_user_data", "Firefox", "Alisa");
INSERT into config (id, api_gateway_url, browser_name, user_name) 
values (3, "http://127.0.0.1:5001/users/get_user_data", "Chrome", "Revital");