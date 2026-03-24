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

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")


# ---------------- CLICK FUNCTION ----------------
def click_AAP321NK(driver, wait):
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'AAP321NK')]")))

    for _ in range(5):
        elements = driver.find_elements(By.XPATH, "//*[contains(text(),'AAP321NK')]")
        for el in elements:
            if el.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                driver.execute_script("arguments[0].click();", el)
                return True
        time.sleep(2)
    return False


# ---------------- EXTRACT FUNCTION ----------------
def extract_details(driver):
    def get(label):
        try:
            return driver.find_element(
                By.XPATH, f"//*[contains(text(),'{label}')]/following::div[1]"
            ).text.strip()
        except:
            return "N/A"

    return {
        "device_name": get("Device name"),
        "serial": get("Serial number"),
        "sw": get("Software version"),
        "hw": get("Hardware version"),
        "boot": get("Boot version")
    }


class FWATool:
    def __init__(self, root):
        self.root = root
        self.root.title("FWA MES Validation Tool")
        self.root.geometry("800x850")

        # SERIAL INPUT
        tk.Label(root, text="SCAN DEVICE SERIAL", font=("Arial", 12, "bold")).pack(pady=5)
        self.serial_entry = tk.Entry(root, font=("Arial", 16), width=30, justify='center')
        self.serial_entry.pack(pady=5)

        # SW INPUT
        tk.Label(root, text="SW VERSION", font=("Arial", 10, "bold")).pack()
        self.sw_entry = tk.Entry(root, font=("Arial", 12), width=25, justify='center')
        self.sw_entry.insert(0, "AAP321NK_R5.0")
        self.sw_entry.pack(pady=5)

        # BUTTON
        self.btn = tk.Button(root, text="START Validation", command=self.start_process,
                             bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=20)
        self.btn.pack(pady=15)

        # RESULT LABEL
        self.result_label = tk.Label(root, text="READY", font=("Arial", 22, "bold"),
                                     bg="#B0BEC5", fg="white", width=38, height=3)
        self.result_label.pack(pady=10)

        # ---------------- DEVICE INFO PANEL ----------------
        self.info_frame = tk.LabelFrame(root, text="Device Information", font=("Arial", 10, "bold"))
        self.info_frame.pack(pady=10, fill="x", padx=20)

        self.device_info_label = tk.Label(
            self.info_frame,
            text="No Data",
            font=("Courier", 10),
            justify="left",
            anchor="w"
        )
        self.device_info_label.pack(fill="x", padx=10, pady=5)

        # IMAGE
        self.img_label = None

    # ---------------- START ----------------
    def start_process(self):
        sn = self.serial_entry.get().strip()
        sw = self.sw_entry.get().strip()

        if not sn or not sw:
            return

        self.result_label.config(text="PROCESSING...", bg="#FF9800")
        self.btn.config(state="disabled")

        threading.Thread(target=self.verify, args=(sn, sw), daemon=True).start()

    # ---------------- MAIN ----------------
    def verify(self, input_sn, input_sw):

        options = Options()
        if not HEADLESS:
            options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")

        driver = None

        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )

            wait = WebDriverWait(driver, 15)

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

            time.sleep(10)

            # CLICK DEVICE
            click_AAP321NK(driver, wait)
            time.sleep(2)

            # POPUP
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Okay')]"))).click()
            except:
                pass

            # WAIT DETAIL
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'details')]")))
            time.sleep(2)

            # EXTRACT
            data = extract_details(driver)

            logging.info(f"Detected: {data}")

            # ---------------- UPDATE INFO PANEL ----------------
            info_text = (
                f"Device Name     : {data['device_name']}\n"
                f"Serial Number   : {data['serial']}\n"
                f"Software Version: {data['sw']}\n"
                f"Hardware Version: {data['hw']}\n"
                f"Boot Version    : {data['boot']}"
            )
            self.update_info(info_text)

            # ---------------- VALIDATION ----------------
            fail_msg = []

            if input_sn != data["serial"]:
                fail_msg.append(f"SN: {input_sn} != {data['serial']}")

            if input_sw != data["sw"]:
                fail_msg.append(f"SW: {input_sw} != {data['sw']}")

            if not fail_msg:
                self.update_result("PASS", "#4CAF50")
            else:
                self.update_result("FAIL\n" + "\n".join(fail_msg), "#F44336")

            # SCREENSHOT
            ss = f"screenshots/{input_sn}.png"
            driver.save_screenshot(ss)
            self.display_screenshot(ss)

        except Exception as e:
            logging.error(str(e))
            self.update_result("ERROR", "#F44336")

        finally:
            if driver:
                driver.quit()

            self.root.after(0, self.reset_ui)

    # ---------------- UI ----------------
    def update_result(self, text, color):
        self.root.after(0, lambda: self.result_label.config(text=text, bg=color))

    def update_info(self, text):
        self.root.after(0, lambda: self.device_info_label.config(text=text))

    def display_screenshot(self, path):
        img = Image.open(path)
        img = img.resize((650, 350))
        photo = ImageTk.PhotoImage(img)

        def update():
            if self.img_label:
                self.img_label.config(image=photo)
                self.img_label.image = photo
            else:
                self.img_label = tk.Label(self.root, image=photo)
                self.img_label.image = photo
                self.img_label.pack()

        self.root.after(0, update)

    def reset_ui(self):
        self.btn.config(state="normal")
        self.serial_entry.delete(0, tk.END)
        self.serial_entry.focus_set()


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FWATool(root)
    root.mainloop()