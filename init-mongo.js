db.createUser(
    {
        user: "admin",
        pwd: "S3cret",
        roles: [
            {
                role: "readWrite",
                db  : "pokemon"
            }
        ]
    }
)