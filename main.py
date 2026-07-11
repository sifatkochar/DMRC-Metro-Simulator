def data_func():
    header=""
    full_data={}
    full_data["Metro_Line"]=[]
    full_data["Stations"]=[]
    full_data["Interchange"]=[]
    full_data["Schedule"]=[]
    full_data["Fare"]=[]


    with open("metro_data.txt","r") as f:
        for line in f:
            line=line.strip()       
        
            if line.startswith("#") or line == "":
                continue

            if line.startswith("[") and line.endswith("]"):
                header=line[1:len(line)-1]
                continue

            if header=="Metro_Line":
                content=line.split(",")
                full_data["Metro_Line"].append({"Line_ID":content[0],"Line":content[1],"D1_End":content[2],"D2_End":content[3]})

            elif header=="Stations":
                content=line.split(",")
                full_data["Stations"].append({"Line":content[0],"From":content[1],"To":content[2],"Time":int(content[3]),"Distance":float(content[4])})

            elif header=="Interchange":
                content=line.split(",")
                full_data["Interchange"].append({"Station":content[0],"L1_ID":content[1],"L2_ID":content[2],"Delay":float(content[3])})

            elif header=="Schedule":
                content=line.split(",")
                full_data["Schedule"].append({content[0]:content[1]})

            elif header=="Fare":
                content=line.split(",")
                full_data["Fare"].append({"Min_Distance":int(content[0]),"Max_Distance":int(content[1]),"Weekday_F":int(content[2]),"Holiday_F":int(content[3])})

    return full_data


data=data_func()


def time_string(min):
    hour=min//60
    minute=min%60
    string=""
    if len(str(hour))==1 and len(str(minute))==1:
        string="0"+str(hour)+":"+"0"+str(minute)
    elif len(str(hour))==1 and len(str(minute))>1:
        string="0"+str(hour)+":"+str(minute)
    elif len(str(hour))>1 and len(str(minute))==1:
        string=str(hour)+":"+"0"+str(minute)
    else:
        string=str(hour)+":"+str(minute)
    
    return string


def time_int(t):
    h=int(t.split(":")[0])
    m=int(t.split(":")[1])
    time_min=h*60+m
    return time_min


def stations_list():
    blue_L3=[]
    blue_L4=[]
    magenta=[]
    yellow=[]

    for i in range(len(data["Stations"])):
        if data["Stations"][i]["Line"]=="Blue (L3)":
            blue_L3.append(data["Stations"][i]["From"])

        elif data["Stations"][i]["Line"]=="Blue (L4)":
            blue_L4.append(data["Stations"][i]["From"]) 
        
        elif data["Stations"][i]["Line"]=="Magenta (L8)":
            magenta.append(data["Stations"][i]["From"]) 

        elif data["Stations"][i]["Line"]=="Yellow (L2)":
            yellow.append(data["Stations"][i]["From"]) 

    blue_L3.append("NOIDA ELECTRONIC CITY")
    blue_L4.append("VAISHALI")
    magenta.append("BOTANICAL GARDEN")
    yellow.append("MILLENNIUM CITY CENTRE GURUGRAM")

    return blue_L3,blue_L4,magenta,yellow


stations_order=stations_list()
blue_l3_forward=stations_order[0]
blue_l3_reverse=list(reversed(blue_l3_forward))
blue_l4_forward=stations_order[1]
blue_l4_reverse=list(reversed(blue_l4_forward))
magenta_forward=stations_order[2]
magenta_reverse=list(reversed(magenta_forward))
yellow_forward=stations_order[3]
yellow_reverse=list(reversed(yellow_forward))



