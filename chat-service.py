from app import create_app, db
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    
# try load_dotenv(dotenv_path):
#     pass
# except SystemError
# ???


app = create_app('development')

@app.cli.command()
def dev():
    
    with app.app_context():
        db.drop_all()
        db.create_all()

    pass


@app.cli.command()
def test():
    """Runs the unit tests."""
    import sys
    import unittest

    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.errors or result.failures:
        sys.exit(1)


@app.cli.command()
def fill_db():
    from utils.db_generator import FakeGenerator
    FakeGenerator().start()
