from app import app
from models import db
from models.role import Role
from models.permission import Permission
from models.rbac_associations import roles_permissions
from models.user import User


def seed_roles_permissions():
    # Ensure Flask has the context to work with the app/db
    with app.app_context():

        # List of permission names to be created
        perm_names = [
            "create_task", "edit_own_task", "delete_own_task",
            "delete_task", "view_users", "assign_roles"
        ]

        permissions = []

        for name in perm_names:
            # Check if permission already exists
            perm = Permission.query.filter_by(name=name).first()
            if not perm:
                # Create and stage new permission
                perm = Permission(name=name)
                db.session.add(perm)
            permissions.append(perm)

        # Commit all permissions to the database
        db.session.commit()

        # Define roles and what permissions they should have
        role_data = {
            "Admin": ["create_task", "delete_task", "view_users", "assign_roles"],
            "User": ["create_task", "edit_own_task", "delete_own_task"]
        }

        for role_name, perm_list in role_data.items():
            # Check if role already exists
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                # Create and stage new role
                role = Role(name=role_name)
                db.session.add(role)

            # Link appropriate permissions to each role
            role.permissions = [
                Permission.query.filter_by(name=perm).first()
                for perm in perm_list
            ]

        # Commit roles and their permissions
        db.session.commit()
        print("Roles and permissions seeded successfully.")

# Run the seeding function if the file is executed directly
if __name__ == "__main__":
    seed_roles_permissions()
