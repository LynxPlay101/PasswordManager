import sql.ManagedPasswordDao as passwordDao
from PasswordManagerGUI import *
from sql.SQLLiteConnection import SQLLiteConnection

dao = passwordDao.ManagedPasswordDao(SQLLiteConnection("passwords.db"))
dao.create_table()

screen = PasswordManagerGui(dao)

screen.screen.deiconify()
screen.screen.lift()
screen.screen.mainloop()


