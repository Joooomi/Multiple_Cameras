# Friendly nameでカメラを起動する
import wmi
import cv2

def get_camera_properties():
    w = wmi.WMI()   
    
    # Win32_PnPEntityから 'USB2.0_Camera'を探す
    cameras = w.query("SELECT * FROM Win32_PnPEntity WHERE Name LIKE '%USB2.0_Camera%'")
    
    camera_properties = []
    for camera in cameras:
        # プロパティを取得
        name = camera.name
        description = camera.Description
        pnp_device_id = camera.PNPDeviceID
        #取得したプログラムをリストに追加
        camera_properties.append({        
            "Name": name,
            "Description": description,
            "PNPDeviceID": pnp_device_id
        })
    
    return camera_properties

def create_camera_mapping(camera_properties):
    # Friendly nameとcamera indexのマップを作成
    mapping = {}
    for index, camera in enumerate(camera_properties):
        
        #serial_number = camera["PNPDeviceID"].split("\\")[2] #==Instance ID
        # Friendly nameを取得
        name = camera["Name"]
        # マップに追加
        mapping[name] = index
    
    return mapping

# カメラのプロパティを取得
camera_properties = get_camera_properties()

# マップ作成
camera_mapping = create_camera_mapping(camera_properties)
print("Camera Mapping:", camera_mapping)

# Friendly name で起動するカメラを選択
desired_name = "USB2.0_Camera_Front"
if desired_name in camera_mapping:
    desired_index = camera_mapping[desired_name] +1 #内臓カメラが index 0 になっているため、１を足す
    print("Desired Camera Index:", desired_index)    

    # 作成したマップから取得したカメラのindexでカメラを開く
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
