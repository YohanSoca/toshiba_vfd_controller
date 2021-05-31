import serial
from flask import Flask, render_template, redirect
import minimalmodbus
import json

app = Flask(__name__)
vfd = None
count = 0
up = True

class VFD:
    def __init__(self, address, speed, parity, size, stop_bits, com):
        self.address = address
        self.speed = speed
        self.parity = parity
        self.size = size
        self.stop_bits = stop_bits
        self.com = com
        self.vfd = None

    def connect(self):
        try:
            self.vfd = minimalmodbus.Instrument(self.com, self.address)
            self.vfd.serial.baudrate = self.speed
            self.vfd.serial.bytesize = self.size
            self.vfd.serial.parity = self.parity
            self.serial.stopbits = self.stop_bits
        except:
            return False
    def set_speed(self, speed):
        try:
            if self.vfd != None:
                self.vfd.write_register(64001, speed)
        except:
            print("No connection")

    def get_speed(self):
        try:
            if self.vfd:
                return int(self.vfd.read_register(64001)) / 10
        except:
            print("No connection")

    def turn_on(self):
        try:
            if self.vfd != None:
                self.vfd.write_register(64000, int("110011000000000", 2))
        except:
            print("No connection")

    def turn_off(self):
        try:
            if self.vfd != None:
                self.vfd.write_register(64000, int("110001000000000", 2))
        except:
            print("No connection")

    def set_direction(self, direction):
        try:
            if self.vfd != None:
                if direction == 1:
                    self.vfd.write_register(64000, int("110011000000000", 2))
                if direction == 0:
                    self.vfd.write_register(64000, int("110010000000000", 2))
        except:
            print("No connection")
    def get_status(self):
        if self.vfd:
            speed = self.get_speed()
            direction = 1
            on = 0
            return {"speed": f"{400}", "direction": f"{1}", "on": f"{0}"}


@app.route('/get_status')
def get_status():
    global vfd
    if vfd:
        data = vfd.get_status()
    data = {"speed": f"{400}", "direction": f"{1}", "on": f"{1}", "connected": f"{1}"}


    return json.dumps(data)

@app.route('/on')
def turn_on():
    global vfd
    if vfd:
        vfd.turn_on()
    print('turning on')
    return ""

@app.route('/off')
def turn_off():
    global vfd
    if vfd:
        vfd.turn_off()
    return ""

@app.route('/<int:herz>')
def turn_update_speed(herz):
    print(f"setting frecuency to {herz}")
    return ""

@app.route('/<int:address>/<int:speed>/<int:parity>/<int:size>/<int:stop_bits>/<int:com>')
def set_up(address, speed, parity, size, stop_bits, com):
    global vfd
    if parity == 1:
        parity = serial.PARITY_NONE
    if parity == 2:
        parity = serial.PARITY_ODD
    if parity == 3:
        parity = serial.PARITY_EVEN


    com = f"COM{com}"
    print(f"address:{address}, speed:{speed}, parity:{parity}, size:{size}, stop_bits:{stop_bits}, com:{com}")
    vfd = VFD(address, speed, parity, size, stop_bits, com)
    vfd.connect()

    return redirect("/")

@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
