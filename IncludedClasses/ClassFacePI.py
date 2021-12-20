import http.client, urllib.request, urllib.parse, urllib.error, json
import IncludedClasses.ClassConfig

class Face:
    def __init__(self):
        self.config = IncludedClasses.ClassConfig.Config()

    def detectLocalImage(self, imagepath):
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.config.readConfig()['api_key'],
        }

        params = urllib.parse.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age, gender',

            'returnRecognitionModel': 'false',
            'detectionModel': 'detection_01',
            'faceIdTimeToLive': '86400',
        })

        print('imagepath=', imagepath)
        requestbody = open(imagepath, "rb").read()

        try:
            conn = http.client.HTTPSConnection(self.config.readConfig()['host'])
            conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody, headers)
            response = conn.getresponse()
            data = response.read()
            json_face_detect = json.loads(str(data, 'UTF-8'))
            print("detectLocalImage.faces=", json_face_detect)

            conn.close()

            print("detectLocalImage:", f"{imagepath} detected {len(json_face_detect)} people.")

            return json_face_detect
        except Exception as e:
            print("[Errno {0}]Connection Failed {1}".format(e.errno, e.strerror))

    def detectImageUrl(self, imageurl):
        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',  # 用本地圖檔辨識
            'Ocp-Apim-Subscription-Key': self.config.readConfig()['api_key'],
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender',
            #'recognitionModel': 'recognition_04',
            'returnRecognitionModel': 'false',
            'detectionModel': 'detection_01',
            'faceIdTimeToLive': '86400',
        })
        #'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure'
        print('imageurl=', imageurl)
        requestbody = '{"url": "' + imageurl + '"}'
        try:
            conn = http.client.HTTPSConnection(self.config.readConfig()['host'])
            conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody,
                         headers)
            response = conn.getresponse()
            data = response.read()
            json_face_detect = json.loads(str(data, 'UTF-8'))
            conn.close()

            print("detectImageUrl:",
                f"{imageurl} detected {len(json_face_detect)} people(person)")
            return json_face_detect
            
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))