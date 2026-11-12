import asyncio
import shelve
from bleak import BleakScanner
from time import strftime, gmtime, sleep

async def scan_for_devices():
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()     #sets dictionary? to whatever the scanner finds
    for device in devices:
        print(f"Device Name: {device.name}, Address: {device.address}")     #prints each device and address for easy reading
    return devices

#asyncio.run(scan_for_devices())

KNOWN_DEVICES = {
    "My Headphones": "11:22:33:44:82:F6",
    "My phone": "BO:64:E0:63:C5:50"
}

async def check_for_known_devices():
    devices = await BleakScanner.discover()     #same as above
    nearby_known_devices = {}       #creates dictionary
    for device in devices:
        if device.address in KNOWN_DEVICES.values():    #if theres a match between my list of known devices and what bluetooth caught
            device_name = [name for name, addr in KNOWN_DEVICES.items() if addr == device.address][0]   #not sure how to read this
            print(f"{device_name} is nearby!")
            nearby_known_devices[device_name] = device.address      #adds to dictionary for the return result

    return nearby_known_devices

def log_devices(devices):
    with shelve.open( "device_log" ) as db:     #db is opened
        for name, address in devices.items():       #for key and value in devices?
            key = name + '_' + address      #key is now name + space + address
            formatted_time = strftime( "%Y-%m-%d %H:%M:%S", gmtime())       #sets the time??
            if key in db:
                time_list = db[key]     #database key given to new var
                time_list.append(formatted_time)    #appends formatted time onto timelist
                db[key] = time_list     #rewrites original key with new information
            else:
                db[key] = [formatted_time]      #otherwise, just uses formatted time
    print( "Logged devices in the shelf database." )

async def scan():
    nearby_devices = await check_for_known_devices()    #runs check for known devices and assigns it to var
    if nearby_devices:      #if yes
        log_devices( nearby_devices )       #log dat bish
    else:
        print( "No known devices nearby." )     #sorry out of luck



def main():
    # asyncio.run( scan_for_devices() )
    counter = 0
    while counter < 3600:
        print("Scanning...")
        asyncio.run( scan() )   #starts the train of functions
        print("sleeping till next loop...")
        counter += 15       #adds the seconds counter
        if counter == 900 or counter == 1800 or counter == 2700:    #at every 15 minute interval
            print("Verifying log...")
            with shelve.open("device_log") as db:       #open the database
                for name, address in db.items():        #splits each entry in the database in two
                    print(f"{name}: {address}")     #prints it!
            sleep(15)       #sleep
        else:
            sleep(15)       #sleep anyway
    else:
        with shelve.open("device_log") as db:   #opens the database
            db.clear()          #clears it
        counter -= 3600         #resets counter
        print("Cleared the device log.")
        main()      #starts the process over again

#not exactly what u asked for with using async sleep stuff but it WORKS

if __name__ == '__main__':      # ❁(•̀ω•́ )✧
    main()



