import tkinter as tk
from datetime import datetime
import threading
import logging
import os
import time
import subprocess

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
USERNAME = "admin"
PASSWORD = "Airtel@123"
HEADLESS = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")


# ---------------- PING ----------------
def ping_device(ip):
    logging.info(f"Pinging {ip}...")
    try:
        result = subprocess.run(["ping", "-n", "1", ip], capture_output=True, text=True)
        return "TTL=" in result.stdout
    except:
        return False

# ---------------- SAFE INPUT ----------------
def safe_send_keys(element, value):
    logging.info(f"input = {element} value = {value}")
    try:
        element.clear()
        element.click()
        element.send_keys(value)
    except:
        logging.warning("Normal send_keys failed → using JS fallback")
        driver = element.parent
        driver.execute_script("arguments[0].value = arguments[1];", element, value)

# ---------------- FACTORY MODE ----------------
def handle_factory_mode(driver, wait, scanned_sn):

    logging.info(f"[FACTORY MODE] Try login with SN: {scanned_sn}")

    try:
        username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        password = driver.find_element(By.XPATH, "//input[@type='password']")

        username.clear()
        username.send_keys("admin")

        password.clear()
        password.send_keys(scanned_sn)
        password.send_keys(Keys.RETURN)

        time.sleep(3)

        # Popup
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Okay')]"))).click()
            logging.info("[FACTORY MODE] Popup handled")
        except:
            logging.info("[FACTORY MODE] No popup → normal device")
            return False

        time.sleep(2)

        # Password fields
        inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        logging.info(f"[FACTORY MODE] Found {len(inputs)} password fields")

        if len(inputs) >= 3:
            logging.info(f"Going to login with [Original Password] : {scanned_sn} [New Password]: {PASSWORD}")
            
            # OLD PASSWORD
            logging.info("OLD PASSWORD")
            safe_send_keys(inputs[1], scanned_sn)

            # NEW PASSWORD
            logging.info("NEW PASSWORD")
            safe_send_keys(inputs[2], PASSWORD)

            # REPEAT PASSWORD (SPECIAL FIX)
            logging.info("REPEAT PASSWORD (SPECIAL FIX)")
            safe_send_keys(inputs[3], PASSWORD)
            time.sleep(4)
    
        # Save
        try:
            save_btn = driver.find_element(By.XPATH, "//button[contains(.,'Save')]")
            driver.execute_script("arguments[0].click();", save_btn)
            logging.info("[FACTORY MODE] Password changed")
        except Exception as e:
            logging.error(f"[FACTORY MODE] Save failed: {e}")

        time.sleep(4)

        # Re-login
        driver.get(f"https://{TARGET_IP}")

        username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        password = driver.find_element(By.XPATH, "//input[@type='password']")

        username.clear()
        username.send_keys("admin")

        password.clear()
        password.send_keys(PASSWORD)
        password.send_keys(Keys.RETURN)

        logging.info("[FACTORY MODE] Re-login successful")
        time.sleep(5)

        return True

    except Exception as e:
        logging.warning(f"[FACTORY MODE] Skipped: {e}")
        return False


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


# ---------------- LOG FUNCTION ----------------
def write_log(input_sn, device_sn, result, data):

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    folder = f"{date_str}_All-Devices"
    os.makedirs(folder, exist_ok=True)

    main_file = os.path.join(folder, f"{date_str}_All-Devices.txt")

    header = "Timestamp             Scanned SN      Device SN          Result        Device Info\n"

    log_line = f"{timestamp}   {input_sn}   {device_sn}   {result}   {data}\n"

    # ✅ Write header only once
    if not os.path.exists(main_file):
        with open(main_file, "w") as f:
            f.write(header)

    # ✅ Always append
    with open(main_file, "a") as f:
        f.write(log_line)

    # ✅ PASS file (NO HEADER)
    if result == "PASS":
        pass_file = os.path.join(folder, f"{date_str}_{time_str}_{input_sn}.txt")
        with open(pass_file, "w") as f:
            f.write(str(data))


def reset_to_factory(driver, wait):

    logging.info("[RESET] Trying Factory Default Reset")

    try:
        # Wait for "Factory default" section
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Factory default')]")
        ))

        # Click RESET button inside Factory default section
        reset_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(.,'Reset')]")
        ))
        driver.execute_script("arguments[0].click();", reset_btn)

        logging.info("[RESET] Reset button clicked")
        time.sleep(2)

        # Handle popup (2 types)
        try:
            # JS alert popup
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert.accept()
            logging.info("[RESET] Alert OK clicked")
        except:
            # UI popup
            ok_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'OK')]")
            ))
            driver.execute_script("arguments[0].click();", ok_btn)
            logging.info("[RESET] UI OK clicked")

        logging.info("[RESET] Device resetting... waiting 25 sec")
        time.sleep(25)

        return True

    except Exception as e:
        logging.warning(f"[RESET] Skipped: {e}")
        return False

