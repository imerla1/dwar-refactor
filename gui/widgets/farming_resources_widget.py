from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget
from utils.json_io import read_json
import requests
import xml.etree.cElementTree as et


class ResourceFarmingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.verticalLayout_5 = None
        self.horizontalLayout_3 = None
        self.stop_bot_button = None
        self.start_bot_button = None
        self.logs_list_view = None
        self.clear_logs_button = None
        self.resources_choose_list_widget = None
        self.remove_resource_button = None
        self.add_resource_button = None
        self.add_button = None
        self.resources_to_choose_list_widget = None
        self.horizontalLayout_2 = None
        self.horizontalLayoutWidget = None
        self.setting_checkbox_4 = None
        self.setting_checkbox_3 = None
        self.setting_checkbox_2 = None
        self.setting_checkbox_1 = None
        self.verticalLayout_3 = None
        self.verticalLayoutWidget_2 = None
        self.location_label = None
        self.location_choose_combo_box: QtWidgets.QComboBox | None = None
        self.bot_state = False
        self.world_json = read_json("world.json")
        self.init_ui()
        self.populate_location_combo_box()

        self.location_choose_combo_box.currentIndexChanged.connect(self.on_location_combobox_changed)

    def init_ui(self):
        self.setObjectName("Form")
        self.resize(736, 595)

        self.create_farming_location_widgets()
        self.create_farming_options_widgets()
        self.create_resource_widgets()

        self.create_layouts()
        self.connect_signals()

    def create_farming_location_widgets(self):
        verticalLayoutWidget = QtWidgets.QWidget(self)
        verticalLayoutWidget.setGeometry(QtCore.QRect(50, 20, 166, 80))
        verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout.setObjectName("verticalLayout")

        self.location_label = QtWidgets.QLabel("choose farming location")
        self.location_label.setObjectName("label")
        verticalLayout.addWidget(self.location_label)

        self.location_choose_combo_box = QtWidgets.QComboBox(verticalLayoutWidget)
        self.location_choose_combo_box.setObjectName("comboBox")

        verticalLayout.addWidget(self.location_choose_combo_box)

    def populate_location_combo_box(self):
        for location in self.world_json:
            loc_title = location.get("loc_title")
            loc_id = location.get("loc_id")
            self.location_choose_combo_box.addItem(loc_title)
            self.location_choose_combo_box.setItemData(self.location_choose_combo_box.count() - 1, loc_id)


    def on_location_combobox_changed(self, index):
        selected_item_text = self.location_choose_combo_box.currentText()
        selected_item_id = self.location_choose_combo_box.itemData(index)
        print("selected_item_text", selected_item_text, selected_item_id)
        area_dict = self.get_area(selected_item_id)
        self.resources_to_choose_list_widget.clear()
        for name, value in area_dict.items():
            skill = value.get("skill")
            resource_full_name = f"{name} [{skill}]"
            self.resources_to_choose_list_widget.addItem(resource_full_name)


    def create_farming_options_widgets(self):
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(340, 20, 160, 112))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.setting_checkbox_1 = QtWidgets.QCheckBox("Option 1", self.verticalLayoutWidget_2)
        self.verticalLayout_3.addWidget(self.setting_checkbox_1)
        self.setting_checkbox_2 = QtWidgets.QCheckBox("Option 2", self.verticalLayoutWidget_2)
        self.verticalLayout_3.addWidget(self.setting_checkbox_2)
        self.setting_checkbox_3 = QtWidgets.QCheckBox("Option 3", self.verticalLayoutWidget_2)
        self.verticalLayout_3.addWidget(self.setting_checkbox_3)
        self.setting_checkbox_4 = QtWidgets.QCheckBox("Option 4", self.verticalLayoutWidget_2)
        self.verticalLayout_3.addWidget(self.setting_checkbox_4)

    def create_resource_widgets(self):
        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 200, 661, 241))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.resources_to_choose_list_widget = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.resources_to_choose_list_widget.setObjectName("listWidget_2")
        self.resources_to_choose_list_widget.addItems(["Item 1", "Item 2", "Item 3"])
        self.horizontalLayout_2.addWidget(self.resources_to_choose_list_widget)

        self.add_resource_button = QtWidgets.QPushButton("add", self.horizontalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.add_resource_button)

        self.resources_choose_list_widget = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.resources_choose_list_widget.setObjectName("listWidget")
        self.resources_choose_list_widget.addItems(["Item A", "Item B"])
        self.horizontalLayout_2.addWidget(self.resources_choose_list_widget)

        self.remove_resource_button = QtWidgets.QPushButton("remove", self.horizontalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.remove_resource_button)

    def create_layouts(self):
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(50, 460, 571, 131))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.logs_list_view = QtWidgets.QListView(self.horizontalLayoutWidget_2)
        self.logs_list_view.setObjectName("listView")
        self.horizontalLayout_3.addWidget(self.logs_list_view)

        self.clear_logs_button = QtWidgets.QPushButton("clear logs", self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.addWidget(self.clear_logs_button)

        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(630, 520, 101, 71))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.start_bot_button = QtWidgets.QPushButton("start bot", self.verticalLayoutWidget_3)
        self.verticalLayout_5.addWidget(self.start_bot_button)
        self.stop_bot_button = QtWidgets.QPushButton("stop bot", self.verticalLayoutWidget_3)
        self.verticalLayout_5.addWidget(self.stop_bot_button)


    def get_area(self, area_id):
        resp = requests.get(f"https://w1.dwar.ru/hunt_conf.php?mode=hunt_farm&area_id={area_id}&instance_id=0")
        result_dict = dict()
        if resp.status_code == 200:
            content = resp.content
            tree = et.fromstring(content)
            for item in tree.findall('farm'):
                for child in item:
                    attrib_name = child.attrib['name']
                    attrib_skill = child.attrib['skill']
                    if attrib_name not in result_dict:
                        result_dict[attrib_name] = {
                            "skill": attrib_skill
                        }

        return dict(sorted(result_dict.items(), key=lambda x: int(x[1]['skill'])))

    def connect_signals(self):
        QtCore.QMetaObject.connectSlotsByName(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    screen = ResourceFarmingWindow()
    screen.show()

    sys.exit(app.exec_())
