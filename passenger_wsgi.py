import sys,os
sys.path.append(os.getcwd())

from app import create_app

application = create_app()

# application.run()