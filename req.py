import requests

import spotify_methods

url = "https://developer.spotify.com/warp/clients/122dd0accd2c491ca81708747ef141ee/users"
payload = {"name":"Benjamin Stahl","email":"benastahl@gmail.com","clientId":"122dd0accd2c491ca81708747ef141ee"}


def get_bearer():
    refresh_token = "AQAiPsdG2z9KBBElbXSmSurOOllY148hsnBdwjvwXhqd46j5jYE9fHVifm2yi-TH178JaJ-zhWufkLBRBAvP1FsENTUZYIRL91hOOWLovExLKoTy157xnpPSIvPNmwXR_TA"
    refresh_token = "AQAzW-CVfRA5vliq6mKgPdE7V8mLlZjXbG2M6kjC4Dvhat5IkAYtzIW4LB9DtaPGuXJEOVWz5P48lV3eC3seXm6LF_XQlcvFd1Y2fwR44Vo9QuOvPXKenlUkefxBk-Bnd05WVSCwLiYO8EDOmwLRNmnxOmY5s_wy"
    refresh_token = "AQAiXoqT79hS_DXmPzSUmnXA7ZJHDxGh63IUAMSAJPVRkKJ_U_O_MF8OXOOVRzAq5QXKN82VDdmPlJP_1bQgMzgwdQL43j8ZJOI"
    refresh_token = "AQDpOEA9NgmDXiS7UlJazy3E5RWzTFQpKdFFab5mBXA0BzXwwEyc0gyCMi4RFoV8zFlt_x_Rw0dBekhL"
    refresh_token = "AQBLZ118Xde2LMupVU7M9i5gLeQPAfT02kFdzat9I9iVvVIKwrjK8TX6wPMPmWD75YV8u-pqykW3b9rTMyV0NfXsQU30E1bueXkcfyVUnLO9nA9DyPdaXYLda4hml6mjNksfG00zk4gjT4NCHw3RAPr0kckUkrDyxIRSwXHVtn-0gN9z9aQ50E2BJ-dZqoWTQChSco3Gvf7dLy12qgNGdh8UvAiXUa9OtVNSxmzxmbHd6PT8BCMQpIGaqweMVVwijQm8RdrS91gU9V57vWjPSh6OjXVBfLz3pACHqd6tyXSlgRBBm9lMR9R7qUPfzeRpuU6rwADsjQEC4rIwshOUcw3oNSSuHmYJGuaIfiLVztRrDqrWO-2UFyhWMS-BdaACad24LqXKU8X7pgSyLvtGZaOKpLEZqnmY-j0VSVfFEt-XgZylYTauFeH6GxIaF90d1PsT7Ut7k_qiaLZCL0D5bTzFzHWjsmYYyh_4s5rcLU_IuqgJioufqPm8w9qLM0HBLQDEGGRwusbAHEO6D-tX-fs59zMpjEf3u5bjJqS3wCNoyg8iNxTPrtJycjinQDR0gV-WI2LNOa1cOlZ-xGOYQMqfsBW38bebGVY_yrZHy4RP4sT3A1x_qo9xYcHRUvD9bixNPt3KTntBhRjLTeju7NZ_Zc5rufuW5R8wBkVX2Y_j48_nZrvWfiMBQc9hmbJvxR5pRYJCW0ztvtjfGqhTpQooLIvoGywu4bsPVLSxCMfd6CreVCUcD0cwaqqktirNrzUSs5xFMQn1iXjO7tE0hiSlHAlXEcERc_PYw2-K3FcFX7PXMRfHEGTqmA4BNLkom_4smu9m2-itG6jjv2FU-eXlOdikkxbXlwvidB2jvHV200Wa5t4ErgpEzsBL3x2gvDW6bhxQmf1EdiCBUiqi7Rs7IsOazzhAwEnn0OgE_kICi7qogwbe3lRdw8DHww"
    refresh_token = "AQBalYNo8Q1PZhDw8au6XfgpBwR7CE1e1rDge8zPE2PityG3XLz3vlApSnasWTwcxudRfPMDn_csVRgTQFKec5oIc6PJ3BK61uxgjujJa77kbhkAcnm4ZOkM3gXgdt1_25s"
    spotify_client = spotify_methods.SpotifyUser(refresh_token=refresh_token)
    print(spotify_client.access_token)
    return spotify_client.access_token

def add_user():
    s = requests.session()

    access_token = get_bearer()
    headers = {
        "authorization": f"Bearer {access_token}",
        "origin": "https://developer.spotify.com",
        "referer": "https://developer.spotify.com/dashboard/122dd0accd2c491ca81708747ef141ee/users",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    print(headers)

    addUser = s.post(url, json=payload, headers=headers)
    print(addUser.status_code)
    print(addUser.text)

if __name__ == '__main__':
    get_bearer()
