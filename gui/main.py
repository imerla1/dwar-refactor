from utils.parse_game_config import parse_game_config
from globals import main_logger
from user_prompt import prompt_user
from utils.generate_world_map import main as generate_world_map
from utils.user_data import check_user_is_admin
import asyncio
from widgets.verify_license_key_window import LicenseKeyVerificationWidget
import sys
from PyQt5.QtWidgets import QApplication
from database import Base, engine, SessionLocal
from models.token_model import TokenModel
from utils.token_manager import fetch_jwt_token
from widgets.splash_screen import SplashScreen



if __name__ == '__main__':
    # game_config = parse_game_config(main_logger, 'game_config.yaml')
    # prompted_user = prompt_user()
    # user = game_config.users.get(prompted_user)
    # assert user is not None, f"{prompted_user} not found"

    # asyncio.run(generate_world_map(main_logger))
    # print(check_if_user_injured("KysBiG", main_logger))
    print(check_user_is_admin("- - Almazik -", main_logger))
    Base.metadata.create_all(bind=engine)
    app = QApplication(sys.argv)
    db = SessionLocal()
    fetch_jwt_token(db)
    # print(db.query(TokenModel).first())
    # Set the application style
    app.setStyle('Fusion')

    # Set a global style for the application
    app.setStyleSheet('QMessageBox {font-size: 14px;}')
    splash_screen = SplashScreen()
    splash_screen.setStyleSheet(
        '''
            #LabelTitle {
                font-size: 60px;
                color: #93deed;
            }

            #LabelDesc {
                font-size: 30px;
                color: #c2ced1;
            }

            #LabelLoading {
                font-size: 30px;
                color: #e8e8eb;
            }

            QFrame {
                background-color: #2F4454;
                color: rgb(220, 220, 220);
            }

            QProgressBar {
                background-color: #DA7B93;
                color: rgb(200, 200, 200);
                border-style: none;
                border-radius: 10px;
                text-align: center;
                font-size: 30px;
            }

            QProgressBar::chunk {
                border-radius: 10px;
                background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
            }
        '''
    )
    splash_screen.show()
    window = LicenseKeyVerificationWidget()
    # window.show()
    sys.exit(app.exec_())