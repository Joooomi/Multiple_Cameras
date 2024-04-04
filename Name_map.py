import wmi
import cv2

def get_camera_properties():
    w = wmi.WMI()   
    
    cameras = w.query("SELECT * FROM Win32_PnPEntity WHERE Name LIKE '%USB2.0_Camera%'")
    
    camera_properties = []
    for camera in cameras:
        name = camera.name
        description = camera.Description
        pnp_device_id = camera.PNPDeviceID
        
        camera_properties.append({        
            "Name": name,
            "Description": description,
            "PNPDeviceID": pnp_device_id
        })
    
    return camera_properties

def create_camera_mapping(camera_properties):
    
    mapping = {}
    for index, camera in enumerate(camera_properties):
        
        serial_number = camera["PNPDeviceID"].split("\\")[2] #==Instance ID
        name = camera["Name"]
        
        mapping[name] = index
    
    return mapping


camera_properties = get_camera_properties()


camera_mapping = create_camera_mapping(camera_properties)
print("Camera Mapping:", camera_mapping)


desired_name = "USB2.0_Camera_1"
if desired_name in camera_mapping:
    desired_index = camera_mapping[desired_name] +1 
    print("Desired Camera Index:", desired_index)    
    
    cap = cv2.VideoCapture(desired_index, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
    else:
        print("Successfully opened camera.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print ("can not get the frame")
                break
            else:                 
                cv2.imshow('Camera', frame)

                # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        
else:
    print("Error: Desired Camera name not found in mapping.")

cap.release()
cv2.destroyAllWindows()
