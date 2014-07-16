class UserRouter(object):
    """
    A router to control all database operations on models in the
    login application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read login models go to users.
        """
        if model._meta.app_label == 'login' or model._meta.app_label == 'auth':
            return 'users'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to users.
        """
        if model._meta.app_label == 'login' or model._meta.app_label == 'auth':
            return 'users'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the login app is involved.
        """
        if obj1._meta.app_label == 'login' or \
           obj2._meta.app_label == 'login' or \
           obj1._meta.app_label == 'auth' or \
           obj2._meta.app_label == 'auth':
           return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the login app only appears in the 'users'
        database.
        """
        if db == 'users':
            return model._meta.app_label == 'login' or model._meta.app_label == 'auth'
        elif model._meta.app_label == 'login' or model._meta.app_label == 'auth':
            return False
        return None
