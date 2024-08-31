from internal.resources.generic.helper.flags import Flags

flags = Flags(env_file="sample.env")

db_username = flags.get("db_user","root", "Database username")
db_password = flags.get("db_pass", "password", "Database password")
db_host = flags.get("db_host", "localhost", "Database host")
db_port = flags.get("db_port", "3306", "Database port")
db_name = flags.get("db_name", "sample_db", "Database name")
server_port = flags.get("server_port", "5000", "Server port")
