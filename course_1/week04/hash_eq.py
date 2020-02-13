class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __hash__(self):
        return hash(self.email)

    def __eq__(self, other):
        return self.email == other.email


def _main():
    jane = User('Jane Doe', 'jdoe@example.com')
    joe = User('Joe Doe', 'jdoe@example.com')
    print(jane == joe) #eq

    print(hash(jane))
    print(hash(joe))

    user_email_map = {user: user.name for user in [jane, joe]}
    print(user_email_map)


if __name__ == "__main__":
    _main()