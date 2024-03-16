class ChatRoom:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if username not in self.users:
            self.users[username] = {'friends': set(), 'messages': []}

    def add_friends(self, username):
        if username in self.users:
            friends = input("Entrez les noms des amis séparés par des virgules : ").split(',')
            existing_users = self.users.keys()
            for friend in friends:
                if friend not in existing_users:
                    print(f"L'ami {friend} n'existe pas.")
                else:
                    self.users[username]['friends'].add(friend)
                    print(f"{friend} ajouté avec succès.")
        else:
            print("Utilisateur non trouvé.")

    def send_message(self, sender, message):
        if sender not in self.users:
            print("Utilisateur non trouvé.")
            return
        for user in self.users:
            self.users[user]['messages'].append((sender, message))


    def get_messages(self, username):
        if username not in self.users:
            print("Utilisateur non trouvé.")
            return []
        return self.users[username]['messages']


def main():
    chat_room = ChatRoom()
    print("\n1. Ajouter un utilisateur")
    print("2. Ajouter des amis")
    print("3. Envoyer un message")
    print("4. Lire les messages")
    print("5. Quitter\n")
    while True:
        choice = input("\nChoisissez une option : ")

        if choice == '1':
            username = input("Entrez le nom de l'utilisateur à ajouter : ")
            chat_room.add_user(username)
            print("Utilisateur ajouté avec succès.")

        elif choice == '2':
            username = input("Entrez le nom de l'utilisateur : ")
            chat_room.add_friends(username)

        elif choice == '3':
            sender = input("Expéditeur : ")
            message = input("Message : ")
            chat_room.send_message(sender, message)
            print("Message envoyé avec succès.")

        elif choice == '4':
            username = input("Entrez votre nom d'utilisateur : ")
            messages = chat_room.get_messages(username)
            print("Vos messages :")
            for sender, message in messages:
                print(f"De {sender}: {message}")

        elif choice == '5':
            print("Merci d'avoir utilisé le chat. Au revoir !")
            break

        else:
            print("Option invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
