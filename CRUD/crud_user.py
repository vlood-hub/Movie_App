from db_manager import user_storage_sql as user_storage
import movie_3


def cmd_users_list():
    print("Select a user or modify the list:\n")
    users = user_storage.list_users()
    for idx, user in enumerate(users):
        print(f"{idx+1}. {user['name']}")
    print(f"\n+. Create a new user")
    print(f"-. Delete auser")
    print(f"o. Update a user's name\n")
    user_choice = input("Enter choice: ")

    if user_choice.isdigit():
        selected_user = users[int(user_choice)-1]
        if selected_user:
            print(f"\nWelcome back, {selected_user['name']}! 🎬")
            movie_3.movies_cmd(selected_user)
        else:
            print("Invalid choice.")
    else:
        match user_choice:
            case "+": cmd_add_user()
            case "-": cmd_del_user()
            case "o": cmd_update_user()


def cmd_add_user():
    """ add user """
    user_name = input("Enter user name: ")
    user_storage.add_user(user_name)
    print(f"User {user_name} successfully added")
    cmd_users_list()


def cmd_del_user():
    """ delete user """
    user_name = input("Enter user name: ")
    user_storage.delete_user(user_name)
    print(f"User {user_name} successfully deleted")
    cmd_users_list()


def cmd_update_user():
    """ upadte user's name """
    old_user_name = input("Enter old user name: ")
    new_user_name = input("Enter new user name: ")
    user_storage.update_user(new_user_name, old_user_name)
    print(f"User {new_user_name} successfully added")
    cmd_users_list()
