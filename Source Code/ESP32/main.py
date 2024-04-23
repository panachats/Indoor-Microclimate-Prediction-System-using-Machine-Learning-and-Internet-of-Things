import machine
import network
import utime
import ntptime
import dht
import ufirebase as firebase
led = machine.Pin(2, machine.Pin.OUT)

WIFIssid = "WIFI_SSID"
WIFIpsw = "WIFI_Password"

sensor = dht.DHT22(machine.Pin(13))
URL = 'https://test-firebase-4d32f-default-rtdb.firebaseio.com/'

Temps = []
Hums = []


def connect_wifi():
    # เชื่อมต่อ Wi-Fi
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to Wi-Fi...', WIFIssid)
        sta_if.active(True)
        sta_if.connect(WIFIssid, WIFIpsw)
        count = 0
        while not sta_if.isconnected():
            if count > 60:
                print('Cannot connect to Wi-Fi...')
                utime.sleep(180)
                machine.reset()
            else:
                print('.', end='')
                utime.sleep(1)
                count += 1
    print()
    print('Network config:', sta_if.ifconfig())
    utime.sleep(5)
    
    # ตั้งเวลาจาก NTP (Network Time Protocol)
    try:
        ntptime.settime()
        print("NTP Time has been set")
    except Exception as e:
        print(e)
        machine.reset()

def read_sensor():
    global Temps, Hums
    temp = 0
    humi = 0
    try:
        # อ่านค่าอุณหภูมิและความชื้นจากเซ็นเซอร์
        sensor.measure()
        temp = sensor.temperature()
        humi = sensor.humidity()
        if humi < 100 and humi != 0:
            Temps.append(temp)
            Hums.append(humi)
            print('Readings:', temp, humi, '#Appended')
        else:
            print('Readings:', temp, humi)
            led.value(1)
            utime.sleep_ms(200)
            led.value(0)
            utime.sleep_ms(200)
    except Exception as e:
        print('Error reading sensor:', e)
        for i in range(3):
            led.value(1)
            utime.sleep_ms(200)
            led.value(0)
            utime.sleep_ms(200)

    # print('Readings:', temp, humi)
    utime.sleep(2)

def send_data_to_firebase(now, minute):
    global Temps, Hums
    if minute % 5 == 0:
        # คำนวณค่าเฉลี่ยของอุณหภูมิและความชื้น
        Datatemp = sum(Temps) / len(Temps) if Temps else 0
        Datahumi = sum(Hums) / len(Hums) if Hums else 0

        print(f"{now} Temperature: {Datatemp:.2f} Humidity: {Datahumi:.2f}")
        # if Datahumi == 0 or Datatemp == 0:
            # machine.reset()
        # สร้างข้อมูลที่จะส่งไปยัง Firebase
        message = {
            "Temperature": '{:.2f}'.format(Datatemp),
            "Humidity": '{:.2f}'.format(Datahumi),
        }

        try:
            path1 = f"Test/ProjectMMicroClimate/{now}/"
            # ส่งข้อมูลไปยัง Firebase
            firebase.patch(path1, message, bg=0)
            print('|' * 30)
            print(f'Send {message}')
            print('|' * 30)
        except Exception as e:
            print(f"Error sending message to Firebase: {e}")
            machine.reset()

        # ล้างข้อมูลที่เก็บไว้หลังจากส่งไปยัง Firebase
        Temps, Hums = [], []

        utime.sleep(60)

def main_loop():
    rtc = machine.RTC()
    utc_shift = 7
    (year, month, mday, week_of_year, hour, minute, second, milisecond) = rtc.datetime()
    rtc.init((year, month, mday, week_of_year, hour + utc_shift, minute, second, milisecond))

    while True:
        # ดึงข้อมูลเวลาปัจจุบันจากราศีนาการ
        t = rtc.datetime()
        now = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:00'.format(t[0], t[1], t[2], t[4], t[5], t[6])

        try:
            # อ่านข้อมูลจากเซ็นเซอร์และส่งไปยัง Firebase
            read_sensor()
            send_data_to_firebase(now, t[5])
        except Exception as e:
            print('Error in main loop:', e)
            utime.sleep(30)
            machine.reset()

try:
    print('Starting...')
    # เริ่มต้นเชื่อมต่อ Wi-Fi และ Firebase
    led.value(1)
    connect_wifi()
    led.value(0)
    firebase.setURL(URL)
    # สำหรับดึงข้อมูลจากเซ็นเซอร์และส่งไปยัง Firebase
    main_loop()

except Exception as e:
    print('Failed...', e)
    utime.sleep(30)
    machine.reset()