def next_metro(l,station,terminal,time):
    try:
        if l=="BLUE":
            if terminal==blue_l3_forward[-1]:
                line=blue_l3_forward
            elif terminal==blue_l3_reverse[-1]:
                line=blue_l3_reverse
            elif terminal==blue_l4_forward[-1]:
                line=blue_l4_forward
            elif terminal==blue_l4_reverse[-1]:
                line=blue_l4_reverse
        
        elif l=="MAGENTA":
            if terminal==magenta_forward[-1]:
                line=magenta_forward
            elif terminal==magenta_reverse[-1]:
                line=magenta_reverse

        elif l=="YELLOW":
            if terminal==yellow_forward[-1]:
                line=yellow_forward
            elif terminal==yellow_reverse[-1]:
                line=yellow_reverse

        index=0
        for i in range(len(line)):
            if line[i]==station:
                index=i
                break
        
        
        time_to_station=0
        for j in range(index):
            time_to_station+=data["Stations"][index]["Time"]


        start=time_int(data["Schedule"][0]["Start_Time"])
        end=time_int(data["Schedule"][1]["End_Time"])
        p1_start=time_int(data["Schedule"][2]["PeakHr_1_Start"])
        p1_end=time_int(data["Schedule"][3]["PeakHr_1_End"])
        p2_start=time_int(data["Schedule"][4]["PeakHr_2_Start"])
        p2_end=time_int(data["Schedule"][5]["PeakHr_2_End"])


        metros_6to8=[]
        k=start
        while k<=p1_start:
            metros_6to8.append(time_string(k))
            k+=8
        
        metros_8to10=[]
        k=p1_start+4
        while k<=p1_end:
            metros_8to10.append(time_string(k))
            k+=4

        metros_10to1700=[]
        k=p1_end+8
        while k<=p2_start:
            metros_10to1700.append(time_string(k))
            k+=8

        metros_1700to1900=[]
        k=p2_start
        while k<=p2_end:
            metros_1700to1900.append(time_string(k))
            k+=4

        metros_1900to2300=[]
        k=p2_end+8
        while k<=end:
            metros_1900to2300.append(time_string(k))
            k+=8


        metros_6to8_update=[]
        for i in metros_6to8:
            metros_6to8_update.append(time_string(time_int(i)+time_to_station))

        metros_8to10_update=[]
        for i in metros_8to10:
            metros_8to10_update.append(time_string(time_int(i)+time_to_station))

        metros_10to1700_update=[]
        for i in metros_10to1700:
            metros_10to1700_update.append(time_string(time_int(i)+time_to_station))

        metros_1700to1900_update=[]
        for i in metros_1700to1900:
            metros_1700to1900_update.append(time_string(time_int(i)+time_to_station))

        metros_1900to2300_update=[]
        for i in metros_1900to2300:
            metros_1900to2300_update.append(time_string(time_int(i)+time_to_station))


        list_updated_times=metros_6to8_update+metros_8to10_update+metros_10to1700_update+metros_1700to1900_update+metros_1900to2300_update


        for i in range(len(list_updated_times)):
            if time_int(list_updated_times[i])==time_int(time):
                next=list_updated_times[i]
                if i not in (len(list_updated_times)-1,len(list_updated_times)-2):
                    subs1,subs2=list_updated_times[i+1],list_updated_times[i+2]
                    break
                elif i==len(list_updated_times)-2:
                    subs1=list_updated_times[i+1]
                    break
                elif i==len(list_updated_times)-1:
                    break
                
            elif time_int(list_updated_times[i])<time_int(time):
                continue

            else:
                next=list_updated_times[i]
                if i not in (len(list_updated_times)-1,len(list_updated_times)-2):
                    subs1,subs2=list_updated_times[i+1],list_updated_times[i+2]
                    break
                elif i==len(list_updated_times)-2:
                    subs1=list_updated_times[i+1]
                    break
                elif i==len(list_updated_times)-1:
                    break

        lst=[]
        lst.append(next)
        lst.append(subs1)
        lst.append(subs2)

        return lst
    
    except UnboundLocalError:
        print("Inputted Line/Stations do not match.")
        return None


def from_to_time(data):
    route={}
    for i in data["Stations"]:
        From=i["From"]
        To=i["To"]
        Time=i["Time"]

        if From not in route:
            route[From] = []   
        
        route[From].append((To, Time))

    return route


def route_shortest_time(route,start,end):
    best_route={start:0}
    fastest={}

    line=[start]

    while line:
        station=line.pop(0)
        current_time=best_route[station]

        for next_station,time in route.get(station,[]):
            new_time=current_time+time

            if next_station not in best_route or new_time<best_route[next_station]:
                best_route[next_station]=new_time
                fastest[next_station]=station
                line.append(next_station)

    if end not in best_route:
        return None
    
    path=[]
    destination=end
    while destination!=start:
        path.append(destination)
        destination=fastest[destination]
    
    path.append(start)
    path.reverse()

    list_best_route=[path,best_route[end]]

    return list_best_route


