"""Module responsible for file management witihin bank statements directories"""
import os
import datetime

class FileManagement:
    """
    Class for filtering and retrieving only new bank statement files
    """
    def __init__(self, directory_path: str) -> None:
        """
        Initializes the FileManagement instance with files from directory_path.

        Args:
            directory_path (str): path to the directory with bank statement files
        """
        self.directory_path = directory_path
        self.all_files = []
        self.new_files = []

    def get_list_of_all_files(self) -> None:
        """
        Generates a list of mt940 files within self.directory_path
        """
        all_files = [
            file for file in os.listdir(self.directory_path ) if file[-4:] == ".old"
        ]
        self.all_files = all_files

    def get_today_created_files(self) -> None:
        """
        Looping each file from directory and retrieve only 
        files with creation date equal to current date.
        """
        if self.all_files is None:
            self.get_list_of_all_files()
        current_date = datetime.datetime.now().date()
        for file in self.all_files:
            creation_time = os.path.getctime(file)
            formatted_time = datetime.datetime.fromtimestamp(creation_time).date()
            if current_date == formatted_time:
                self.new_files.append(file)
