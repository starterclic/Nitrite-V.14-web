"""
Script de migration des données JSON vers PostgreSQL
Migre les données de l'ancienne version vers la nouvelle architecture
"""
import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.db.base import AsyncSessionLocal, engine, Base
from app.db.models.application import Application
from app.db.models.tool import Tool
from app.db.models.profile import Profile


async def load_json_file(file_path: str):
    """Charger un fichier JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Fichier non trouvé: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de parsing JSON: {e}")
        return None


async def migrate_applications(session):
    """Migrer les applications depuis programs.json"""
    print("\n📦 Migration des applications...")

    # Path to old data
    old_data_path = Path(__file__).parent.parent.parent.parent / "data" / "programs.json"

    data = await load_json_file(str(old_data_path))
    if not data:
        print("⚠️  Fichier programs.json non trouvé, utilisation de données d'exemple")
        # Create sample data
        data = {
            "Navigateurs": {
                "Google Chrome": {
                    "description": "Navigateur web rapide et sécurisé de Google",
                    "download_url": "https://www.google.com/chrome/",
                    "install_args": "/silent /install",
                    "category": "Navigateurs",
                    "essential": True,
                    "winget_id": "Google.Chrome",
                    "admin_required": True
                },
                "Mozilla Firefox": {
                    "description": "Navigateur web open source et respectueux de la vie privée",
                    "download_url": "https://www.mozilla.org/firefox/",
                    "install_args": "/S",
                    "category": "Navigateurs",
                    "essential": True,
                    "winget_id": "Mozilla.Firefox",
                    "admin_required": True
                }
            },
            "Bureautique": {
                "Microsoft Office": {
                    "description": "Suite bureautique complète de Microsoft",
                    "download_url": "https://www.office.com",
                    "category": "Bureautique",
                    "essential": True,
                    "admin_required": True
                }
            }
        }

    count = 0
    for category, apps in data.items():
        for app_name, app_data in apps.items():
            # Check if app already exists
            query = select(Application).where(Application.name == app_name)
            result = await session.execute(query)
            existing = result.scalar_one_or_none()

            if existing:
                print(f"  ⏭️  {app_name} existe déjà")
                continue

            # Create new application
            app = Application(
                name=app_name,
                description=app_data.get("description", ""),
                category=category,
                winget_id=app_data.get("winget_id"),
                download_url=app_data.get("download_url"),
                install_args=app_data.get("install_args"),
                essential=app_data.get("essential", False),
                admin_required=app_data.get("admin_required", True),
                website=app_data.get("download_url"),
                metadata=app_data
            )

            session.add(app)
            count += 1

            if count % 50 == 0:
                print(f"  📝 {count} applications traitées...")

    await session.commit()
    print(f"✅ {count} applications migrées")


async def migrate_tools(session):
    """Migrer les outils système depuis tools.json"""
    print("\n🔧 Migration des outils système...")

    old_data_path = Path(__file__).parent.parent.parent.parent / "web" / "data" / "tools.json"

    data = await load_json_file(str(old_data_path))
    if not data:
        print("⚠️  Fichier tools.json non trouvé, utilisation de données d'exemple")
        data = [
            {
                "section": "Réparation Système",
                "tools": [
                    {
                        "name": "DISM Scan",
                        "description": "Analyser et réparer l'image système Windows",
                        "command": "DISM /Online /Cleanup-Image /RestoreHealth",
                        "requires_admin": 1,
                        "icon": "🔧"
                    },
                    {
                        "name": "SFC Scan",
                        "description": "Vérifier l'intégrité des fichiers système",
                        "command": "sfc /scannow",
                        "requires_admin": 1,
                        "icon": "🔍"
                    }
                ]
            },
            {
                "section": "Réseau",
                "tools": [
                    {
                        "name": "Reset Network",
                        "description": "Réinitialiser les paramètres réseau",
                        "command": "netsh winsock reset && netsh int ip reset",
                        "requires_admin": 1,
                        "icon": "🌐"
                    }
                ]
            }
        ]

    count = 0
    for section_data in data:
        section = section_data.get("section", "Autres")
        tools = section_data.get("tools", [])

        for tool_data in tools:
            tool_name = tool_data.get("name", "")

            # Check if tool already exists
            query = select(Tool).where(Tool.name == tool_name, Tool.section == section)
            result = await session.execute(query)
            existing = result.scalar_one_or_none()

            if existing:
                print(f"  ⏭️  {tool_name} existe déjà")
                continue

            # Create new tool
            tool = Tool(
                name=tool_name,
                description=tool_data.get("description", ""),
                section=section,
                command=tool_data.get("command", ""),
                requires_admin=tool_data.get("requires_admin", 1),
                icon=tool_data.get("icon"),
                metadata=tool_data
            )

            session.add(tool)
            count += 1

    await session.commit()
    print(f"✅ {count} outils migrés")


async def migrate_profiles(session):
    """Migrer les profils prédéfinis"""
    print("\n👤 Migration des profils...")

    profiles_data = [
        {
            "name": "🎮 Gaming Station",
            "description": "Configuration optimale pour les joueurs",
            "icon": "🎮",
            "applications": [],  # To be populated later
            "tools": []
        },
        {
            "name": "💼 Bureau Professionnel",
            "description": "Outils essentiels pour le travail de bureau",
            "icon": "💼",
            "applications": [],
            "tools": []
        },
        {
            "name": "💻 Développeur",
            "description": "Environnement de développement complet",
            "icon": "💻",
            "applications": [],
            "tools": []
        },
        {
            "name": "🎨 Création Multimédia",
            "description": "Outils de création graphique et vidéo",
            "icon": "🎨",
            "applications": [],
            "tools": []
        },
        {
            "name": "🏫 Étudiant",
            "description": "Applications pour les études",
            "icon": "🏫",
            "applications": [],
            "tools": []
        },
        {
            "name": "🔧 Maintenance Technique",
            "description": "Tous les outils de maintenance",
            "icon": "🔧",
            "applications": [],
            "tools": []
        },
    ]

    count = 0
    for profile_data in profiles_data:
        # Check if profile exists
        query = select(Profile).where(Profile.name == profile_data["name"])
        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            print(f"  ⏭️  {profile_data['name']} existe déjà")
            continue

        # Create new profile
        profile = Profile(
            name=profile_data["name"],
            description=profile_data["description"],
            icon=profile_data["icon"],
            applications=profile_data["applications"],
            tools=profile_data["tools"]
        )

        session.add(profile)
        count += 1

    await session.commit()
    print(f"✅ {count} profils migrés")


async def main():
    """Main migration function"""
    print("🚀 Démarrage de la migration des données...")
    print("=" * 60)

    # Create tables
    print("\n📋 Création des tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables créées")

    # Run migrations
    async with AsyncSessionLocal() as session:
        try:
            await migrate_applications(session)
            await migrate_tools(session)
            await migrate_profiles(session)

            print("\n" + "=" * 60)
            print("🎉 Migration terminée avec succès !")
            print("\n📊 Statistiques:")

            # Get counts
            apps_count = await session.execute(select(Application))
            tools_count = await session.execute(select(Tool))
            profiles_count = await session.execute(select(Profile))

            print(f"  Applications: {len(apps_count.scalars().all())}")
            print(f"  Outils: {len(tools_count.scalars().all())}")
            print(f"  Profils: {len(profiles_count.scalars().all())}")

        except Exception as e:
            print(f"\n❌ Erreur lors de la migration: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
