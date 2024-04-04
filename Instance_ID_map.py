import wmi
import cv2

def get_camera_properties():
    w = wmi.WMI()
    
    # Win32_PnPEntity devicesから 'USB2.0_Camera'を探す 
    cameras = w.query("SELECT * FROM Win32_PnPEntity WHERE Name LIKE '%USB2.0_Camera%'")
    
    camera_properties = []
    for camera in cameras:
        # プロパティを取得　        
        name = camera.name
        description = camera.Description
        pnp_device_id = camera.PNPDeviceID
        # 取得したプロパティをリストに追加
        camera_properties.append({         
            "Name": name,
            "PNPDeviceID": pnp_device_id
        })
    
    return camera_properties

def create_camera_mapping(camera_properties):
    # Instance IDとcamera index のマップを作成
    mapping = {}
    for index, camera in enumerate(camera_properties):
        # Instance IDを抽出
        InstanceID = camera["PNPDeviceID"].split("\\")[2] 
        # マップに追加
        mapping[InstanceID] = index
    
    return mapping

# カメラのプロパティを取得
camera_properties = get_camera_properties()

# マップ作成　
camera_mapping = create_camera_mapping(camera_properties)
print("Camera Mapping:", camera_mapping)

# Instance IDでカメラ選択
desired_InstanceID = "6&3A0B45F5&0&0000"  

if desired_InstanceID in camera_mapping:
    desired_index = camera_mapping[desired_InstanceID] +1 #内臓カメラが０になっていたため、1を足す
    print("Desired Camera Index:", desired_index)
    
    # 作成したマップから取得したカメラのインデクスでカメラを開く
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
    print("Error: Desired serial number not found in mapping.")

cap.release()
cv2.destroyAllWindows()