# ---------------- GUI ----------------
class FWATool:
    def __init__(self, root):
        self.root = root
        self.root.title("FWA MES Validation Tool")
        self.root.geometry("800x850")

        tk.Label(root, text="SCAN DEVICE SERIAL", font=("Arial", 12, "bold")).pack(pady=5)
        self.serial_entry = tk.Entry(root, font=("Arial", 16), width=30, justify='center')
        self.serial_entry.pack(pady=5)

        tk.Label(root, text="SW VERSION", font=("Arial", 10, "bold")).pack()
        self.sw_entry = tk.Entry(root, font=("Arial", 12), width=25, justify='center')
        self.sw_entry.insert(0, "AAP321NK_R5.0")
        self.sw_entry.pack(pady=5)

        self.btn = tk.Button(root, text="START Validation", command=self.start_process,
                             bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=20)
        self.btn.pack(pady=15)

        self.result_label = tk.Label(root, text="READY", font=("Arial", 22, "bold"),
                                     bg="#B0BEC5", fg="white", width=38, height=3)
        self.result_label.pack(pady=10)

        self.info_frame = tk.LabelFrame(root, text="Device Information")
        self.info_frame.pack(pady=10, fill="x", padx=20)

        self.device_info_label = tk.Label(self.info_frame, text="No Data", justify="left")
        self.device_info_label.pack(padx=10, pady=5)

        self.img_label = None

    def start_process(self):
        sn = self.serial_entry.get().strip()
        sw = self.sw_entry.get().strip()

        if not sn or not sw:
            return

        self.result_label.config(text="PROCESSING...", bg="#FF9800")
        self.btn.config(state="disabled")

        threading.Thread(target=self.verify, args=(sn, sw), daemon=True).start()

    def verify(self, input_sn, input_sw):

        # -------- PING --------
        if not ping_device(TARGET_IP):
            self.update_result("DEVICE NOT REACHABLE", "#F44336")
            self.root.after(0, self.reset_ui)
            return

        options = Options()
        if not HEADLESS:
            options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")

        driver = None

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            wait = WebDriverWait(driver, 15)

            driver.get(f"https://{TARGET_IP}")
            time.sleep(2)

            # SSL bypass
            try:
                wait.until(EC.presence_of_element_located((By.ID, "details-button"))).click()
                wait.until(EC.presence_of_element_located((By.ID, "proceed-link"))).click()
            except:
                pass

            # -------- FACTORY MODE --------
            factory_done = handle_factory_mode(driver, wait, input_sn)

            # -------- NORMAL LOGIN --------
            if not factory_done:
                wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))).send_keys(USERNAME)
                driver.find_element(By.XPATH, "//input[@type='password']").send_keys(PASSWORD + Keys.RETURN)
                time.sleep(10)

            # CLICK
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

            # UPDATE GUI
            info_text = "\n".join([f"{k}: {v}" for k, v in data.items()])
            self.update_info(info_text)

            # VALIDATION
            fail = []
            if input_sn != data["serial"]:
                fail.append("SN Mismatch")
            if input_sw != data["sw"]:
                fail.append("SW Mismatch")

            if not fail:
                result = "PASS"
                self.update_result("PASS", "#4CAF50")
            else:
                result = "FAIL"
                self.update_result("FAIL\n" + "\n".join(fail), "#F44336")

            # LOG WRITE
            write_log(input_sn, data["serial"], result, data)

            # SCREENSHOT
            ss = f"screenshots/{input_sn}.png"
            driver.save_screenshot(ss)
            self.display_screenshot(ss)

            # -------- TRY RESET --------
            reset_done = reset_to_factory(driver, wait)

            if reset_done:
                logging.info("[FLOW] Reset done → reload login page")
                driver.get(f"https://{TARGET_IP}")
                time.sleep(5)

        except Exception as e:
            logging.error(str(e))
            self.update_result("ERROR", "#F44336")

        finally:
            if driver:
                driver.quit()
            self.root.after(0, self.reset_ui)

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


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FWATool(root)
    root.mainloop()