SELECT users.id,
    users.uid,
    users.name,
    users.enable,
    users.blacklist,
    rank.intlevel as level
FROM users
    LEFT JOIN rank ON rank.id = users.rank
WHERE users.uid = ?