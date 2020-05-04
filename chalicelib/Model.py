# see subclass for more specific Docstrings

class Model():
    def select(self):
        """
        Gets all entries from the database
        :return: list of dicts
        :raises: generic exception
        """
        pass

    def insert(self, name, email, message):
        """
        Inserts entry into database
        :param name: String
        :param email: String
        :param message: String
        :return: none, or string if failed
        :raises: Database errors on connection and insertion
        """
        pass
