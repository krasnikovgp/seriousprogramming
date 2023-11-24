def write_to_db(userid, name, surname, birthday):
    with open('database.txt', 'a', encoding='UTF-8') as file:
        file.write(str(userid))
        file.write('\t')
        file.write(name)
        file.write('\t')
        file.write(surname)
        file.write('\t')
        file.write(str(birthday))
        file.write('\n')

