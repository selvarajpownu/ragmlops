import uvicorn
from utils import config_reader

configFileData = config_reader.configData()

if __name__ == '__main__':                  
    uvicorn.run('servers.app:app',  # Corrected path to the app
                host=configFileData['config']['DB_HOST'],
                port=configFileData['config']['DB_PORT'],
                reload=True)
