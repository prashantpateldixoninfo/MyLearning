import tkinter as tk
import csv
from datetime import datetime
import threading
import logging
import os
import time

from PIL import Image, ImageTk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# ---------------- SETTINGS ----------------
TARGET_IP = "192.168.1.1"
LOG_FILE = "device_logs.csv"
USERNAME = "admin"
PASSWORD = "Airtel@123"

HEADLESS = False
DEBUG_DELAY = 1

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")


# ---------------- CLICK FUNCTION ----------------
def click_AAP321NK(driver, wait):
    logging.info("Waiting for AAP321NK to appear...")

    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'AAP321NK')]")
        ))
    except:
        logging.error("AAP321NK not found")
        return False

    for i in range(5):
        try:
            logging.info(f"Click attempt {i+1}")

            elements = driver.find_elements(By.XPATH, "//*[contains(text(),'AAP321NK')]")

            for el in elements:
                if el.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    time.sleep(1)

                    driver.execute_script("arguments[0].click();", el)

                    logging.info("AAP321NK clicked successfully")
                    return True

        except Exception as e:
            logging.warning(f"Retry failed: {e}")

        time.sleep(2)

    return False


# ---------------- EXTRACT FUNCTION ----------------
def extract_device_details(driver):
    logging.info("Extracting device details...")

    def get_value(label):
        try:
            return driver.find_element(
                By.XPATH,
                f"//*[contains(text(),'{label}')]/following::div[1]"
            ).text.strip()
        except:
            return "N/A"

    device_name = get_value("Device name")
    serial_number = get_value("Serial number")
    sw_version = get_value("Software version")
    hw_version = get_value("Hardware version")
    boot_version = get_value("Boot version")

    logging.info("===== DEVICE DETAILS =====")
    logging.info(f"Device Name     : {device_name}")
    logging.info(f"Serial Number   : {serial_number}")
    logging.info(f"Software Version: {sw_version}")
    logging.info(f"Hardware Version: {hw_version}")
    logging.info(f"Boot Version    : {boot_version}")
    logging.info("==========================")

    return device_name, serial_number, sw_version, hw_version, boot_version


class FWATool:
    def __init__(self, root):
        self.root = root
        self.root.title("FWA Debug Tool (Final)")
        self.root.geometry("700x650")

        tk.Label(root, text="SCAN DEVICE SERIAL", font=("Arial", 12, "bold")).pack(pady=10)

        self.serial_entry = tk.Entry(root, font=("Arial", 16), width=30, justify='center')
        self.serial_entry.pack(pady=10)
        self.serial_entry.focus_set()
        self.serial_entry.bind('<Return>', self.start_process)

        self.btn = tk.Button(root, text="START CHECK", command=self.start_process,
                             bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=20)
        self.btn.pack(pady=20)

        self.status_label = tk.Label(root, text="READY", font=("Arial", 18, "bold"),
                                     bg="#B0BEC5", fg="white", width=40, height=3)
        self.status_label.pack(pady=10)

        self.img_label = None

    # ---------------- CSV ----------------
    def save_to_log(self, sn, status, screenshot_path):
        file_exists = os.path.exists(LOG_FILE)

        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(["Timestamp", "SN", "Status", "Screenshot"])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                sn,
                status,
                screenshot_path
            ])

    # ---------------- START ----------------
    def start_process(self, event=None):
        scanned_sn = self.serial_entry.get().strip()

        if not scanned_sn:
            return

        self.status_label.config(text="PROCESSING...", bg="#FF9800")
        self.btn.config(state="disabled")

        threading.Thread(target=self.verify_device, args=(scanned_sn,), daemon=True).start()

    # ---------------- MAIN ----------------
    def verify_device(self, scanned_sn):

        options = Options()

        if HEADLESS:
            options.add_argument("--headless=new")
        else:
            options.add_argument("--start-maximized")

        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--ignore-ssl-errors=yes")

        driver = None
        status = "ERROR"
        screenshot_path = ""

        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )

            wait = WebDriverWait(driver, 15)

            # Open URL
            driver.get(f"https://{TARGET_IP}")
            time.sleep(2)

            # SSL bypass
            try:
                wait.until(EC.presence_of_element_located((By.ID, "details-button"))).click()
                wait.until(EC.presence_of_element_located((By.ID, "proceed-link"))).click()
            except:
                pass

            # LOGIN
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))).send_keys(USERNAME)
            driver.find_element(By.XPATH, "//input[@type='password']").send_keys(PASSWORD + Keys.RETURN)

            time.sleep(3)

            # WAIT FULL UI
            logging.info("Waiting 10 sec for full UI load...")
            time.sleep(10)

            # CLICK DEVICE
            if not click_AAP321NK(driver, wait):
                raise Exception("Click failed")

            time.sleep(2)

            # HANDLE POPUP
            try:
                ok_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Okay')]"))
                )
                ok_btn.click()
                logging.info("Popup handled")
            except:
                logging.info("No popup")

            # WAIT DETAIL PAGE
            logging.info("Waiting for detail page...")
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'AAP321NK details')]")
            ))

            time.sleep(2)

            # EXTRACT DATA
            extract_device_details(driver)

            # SCREENSHOT
            screenshot_path = f"screenshots/{scanned_sn}_FINAL.png"
            driver.save_screenshot(screenshot_path)

            self.display_screenshot(screenshot_path)

            status = "SUCCESS"

        except Exception as e:
            logging.error(str(e))
            self.update_status("ERROR", "#F44336")

        finally:
            if driver:
                driver.quit()

            self.save_to_log(scanned_sn, status, screenshot_path)
            self.root.after(0, self.reset_ui)

    # ---------------- DISPLAY ----------------
    def display_screenshot(self, path):
        try:
            img = Image.open(path)
            img = img.resize((600, 320))
            photo = ImageTk.PhotoImage(img)

            def update():
                if self.img_label:
                    self.img_label.config(image=photo)
                    self.img_label.image = photo
                else:
                    self.img_label = tk.Label(self.root, image=photo)
                    self.img_label.image = photo
                    self.img_label.pack(pady=10)

                self.status_label.config(text="DONE", bg="#4CAF50")

            self.root.after(0, update)

        except Exception as e:
            logging.error(str(e))

    def update_status(self, text, color):
        self.root.after(0, lambda: self.status_label.config(text=text, bg=color))

    def reset_ui(self):
        self.serial_entry.delete(0, tk.END)
        self.btn.config(state="normal")
        self.serial_entry.focus_set()


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FWATool(root)
    root.mainloop()