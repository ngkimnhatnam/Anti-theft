import serial
import pynmea2
import math
import time

serialStream= serial.Serial("/dev/ttyS0",9600,timeout=0.5)
coord=[]
collected_dist=[]

def total_distance(): #Calculate total distance travelled so far
        
        while True:

                if len(coord)<4:
                        current_location()
                
                elif len(coord)==4:
                        haversine(coord[0],coord[1],coord[2],coord[3])
                        del coord[:]
                        total_dist=sum(collected_dist)
                        print ("Total distance travelled is: ",total_dist)
                

def current_location(): #Get current location and append to list
        sentence=serialStream.readline()
        if sentence.find('GGA')>0:
                data=pynmea2.parse(sentence)
                lati=data.latitude
                longi=data.longitude
                la=round(lati,5)
                lo=round(longi,5)
                coord.append(lo)
                coord.append(la)
                print ("Current location: {lat} North,{lon} East".format(lat=data.latitude, lon=data.longitude))
                print (coord)
                time.sleep(2)
                
                


def haversine(lon1,lat1,lon2,lat2): #Haversine formula to calculate distance between two points
    
    distance=[]
    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    #lon1, lat1 = coord1
    #lon2, lat2 = coord2

    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers

    meters = round(meters, 3)
    km = round(km, 3)

    collected_dist.append(meters)

    print("Distance:",meters," m")
    
    
    #print("Distance:",km," km")                

total_distance()


        
        
                

