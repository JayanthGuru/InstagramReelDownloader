import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
from bs4 import BeautifulSoup
import requests
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.folder_location = "C:\\Users\\Username\\Downloads"
        self.title("uBe Reel Downloader")
        self.geometry("900x200")
        self.iconbitmap("assets/uBe_reel_icon.ico")

        # Create the frames
        self.logo_frame = tk.Frame(self, width=200, height=200)
        self.info_frame = tk.Frame(self, width=300, height=200)

        # Add widgets to the logo frame
        self.image_file = (
            "assets/logo.png"  # Replace with the path to your image file
        )
        self.image = Image.open(self.image_file)
        self.image = self.image.resize((150, 150))  # Set the desired width and height
        self.logo_image = ImageTk.PhotoImage(self.image)

        self.logo_label = tk.Label(self.logo_frame, image=self.logo_image)

        # Add widgets to the info frame
        self.url_label = tk.Label(self.info_frame, text="URL:")
        self.url_entry = tk.Entry(self.info_frame, width=70)

        self.folder_location_label = tk.Label(self.info_frame, text="Folder location:")
        self.folder_location_entry = tk.Entry(self.info_frame, width=70)

        self.download_button = tk.Button(
            self.info_frame, text="Download", command=self.submit_info, width=20
        )

        # Position the frames
        self.logo_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.info_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Position the logo label
        self.logo_label.pack()

        # Position the info labels, entry fields, and button
        self.url_label.grid(row=0, column=0, padx=10, pady=5)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.folder_location_label.grid(row=1, column=0, padx=10, pady=5)
        self.folder_location_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        # self.folder_location_entry.insert(0, self.folder_location)

        self.select_folder_image = Image.open("assets/select_folder_logo.png")
        self.select_folder_image = self.select_folder_image.resize((20, 20))
        self.select_folder_icon = ImageTk.PhotoImage(self.select_folder_image)
        self.select_folder_button = tk.Label(
            self.info_frame, image=self.select_folder_icon
        )
        self.select_folder_button.bind("<Button-1>", self.select_folder_location)
        self.select_folder_button.grid(row=1, column=2, padx=10, pady=5, sticky=tk.E)

        self.download_button.grid(row=2, columnspan=2, padx=10, pady=10)

        # Create the status label
        self.status_label = tk.Label(self.info_frame, text="")
        self.status_label.grid(row=3, column=0, columnspan=2)

    def submit_info(self):  # sourcery skip: remove-redundant-if
        url_entry = self.url_entry.get()
        folder_location_entry = self.folder_location_entry.get()

        self.config(cursor="wait")

        if url_entry != "" and folder_location_entry != "":
            status = str(self.download_reel(url_entry, folder_location_entry))
            if status == "Successful":
                self.status_label.config(text="Successful", fg="green")
                self.url_entry.delete(0, tk.END)
            else:
                self.status_label.config(text=status, fg="red")
        elif url_entry == "":
            self.status_label.config(text="URL can't be empty", fg="red")
            print("Submission failed. Please provide url.")
        elif folder_location_entry == "":
            self.status_label.config(text="folder location can't be empty", fg="red")
            print("Submission failed. Please provide folder location.")
        else:
            self.status_label.config(text="ERROR", fg="red")
            print("Submission failed. Please provide all required information.")

        self.config(cursor="")
        self.download_button.config(text="Download", fg="black")
        self.download_button.config(state=tk.NORMAL)

    def select_folder_location(self, event):
        self.folder_location = filedialog.askdirectory()
        self.folder_location_entry.delete(0, tk.END)
        self.folder_location_entry.insert(0, self.folder_location)

    def download_reel(self, reel_url, folder_location):
        downloader = ReelDownloader()
        return downloader.start_process(reel_url, folder_location)


class ReelDownloader:
    def __init__(self):
        self.guardian_url = "https://en.savefrom.net/391GA/"

    def download_song(self, video_title, video_download_link, folder_location):
        """Downloads the reel from single_link provided by gardian_website"""

        try:
            new_filename = f"{video_title}.mp4"

            # Create the directory if it doesn't exist
            if not os.path.exists(folder_location):
                os.makedirs(folder_location)

            if os.path.exists(os.path.join(folder_location, new_filename)):
                return "File already exists"

            # Download the file using requests
            response = requests.get(video_download_link, stream=True)

            # Save the file to a temporary location
            temp_filepath = os.path.join(folder_location, "temp_file")

            with open(temp_filepath, "wb") as file:
                shutil.copyfileobj(response.raw, file)

            # Rename the file
            new_filepath = os.path.join(folder_location, new_filename)
            os.rename(temp_filepath, new_filepath)
            return "Successful"

        except Exception as e:
            """
            Error-2 : The error is caused by while downloading the video which means due to shutil or os modules
            """
            return "Error Type-2, Please try again."

    def start_process(self, reel_url, folder_location):
        """This function opens the chrome browser and then goes to Gardian url and then uses selenium to fill the reel_url and click download button and then get reel_name and single_link to download the reel"""

        try:
            #service = Service('path/to/chromedriver')
            #service.creationflags = CREATE_NO_WINDOW
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--user-agent=Your Custom User Agent")
            
            # driver = webdriver.Chrome(service=service, options=chrome_options)
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(self.guardian_url)

            time.sleep(2)

            try:
                # Find the form elements and fill in the details
                input_field = driver.find_element(By.ID, "sf_url")
                input_field.send_keys(reel_url)

                time.sleep(1)

                # Find and click the button
                button = driver.find_element(By.ID, "sf_submit")
                button.click()

                time.sleep(2)

                updated_html_code = driver.page_source
                driver.quit()

                soup = BeautifulSoup(updated_html_code, "html.parser")

                video_title = soup.find("div", {"class": "row title"})
                video_title = str(video_title["title"])[:15] + ".."

                video_download_link = soup.find(
                    "a", {"class": "link link-download ga_track_events download-icon"}
                )
                video_download_link = video_download_link["href"]
                return self.download_song(
                    video_title, video_download_link, folder_location
                )

            except Exception as e:
                """
                Error-1 : NoneType be returned by selinium just the script could not get the link.
                """
                return "Error Type-1, Please try again."
        except Exception as e:
                """
                Error-3 : Selenium error i think no chrome.
                """
                return "Error Type-3, Please check if selenium is installed or not, try again."


if __name__ == "__main__":
    app = Application()
    app.mainloop()