def best_route_time(data,start,end):
    route=from_to_time(data)

    return route_shortest_time(route,start,end)


    
#Main Program

def menu():
    print("____________METRO SIMULATOR___________")
    print("1. Compute next metro timings.")
    print("2. Compute journey/path and time between stations.")
    print("3. Exit.")

while True:
    menu()

    try:
        choice=int(input("Enter your choice(1-3) : "))

        if choice in [1,2,3]:

            if choice==1:
                try:
                    line=input("Enter metro line : ")
                    current_station=input("Enter current station : ")
                    terminal=input("Enter terminal station of your direction : ")
                    current_time=(input("Enter current time : "))

                    output=next_metro(line,current_station,terminal,current_time)

                    if output!=None:
                        print("Next metro arrives at - ",output[0])
                        if output[1]!=None and output[2]!=None:
                            print("Subsequent metros at - ",output[1],output[2])
                        elif output[1]!=None:
                            print("Subsequent metro at - ",output[1])
                    else:
                        pass

                except TypeError:
                    print("Inputted Line/Stations do not match.")


            elif choice==2:
                try:
                    station=input("Enter current station : ")
                    destination=input("Enter destination station : ")

                    list_lines=[blue_l3_forward,blue_l4_forward,magenta_forward,yellow_forward]

                    if station in list_lines[0] or station in list_lines[1] or station in list_lines[2] or station in list_lines[3]:

                        if station in list_lines[0]:
                            if destination in list_lines[0]:
                                print("Route is on a single line.")
                            elif destination in list_lines[1]:
                                print("Route is NOT on a single line.")
                            elif destination in list_lines[2]:
                                print("Route is NOT on a single line.")
                            elif destination in list_lines[3]:
                                print("Route is NOT on a single line.")
                            else:
                                print("Entered Station/Destination not on BLUE, MAGENTA or YELLOW line.")
                            
                        elif station in list_lines[1]:
                            if destination in list_lines[0]:
                                print("Route is NOT on a single line.")
                            elif destination in list_lines[1]:
                                print("Route is on a single line.")
                            elif destination in list_lines[2]:
                                print("Route is NOT on a single line.")
                            elif destination in list_lines[3]:
                                print("Route is NOT on a single line.")
                            else:
                                print("Entered Station/Destination not on BLUE, MAGENTA or YELLOW line.")
                        
                        elif station in list_lines[2]:
                            if destination in list_lines[0]:
                                print("Route is NOT on a single line.")
                            elif destination in list_lines[1]:
                                print("Route is NOT on a single line.")
                            elif destination in list_lines[2]:
                                print("Route is on a single line.")
                            elif destination in list_lines[3]:
                                print("Route is NOT on a single line.")
                            else:
                                print("Entered Station/Destination not on BLUE, MAGENTA or YELLOW line.")

                        elif station in list_lines[3]:
                            if destination in list_lines[0]:
                                print("Route is NOT on a single line.")
                            elif destination in list_lines[1]:
                                print("Route is NOT on a single line.")
                            elif destination in list_lines[2]:
                                print("Route is NOT on a single line.")
                            elif destination in list_lines[3]:
                                print("Route is on a single line.")
                            else:
                                print("Entered Station/Destination not on BLUE, MAGENTA or YELLOW line.")
                    
                    else:
                        print("Entered Station/Destination not on BLUE, MAGENTA or YELLOW line.")           


                    output=best_route_time(data,station,destination)

                    print("Your Path - ")
                    for i in range(len(output[0])):
                        if i==len(output[0])-1:
                            print(output[0][i])
                        else:
                            print(output[0][i],end="--")
                    
                    print("Time Taken - ",output[1],"minutes.")
                
                except TypeError:
                    print("Inputted Station/Destination do not match.")

            elif choice==3:
                print("Have a great journey!")
                break

        else:
            print("Enter a choice from 1,2,3.")

    except ValueError:
        print("Enter a choice from 1,2,3.")