create database pico;
create database test_pico;
grant all on pico.* to 'pico' identified by 'password';
grant all on pico.* to 'pico'@'localhost' identified by 'password';
grant all on test_pico.* to 'pico' identified by 'password';
grant all on test_pico.* to 'pico'@'localhost' identified by 'password';
