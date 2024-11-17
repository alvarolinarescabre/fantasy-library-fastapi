    #!/bin/bash
    
    echo "Creating users..."
    echo "Creating admin user..."
    mongosh admin --host localhost -u root -p root --eval "db.createUser({user: 'admin', pwd: 'admin', roles: [ { role: 'userAdminAnyDatabase', db: 'admin' },{ role: 'root', db: 'admin' } ]});"
    echo "Creating myuser in fantasy_library..."
    # note: creating a user other than in admin db is not recommended.
    mongosh admin --host localhost -u root -p root --eval "db = db.getSiblingDB('fantasy_library'); db.createUser({user: 'myuser', pwd: 'mypwd', roles: [ { role: 'readWrite', db: 'fantasy_library' } ]});"
    echo "Users created."
