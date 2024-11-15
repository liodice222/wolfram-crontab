#List of commands used to set up key chain 

security add-generic-password -a "application" -s "secret_name" -w "actual_password"
security find-generic-password -a "application" -s "secret_name"
