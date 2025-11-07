from tortoise import Tortoise
from database.models.all_models import QuarterSettings

async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['database.models.all_models']}
    )
    await Tortoise.generate_schemas()
    
    # Default chorak sozlamalarini yaratish
    quarter_settings = await QuarterSettings.first()
    if not quarter_settings:
        await QuarterSettings.create(current_quarter=1)
